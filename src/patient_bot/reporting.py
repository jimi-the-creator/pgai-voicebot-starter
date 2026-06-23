from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import json


ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT_DIR = ROOT / "calls" / "transcripts"


def _stringify_turn(item: dict[str, Any]) -> str | None:
    role = (
        item.get("role")
        or item.get("speaker")
        or item.get("participant_identity")
        or item.get("sender")
        or "unknown"
    )

    content = item.get("content") or item.get("text") or item.get("message")
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, str):
                parts.append(c)
            elif isinstance(c, dict):
                parts.append(str(c.get("text") or c.get("content") or ""))
        content = " ".join(p for p in parts if p).strip()

    if not content:
        return None

    return f"{role}: {content}"


def _find_turns(obj: Any) -> list[str]:
    turns: list[str] = []

    if isinstance(obj, dict):
        maybe = _stringify_turn(obj)
        if maybe:
            turns.append(maybe)

        for value in obj.values():
            turns.extend(_find_turns(value))

    elif isinstance(obj, list):
        for item in obj:
            turns.extend(_find_turns(item))

    # Deduplicate while preserving order.
    seen = set()
    clean = []
    for t in turns:
        if t not in seen:
            seen.add(t)
            clean.append(t)
    return clean


def save_session_report(room_name: str, scenario_id: str, report_dict: dict[str, Any]) -> None:
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = TRANSCRIPT_DIR / f"call-{scenario_id}-{room_name}-{stamp}"

    json_path = base.with_suffix(".json")
    txt_path = base.with_suffix(".txt")

    json_path.write_text(json.dumps(report_dict, indent=2), encoding="utf-8")

    turns = _find_turns(report_dict)
    if turns:
        text = "\n".join(turns)
    else:
        text = (
            "Transcript extraction fallback: no simple turn list found. "
            "Open the JSON session report next to this file and copy the history section.\n\n"
            + json.dumps(report_dict, indent=2)[:12000]
        )

    txt_path.write_text(text, encoding="utf-8")

    print(f"Saved session report: {json_path}")
    print(f"Saved transcript: {txt_path}")
