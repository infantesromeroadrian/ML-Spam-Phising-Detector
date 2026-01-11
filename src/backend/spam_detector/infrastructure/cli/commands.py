"""CLI commands implementation."""

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from ...application import Container
from ...domain.ports import DetailLevel

console = Console()

# Models subcommand app
models_app = typer.Typer(help="Manage and list available models")


def predict_command(
    ctx: typer.Context,
    text: Annotated[str | None, typer.Argument(help="Email text to classify")] = None,
    file: Annotated[Path | None, typer.Option("--file", "-f", help="Read email from file")] = None,
    subject: Annotated[str | None, typer.Option("--subject", "-s", help="Email subject")] = None,
    sender: Annotated[str | None, typer.Option("--sender", help="Email sender address")] = None,
    format: Annotated[str, typer.Option("--format", help="Output format (text or json)")] = "text",
    detail: Annotated[
        str, typer.Option("--detail", "-d", help="Detail level (simple, detailed, debug)")
    ] = "simple",
) -> None:
    """
    Classify an email as SPAM or PHISHING.

    Examples:
        # From text argument
        email-classifier predict "WINNER! Click here!"

        # From file
        email-classifier predict --file email.txt

        # From stdin
        cat email.txt | email-classifier predict

        # JSON output
        email-classifier predict "Test" --format json

        # Detailed output
        email-classifier predict "Test" --detail detailed
    """
    # Get container from context
    container: Container = ctx.obj

    # Determine input source
    email_text = _get_email_text(text, file)

    if not email_text:
        console.print("[red]Error:[/red] No email text provided")
        console.print("Use: email-classifier predict <text>")
        console.print("  or: email-classifier predict --file <path>")
        console.print("  or: cat file.txt | email-classifier predict")
        raise typer.Exit(1) from None

    # Validate format
    if format not in ("text", "json"):
        console.print(f"[red]Error:[/red] Invalid format '{format}'")
        console.print("Valid formats: text, json")
        raise typer.Exit(1) from None

    # Validate detail level
    valid_details: list[DetailLevel] = ["simple", "detailed", "debug"]
    if detail not in valid_details:
        console.print(f"[red]Error:[/red] Invalid detail level '{detail}'")
        console.print(f"Valid levels: {', '.join(valid_details)}")
        raise typer.Exit(1) from None

    try:
        # Get use case
        use_case = container.get_classify_use_case(format_type=format)  # type: ignore

        # Execute classification
        result = use_case.execute(
            email_text=email_text,
            subject=subject,
            sender=sender,
            detail_level=detail,  # type: ignore
        )

        # Output result
        console.print(result)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from None
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] Model not found: {e}")
        console.print("\nMake sure you have trained models in the models directory.")
        raise typer.Exit(1) from None
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        if container._settings.verbose:
            console.print_exception()
        raise typer.Exit(1) from None


@models_app.command("list")
def models_list(
    ctx: typer.Context,
    model: Annotated[
        str, typer.Argument(help="Model name (spam_detector or phishing_detector)")
    ] = "spam_detector",
) -> None:
    """
    List available model versions.

    Examples:
        email-classifier models list
        email-classifier models list spam_detector
        email-classifier models list phishing_detector
    """
    container: Container = ctx.obj

    # Validate model name
    if model not in ("spam_detector", "phishing_detector"):
        console.print(f"[red]Error:[/red] Invalid model name '{model}'")
        console.print("Valid models: spam_detector, phishing_detector")
        raise typer.Exit(1) from None

    try:
        use_case = container.get_list_models_use_case()
        models = use_case.execute(model)  # type: ignore

        if not models:
            console.print(f"[yellow]No models found for '{model}'[/yellow]")
            return

        # Create table
        table = Table(title=f"Available Models: {model}")
        table.add_column("#", style="cyan", justify="right")
        table.add_column("Timestamp", style="green")
        table.add_column("Accuracy", justify="right")
        table.add_column("Samples", justify="right")
        table.add_column("Vocab", justify="right")
        table.add_column("Size", justify="right")

        for i, m in enumerate(models, 1):
            latest = " (latest)" if i == 1 else ""
            table.add_row(
                f"{i}{latest}",
                m.timestamp,
                f"{m.accuracy_percent:.2f}%",
                f"{m.train_samples:,}",
                f"{m.vocabulary_size:,}",
                f"{m.file_size_mb:.2f}MB",
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from None


@models_app.command("info")
def models_info(
    ctx: typer.Context,
    model: Annotated[str, typer.Argument(help="Model name")] = "spam_detector",
) -> None:
    """
    Show detailed information about latest model.

    Examples:
        email-classifier models info
        email-classifier models info spam_detector
    """
    container: Container = ctx.obj

    if model not in ("spam_detector", "phishing_detector"):
        console.print(f"[red]Error:[/red] Invalid model name '{model}'")
        raise typer.Exit(1) from None

    try:
        use_case = container.get_list_models_use_case()
        latest = use_case.get_latest(model)  # type: ignore

        if not latest:
            console.print(f"[yellow]No models found for '{model}'[/yellow]")
            return

        # Display info
        console.print(f"\n[bold cyan]Model Information: {model}[/bold cyan]")
        console.print(f"  Version:    {latest.timestamp}")
        console.print(f"  Accuracy:   {latest.accuracy_percent:.2f}%")
        console.print(f"  Samples:    {latest.train_samples:,}")
        console.print(f"  Vocabulary: {latest.vocabulary_size:,} words")
        console.print(f"  File Size:  {latest.file_size_mb:.2f}MB")
        console.print()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from None


# === Helper functions ===


def _get_email_text(text_arg: str | None, file_path: Path | None) -> str:
    """Get email text from various sources."""
    # Priority: file > argument > stdin

    if file_path:
        if not file_path.exists():
            console.print(f"[red]Error:[/red] File not found: {file_path}")
            raise typer.Exit(1) from None

        try:
            return file_path.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Error reading file:[/red] {e}")
            raise typer.Exit(1) from None

    if text_arg:
        return text_arg

    # Check stdin
    if not sys.stdin.isatty():
        return sys.stdin.read()

    return ""
