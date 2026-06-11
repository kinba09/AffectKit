"""Framework-agnostic AffectKit wrapper."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from affectkit.engine import AffectEngine


class AffectWrapper:
    """Wrap a plain Python callable with affective context."""

    def __init__(self, agent: Callable[[dict[str, Any]], Any], engine: AffectEngine) -> None:
        self.agent = agent
        self.engine = engine

    def invoke(self, user_input: str, **kwargs: Any) -> dict[str, Any]:
        state = self.engine.update(user_input)
        affect_context = self.engine.to_prompt()
        payload = {
            "input": user_input,
            "affect_context": affect_context,
            "emotion_state": state.to_dict(),
            **kwargs,
        }
        response = self.agent(payload)
        self.engine.record_interaction(user_input, self._stringify_response(response))
        return {
            "response": response,
            "emotion_state": state.to_dict(),
            "affect_context": affect_context,
            "detected_events": list(self.engine.last_detected_events),
        }

    @staticmethod
    def _stringify_response(response: Any) -> str:
        if isinstance(response, str):
            return response
        if isinstance(response, dict):
            for key in ("response", "output", "content", "text"):
                value = response.get(key)
                if isinstance(value, str):
                    return value
        return str(response)

