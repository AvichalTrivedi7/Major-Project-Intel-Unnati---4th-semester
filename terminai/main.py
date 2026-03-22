"""TerminAI — Intelligent AI Terminal Assistant.

Main entry point: runs the interactive terminal loop.
"""

import sys

from executor import CommandExecutor
from error_detector import ErrorDetector
from ai_engine import get_ai_suggestion
from formatter import (
    print_banner,
    print_prompt,
    print_output,
    print_error,
    print_suggestion,
    print_ai_suggestion,
    print_no_suggestion,
    print_ai_status,
    print_fix_prompt,
    print_fix_running,
    print_fix_result,
    print_fix_skipped,
    print_info,
)


def _extract_fix_command(error_info, ai_result):
    """Extract an executable fix command from the suggestion sources.

    Returns the command string if one is available, or empty string.
    DB suggestions are free-text so they don't carry an executable command.
    AI results carry a parsed 'command' field.
    """
    if ai_result and ai_result.get("command", "").strip():
        return ai_result["command"].strip()
    return ""


def _ask_user_confirmation() -> bool:
    """Ask user y/n and return True for yes."""
    try:
        answer = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return answer in ("y", "yes")


def main():
    executor = CommandExecutor()
    detector = ErrorDetector()

    print_banner()

    while True:
        try:
            print_prompt(executor.cwd)
            user_input = input().strip()
        except (EOFError, KeyboardInterrupt):
            print_info("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print_info("Goodbye!")
            break

        # 1. Execute the command
        result = executor.execute(user_input)

        # 2. Show stdout if present
        print_output(result)

        # 3. Detect and analyze errors
        error_info = detector.analyze(result)
        if not error_info:
            continue

        print_error(result, error_info)

        # 4. Try error database first, then AI
        ai_result = None
        fix_command = ""

        if error_info.suggestion:
            # DB match found — display it
            print_suggestion(error_info.suggestion)
            # DB suggestions are descriptive text, no executable command to offer
        else:
            # No DB match — query AI
            print_ai_status("No match in error database. Querying AI engine...")
            ai_result = get_ai_suggestion(
                result.command, result.stderr, executor.cwd
            )
            if ai_result:
                print_ai_suggestion(ai_result)
                fix_command = ai_result.get("command", "").strip()
            else:
                print_no_suggestion()

        # 5. Offer to execute fix if we have a valid command
        if fix_command:
            print_fix_prompt(fix_command)
            if _ask_user_confirmation():
                print_fix_running(fix_command)
                fix_result = executor.execute(fix_command)
                print_fix_result(fix_result)
            else:
                print_fix_skipped()


if __name__ == "__main__":
    main()
