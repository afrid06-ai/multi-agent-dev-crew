# Elite AI Software Development Team — Project Walkthrough

A complete guide to how this CrewAI multi-agent system was implemented.

---

## 1. High-Level Architecture

The project is a **multi-agent software development pipeline** where 6 AI agents work in sequence, with a **review-fix loop** (2 cycles) to improve code quality. Each agent has a specialized role and uses tools to perform its job.

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Research   │ ──► │  Architect  │ ──► │ Code Generator   │ ──► │  Reviewer   │
└─────────────┘     └─────────────┘     └──────────────────┘     └──────┬──────┘
       │                    │                      │                     │
       │                    │                      │                     ▼
       │                    │                      │              ┌─────────────┐
       │                    │                      │              │   Fixer     │ ──┐
       │                    │                      │              └──────┬──────┘   │
       │                    │                      │                     │         │ 2 cycles
       │                    │                      │                     ▼         │
       │                    │                      │              ┌─────────────┐ │
       │                    │                      └─────────────►│  Reviewer   │─┘
       │                    │                                     └──────┬──────┘
       │                    │                                            │
       │                    │                                            ▼
       │                    │                                     ┌─────────────┐
       └────────────────────┴─────────────────────────────────────►│   Memory    │
                                                                    └─────────────┘
```

---

## 2. Entry Point: `src/main.py`

**Purpose:** CLI entry point that accepts a software request and runs the full crew.

**Flow:**
1. Loads `.env` for `DEEPSEEK_API_KEY`
2. Gets the prompt from command-line args or interactive input
3. Creates `output/` and `memory/` directories if missing
4. Instantiates the crew and calls `crew.kickoff(inputs={"topic": prompt})`
5. Prints the final result and each task’s output

```python
# Run with: python -m src.main "Your request here"
result = crew.kickoff(inputs={"topic": prompt})
```

---

## 3. LLM Configuration: `src/llm.py`

**Purpose:** Central LLM configuration using DeepSeek (OpenAI-compatible API).

**Implementation:**
- Reads `DEEPSEEK_API_KEY` from environment
- Creates a CrewAI `LLM` instance with:
  - `model="deepseek-chat"`
  - `base_url="https://api.deepseek.com/v1"` (required for compatibility)
  - `api_key` from env

**Why `/v1` in base_url?**  
CrewAI’s OpenAI-compatible client expects the base URL to end with `/v1` for chat completions.

---

## 4. Agents (`src/agents/`)

Each agent is defined by:
- **role** — Agent identity
- **goal** — What it optimizes for
- **backstory** — Context and behavior
- **tools** — Functions it can call
- **llm** — Shared DeepSeek LLM via `get_llm()`

### 4.1 Research Agent (`research.py`)

| Property  | Value |
|-----------|--------|
| Role      | Research Agent |
| Goal      | Fetch docs, version changes, breaking updates, structured summaries |
| Tools     | `read_file_tool`, `read_directory_tool` |
| Output    | Markdown technical summary |

Explores the project via file/directory tools and produces a structured research summary.

### 4.2 Architect Agent (`architect.py`)

| Property  | Value |
|-----------|--------|
| Role      | Architect Agent |
| Goal      | Design architecture, folder structure, APIs, library choices |
| Tools     | `read_file_tool`, `retrieve_decisions_tool` |
| Output    | Architecture document |
| Context   | Depends on Research task output |

Checks past decisions (memory) and produces an architecture document: folder layout, APIs, libraries.

### 4.3 Code Generator Agent (`code_generator.py`)

| Property  | Value |
|-----------|--------|
| Role      | Code Generator Agent |
| Goal      | Implement production-ready code following the architecture |
| Tools     | `read_file_tool`, `read_directory_tool`, `retrieve_decisions_tool` |
| Output    | Implementation (written to `output/implementation.md`) |
| Context   | Depends on Architect task output |

Uses the architecture and project context to produce detailed implementation specs and code.

### 4.4 Reviewer Agent (`reviewer.py`)

| Property  | Value |
|-----------|--------|
| Role      | Reviewer Agent |
| Goal      | Review for bugs, performance, security, refinements |
| Tools     | `read_file_tool`, `retrieve_decisions_tool` |
| Output    | Code review report (written to `output/review_report.md`) |
| Context   | Depends on Code Generator or Fixer task output |

Reviews the generated/fixed code and writes a prioritized review report.

### 4.5 Fixer Agent (`fixer.py`)

| Property  | Value |
|-----------|--------|
| Role      | Fixer Agent |
| Goal      | Apply review feedback; fix bugs, security, missing modules |
| Tools     | `read_file_tool`, `read_directory_tool`, `retrieve_decisions_tool` |
| Output    | Corrected implementation (overwrites `output/implementation.md`) |
| Context   | Depends on Code/Fix task + Review task output |

Addresses critical and high-priority issues from the review. Runs twice in the pipeline.

### 4.6 Memory Agent (`memory_agent.py`)

| Property  | Value |
|-----------|--------|
| Role      | Memory Agent |
| Goal      | Store and retrieve decisions; keep context for future runs |
| Tools     | `store_decision_tool`, `retrieve_decisions_tool` |
| Output    | Summary of stored decisions |
| Context   | Depends on Research, Architect, Reviewer outputs |

Extracts and stores architecture, library, and preference decisions for later sessions.

---

## 5. Tools (`src/tools/`)

### 5.1 Documentation Tools (`docs_tools.py`)

**`read_file_tool(file_path: str)`**
- Reads project files
- Paths are checked against the project root (no escape outside project)
- Returns file content or an error message

**`read_directory_tool(directory: str, pattern: Optional[str] = None)`**
- Lists files and subdirectories
- Optional glob pattern (e.g. `*.py`)
- Returns a formatted list (max 50 items)

### 5.2 Memory Tools (`memory_tools.py`)

**`store_decision_tool(category: str, content: str, tags: Optional[str] = None)`**
- Persists decisions in `memory/project_memory.json`
- Categories: `architecture`, `api`, `library`, `preference`, `bug_fix`, `security`
- Tags: comma-separated keywords for retrieval

**`retrieve_decisions_tool(query: str, category: Optional[str] = None)`**
- Searches by query and optional category
- Returns up to 10 recent matching decisions

---

## 6. Crew Definition: `src/crew.py`

**Task flow and dependencies:**

| Task  | Depends On | Output File |
|-------|------------|--------------|
| t1: Research | — | (in-memory) |
| t2: Architect | t1 | (in-memory) |
| t3: Code Generator | t2 | `output/implementation.md` |
| t4: Reviewer | t3 | `output/review_report.md` |
| t5: Fixer | t3, t4 | `output/implementation.md` |
| t6: Reviewer | t5 | `output/review_report.md` |
| t7: Fixer | t5, t6 | `output/implementation.md` |
| t8: Reviewer | t7 | `output/review_report.md` |
| t9: Memory | t1, t2, t8 | (in-memory) |

**Task descriptions use `{topic}`** — filled from `inputs={"topic": prompt}` at kickoff.

**Crew configuration:**
- `process=Process.sequential` — tasks run one after another
- `verbose=True` — detailed logging

---

## 7. Memory Storage: `src/memory_store.py` + `memory/`

- **Programmatic API:** `memory_store.store()` and `memory_store.retrieve()`
- **Agent access:** via `store_decision_tool` and `retrieve_decisions_tool`
- **Storage:** `memory/project_memory.json` — append-only JSON list of decisions

---

## 8. File Structure

```
GENAI_PROJECT/
├── .env                    # DEEPSEEK_API_KEY (not committed)
├── .env.example            # Template for .env
├── .python-version         # 3.11.9
├── requirements.txt       # crewai, openai, python-dotenv, pydantic
├── ARCHITECTURE.md         # Design doc
├── README.md               # User docs
├── WALKTHROUGH.md          # This file
│
├── src/
│   ├── main.py             # CLI entry
│   ├── crew.py             # Crew + tasks
│   ├── llm.py              # DeepSeek LLM config
│   ├── memory_store.py     # Programmatic memory
│   │
│   ├── agents/
│   │   ├── research.py
│   │   ├── architect.py
│   │   ├── code_generator.py
│   │   ├── reviewer.py
│   │   ├── fixer.py
│   │   └── memory_agent.py
│   │
│   └── tools/
│       ├── docs_tools.py   # read_file, read_directory
│       └── memory_tools.py # store_decision, retrieve_decisions
│
├── memory/
│   └── project_memory.json # Stored decisions
│
└── output/
    ├── implementation.md   # Code Generator output
    └── review_report.md   # Reviewer output
```

---

## 9. Execution Flow (Example Run)

**Command:** `python -m src.main "Build a FastAPI REST API for todo list"`

1. **main.py**
   - Load `.env`, ensure `output/` and `memory/` exist
   - Create crew
   - Call `crew.kickoff(inputs={"topic": "Build a FastAPI REST API for todo list"})`

2. **Research Agent**
   - Uses `read_file_tool` and `read_directory_tool` to inspect the project
   - Produces technical summary in Markdown

3. **Architect Agent**
   - Reads Research output from context
   - Uses `retrieve_decisions_tool` to avoid duplicating past decisions
   - Produces architecture document

4. **Code Generator Agent**
   - Reads Architect output from context
   - Produces implementation and writes to `output/implementation.md`

5. **Reviewer Agent**
   - Reads Code Generator output from context
   - Produces review and writes to `output/review_report.md`

6. **Memory Agent**
   - Reads Research, Architect, Reviewer outputs from context
   - Uses `store_decision_tool` to persist decisions
   - Produces summary of stored decisions

7. **main.py**
   - Prints the final result and per-task outputs

---

## 10. Dependencies

| Package | Purpose |
|---------|---------|
| crewai | Multi-agent framework |
| crewai-tools | Tool decorators |
| openai | Used by CrewAI for LLM calls |
| python-dotenv | Load `.env` |
| pydantic | Data validation |

---

## 11. Design Choices

1. **Sequential process with review-fix loop** — Research → Architect → Code → Review → [Fix → Review]×2 → Memory
2. **Context chaining** — Each task receives outputs from prior tasks as context
3. **Shared LLM** — Same DeepSeek LLM for all agents (via `get_llm()`)
4. **Path restrictions** — Tools limit access to project directory only
5. **JSON memory** — Simple, file-based storage for decisions across runs
6. **Output files** — `implementation.md` and `review_report.md` for generated code and reviews
