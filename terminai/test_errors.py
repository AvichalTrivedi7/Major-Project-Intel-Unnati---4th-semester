"""Phase 2 — Error Injection & Validation.

Runs a suite of intentionally failing commands to validate the error detection
and classification pipeline. No AI is involved — this tests the executor +
error_detector + error_db layers only.
"""

import os
import sys
import shutil

from rich.console import Console
from rich.table import Table

from executor import CommandExecutor
from error_detector import ErrorDetector

console = Console()

# Detect the Python interpreter available on this system
PYTHON = "py" if shutil.which("py") else ("python3" if shutil.which("python3") else "python")


def _py(code: str) -> str:
    """Build a python -c command with proper quoting."""
    # On Windows, subprocess shell mode handles double-quote wrapping;
    # use single quotes inside to avoid escaping issues.
    return f'{PYTHON} -c "{code}"'


# Each test case: (description, command, expected_category)
TEST_CASES = [
    # ── Command Not Found ─────────────────────────────────────────
    (
        "Non-existent command",
        "thisisnotarealcommand123",
        "Command Not Found",
    ),
    # ── File Not Found ────────────────────────────────────────────
    (
        "Access non-existent file",
        "type nonexistent_file_xyz.txt" if os.name == "nt" else "cat nonexistent_file_xyz.txt",
        "File Not Found",
    ),
    # ── Python Syntax Error ───────────────────────────────────────
    (
        "Python syntax error",
        _py("def f( :"),
        "Syntax Error",
    ),
    # ── Python Module Not Found ───────────────────────────────────
    (
        "Python missing module",
        _py("import nonexistent_module_xyz"),
        "Module Not Found",
    ),
    # ── Python Name Error ─────────────────────────────────────────
    (
        "Python name error",
        _py("print(undefined_var_xyz)"),
        "Name Error",
    ),
    # ── Python Type Error ─────────────────────────────────────────
    (
        "Python type error",
        _py("len(42)"),
        "Type Error",
    ),
    # ── Permission Denied (simulated via stderr message) ──────────
    (
        "Simulated permission denied",
        _py("import sys; sys.stderr.write('PermissionError: Permission denied'); sys.exit(1)"),
        "Permission Denied",
    ),
    # ── FileNotFoundError via Python ──────────────────────────────
    (
        "Python FileNotFoundError",
        _py("import sys; sys.stderr.write('FileNotFoundError: No such file'); sys.exit(1)"),
        "File Not Found",
    ),
]


def run_tests():
    """Execute all error injection tests and display results."""
    executor = CommandExecutor()
    detector = ErrorDetector()

    table = Table(title="TerminAI — Error Injection Test Results", show_lines=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Test", style="cyan", min_width=30)
    table.add_column("Expected", style="yellow", min_width=18)
    table.add_column("Detected", style="magenta", min_width=18)
    table.add_column("DB Match", style="blue", min_width=6)
    table.add_column("Result", min_width=6)

    passed = 0
    total = len(TEST_CASES)

    for i, (description, command, expected_category) in enumerate(TEST_CASES, 1):
        result = executor.execute(command)
        error_info = detector.analyze(result)

        if error_info is None:
            detected = "No error detected"
            has_suggestion = "-"
            status = "[bold red]FAIL[/bold red]"
        else:
            detected = error_info.category
            has_suggestion = "Yes" if error_info.suggestion else "No"
            if detected == expected_category:
                status = "[bold green]PASS[/bold green]"
                passed += 1
            else:
                status = "[bold red]FAIL[/bold red]"

        table.add_row(str(i), description, expected_category, detected, has_suggestion, status)

    console.print()
    console.print(table)
    console.print(f"\n  [bold]{passed}/{total}[/bold] tests passed.\n")

    return passed == total


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
