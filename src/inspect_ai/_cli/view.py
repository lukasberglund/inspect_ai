import click
from typing_extensions import Unpack

from inspect_ai._util.constants import DEFAULT_SERVER_HOST, DEFAULT_VIEW_PORT
from inspect_ai._view.view import view
from inspect_ai.log._bundle import bundle_log_dir

from .common import CommonOptions, common_options, resolve_common_options


# Define the base command group
@click.group(name="view", invoke_without_command=True)
@common_options
@click.pass_context
def view_command(ctx: click.Context, **kwargs: Unpack[CommonOptions]) -> None:
    """View command group."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(start, **kwargs)
    else:
        pass


@view_command.command("start")
@common_options
@click.option(
    "--recursive",
    type=bool,
    is_flag=True,
    default=True,
    help="Include all logs in log_dir recursively.",
)
@click.option(
    "--host",
    default=DEFAULT_SERVER_HOST,
    help="Tcp/Ip host",
)
@click.option("--port", default=DEFAULT_VIEW_PORT, help="TCP/IP port")
def start(
    recursive: bool,
    host: str,
    port: int,
    **kwargs: Unpack[CommonOptions],
) -> None:
    """View evaluation logs."""
    # read common options
    (log_dir, log_level) = resolve_common_options(kwargs)

    # run the viewer
    view(
        log_dir=log_dir, recursive=recursive, host=host, port=port, log_level=log_level
    )


@view_command.command("bundle")
@common_options
@click.option(
    "--output-dir",
    required=True,
    help="The directory where bundled output will be placed.",
)
@click.option(
    "--overwrite",
    type=bool,
    is_flag=True,
    default=False,
    help="Overwrite files in the output directory.",
)
def bundle_command(
    output_dir: str,
    overwrite: bool,
    **kwargs: Unpack[CommonOptions],
) -> None:
    """Bundle evaluation logs"""
    # read common options
    (log_dir, log_level) = resolve_common_options(kwargs)

    bundle_log_dir(output_dir=output_dir, log_dir=log_dir, overwrite=overwrite)