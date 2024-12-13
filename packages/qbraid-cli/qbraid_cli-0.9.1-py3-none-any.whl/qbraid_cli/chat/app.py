# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining commands in the 'qbraid chat' namespace.

"""
from enum import Enum

import typer
from rich.console import Console
from rich.table import Table

from qbraid_cli.handlers import handle_error, run_progress_task

chat_app = typer.Typer(
    help="Interact with qBraid AI chat service.", pretty_exceptions_show_locals=False
)


class ChatFormat(str, Enum):
    """Format of the response from the chat service."""

    text = "text"  # pylint: disable=invalid-name
    code = "code"  # pylint: disable=invalid-name


@chat_app.command("send")
def chat_send(
    prompt: str = typer.Argument(..., help="The prompt to send to the chat service."),
    model: str = typer.Option(None, "--model", "-m", help="The model to use for the chat service."),
    response_format: ChatFormat = typer.Option(
        ChatFormat.text, "--format", "-f", help="The format of the response."
    ),
    stream: bool = typer.Option(False, "--stream", "-s", help="Stream the response."),
):
    """
    Interact with qBraid AI chat service.

    """
    # pylint: disable-next=import-outside-toplevel
    from qbraid_core.services.chat import ChatClient, ChatServiceRequestError

    client = ChatClient()

    if response_format == ChatFormat.code:
        prompt += " Return only raw code. Do not include any text outside of code blocks."

    if stream:
        try:
            for chunk in client.chat_stream(prompt, model, response_format):
                print(chunk, end="")
        except ChatServiceRequestError as err:
            handle_error(message=str(err), include_traceback=False)
    else:
        content = run_progress_task(
            client.chat,
            prompt,
            model,
            response_format,
            description="Connecting to chat service...",
            include_error_traceback=False,
        )
        print(content)


@chat_app.command(name="models")
def chat_models():
    """List available chat models."""
    # pylint: disable-next=import-outside-toplevel
    from qbraid_core.services.chat import ChatClient

    client = ChatClient()

    models = run_progress_task(
        client.get_models,
        description="Connecting to chat service...",
        include_error_traceback=False,
    )

    console = Console()
    table = Table(title="Available Chat Models\n", show_lines=True, title_justify="left")

    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("Pricing [not bold](1k tokens ~750 words)", style="magenta")
    table.add_column("Description", style="green")

    for model in models:
        table.add_row(
            model["model"],
            f"{model['pricing']['input']} credits / 1M input tokens\n"
            f"{model['pricing']['output']} credits / 1M output tokens",
            model["description"],
        )

    console.print(table)
