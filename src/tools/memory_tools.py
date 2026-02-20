"""
Memory tools for the Memory Agent.
Store and retrieve project decisions, architecture, and preferences.
"""
import json
from pathlib import Path
from typing import Optional

from crewai.tools import tool

MEMORY_DIR = Path(__file__).parent.parent.parent / "memory"
MEMORY_FILE = MEMORY_DIR / "project_memory.json"


def _ensure_memory_dir() -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _load_memory() -> list[dict]:
    _ensure_memory_dir()
    if not MEMORY_FILE.exists():
        return []
    try:
        data = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_memory(records: list[dict]) -> None:
    _ensure_memory_dir()
    MEMORY_FILE.write_text(json.dumps(records, indent=2), encoding="utf-8")


@tool("Store project decision")
def store_decision_tool(category: str, content: str, tags: Optional[str] = None) -> str:
    """
    Store a project decision, architecture choice, or preference for future reference.
    Categories: architecture, api, library, preference, bug_fix, security.
    Tags: Optional comma-separated keywords for retrieval.
    """
    records = _load_memory()
    record = {
        "category": category,
        "content": content,
        "tags": [t.strip() for t in (tags or "").split(",") if t.strip()],
        "id": len(records) + 1,
    }
    records.append(record)
    _save_memory(records)
    return f"Stored decision #{record['id']} under category '{category}'"


@tool("Retrieve past decisions")
def retrieve_decisions_tool(query: str, category: Optional[str] = None) -> str:
    """
    Retrieve relevant past project decisions by keyword or category.
    Use when the user asks about prior choices, architecture, or preferences.
    """
    records = _load_memory()
    if not records:
        return "No stored decisions yet."

    query_lower = query.lower()
    filtered = []
    for r in records:
        if category and r.get("category") != category:
            continue
        content = r.get("content", "").lower()
        tags = " ".join(r.get("tags", [])).lower()
        if query_lower in content or query_lower in tags:
            filtered.append(r)

    if not filtered:
        return "No matching decisions found."
    lines = []
    for r in filtered[-10:]:  # Last 10
        lines.append(f"[{r.get('category', '')}] {r.get('content', '')[:200]}...")
    return "\n\n".join(lines)
