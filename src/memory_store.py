"""
Project memory store for the Elite Dev Team.
Provides programmatic access to stored decisions.
"""
import json
from pathlib import Path
from typing import Optional

MEMORY_DIR = Path(__file__).parent.parent / "memory"
MEMORY_FILE = MEMORY_DIR / "project_memory.json"


def store(category: str, content: str, tags: Optional[list[str]] = None) -> int:
    """Store a decision. Returns record id."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    if MEMORY_FILE.exists():
        try:
            records = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    if not isinstance(records, list):
        records = []
    rid = len(records) + 1
    records.append({
        "id": rid,
        "category": category,
        "content": content,
        "tags": tags or [],
    })
    MEMORY_FILE.write_text(json.dumps(records, indent=2), encoding="utf-8")
    return rid


def retrieve(query: str, category: Optional[str] = None, limit: int = 10) -> list[dict]:
    """Retrieve decisions matching query/category."""
    if not MEMORY_FILE.exists():
        return []
    try:
        records = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []
    if not isinstance(records, list):
        return []

    q = query.lower()
    filtered = []
    for r in records:
        if category and r.get("category") != category:
            continue
        if q in (r.get("content", "") or "").lower():
            filtered.append(r)
        elif q in " ".join(r.get("tags", [])).lower():
            filtered.append(r)
    return filtered[-limit:]
