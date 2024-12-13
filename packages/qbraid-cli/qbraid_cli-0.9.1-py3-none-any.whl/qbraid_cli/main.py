# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Entrypoint for the qBraid CLI.

"""

import rich
import typer

from qbraid_cli.account.app import account_app
from qbraid_cli.admin.app import admin_app
from qbraid_cli.chat.app import chat_app
from qbraid_cli.configure.app import configure_app
from qbraid_cli.devices.app import devices_app
from qbraid_cli.jobs.app import jobs_app

try:
    from qbraid_cli.envs.app import envs_app
    from qbraid_cli.kernels.app import kernels_app
    from qbraid_cli.pip.app import pip_app

    ENVS_COMMANDS = True
except ImportError:
    ENVS_COMMANDS = False

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

app.add_typer(admin_app, name="admin")
app.add_typer(chat_app, name="chat")
app.add_typer(configure_app, name="configure")
app.add_typer(account_app, name="account")
app.add_typer(devices_app, name="devices")
app.add_typer(jobs_app, name="jobs")

if ENVS_COMMANDS is True:
    app.add_typer(envs_app, name="envs")
    app.add_typer(kernels_app, name="kernels")
    app.add_typer(pip_app, name="pip")


def version_callback(value: bool):
    """Show the version and exit."""
    if value:
        # pylint: disable-next=import-error
        from ._version import __version__  # type: ignore

        typer.echo(f"qbraid-cli/{__version__}")
        raise typer.Exit(0)


def show_banner():
    """Show the qBraid CLI banner."""
    typer.secho("----------------------------------", fg=typer.colors.BRIGHT_BLACK)
    typer.secho("  * ", fg=typer.colors.BRIGHT_BLACK, nl=False)
    typer.secho("Welcome to the qBraid CLI!", fg=typer.colors.MAGENTA, nl=False)
    typer.secho(" * ", fg=typer.colors.BRIGHT_BLACK)
    typer.secho("----------------------------------", fg=typer.colors.BRIGHT_BLACK)
    typer.echo("")
    typer.echo("        ____            _     _  ")
    typer.echo("   __ _| __ ) _ __ __ _(_) __| | ")
    typer.echo(r"  / _` |  _ \| '__/ _` | |/ _` | ")
    typer.echo(" | (_| | |_) | | | (_| | | (_| | ")
    typer.echo(r"  \__,_|____/|_|  \__,_|_|\__,_| ")
    typer.echo("     |_|                         ")
    typer.echo("")
    typer.echo("")
    typer.echo("- Use 'qbraid --help' to see available commands.")
    typer.echo("")
    typer.echo("- Use 'qbraid --version' to see the current version.")
    typer.echo("")
    rich.print("Reference Docs: https://docs.qbraid.com/cli/api-reference/qbraid")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    """The qBraid CLI."""
    if ctx.invoked_subcommand is None and not version:
        show_banner()


if __name__ == "__main__":
    app()
