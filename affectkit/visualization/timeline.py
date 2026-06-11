"""Terminal timeline rendering."""

from __future__ import annotations

from typing import Any

from affectkit.state import EmotionState


def format_timeline(records: list[dict[str, Any]]) -> str:
    """Return a terminal-friendly emotion timeline."""

    lines = ["Emotion Timeline", ""]
    for record in records:
        after = record.get("emotion_state_after") or {}
        state = EmotionState(**after)
        lines.append(
            "Turn {turn:<2} | primary={primary:<11} | "
            "anger={anger:.2f} sadness={sadness:.2f} trust={trust:.2f} patience={patience:.2f}".format(
                turn=record.get("turn_id", "?"),
                primary=state.primary_emotion(),
                anger=state.anger,
                sadness=state.sadness,
                trust=state.trust,
                patience=state.patience,
            )
        )
    return "\n".join(lines)


def render_timeline(records: list[dict[str, Any]]) -> None:
    """Print a terminal-friendly emotion timeline."""

    print(format_timeline(records))

