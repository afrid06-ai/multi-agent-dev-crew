# Elite AI Software Development Team

A production-grade CrewAI multi-agent system for designing, developing, and reviewing software using structured delegation.

## Workflow

```
Research → Architect → Code Generator → Reviewer → [Fixer → Reviewer]×2 → Memory
```

| Agent | Responsibility |
|-------|----------------|
| **Research** | Fetch docs, version changes, technical summaries |
| **Architect** | Design architecture, folder structure, APIs |
| **Code Generator** | Write production-ready code |
| **Reviewer** | Review for bugs, performance, security |
| **Fixer** | Apply review feedback, fix critical issues (2 cycles) |
| **Memory** | Store and retrieve project decisions |

## Requirements

- **Python 3.11+** (uses `.python-version` for pyenv)
- **DEEPSEEK_API_KEY** (get key at https://platform.deepseek.com/)

## Setup

```bash
# Virtual env uses Python 3.11 (already configured)
source .venv/bin/activate
cp .env.example .env
# Add your DEEPSEEK_API_KEY to .env
```

## Run

```bash
python -m src.main "Build a FastAPI REST API for user management"
```

Or interactively:
```bash
python -m src.main
# Enter your request when prompted
```

## Project Structure

```
GENAI_PROJECT/
├── src/
│   ├── agents/       # Research, Architect, Code Generator, Reviewer, Memory
│   ├── tools/       # read_file, read_directory, store/retrieve decisions
│   ├── crew.py      # EliteDevCrew definition
│   └── main.py      # CLI entry
├── output/          # Generated artifacts
├── memory/          # Stored project decisions
└── ARCHITECTURE.md  # Design document
```

## Environment

- `DEEPSEEK_API_KEY` - Required for LLM (DeepSeek)
