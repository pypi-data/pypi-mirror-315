import asyncio
from pathlib import Path
from typing import Any

import typer
from amsdal.manager import AsyncAmsdalManager
from amsdal.services.transaction_execution import TransactionExecutionService
from amsdal_data.transactions.background.connections.base import WorkerMode
from amsdal_data.transactions.background.manager import AsyncBackgroundTransactionManager
from amsdal_data.transactions.background.manager import BackgroundTransactionManager
from amsdal_server.apps.transactions.services.transaction_api import TransactionApi
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.errors import AmsdalInitiationError
from rich import print as rprint

from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.serve.utils import async_build_app_and_check_migrations
from amsdal_cli.commands.serve.utils import build_app_and_check_migrations
from amsdal_cli.commands.worker.app import sub_app
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_error


def _sync_run(cli_config: CliConfig, app_source_path: Path, mode: WorkerMode) -> None:
    def _init_function(**kwargs: Any) -> None:  # noqa: ARG001
        manager = build_app_and_check_migrations(
            output_path=cli_config.app_directory,
            app_source_path=app_source_path,
            config_path=cli_config.config_path,
            apply_fixtures=False,
            confirm_migrations=False,
        )

        if not manager.is_setup:
            manager.setup()
            manager.authenticate()

        for transaction in TransactionApi().get_transactions().rows:
            TransactionExecutionService().get_transaction_func(transaction.title)

    _init_function()

    try:
        BackgroundTransactionManager().connection.run_worker(_init_function, mode=mode)
    except AmsdalInitiationError:
        rprint(rich_error('Worker is not registered.'))
        return


async def _async_run(cli_config: CliConfig, app_source_path: Path, mode: WorkerMode) -> None:

    async def _init_function(**kwargs: Any) -> None:  # noqa: ARG001
        manager = await async_build_app_and_check_migrations(
            output_path=cli_config.app_directory,
            app_source_path=app_source_path,
            config_path=cli_config.config_path,
            apply_fixtures=False,
            confirm_migrations=False,
        )

        if not manager.is_setup:
            await manager.setup()
            manager.authenticate()

        for transaction in TransactionApi().get_transactions().rows:
            TransactionExecutionService().get_transaction_func(transaction.title)

    async def _shutdown_function(**kwargs: Any) -> None:  # noqa: ARG001
        manager = AsyncAmsdalManager()
        if manager.is_setup:
            await manager.teardown()

    await _init_function()

    try:
        await AsyncBackgroundTransactionManager().connection.run_worker(_init_function, _shutdown_function, mode=mode)  # type: ignore  # noqa: [arg-type]
    except AmsdalInitiationError as e:
        rprint(rich_error('Worker is not registered.'), e)
        return


@sub_app.command(name='run')
def run_worker(
    ctx: typer.Context,
    mode: WorkerMode = typer.Option(WorkerMode.EXECUTOR, help='Worker mode.'),  # noqa: B008
) -> None:
    """
    Run worker.

    Args:
        ctx (typer.Context): The Typer context object.
        mode (WorkerMode): The mode in which the worker should run. Defaults to WorkerMode.EXECUTOR.

    Returns:
        None
    """

    cli_config: CliConfig = ctx.meta['config']
    app_source_path = cli_config.app_directory / SOURCES_DIR
    config_path = cli_config.config_path
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config_path)

    if config_manager.get_config().async_mode:
        asyncio.run(_async_run(cli_config, app_source_path, mode))
    else:
        _sync_run(cli_config, app_source_path, mode)
