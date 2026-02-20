# Elite AI Software Development Team - Architecture

## Design Overview

A CrewAI-based multi-agent system that follows a strict sequential workflow for software development.

## Workflow (Sequential)

```
Research → Architect → Code Generator → Reviewer → [Fixer → Reviewer]×2 → Memory
```

## Folder Structure

```
GENAI_PROJECT/
├── src/
│   ├── __init__.py
│   ├── agents/           # Agent definitions
│   │   ├── __init__.py
│   │   ├── research.py
│   │   ├── architect.py
│   │   ├── code_generator.py
│   │   ├── reviewer.py
│   │   ├── fixer.py
│   │   └── memory_agent.py
│   ├── tools/            # Custom tools
│   │   ├── __init__.py
│   │   ├── docs_tools.py
│   │   └── memory_tools.py
│   ├── crew.py           # EliteDevCrew
│   ├── memory_store.py   # Project memory
│   └── main.py           # CLI entry
├── config/               # Configuration
├── memory/               # Persisted memory data
├── output/               # Generated artifacts
├── requirements.txt
└── README.md
```

## Agent Responsibilities

| Agent | Input | Output | Tools |
|-------|-------|--------|-------|
| Research | User request, topic | Technical summary, version info | FileReadTool, DirectoryReadTool |
| Architect | Research output | Architecture doc, folder structure, APIs | FileReadTool |
| Code Generator | Architecture, research | Production code | FileReadTool |
| Reviewer | Generated/fixed code | Review report, improvements | FileReadTool |
| Fixer | Code + Review output | Fixed implementation | FileReadTool, DirectoryReadTool |
| Memory | All outputs | Updated memory, stored decisions | MemoryStoreTool |

## APIs

- **EliteDevCrew.kickoff(inputs)** - Run full pipeline
- **EliteDevCrew.run_research_only()** - Research only
- **MemoryStore.store()** - Store decision
- **MemoryStore.retrieve()** - Retrieve by query
