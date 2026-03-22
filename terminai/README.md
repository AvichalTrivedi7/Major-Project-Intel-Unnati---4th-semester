# TerminAI — Intelligent AI Terminal Assistant

A developer tool that wraps your terminal, detects command errors in real time, classifies them, and provides intelligent fix suggestions.

## Features (Phase 1–2)

- Interactive terminal with persistent working directory
- Full command execution with stdout/stderr/exit-code capture
- Automatic error detection and keyword-based classification
- Predefined error database with fix suggestions
- Error injection test suite for validation
- Cross-platform support (Windows & Linux/macOS)
- Clean, colored UI via `rich`

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Copy and configure environment
cp .env.example .env
```

## Usage

```bash
# Start the interactive terminal
python main.py

# Run the error injection test suite
python test_errors.py
```

### Example session

```
TerminAI v0.1.0 — Intelligent AI Terminal Assistant
Type commands as usual. Type exit or quit to leave.

TerminAI /home/user
> pip install nonexistent-package-xyz

┌── ERROR ──────────────────────────────────┐
│ Category: Unknown Error                   │
│ ERROR: No matching distribution found ... │
└───────────────────────────────────────────┘
```

## Project Structure

```
terminai/
├── main.py              # Entry point — interactive loop
├── executor.py          # Command execution engine
├── error_detector.py    # Error detection & classification
├── ai_engine.py         # AI suggestion engine (Phase 3)
├── prompt_templates.py  # AI prompt formats (Phase 3)
├── formatter.py         # Rich terminal UI
├── config.py            # Centralized configuration
├── test_errors.py       # Error injection tests
├── data/
│   └── error_db.json    # Predefined error database
├── .env.example
├── requirements.txt
└── README.md
```

## Roadmap

- **Phase 1** — Terminal wrapper + error detection ✅
- **Phase 2** — Error injection & validation ✅
- **Phase 3** — AI integration (local model / API)
- **Phase 4** — UX enhancements + auto-fix execution
