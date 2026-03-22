"""Prompt templates for the AI suggestion engine.

Builds structured prompts that enforce a strict output format from the AI model.
"""

import os

SYSTEM_PROMPT = (
    "You are a terminal and DevOps expert. "
    "When given a failed command and its error output, you diagnose the issue "
    "and provide a concrete fix. "
    "You MUST respond STRICTLY in the following format with NO extra text:\n\n"
    "Explanation: <short explanation of the error>\n"
    "Fix: <what the user should do>\n"
    "Command: <exact command to run>\n"
)

ERROR_ANALYSIS_TEMPLATE = (
    "User executed the following command:\n"
    "{command}\n\n"
    "Error output:\n"
    "{error}\n\n"
    "Operating system: {os_name}\n"
    "Working directory: {cwd}\n\n"
    "Analyze this error and respond STRICTLY in this format:\n"
    "Explanation: <short explanation>\n"
    "Fix: <what to do>\n"
    "Command: <exact command>\n"
)


def build_error_prompt(command: str, error: str, cwd: str = "") -> str:
    """Build the user-message prompt for error analysis.

    Args:
        command: The command that failed.
        error: The stderr / error output.
        cwd: Current working directory (optional).

    Returns:
        A formatted prompt string.
    """
    return ERROR_ANALYSIS_TEMPLATE.format(
        command=command,
        error=error,
        os_name="Windows" if os.name == "nt" else "Linux/macOS",
        cwd=cwd or os.getcwd(),
    )
