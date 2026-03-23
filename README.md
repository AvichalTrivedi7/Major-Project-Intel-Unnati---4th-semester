# 🧠 TerminAI — Intelligent AI Terminal Assistant

TerminAI is an AI-powered terminal wrapper that enhances traditional command-line interfaces by **detecting errors, analyzing them, and suggesting intelligent fixes in real-time**.

Built as part of the **Intel Unnati Program (End Semester Project)**, this project focuses on improving developer productivity in terminal-based environments.

---

## 🚀 Overview

Traditional terminals execute commands but provide limited assistance when errors occur.

TerminAI introduces an intelligent layer on top of the terminal:

* Executes commands like a normal shell
* Detects errors using system signals (exit codes + stderr)
* Classifies errors into meaningful categories
* Suggests fixes using:

  * Predefined knowledge base
  * AI (optional integration)
* Allows users to **auto-execute fixes safely**

---

## ⚙️ Core Features

### ✅ Terminal Wrapper

* Interactive CLI interface
* Executes real system commands
* Maintains working directory (`cd` support)

---

### ⚠️ Error Detection Engine

* Detects failures using:

  * Exit codes
  * stderr output
* Classifies errors:

  * Command not found
  * Module not found
  * Syntax error
  * Permission denied
  * File not found

---

### 📚 Predefined Fix System

* Uses `error_db.json`
* Provides instant suggestions for common errors
* Works without AI

---

### 🤖 AI Integration (Optional)

* Generates intelligent fixes when no predefined solution exists
* Supports:

  * OpenAI API (via API key)
  * Local models (llama-cpp)

---

### 🔄 Auto-Fix Execution

* Prompts user before executing fixes
* Executes safe suggested commands
* Displays results in real-time

---

### 🛑 Smart Safety Handling

* Blocks interactive commands like:

  * `python`, `py`, `node`, `bash`
* Prevents terminal hanging
* Allows safe alternatives (e.g., `py -c "code"`)

---

### 🎨 Clean CLI UI

* Built using `rich`
* Structured output:

  * COMMAND
  * OUTPUT
  * ERROR
  * SUGGESTION

---

## 🏗️ Architecture

```
User Input
   ↓
Command Execution (subprocess)
   ↓
Capture stdout / stderr / return code
   ↓
Error Detection & Classification
   ↓
Check Error Database
   ↓
AI Engine (if needed)
   ↓
Suggestion Output
   ↓
(Optional Auto-Fix Execution)
```

---

## 📁 Project Structure

```
terminai/
│
├── main.py              # CLI entry point
├── executor.py          # Command execution engine
├── error_detector.py    # Error detection & classification
├── ai_engine.py         # AI suggestion system
├── prompt_templates.py  # AI prompts
├── formatter.py         # CLI UI formatting
│
├── data/
│   └── error_db.json    # Predefined error solutions
│
├── config.py            # Configuration settings
├── .env.example         # Environment variables template
├── requirements.txt     # Dependencies
└── README.md
```

---

## 🧪 Example Usage

```bash
> py -c "import numpyy"
```

### Output:

```
[ERROR]
ModuleNotFoundError: No module named 'numpyy'

[SUGGESTION]
Explanation: Required Python module is missing
Fix: Install the module using pip
Command: pip install numpy

Run this fix? (y/n): y
```

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/terminai.git
cd terminai
pip install -r requirements.txt
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 🔑 Enable AI (Optional)

1. Copy environment file:

```bash
cp .env.example .env
```

2. Add your API key:

```
TERMINAI_AI_PROVIDER=api
TERMINAI_API_KEY=your_api_key_here
```

---

## 🧠 Tech Stack

* Python
* subprocess (system execution)
* rich (CLI UI)
* python-dotenv
* OpenAI API (optional)
* llama-cpp (optional local models)

---

## 📌 Key Highlights

* Built a **custom terminal wrapper**
* Implemented **real-time error detection system**
* Designed **modular AI integration layer**
* Ensured **safe execution with user confirmation**
* Created a **scalable architecture for future expansion**

---

## 🚀 Future Scope (Post Submission)

* Context-aware command suggestions
* DevOps workflow automation
* Project-aware AI assistant
* Full GUI-based terminal
* Learning-based error resolution system

---

## 👨‍💻 Author

_**Avichal Trivedi**_

AI & Software Development Enthusiast

---

## ⭐ Acknowledgment

Developed as part of the **Intel Unnati Program** focusing on real-world AI applications in developer tools.

---

