"""Command Execution Engine for TerminAI.

Handles subprocess execution, output capture, and working directory management.
"""

import subprocess
import shlex
import os
import re
from dataclasses import dataclass
from typing import Optional

from config import COMMAND_TIMEOUT, SHELL_MODE, INTERACTIVE_COMMANDS


@dataclass
class CommandResult:
    """Structured result from command execution."""
    stdout: str
    stderr: str
    returncode: int
    command: str
    timed_out: bool = False


class CommandExecutor:
    """Executes shell commands and captures structured output."""

    def __init__(self):
        self.cwd = os.getcwd()

    def execute(self, command: str, timeout: Optional[int] = None) -> CommandResult:
        """Execute a command and return structured output."""
        timeout = timeout or COMMAND_TIMEOUT

        # Block bare interactive commands that would hang the terminal
        if self._is_interactive(command):
            base = command.strip().split()[0]
            return CommandResult(
                stdout="",
                stderr=(
                    f"Interactive shell commands are not supported to prevent blocking. "
                    f"Use flags like '-c' to pass code directly.\n"
                    f"Example: {base} -c \"print('hello')\""
                ),
                returncode=1,
                command=command,
            )

        # Handle cd separately — it must modify our tracked cwd
        cd_path = self._parse_cd(command)
        if cd_path is not None:
            return self._handle_cd(cd_path, command)

        try:
            # On Windows, use shell=True so built-in commands (dir, cls, etc.) work.
            # On Unix, parse with shlex for safety unless the command uses shell features.
            if SHELL_MODE:
                args = command
                shell = True
            else:
                if self._needs_shell(command):
                    args = command
                    shell = True
                else:
                    args = shlex.split(command)
                    shell = False

            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                cwd=self.cwd,
                shell=shell,
                timeout=timeout,
                env=os.environ.copy(),
            )

            return CommandResult(
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode,
                command=command,
            )

        except subprocess.TimeoutExpired:
            return CommandResult(
                stdout="",
                stderr=f"Command timed out after {timeout} seconds.",
                returncode=-1,
                command=command,
                timed_out=True,
            )
        except FileNotFoundError:
            return CommandResult(
                stdout="",
                stderr=f"Command not found: {command.split()[0]}",
                returncode=127,
                command=command,
            )
        except Exception as e:
            return CommandResult(
                stdout="",
                stderr=str(e),
                returncode=1,
                command=command,
            )

    # ── Internal helpers ──────────────────────────────────────────────

    def _parse_cd(self, command: str) -> Optional[str]:
        """Return the target path if the command is a cd, else None."""
        stripped = command.strip()
        if stripped == "cd":
            return os.path.expanduser("~")
        match = re.match(r'^cd\s+(.+)$', stripped)
        if match:
            return match.group(1).strip().strip('"').strip("'")
        return None

    def _handle_cd(self, path: str, raw_command: str) -> CommandResult:
        """Change the tracked working directory."""
        target = os.path.expanduser(path)
        if not os.path.isabs(target):
            target = os.path.normpath(os.path.join(self.cwd, target))

        if os.path.isdir(target):
            self.cwd = target
            return CommandResult(
                stdout="",
                stderr="",
                returncode=0,
                command=raw_command,
            )
        else:
            return CommandResult(
                stdout="",
                stderr=f"cd: no such directory: {path}",
                returncode=1,
                command=raw_command,
            )

    @staticmethod
    def _is_interactive(command: str) -> bool:
        """Check if a command would open an interactive shell (no arguments)."""
        parts = command.strip().split()
        if len(parts) != 1:
            return False
        base = os.path.basename(parts[0]).lower()
        # Strip .exe suffix on Windows
        if base.endswith(".exe"):
            base = base[:-4]
        return base in INTERACTIVE_COMMANDS

    @staticmethod
    def _needs_shell(command: str) -> bool:
        """Check if a command requires shell interpretation (pipes, redirects, etc.)."""
        shell_chars = {'|', '>', '<', '&', ';', '&&', '||'}
        return any(ch in command for ch in shell_chars)
