"""Error Detection and Classification for TerminAI.

Detects errors via exit codes and stderr, classifies them using keyword matching,
and looks up suggestions from the predefined error database.
"""

import json
from dataclasses import dataclass
from typing import Optional, List

from executor import CommandResult
from config import ERROR_DB_PATH


@dataclass
class ErrorInfo:
    """Structured error analysis."""
    category: str
    stderr: str
    suggestion: Optional[str] = None
    matched_keyword: Optional[str] = None


# Ordered list — first match wins
ERROR_PATTERNS: List[dict] = [
    {"keyword": "command not found",    "category": "Command Not Found"},
    {"keyword": "not recognized",       "category": "Command Not Found"},       # Windows
    {"keyword": "is not recognized",    "category": "Command Not Found"},       # Windows verbose
    {"keyword": "no such file",         "category": "File Not Found"},
    {"keyword": "cannot find the path", "category": "File Not Found"},          # Windows
    {"keyword": "cannot find the file", "category": "File Not Found"},          # Windows type command
    {"keyword": "permission denied",    "category": "Permission Denied"},
    {"keyword": "access is denied",     "category": "Permission Denied"},       # Windows
    {"keyword": "modulenotfounderror",  "category": "Module Not Found"},
    {"keyword": "no module named",      "category": "Module Not Found"},
    {"keyword": "importerror",          "category": "Import Error"},
    {"keyword": "syntaxerror",          "category": "Syntax Error"},
    {"keyword": "invalid syntax",       "category": "Syntax Error"},
    {"keyword": "nameerror",            "category": "Name Error"},
    {"keyword": "typeerror",            "category": "Type Error"},
    {"keyword": "filenotfounderror",    "category": "File Not Found"},
    {"keyword": "connectionrefused",    "category": "Connection Error"},
    {"keyword": "connection refused",   "category": "Connection Error"},
    {"keyword": "timeout",             "category": "Timeout"},
]


class ErrorDetector:
    """Detects and classifies command execution errors."""

    def __init__(self):
        self.error_db = self._load_error_db()

    def analyze(self, result: CommandResult) -> Optional[ErrorInfo]:
        """Analyze a CommandResult and return ErrorInfo if an error is detected."""
        if not self._is_error(result):
            return None

        stderr_lower = result.stderr.lower()

        # Classify by keyword matching
        category = "Unknown Error"
        matched_keyword = None
        for pattern in ERROR_PATTERNS:
            if pattern["keyword"] in stderr_lower:
                category = pattern["category"]
                matched_keyword = pattern["keyword"]
                break

        # Look up suggestion from the error database
        suggestion = self._lookup_suggestion(stderr_lower, category)

        return ErrorInfo(
            category=category,
            stderr=result.stderr.strip(),
            suggestion=suggestion,
            matched_keyword=matched_keyword,
        )

    # ── Internal helpers ──────────────────────────────────────────────

    @staticmethod
    def _is_error(result: CommandResult) -> bool:
        """Determine if a command result represents an error."""
        if result.returncode != 0:
            return True
        # Some tools write warnings to stderr but exit 0 — only flag if exit code is nonzero
        return False

    def _lookup_suggestion(self, stderr_lower: str, category: str) -> Optional[str]:
        """Search the error database for a matching suggestion."""
        for entry in self.error_db:
            entry_keywords = [k.lower() for k in entry.get("keywords", [])]
            # Match if any keyword appears in stderr
            if any(kw in stderr_lower for kw in entry_keywords):
                return entry.get("suggestion")
            # Fallback: match by category name
            if entry.get("category", "").lower() == category.lower():
                return entry.get("suggestion")
        return None

    @staticmethod
    def _load_error_db() -> list:
        """Load the predefined error database."""
        try:
            with open(ERROR_DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
