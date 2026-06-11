"""LangChain-style adapter.

LangChain is optional. This module does not import LangChain directly; it only
expects the wrapped object to expose an ``invoke`` method.
"""

from __future__ import annotations

from typing import Any

from affectkit.engine import AffectEngine, extract_user_input


class AffectLangChainWrapper:
    """Wrapper for LangChain-like runnables with an ``invoke`` method."""

    def __init__(self, agent: Any, engine: AffectEngine) -> None:
        self.agent = agent
        self.engine = engine

    def invoke(self, input_data: dict[str, Any] | str, *args: Any, **kwargs: Any) -> Any:
        payload = dict(input_data) if isinstance(input_data, dict) else {"input": input_data}
        user_input = extract_user_input(payload)
        state = self.engine.update(user_input)
        payload["affect_context"] = self.engine.to_prompt()
        payload["emotion_state"] = state.to_dict()
        payload["detected_events"] = list(self.engine.last_detected_events)
        result = self.agent.invoke(payload, *args, **kwargs)
        self.engine.record_interaction(user_input, _stringify_result(result))
        return result


def wrap_langchain_agent(agent: Any, engine: AffectEngine) -> AffectLangChainWrapper:
    """Wrap a LangChain-like agent or runnable."""

    return AffectLangChainWrapper(agent, engine)


def _stringify_result(result: Any) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        for key in ("output", "response", "content", "text"):
            value = result.get(key)
            if isinstance(value, str):
                return value
    return str(result)

