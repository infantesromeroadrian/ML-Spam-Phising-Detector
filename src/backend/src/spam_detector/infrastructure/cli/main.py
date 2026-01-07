"""CLI main entry point."""

import sys
from pathlib import Path

import typer
from rich.console import Console

from ...config import Settings
from .commands import models_app, predict_command

# Create main app
app = typer.Typer(
    name="email-classifier",
    help="Email classification tool for SPAM and PHISHING detection",
    add_completion=False,
    rich_markup_mode="rich",
)

# Add subcommands
app.command(name="predict")(predict_command)
app.add_typer(models_app, name="models")

# Global console for rich output
console = Console()


@app.callback()
def main_callback(
    ctx: typer.Context,
    models_dir: Path = typer.Option(
        Path("models"),
        "--models-dir",
        "-m",
        help="Directory containing trained models",
        envvar="EMAIL_CLASSIFIER_MODELS_DIR",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """
    Email Classifier - Detect SPAM and PHISHING emails.

    Uses machine learning models to classify emails with dual detection:
    - SPAM detection (unwanted commercial emails)
    - PHISHING detection (fraudulent/malicious emails)
    """
    # Store settings in context
    settings = Settings(models_dir=models_dir, verbose=verbose)

    # Re-initialize container with custom settings
    from ...application import Container

    ctx.obj = Container(settings)


def cli_main() -> None:
    """Main CLI entry point."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        if "--verbose" in sys.argv or "-v" in sys.argv:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
