"""Text output formatter with Rich formatting."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ...domain.entities import ClassificationResult
from ...domain.ports import DetailLevel


class TextFormatter:
    """
    Format classification results as rich text.

    Implements IOutputFormatter port for human-readable terminal output.
    Uses Rich library for colors, tables, and formatting.

    Examples:
        >>> formatter = TextFormatter()
        >>> output = formatter.format(result, detail_level="simple")
        >>> print(output)
        ⚠️  SPAM + PHISHING (92.7% confidence)
    """

    def __init__(self) -> None:
        """Initialize formatter with Rich console."""
        self._console = Console()

    def format(self, result: ClassificationResult, detail_level: DetailLevel = "simple") -> str:
        """
        Format classification result as rich text.

        Args:
            result: Classification result to format
            detail_level: Amount of detail to include
                - "simple": Just verdict and confidence
                - "detailed": Include both predictions, models used
                - "debug": Include all metadata, execution time, etc.

        Returns:
            Formatted string with ANSI color codes
        """
        if detail_level == "simple":
            return self._format_simple(result)
        elif detail_level == "detailed":
            return self._format_detailed(result)
        else:  # debug
            return self._format_debug(result)

    # === Private methods ===

    def _format_simple(self, result: ClassificationResult) -> str:
        """Format simple one-line output."""
        icon = self._get_risk_icon(result.risk_level)
        verdict = result.final_verdict
        confidence = result.max_confidence * 100

        text = Text()
        text.append(f"{icon} ", style="bold")
        text.append(verdict, style=self._get_verdict_style(verdict))
        text.append(f" ({confidence:.1f}% confidence)", style="dim")

        return text.plain

    def _format_detailed(self, result: ClassificationResult) -> str:
        """Format detailed output with table."""
        # Build table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Label", style="bold")
        table.add_column("Value")

        # Email preview
        table.add_row("Email", result.email.preview)
        table.add_section()

        # Spam detection
        spam_icon = "🔴" if result.spam_prediction.is_positive else "🟢"
        spam_conf = result.spam_prediction.probability_percent
        table.add_row(f"{spam_icon} SPAM", f"{result.spam_prediction.label} ({spam_conf:.1f}%)")

        # Phishing detection
        phish_icon = "🔴" if result.phishing_prediction.is_positive else "🟢"
        phish_conf = result.phishing_prediction.probability_percent
        table.add_row(
            f"{phish_icon} PHISHING", f"{result.phishing_prediction.label} ({phish_conf:.1f}%)"
        )

        table.add_section()

        # Final verdict
        verdict_icon = self._get_risk_icon(result.risk_level)
        table.add_row(f"{verdict_icon} VERDICT", f"{result.final_verdict} ({result.risk_level})")

        # Render to string
        with self._console.capture() as capture:
            self._console.print(table)

        return capture.get()

    def _format_debug(self, result: ClassificationResult) -> str:
        """Format debug output with full details."""
        # Create panel content
        lines = []

        # Email info
        lines.append("[bold cyan]EMAIL DETAILS:[/]")
        lines.append(f"  Preview: {result.email.preview}")
        lines.append(f"  Words: {result.email.word_count} | Chars: {result.email.char_count}")
        if result.email.subject:
            lines.append(f"  Subject: {result.email.subject}")
        if result.email.sender:
            lines.append(f"  Sender: {result.email.sender}")
        lines.append("")

        # Spam prediction
        lines.append("[bold red]SPAM DETECTION:[/]")
        lines.append(f"  Label: {result.spam_prediction.label}")
        lines.append(
            f"  Probability: {result.spam_prediction.probability:.4f} ({result.spam_prediction.probability_percent:.2f}%)"
        )
        lines.append(f"  Model: {result.spam_prediction.model_name}")
        lines.append(f"  Version: {result.spam_prediction.model_timestamp}")
        lines.append("")

        # Phishing prediction
        lines.append("[bold yellow]PHISHING DETECTION:[/]")
        lines.append(f"  Label: {result.phishing_prediction.label}")
        lines.append(
            f"  Probability: {result.phishing_prediction.probability:.4f} ({result.phishing_prediction.probability_percent:.2f}%)"
        )
        lines.append(f"  Model: {result.phishing_prediction.model_name}")
        lines.append(f"  Version: {result.phishing_prediction.model_timestamp}")
        lines.append("")

        # Final verdict
        verdict_style = self._get_verdict_style(result.final_verdict)
        lines.append("[bold]FINAL VERDICT:[/]")
        lines.append(f"  Verdict: [{verdict_style}]{result.final_verdict}[/]")
        lines.append(f"  Risk Level: {result.risk_level}")
        lines.append(f"  Malicious: {result.is_malicious}")
        lines.append(f"  Max Confidence: {result.max_confidence:.4f}")
        lines.append("")

        # Performance
        lines.append("[bold dim]PERFORMANCE:[/]")
        lines.append(f"  Execution Time: {result.execution_time_ms:.2f}ms")

        content = "\n".join(lines)

        # Render panel
        icon = self._get_risk_icon(result.risk_level)
        panel = Panel(
            content,
            title=f"{icon} Email Classification Report",
            border_style=self._get_verdict_style(result.final_verdict),
        )

        with self._console.capture() as capture:
            self._console.print(panel)

        return capture.get()

    def _get_risk_icon(self, risk_level: str) -> str:
        """Get emoji icon for risk level."""
        icons = {"LOW": "✅", "MEDIUM": "⚠️", "HIGH": "🔴", "CRITICAL": "🚨"}
        return icons.get(risk_level, "❓")

    def _get_verdict_style(self, verdict: str) -> str:
        """Get Rich style for verdict."""
        styles = {"HAM": "green", "SPAM": "red", "PHISHING": "yellow", "SPAM+PHISHING": "bold red"}
        return styles.get(verdict, "white")
