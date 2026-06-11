"""LangGraph node adapter."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from affectkit.engine import AffectEngine, extract_user_input


def create_affect_node(engine: AffectEngine) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Create a LangGraph-compatible node that enriches graph state."""

    def affect_node(state: dict[str, Any]) -> dict[str, Any]:
        user_input = extract_user_input(state)
        emotion_state = engine.update(user_input)
        return {
            **state,
            "emotion_state": emotion_state.to_dict(),
            "affect_context": engine.to_prompt(),
            "detected_events": list(engine.last_detected_events),
        }

    return affect_node

