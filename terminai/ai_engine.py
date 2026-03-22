"""AI Suggestion Engine for TerminAI.

Supports two backends:
  1. Local model via llama-cpp-python (preferred)
  2. API fallback via OpenAI-compatible SDK

Returns structured suggestions parsed from the AI response.
"""

import re
from typing import Optional, Dict

from config import (
    AI_PROVIDER,
    AI_API_KEY,
    AI_MODEL,
    AI_API_BASE,
    LOCAL_MODEL_PATH,
    LOCAL_MODEL_CONTEXT,
    LOCAL_MODEL_THREADS,
)
from prompt_templates import SYSTEM_PROMPT, build_error_prompt


# ── Response parser ───────────────────────────────────────────────────────────

def _parse_response(raw: str) -> Dict[str, str]:
    """Parse the AI response into explanation / fix / command.

    Expected format:
        Explanation: ...
        Fix: ...
        Command: ...

    Falls back to a safe default if parsing fails.
    """
    result: Dict[str, str] = {}

    explanation_match = re.search(
        r"Explanation:\s*(.+?)(?=\nFix:|\Z)", raw, re.DOTALL | re.IGNORECASE
    )
    fix_match = re.search(
        r"Fix:\s*(.+?)(?=\nCommand:|\Z)", raw, re.DOTALL | re.IGNORECASE
    )
    command_match = re.search(
        r"Command:\s*(.+?)(?=\n\n|\Z)", raw, re.DOTALL | re.IGNORECASE
    )

    result["explanation"] = (
        explanation_match.group(1).strip() if explanation_match else "Could not determine the cause."
    )
    result["fix"] = (
        fix_match.group(1).strip() if fix_match else "Review the error output manually."
    )
    result["command"] = (
        command_match.group(1).strip() if command_match else ""
    )

    return result


# ── Local model backend (llama-cpp-python) ────────────────────────────────────

_local_model = None  # Lazy-loaded singleton


def _get_local_model():
    """Load the local GGUF model once and cache it."""
    global _local_model
    if _local_model is not None:
        return _local_model

    if not LOCAL_MODEL_PATH:
        return None

    try:
        from llama_cpp import Llama
        _local_model = Llama(
            model_path=LOCAL_MODEL_PATH,
            n_ctx=LOCAL_MODEL_CONTEXT,
            n_threads=LOCAL_MODEL_THREADS,
            verbose=False,
        )
        return _local_model
    except ImportError:
        return None
    except Exception:
        return None


def _query_local(prompt: str) -> Optional[str]:
    """Query the local llama-cpp model."""
    model = _get_local_model()
    if model is None:
        return None

    try:
        response = model.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=256,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]
    except Exception:
        return None


# ── API backend (OpenAI-compatible) ──────────────────────────────────────────

def _query_api(prompt: str) -> Optional[str]:
    """Query an OpenAI-compatible API."""
    if not AI_API_KEY:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=AI_API_KEY, base_url=AI_API_BASE)
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=256,
            temperature=0.2,
        )
        return response.choices[0].message.content
    except ImportError:
        return None
    except Exception:
        return None


# ── Public interface ─────────────────────────────────────────────────────────

def get_ai_suggestion(command: str, error: str, cwd: str = "") -> Optional[Dict[str, str]]:
    """Get an AI-generated fix suggestion for a failed command.

    Tries the configured provider first, falls back to the other.

    Args:
        command: The command that failed.
        error: The stderr output.
        cwd: Current working directory.

    Returns:
        A dict with keys 'explanation', 'fix', 'command', or None if AI
        is unavailable.
    """
    prompt = build_error_prompt(command, error, cwd)
    raw_response: Optional[str] = None

    if AI_PROVIDER == "local":
        raw_response = _query_local(prompt)
        if raw_response is None:
            # Fallback to API
            raw_response = _query_api(prompt)
    else:
        raw_response = _query_api(prompt)
        if raw_response is None:
            # Fallback to local
            raw_response = _query_local(prompt)

    if raw_response is None:
        return _fallback_response()

    return _parse_response(raw_response)


def _fallback_response() -> Dict[str, str]:
    """Return a safe fallback when AI is unavailable."""
    has_api = bool(AI_API_KEY)
    has_local = bool(LOCAL_MODEL_PATH)

    if not has_api and not has_local:
        return {
            "explanation": "AI is not configured.",
            "fix": "Set your API key in the .env file (TERMINAI_API_KEY) or provide a local model path (TERMINAI_LOCAL_MODEL_PATH).",
            "command": "",
        }

    return {
        "explanation": "AI engine could not generate a response.",
        "fix": "Check your AI provider configuration and network connectivity.",
        "command": "",
    }
