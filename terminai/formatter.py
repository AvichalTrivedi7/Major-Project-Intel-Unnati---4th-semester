"""Terminal UI Formatter for TerminAI.

Uses the rich library for colored, structured output.
"""

from typing import Dict, Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from executor import CommandResult
from error_detector import ErrorInfo
from config import APP_NAME, VERSION

console = Console()


def print_banner():
    """Display the startup banner."""
    banner = Text()
    banner.append(f"  {APP_NAME} ", style="bold white on blue")
    banner.append(f" v{VERSION} ", style="bold cyan")
    banner.append(" — Intelligent AI Terminal Assistant", style="dim")
    console.print()
    console.print(Panel(banner, border_style="blue"))
    console.print("  Type commands as usual. Type [bold]exit[/bold] or [bold]quit[/bold] to leave.\n")


def print_prompt(cwd: str):
    """Print the input prompt with current directory."""
    console.print(f"[bold cyan]{APP_NAME}[/bold cyan] [dim]{cwd}[/dim]")
    console.print("[bold green]>[/bold green] ", end="")


def print_output(result: CommandResult):
    """Display command stdout."""
    if result.stdout.strip():
        console.print(Panel(
            result.stdout.rstrip(),
            title="[bold green]OUTPUT[/bold green]",
            border_style="green",
            padding=(0, 1),
        ))


def print_error(result: CommandResult, error_info: ErrorInfo):
    """Display detected error with classification."""
    error_text = Text()
    error_text.append(f"Category: {error_info.category}\n", style="bold red")
    error_text.append(error_info.stderr, style="red")

    console.print(Panel(
        error_text,
        title="[bold red]ERROR[/bold red]",
        border_style="red",
        padding=(0, 1),
    ))


def print_suggestion(suggestion: str):
    """Display a fix suggestion from the error database."""
    console.print(Panel(
        suggestion,
        title="[bold yellow]SUGGESTION[/bold yellow]",
        border_style="yellow",
        padding=(0, 1),
    ))


def print_ai_suggestion(suggestion: Dict[str, str]):
    """Display a structured AI-generated suggestion."""
    text = Text()
    text.append("Explanation: ", style="bold yellow")
    text.append(suggestion.get("explanation", "N/A") + "\n")
    text.append("Fix: ", style="bold yellow")
    text.append(suggestion.get("fix", "N/A") + "\n")
    cmd = suggestion.get("command", "")
    if cmd:
        text.append("Command: ", style="bold yellow")
        text.append(cmd, style="bold green")

    console.print(Panel(
        text,
        title="[bold magenta]AI SUGGESTION[/bold magenta]",
        border_style="magenta",
        padding=(0, 1),
    ))


def print_no_suggestion():
    """Inform user that no suggestion is available."""
    console.print(
        "[dim]No suggestion available. "
        "Configure an AI provider in .env for intelligent fix suggestions.[/dim]"
    )


def print_ai_status(message: str):
    """Print an AI-related status message."""
    console.print(f"[dim italic]AI > {message}[/dim italic]")


def print_fix_prompt(command: str):
    """Ask the user whether to execute a suggested fix command."""
    console.print()
    console.print(f"  [bold yellow]Suggested command:[/bold yellow] [bold green]{command}[/bold green]")
    console.print("  [bold]Run this fix? (y/n):[/bold] ", end="")


def print_fix_running(command: str):
    """Show that a fix command is being executed."""
    console.print(Panel(
        f"Running: {command}",
        title="[bold blue]FIX EXECUTION[/bold blue]",
        border_style="blue",
        padding=(0, 1),
    ))


def print_fix_result(result):
    """Display the result of executing a fix command."""
    from executor import CommandResult
    if result.stdout.strip():
        console.print(Panel(
            result.stdout.rstrip(),
            title="[bold green]FIX OUTPUT[/bold green]",
            border_style="green",
            padding=(0, 1),
        ))
    if result.returncode != 0 and result.stderr.strip():
        console.print(Panel(
            result.stderr.rstrip(),
            title="[bold red]FIX ERROR[/bold red]",
            border_style="red",
            padding=(0, 1),
        ))
    elif result.returncode == 0:
        console.print("[bold green]  Fix executed successfully.[/bold green]")


def print_fix_skipped():
    """Inform user the fix was skipped."""
    console.print("[dim]  Fix skipped.[/dim]")


def print_info(message: str):
    """Print an informational message."""
    console.print(f"[dim]{message}[/dim]")
