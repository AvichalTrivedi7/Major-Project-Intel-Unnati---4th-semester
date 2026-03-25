"""Centralized configuration for TerminAI."""

import os
from pathlib import Path

# Load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
ERROR_DB_PATH = DATA_DIR / "error_db.json"

# Execution settings
COMMAND_TIMEOUT = 30  # seconds
SHELL_MODE = os.name == "nt"  # Use shell=True on Windows

# Interactive commands that block the terminal when run without arguments
INTERACTIVE_COMMANDS = {"python", "python3", "py", "node", "bash", "sh", "zsh",
                        "irb", "ruby", "lua", "R", "julia", "powershell", "pwsh"}

# AI settings
# Provider: "google" for Gemini API, "local" for llama-cpp-python
AI_PROVIDER = os.getenv("TERMINAI_AI_PROVIDER", "google")
GOOGLE_API_KEY = os.getenv("TERMINAI_GOOGLE_API_KEY", "")
GOOGLE_MODEL = os.getenv("TERMINAI_GOOGLE_MODEL", "gemini-1.5-flash")

# Local model settings (llama-cpp-python)
LOCAL_MODEL_PATH = os.getenv("TERMINAI_LOCAL_MODEL_PATH", "")
LOCAL_MODEL_CONTEXT = int(os.getenv("TERMINAI_LOCAL_MODEL_CONTEXT", "2048"))
LOCAL_MODEL_THREADS = int(os.getenv("TERMINAI_LOCAL_MODEL_THREADS", "4"))

# UI settings
APP_NAME = "TerminAI"
VERSION = "0.3.0"
