# Copyright (c) 2024 Snowflake Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from textwrap import dedent
from unittest import mock
from unittest.mock import MagicMock

import pytest
import typer
from click import UsageError
from snowflake.cli._plugins.connection.util import UIParameter
from snowflake.cli._plugins.nativeapp.constants import (
    LOOSE_FILES_MAGIC_VERSION,
    SPECIAL_COMMENT,
)
from snowflake.cli._plugins.nativeapp.entities.application import (
    ApplicationEntity,
    ApplicationEntityModel,
)
from snowflake.cli._plugins.nativeapp.entities.application_package import (
    ApplicationPackageEntity,
    ApplicationPackageEntityModel,
)
from snowflake.cli._plugins.nativeapp.exceptions import (
    ApplicationCreatedExternallyError,
    ApplicationPackageDoesNotExistError,
)
from snowflake.cli._plugins.nativeapp.policy import (
    AllowAlwaysPolicy,
    AskAlwaysPolicy,
    DenyAlwaysPolicy,
    PolicyBase,
)
from snowflake.cli._plugins.nativeapp.same_account_install_method import (
    SameAccountInstallMethod,
)
from snowflake.cli._plugins.stage.diff import DiffResult
from snowflake.cli._plugins.workspace.context import ActionContext, WorkspaceContext
from snowflake.cli._plugins.workspace.manager import WorkspaceManager
from snowflake.cli.api.console import cli_console as cc
from snowflake.cli.api.console.abc import AbstractConsole
from snowflake.cli.api.constants import ObjectType
from snowflake.cli.api.entities.common import EntityActions
from snowflake.cli.api.errno import (
    APPLICATION_NO_LONGER_AVAILABLE,
    APPLICATION_OWNS_EXTERNAL_OBJECTS,
    CANNOT_UPGRADE_FROM_LOOSE_FILES_TO_VERSION,
    INSUFFICIENT_PRIVILEGES,
)
from snowflake.cli.api.exceptions import (
    CouldNotUseObjectError,
    NoWarehouseSelectedInSessionError,
)
from snowflake.cli.api.project.definition_manager import DefinitionManager
from snowflake.connector import ProgrammingError
from snowflake.connector.cursor import DictCursor

from tests.nativeapp.patch_utils import (
    mock_connection,
)
from tests.nativeapp.utils import (
    APP_ENTITY_GET_EXISTING_APP_INFO,
    APP_PACKAGE_ENTITY_GET_EXISTING_VERSION_INFO,
    GET_UI_PARAMETERS,
    SQL_EXECUTOR_EXECUTE,
    TYPER_CONFIRM,
    mock_execute_helper,
    quoted_override_yml_file_v2,
)
from tests.testing_utils.files_and_dirs import create_named_file
from tests.testing_utils.fixtures import MockConnectionCtx

allow_always_policy = AllowAlwaysPolicy()
ask_always_policy = AskAlwaysPolicy()
deny_always_policy = DenyAlwaysPolicy()
test_manifest_contents = dedent(
    """\
    manifest_version: 1

    version:
        name: dev
        label: "Dev Version"
        comment: "Default version used for development. Override for actual deployment."

    artifacts:
        setup_script: setup.sql
        readme: README.md

    configuration:
        log_level: INFO
        trace_level: ALWAYS
"""
)


def _get_wm():
    dm = DefinitionManager()
    return WorkspaceManager(
        project_definition=dm.project_definition,
        project_root=dm.project_root,
    )


def _create_or_upgrade_app(
    policy: PolicyBase,
    install_method: SameAccountInstallMethod,
    interactive: bool = False,
    package_id: str = "app_pkg",
    app_id: str = "myapp",
    console: AbstractConsole | None = None,
):
    dm = DefinitionManager()
    pd = dm.project_definition
    pkg_model: ApplicationPackageEntityModel = pd.entities[package_id]
    app_model: ApplicationEntityModel = pd.entities[app_id]
    ctx = WorkspaceContext(
        console=console or cc,
        project_root=dm.project_root,
        get_default_role=lambda: "mock_role",
        get_default_warehouse=lambda: "mock_warehouse",
    )
    app = ApplicationEntity(app_model, ctx)
    pkg = ApplicationPackageEntity(pkg_model, ctx)
    stage_fqn = f"{pkg_model.fqn.name}.{pkg_model.stage}"

    pkg.action_bundle(action_ctx=ActionContext(get_entity=lambda *args: None))

    return app.create_or_upgrade_app(
        package=pkg,
        stage_fqn=stage_fqn,
        install_method=install_method,
        policy=policy,
        interactive=interactive,
    )


test_pdf = dedent(
    """\
        definition_version: 2
        entities:
            app_pkg:
                type: application package
                stage: app_src.stage
                manifest: app/manifest.yml
                artifacts:
                    - setup.sql
                    - src: app/manifest.yml
                      dest: manifest.yml
                meta:
                    role: package_role
                    warehouse: pkg_warehouse
            myapp:
                type: application
                debug: true
                from:
                    target: app_pkg
                meta:
                    role: app_role
                    warehouse: app_warehouse
    """
)


def setup_project_file(current_working_directory: str, pdf=None):
    create_named_file(
        file_name="snowflake.yml",
        dir_name=current_working_directory,
        contents=[pdf or test_pdf],
    )

    create_named_file(
        file_name="manifest.yml",
        dir_name=f"{current_working_directory}/app",
        contents=[test_manifest_contents],
    )
    create_named_file(
        file_name="README.md",
        dir_name=f"{current_working_directory}/app",
        contents=["# This is readme"],
    )

    create_named_file(
        file_name="setup.sql",
        dir_name=current_working_directory,
        contents=["-- hi"],
    )


# Test create_dev_app with exception thrown trying to use the warehouse
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_w_warehouse_access_exception(
    mock_param, mock_conn, mock_execute, temp_dir, mock_cursor
):
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (
                CouldNotUseObjectError(
                    object_type=ObjectType.WAREHOUSE, name="app_warehouse"
                ),
                mock.call("use warehouse app_warehouse"),
            ),
            (
                None,
                mock.call("use warehouse old_wh"),
            ),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()
    setup_project_file(os.getcwd())

    assert not mock_diff_result.has_changes()

    with pytest.raises(CouldNotUseObjectError) as err:
        _create_or_upgrade_app(
            policy=MagicMock(),
            install_method=SameAccountInstallMethod.unversioned_dev(),
        )

    assert mock_execute.mock_calls == expected
    assert (
        "Could not use warehouse app_warehouse. Object does not exist, or operation cannot be performed."
        in err.value.message
    )


# Test create_dev_app with no existing application AND create succeeds AND app role == package role
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO, return_value=None)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_create_new_w_no_additional_privileges(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
                    create application myapp
                        from application package app_pkg using @app_pkg.app_src.stage debug_mode = True
                        comment = {SPECIAL_COMMENT}
                    """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()

    setup_project_file(os.getcwd(), test_pdf.replace("package_role", "app_role"))

    assert not mock_diff_result.has_changes()
    _create_or_upgrade_app(
        policy=MagicMock(),
        install_method=SameAccountInstallMethod.unversioned_dev(),
    )
    assert mock_execute.mock_calls == expected


# Test create_dev_app with no existing application AND create returns a warning
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO, return_value=None)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize(
    "existing_app_info",
    [
        None,
        {
            "name": "MYAPP",
            "comment": SPECIAL_COMMENT,
            "version": LOOSE_FILES_MAGIC_VERSION,
            "owner": "APP_ROLE",
        },
    ],
)
def test_create_or_upgrade_dev_app_with_warning(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
    existing_app_info,
):
    status_messages = ["App created/upgraded", "Warning: some warning"]
    status_cursor = mock_cursor(
        [(msg,) for msg in status_messages],
        ["status"],
    )
    create_or_upgrade_calls = (
        [
            (
                status_cursor,
                mock.call(
                    dedent(
                        f"""\
                create application myapp
                    from application package app_pkg using @app_pkg.app_src.stage debug_mode = True
                    comment = {SPECIAL_COMMENT}
                """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
        ]
        if existing_app_info is None
        else [
            (
                status_cursor,
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "desc application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("alter application myapp set debug_mode = True")),
        ]
    )

    mock_get_existing_app_info.return_value = existing_app_info
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            *create_or_upgrade_calls,
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()
    setup_project_file(os.getcwd(), test_pdf.replace("package_role", "app_role"))

    assert not mock_diff_result.has_changes()
    mock_console = mock.MagicMock()
    _create_or_upgrade_app(
        policy=MagicMock(),
        install_method=SameAccountInstallMethod.unversioned_dev(),
        console=mock_console,
    )
    assert mock_execute.mock_calls == expected

    mock_console.warning.assert_has_calls([mock.call(msg) for msg in status_messages])


# Test create_dev_app with no existing application AND create succeeds AND app role != package role
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO, return_value=None)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_create_new_with_additional_privileges(
    mock_param,
    mock_conn,
    mock_execute_query,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    side_effects, mock_execute_query_expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role package_role")),
            (
                None,
                mock.call(
                    "grant install, develop on application package app_pkg to role app_role"
                ),
            ),
            (
                None,
                mock.call("grant usage on schema app_pkg.app_src to role app_role"),
            ),
            (
                None,
                mock.call("grant read on stage app_pkg.app_src.stage to role app_role"),
            ),
            (None, mock.call("use role app_role")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
                    create application myapp
                        from application package app_pkg using @app_pkg.app_src.stage debug_mode = True
                        comment = {SPECIAL_COMMENT}
                    """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute_query.side_effect = side_effects

    mock_diff_result = DiffResult()
    setup_project_file(os.getcwd())

    assert not mock_diff_result.has_changes()
    _create_or_upgrade_app(
        policy=MagicMock(), install_method=SameAccountInstallMethod.unversioned_dev()
    )
    assert mock_execute_query.mock_calls == mock_execute_query_expected


# Test create_dev_app with no existing application AND create throws an exception
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO, return_value=None)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_create_new_w_missing_warehouse_exception(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                NoWarehouseSelectedInSessionError(
                    msg="No active warehouse selected in the current session"
                ),
                mock.call(
                    dedent(
                        f"""\
                    create application myapp
                        from application package app_pkg using @app_pkg.app_src.stage debug_mode = True
                        comment = {SPECIAL_COMMENT}
                    """
                    )
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )

    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()
    setup_project_file(os.getcwd(), test_pdf.replace("package_role", "app_role"))

    assert not mock_diff_result.has_changes()

    with pytest.raises(NoWarehouseSelectedInSessionError) as err:
        _create_or_upgrade_app(
            policy=MagicMock(),
            install_method=SameAccountInstallMethod.unversioned_dev(),
        )

    assert "Please provide a warehouse for the active session role" in err.value.message
    assert mock_execute.mock_calls == expected


# Test create_dev_app with existing application AND bad comment AND good version
# Test create_dev_app with existing application AND bad comment AND bad version
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize(
    "comment, version",
    [
        ("dummy", LOOSE_FILES_MAGIC_VERSION),
        ("dummy", "dummy"),
    ],
)
def test_create_dev_app_incorrect_properties(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    comment,
    version,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "MYAPP",
        "comment": comment,
        "version": version,
        "owner": "APP_ROLE",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()
    setup_project_file(os.getcwd())

    with pytest.raises(ApplicationCreatedExternallyError):
        assert not mock_diff_result.has_changes()
        _create_or_upgrade_app(
            policy=MagicMock(),
            install_method=SameAccountInstallMethod.unversioned_dev(),
        )

    assert mock_execute.mock_calls == expected


# Test create_dev_app with existing application AND incorrect owner
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_incorrect_owner(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "MYAPP",
        "comment": SPECIAL_COMMENT,
        "version": LOOSE_FILES_MAGIC_VERSION,
        "owner": "wrong_owner",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(
                    msg="Insufficient privileges to operate on database",
                    errno=INSUFFICIENT_PRIVILEGES,
                ),
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()
    setup_project_file(os.getcwd())

    with pytest.raises(ProgrammingError):
        assert not mock_diff_result.has_changes()
        _create_or_upgrade_app(
            policy=MagicMock(),
            install_method=SameAccountInstallMethod.unversioned_dev(),
        )

    assert mock_execute.mock_calls == expected


# Test create_dev_app with existing application AND diff has no changes
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@mock_connection()
def test_create_dev_app_no_diff_changes(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "MYAPP",
        "comment": SPECIAL_COMMENT,
        "version": LOOSE_FILES_MAGIC_VERSION,
        "owner": "APP_ROLE",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                None,
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "desc application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("alter application myapp set debug_mode = True")),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()
    setup_project_file(os.getcwd())

    assert not mock_diff_result.has_changes()
    _create_or_upgrade_app(
        policy=MagicMock(), install_method=SameAccountInstallMethod.unversioned_dev()
    )
    assert mock_execute.mock_calls == expected


# Test create_dev_app with existing application AND diff has changes
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_w_diff_changes(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "MYAPP",
        "comment": SPECIAL_COMMENT,
        "version": LOOSE_FILES_MAGIC_VERSION,
        "owner": "APP_ROLE",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                None,
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "desc application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("alter application myapp set debug_mode = True")),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult(different=["setup.sql"])
    setup_project_file(os.getcwd())

    assert mock_diff_result.has_changes()
    _create_or_upgrade_app(
        policy=MagicMock(), install_method=SameAccountInstallMethod.unversioned_dev()
    )
    assert mock_execute.mock_calls == expected


# Test create_dev_app with existing application AND alter throws an error
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_recreate_w_missing_warehouse_exception(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "MYAPP",
        "comment": SPECIAL_COMMENT,
        "version": LOOSE_FILES_MAGIC_VERSION,
        "owner": "APP_ROLE",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                NoWarehouseSelectedInSessionError(
                    msg="No active warehouse selected in the current session"
                ),
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult(different=["setup.sql"])
    setup_project_file(os.getcwd())

    assert mock_diff_result.has_changes()

    with pytest.raises(NoWarehouseSelectedInSessionError) as err:
        _create_or_upgrade_app(
            policy=MagicMock(),
            install_method=SameAccountInstallMethod.unversioned_dev(),
        )

    assert mock_execute.mock_calls == expected
    assert "Please provide a warehouse for the active session role" in err.value.message


# Test create_dev_app with no existing application AND quoted name scenario 1
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO, return_value=None)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_create_new_quoted(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
                    create application "My Application"
                        from application package "My Package" using '@"My Package".app_src.stage' debug_mode = True
                        comment = {SPECIAL_COMMENT}
                    """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    'show telemetry event definitions in application "My Application"',
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()
    pdf_content = dedent(
        """\
        definition_version: 2
        entities:
            app_pkg:
                type: application package
                identifier: '"My Package"'
                artifacts:
                - setup.sql
                - app/README.md
                - src: app/manifest.yml
                  dest: manifest.yml
                manifest: app/manifest.yml
                stage: app_src.stage
                meta:
                    role: app_role
                    post_deploy:
                    - sql_script: shared_content.sql
            myapp:
                type: application
                identifier: '"My Application"'
                debug: true
                from:
                    target: app_pkg
                meta:
                    role: app_role
                    warehouse: app_warehouse
    """
    )
    setup_project_file(os.getcwd(), pdf_content)

    assert not mock_diff_result.has_changes()
    _create_or_upgrade_app(
        policy=MagicMock(), install_method=SameAccountInstallMethod.unversioned_dev()
    )
    assert mock_execute.mock_calls == expected


# Test create_dev_app with no existing application AND quoted name scenario 2
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO, return_value=None)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_create_new_quoted_override(
    mock_param,
    mock_conn,
    mock_execute,
    mock_get_existing_app_info,
    temp_dir,
    mock_cursor,
):
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
                    create application "My Application"
                        from application package "My Package" using '@"My Package".app_src.stage' debug_mode = True
                        comment = {SPECIAL_COMMENT}
                    """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    'show telemetry event definitions in application "My Application"',
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    mock_diff_result = DiffResult()
    current_working_directory = os.getcwd()
    setup_project_file(
        current_working_directory, test_pdf.replace("package_role", "app_role")
    )
    create_named_file(
        file_name="snowflake.local.yml",
        dir_name=current_working_directory,
        contents=[quoted_override_yml_file_v2],
    )

    assert not mock_diff_result.has_changes()
    _create_or_upgrade_app(
        policy=MagicMock(), install_method=SameAccountInstallMethod.unversioned_dev()
    )
    assert mock_execute.mock_calls == expected


# Test run existing app info
# AND app package has been dropped
# AND user wants to drop app
# AND drop succeeds
# AND app is created successfully.
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_recreate_app_when_orphaned(
    mock_param,
    mock_conn,
    mock_get_existing_app_info,
    mock_execute,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
        "version": LOOSE_FILES_MAGIC_VERSION,
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(errno=APPLICATION_NO_LONGER_AVAILABLE),
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (None, mock.call("drop application myapp")),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role package_role")),
            (
                None,
                mock.call(
                    "grant install, develop on application package app_pkg to role app_role"
                ),
            ),
            (
                None,
                mock.call("grant usage on schema app_pkg.app_src to role app_role"),
            ),
            (
                None,
                mock.call("grant read on stage app_pkg.app_src.stage to role app_role"),
            ),
            (None, mock.call("use role app_role")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
                    create application myapp
                        from application package app_pkg using @app_pkg.app_src.stage debug_mode = True
                        comment = {SPECIAL_COMMENT}
                    """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    _create_or_upgrade_app(
        policy=MagicMock(), install_method=SameAccountInstallMethod.unversioned_dev()
    )
    assert mock_execute.mock_calls == expected


# Test run existing app info
# AND app package has been dropped
# AND user wants to drop app
# AND drop requires cascade
# AND drop succeeds
# AND app is created successfully.
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_recreate_app_when_orphaned_requires_cascade(
    mock_param,
    mock_conn,
    mock_get_existing_app_info,
    mock_execute,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
        "version": LOOSE_FILES_MAGIC_VERSION,
    }
    # side_effects, expected = mock_execute_helper(
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(errno=APPLICATION_NO_LONGER_AVAILABLE),
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (
                ProgrammingError(errno=APPLICATION_OWNS_EXTERNAL_OBJECTS),
                mock.call("drop application myapp"),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor(
                    [
                        [None, "mypool", "COMPUTE_POOL"],
                    ],
                    [],
                ),
                mock.call("show objects owned by application myapp"),
            ),
            (None, mock.call("drop application myapp cascade")),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role package_role")),
            (
                None,
                mock.call(
                    "grant install, develop on application package app_pkg to role app_role"
                ),
            ),
            (
                None,
                mock.call("grant usage on schema app_pkg.app_src to role app_role"),
            ),
            (
                None,
                mock.call("grant read on stage app_pkg.app_src.stage to role app_role"),
            ),
            (None, mock.call("use role app_role")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
                    create application myapp
                        from application package app_pkg using @app_pkg.app_src.stage debug_mode = True
                        comment = {SPECIAL_COMMENT}
                    """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    _create_or_upgrade_app(
        policy=MagicMock(), install_method=SameAccountInstallMethod.unversioned_dev()
    )
    assert mock_execute.mock_calls == expected


# Test run existing app info
# AND app package has been dropped
# AND user wants to drop app
# AND drop requires cascade
# AND we can't see which objects are owned by the app
# AND drop succeeds
# AND app is created successfully.
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_create_dev_app_recreate_app_when_orphaned_requires_cascade_unknown_objects(
    mock_param,
    mock_conn,
    mock_get_existing_app_info,
    mock_execute,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
        "version": LOOSE_FILES_MAGIC_VERSION,
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(errno=APPLICATION_NO_LONGER_AVAILABLE),
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (
                ProgrammingError(errno=APPLICATION_OWNS_EXTERNAL_OBJECTS),
                mock.call("drop application myapp"),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                ProgrammingError(errno=APPLICATION_NO_LONGER_AVAILABLE),
                mock.call("show objects owned by application myapp"),
            ),
            (None, mock.call("drop application myapp cascade")),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role package_role")),
            (
                None,
                mock.call(
                    "grant install, develop on application package app_pkg to role app_role"
                ),
            ),
            (
                None,
                mock.call("grant usage on schema app_pkg.app_src to role app_role"),
            ),
            (
                None,
                mock.call("grant read on stage app_pkg.app_src.stage to role app_role"),
            ),
            (None, mock.call("use role app_role")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
                    create application myapp
                        from application package app_pkg using @app_pkg.app_src.stage debug_mode = True
                        comment = {SPECIAL_COMMENT}
                    """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    _create_or_upgrade_app(
        policy=MagicMock(), install_method=SameAccountInstallMethod.unversioned_dev()
    )
    assert mock_execute.mock_calls == expected


# Test upgrade app method for release directives AND throws warehouse error
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize(
    "policy_param", [allow_always_policy, ask_always_policy, deny_always_policy]
)
def test_upgrade_app_warehouse_error(
    mock_param, mock_conn, mock_execute, policy_param, temp_dir, mock_cursor
):
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (
                CouldNotUseObjectError(
                    object_type=ObjectType.WAREHOUSE, name="app_warehouse"
                ),
                mock.call("use warehouse app_warehouse"),
            ),
            (
                None,
                mock.call("use warehouse old_wh"),
            ),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    with pytest.raises(CouldNotUseObjectError):
        _create_or_upgrade_app(
            policy_param,
            interactive=True,
            install_method=SameAccountInstallMethod.release_directive(),
        )
    assert mock_execute.mock_calls == expected


# Test upgrade app method for release directives AND existing app info AND bad owner
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize(
    "policy_param", [allow_always_policy, ask_always_policy, deny_always_policy]
)
def test_upgrade_app_incorrect_owner(
    mock_param,
    mock_conn,
    mock_get_existing_app_info,
    mock_execute,
    policy_param,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "APP",
        "comment": SPECIAL_COMMENT,
        "owner": "wrong_owner",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(
                    msg="Insufficient privileges to operate on database",
                    errno=INSUFFICIENT_PRIVILEGES,
                ),
                mock.call("alter application myapp upgrade "),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    with pytest.raises(ProgrammingError):
        _create_or_upgrade_app(
            policy=policy_param,
            interactive=True,
            install_method=SameAccountInstallMethod.release_directive(),
        )
    assert mock_execute.mock_calls == expected


# Test upgrade app method for release directives AND existing app info AND upgrade succeeds
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize(
    "policy_param", [allow_always_policy, ask_always_policy, deny_always_policy]
)
def test_upgrade_app_succeeds(
    mock_param,
    mock_conn,
    mock_get_existing_app_info,
    mock_execute,
    policy_param,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (None, mock.call("alter application myapp upgrade ")),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "desc application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    _create_or_upgrade_app(
        policy=policy_param,
        interactive=True,
        install_method=SameAccountInstallMethod.release_directive(),
    )
    assert mock_execute.mock_calls == expected


# Test upgrade app method for release directives AND existing app info AND upgrade fails due to generic error
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize(
    "policy_param", [allow_always_policy, ask_always_policy, deny_always_policy]
)
def test_upgrade_app_fails_generic_error(
    mock_param,
    mock_conn,
    mock_get_existing_app_info,
    mock_execute,
    policy_param,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(
                    errno=1234,
                ),
                mock.call("alter application myapp upgrade "),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    with pytest.raises(ProgrammingError):
        _create_or_upgrade_app(
            policy=policy_param,
            interactive=True,
            install_method=SameAccountInstallMethod.release_directive(),
        )
    assert mock_execute.mock_calls == expected


# Test upgrade app method for release directives AND existing app info AND upgrade fails due to upgrade restriction error AND --force is False AND interactive mode is False AND --interactive is False
# Test upgrade app method for release directives AND existing app info AND upgrade fails due to upgrade restriction error AND --force is False AND interactive mode is False AND --interactive is True AND  user does not want to proceed
# Test upgrade app method for release directives AND existing app info AND upgrade fails due to upgrade restriction error AND --force is False AND interactive mode is True AND user does not want to proceed
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(
    f"snowflake.cli._plugins.nativeapp.policy.{TYPER_CONFIRM}", return_value=False
)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize(
    "policy_param, interactive, expected_code",
    [(deny_always_policy, False, 1), (ask_always_policy, True, 0)],
)
def test_upgrade_app_fails_upgrade_restriction_error(
    mock_param,
    mock_conn,
    mock_typer_confirm,
    mock_get_existing_app_info,
    mock_execute,
    policy_param,
    interactive,
    expected_code,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(
                    errno=CANNOT_UPGRADE_FROM_LOOSE_FILES_TO_VERSION,
                ),
                mock.call("alter application myapp upgrade "),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    with pytest.raises(typer.Exit):
        result = _create_or_upgrade_app(
            policy_param,
            interactive=interactive,
            install_method=SameAccountInstallMethod.release_directive(),
        )
        assert result.exit_code == expected_code
    assert mock_execute.mock_calls == expected


@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
def test_versioned_app_upgrade_to_unversioned(
    mock_param,
    mock_conn,
    mock_get_existing_app_info,
    mock_execute,
    temp_dir,
    mock_cursor,
):
    """
    Ensure that attempting to upgrade from a versioned dev mode
    application to an unversioned one can succeed given a permissive policy.
    """
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
        "version": "v1",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(
                    msg="Some Error Message.",
                    errno=93045,
                ),
                mock.call(
                    "alter application myapp upgrade using @app_pkg.app_src.stage"
                ),
            ),
            (None, mock.call("drop application myapp")),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role package_role")),
            (
                None,
                mock.call(
                    "grant install, develop on application package app_pkg to role app_role"
                ),
            ),
            (
                None,
                mock.call("grant usage on schema app_pkg.app_src to role app_role"),
            ),
            (
                None,
                mock.call("grant read on stage app_pkg.app_src.stage to role app_role"),
            ),
            (None, mock.call("use role app_role")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
            create application myapp
                from application package app_pkg using @app_pkg.app_src.stage debug_mode = True
                comment = {SPECIAL_COMMENT}
            """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    _create_or_upgrade_app(
        policy=AllowAlwaysPolicy(),
        interactive=False,
        install_method=SameAccountInstallMethod.unversioned_dev(),
    )
    assert mock_execute.mock_calls == expected


# Test upgrade app method for release directives AND existing app info AND upgrade fails due to upgrade restriction error AND --force is True AND drop fails
# Test upgrade app method for release directives AND existing app info AND upgrade fails due to upgrade restriction error AND --force is False AND interactive mode is False AND --interactive is True AND user wants to proceed AND drop fails
# Test upgrade app method for release directives AND existing app info AND upgrade fails due to upgrade restriction error AND --force is False AND interactive mode is True AND user wants to proceed AND drop fails
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(
    f"snowflake.cli._plugins.nativeapp.policy.{TYPER_CONFIRM}", return_value=True
)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize(
    "policy_param, interactive",
    [(allow_always_policy, False), (ask_always_policy, True)],
)
def test_upgrade_app_fails_drop_fails(
    mock_param,
    mock_conn,
    mock_typer_confirm,
    mock_get_existing_app_info,
    mock_execute,
    policy_param,
    interactive,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(
                    errno=CANNOT_UPGRADE_FROM_LOOSE_FILES_TO_VERSION,
                ),
                mock.call("alter application myapp upgrade "),
            ),
            (
                ProgrammingError(
                    errno=1234,
                ),
                mock.call("drop application myapp"),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    with pytest.raises(ProgrammingError):
        _create_or_upgrade_app(
            policy_param,
            interactive=interactive,
            install_method=SameAccountInstallMethod.release_directive(),
        )
    assert mock_execute.mock_calls == expected


# Test upgrade app method for release directives AND existing app info AND user wants to drop app AND drop succeeds AND app is created successfully.
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(
    f"snowflake.cli._plugins.nativeapp.policy.{TYPER_CONFIRM}", return_value=True
)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize("policy_param", [allow_always_policy, ask_always_policy])
def test_upgrade_app_recreate_app(
    mock_param,
    mock_conn,
    mock_typer_confirm,
    mock_get_existing_app_info,
    mock_execute,
    policy_param,
    temp_dir,
    mock_cursor,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(
                    errno=CANNOT_UPGRADE_FROM_LOOSE_FILES_TO_VERSION,
                ),
                mock.call("alter application myapp upgrade "),
            ),
            (None, mock.call("drop application myapp")),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role package_role")),
            (
                None,
                mock.call(
                    "grant install, develop on application package app_pkg to role app_role"
                ),
            ),
            (
                None,
                mock.call("grant usage on schema app_pkg.app_src to role app_role"),
            ),
            (
                None,
                mock.call("grant read on stage app_pkg.app_src.stage to role app_role"),
            ),
            (None, mock.call("use role app_role")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
            create application myapp
                from application package app_pkg  
                comment = {SPECIAL_COMMENT}
            """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    _create_or_upgrade_app(
        policy_param,
        interactive=True,
        install_method=SameAccountInstallMethod.release_directive(),
    )
    assert mock_execute.mock_calls == expected


# Test upgrade app method for version AND no existing version info
@mock.patch(
    APP_PACKAGE_ENTITY_GET_EXISTING_VERSION_INFO,
    return_value=None,
)
def test_upgrade_app_from_version_throws_usage_error_one(mock_existing, temp_dir):
    setup_project_file(os.getcwd())

    wm = _get_wm()
    with pytest.raises(UsageError):
        wm.perform_action(
            "myapp",
            EntityActions.DEPLOY,
            from_release_directive=False,
            prune=True,
            recursive=True,
            paths=[],
            validate=False,
            version="v1",
        )


# Test upgrade app method for version AND no existing app package from version info
@mock.patch(
    APP_PACKAGE_ENTITY_GET_EXISTING_VERSION_INFO,
    side_effect=ApplicationPackageDoesNotExistError("app_pkg"),
)
def test_upgrade_app_from_version_throws_usage_error_two(
    mock_existing,
    temp_dir,
):
    setup_project_file(os.getcwd())

    wm = _get_wm()
    with pytest.raises(UsageError):
        wm.perform_action(
            "myapp",
            EntityActions.DEPLOY,
            from_release_directive=False,
            prune=True,
            recursive=True,
            paths=[],
            validate=False,
            version="v1",
        )


# Test upgrade app method for version AND existing app info AND user wants to drop app AND drop succeeds AND app is created successfully
@mock.patch(
    APP_PACKAGE_ENTITY_GET_EXISTING_VERSION_INFO,
    return_value={"key": "val"},
)
@mock.patch(SQL_EXECUTOR_EXECUTE)
@mock.patch(APP_ENTITY_GET_EXISTING_APP_INFO)
@mock.patch(
    f"snowflake.cli._plugins.nativeapp.policy.{TYPER_CONFIRM}", return_value=True
)
@mock_connection()
@mock.patch(
    GET_UI_PARAMETERS,
    return_value={
        UIParameter.NA_EVENT_SHARING_V2: "false",
        UIParameter.NA_ENFORCE_MANDATORY_FILTERS: "false",
    },
)
@pytest.mark.parametrize("policy_param", [allow_always_policy, ask_always_policy])
def test_upgrade_app_recreate_app_from_version(
    mock_param,
    mock_conn,
    mock_typer_confirm,
    mock_get_existing_app_info,
    mock_execute,
    mock_existing,
    policy_param,
    temp_dir,
    mock_cursor,
    mock_bundle_map,
):
    mock_get_existing_app_info.return_value = {
        "name": "myapp",
        "comment": SPECIAL_COMMENT,
        "owner": "app_role",
    }
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role app_role")),
            (
                mock_cursor([("old_wh",)], []),
                mock.call("select current_warehouse()"),
            ),
            (None, mock.call("use warehouse app_warehouse")),
            (
                ProgrammingError(
                    errno=CANNOT_UPGRADE_FROM_LOOSE_FILES_TO_VERSION,
                ),
                mock.call("alter application myapp upgrade using version v1 "),
            ),
            (None, mock.call("drop application myapp")),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role package_role")),
            (
                None,
                mock.call(
                    "grant install, develop on application package app_pkg to role app_role"
                ),
            ),
            (
                None,
                mock.call("grant usage on schema app_pkg.app_src to role app_role"),
            ),
            (
                None,
                mock.call("grant read on stage app_pkg.app_src.stage to role app_role"),
            ),
            (None, mock.call("use role app_role")),
            (
                None,
                mock.call(
                    dedent(
                        f"""\
            create application myapp
                from application package app_pkg using version v1  debug_mode = True
                comment = {SPECIAL_COMMENT}
            """
                    )
                ),
            ),
            (
                mock_cursor([("app_role",)], []),
                mock.call("select current_role()"),
            ),
            (
                mock_cursor([], []),
                mock.call(
                    "show telemetry event definitions in application myapp",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use warehouse old_wh")),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_conn.return_value = MockConnectionCtx()
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    wm = _get_wm()
    wm.perform_action(
        "app_pkg",
        EntityActions.BUNDLE,
    )
    wm.perform_action(
        "myapp",
        EntityActions.DEPLOY,
        from_release_directive=False,
        prune=True,
        recursive=True,
        paths=[],
        validate=False,
        version="v1",
    )
    assert mock_execute.mock_calls == expected


# Test get_existing_version_info returns version info correctly
@mock.patch(SQL_EXECUTOR_EXECUTE)
def test_get_existing_version_info(
    mock_execute, temp_dir, mock_cursor, workspace_context
):
    version = "V1"
    side_effects, expected = mock_execute_helper(
        [
            (
                mock_cursor([("old_role",)], []),
                mock.call("select current_role()"),
            ),
            (None, mock.call("use role package_role")),
            (
                mock_cursor(
                    [
                        {
                            "name": "My Package",
                            "comment": "some comment",
                            "owner": "PACKAGE_ROLE",
                            "version": version,
                            "patch": 0,
                        }
                    ],
                    [],
                ),
                mock.call(
                    f"show versions like 'V1' in application package app_pkg",
                    cursor_class=DictCursor,
                ),
            ),
            (None, mock.call("use role old_role")),
        ]
    )
    mock_execute.side_effect = side_effects

    setup_project_file(os.getcwd())

    dm = DefinitionManager()
    pd = dm.project_definition
    pkg_model: ApplicationPackageEntityModel = pd.entities["app_pkg"]
    pkg = ApplicationPackageEntity(pkg_model, workspace_context)
    result = pkg.get_existing_version_info(version=version)
    assert mock_execute.mock_calls == expected
    assert result["version"] == version
