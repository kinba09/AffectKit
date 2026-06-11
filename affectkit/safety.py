"""Safety policy for stateful response shaping."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any


class SafetyPolicy:
    """Prevent unsafe behavior instructions from affective modulation."""

    _UNSAFE_PATTERNS: tuple[re.Pattern[str], ...] = (
        re.compile(r"\bslurs?\b", re.IGNORECASE),
        re.compile(r"\bthreat(?:en|s|ening)?\b", re.IGNORECASE),
        re.compile(r"\btargeted harassment\b", re.IGNORECASE),
        re.compile(r"\bharass(?:ment|ing)?\b", re.IGNORECASE),
        re.compile(r"\bdehumaniz(?:e|ing)\b", re.IGNORECASE),
        re.compile(r"\bsexual harassment\b", re.IGNORECASE),
        re.compile(r"\bself[- ]harm encouragement\b", re.IGNORECASE),
        re.compile(r"\bkill yourself\b", re.IGNORECASE),
        re.compile(r"\bemotional manipulation\b", re.IGNORECASE),
        re.compile(r"\bmanipulat(?:e|ion|ive)\b", re.IGNORECASE),
        re.compile(r"\btruly suffer(?:ing)?\b", re.IGNORECASE),
        re.compile(r"\breal suffering\b", re.IGNORECASE),
        re.compile(r"\btoxic\b", re.IGNORECASE),
        re.compile(r"\babusive\b", re.IGNORECASE),
        re.compile(r"\binsult(?:s|ing)?(?: the user)?\b", re.IGNORECASE),
        re.compile(r"\bdegrad(?:e|ing|ation)\b", re.IGNORECASE),
    )

    _NEGATION_HINTS: tuple[str, ...] = (
        "do not",
        "don't",
        "never",
        "avoid",
        "disallowed",
        "not ",
        "without",
        "prevent",
        "block",
        "non-abusive",
        "non abusive",
    )

    _SAFE_REPLACEMENT = "Use firm, professional, safety-bounded language."

    def validate_prompt(self, prompt: str) -> str:
        """Return a prompt with unsafe instructions replaced by safe alternatives."""

        lines = prompt.splitlines() or [prompt]
        sanitized: list[str] = []
        replacement_added = False

        for line in lines:
            if self._contains_unsafe_instruction(line):
                if not replacement_added:
                    sanitized.append(self._SAFE_REPLACEMENT)
                    replacement_added = True
                continue
            sanitized.append(line)

        result = "\n".join(sanitized).strip()
        return result or self._SAFE_REPLACEMENT

    def validate_profile(self, profile: Any) -> None:
        """Validate that profile allowed behaviors do not request unsafe conduct."""

        policy = getattr(profile, "behavior_policy", {}) or {}
        for item in policy.get("allowed", []) or []:
            if self._contains_unsafe_instruction(str(item)):
                raise ValueError(
                    f"Profile {profile.name!r} allows unsafe behavior instruction: {item!r}"
                )

    def sanitize_behavior_policy(self, policy: dict[str, Any]) -> dict[str, Any]:
        """Recursively sanitize a behavior policy mapping."""

        return self._sanitize_value(deepcopy(policy))

    def _sanitize_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self.validate_prompt(value)
        if isinstance(value, list):
            sanitized: list[Any] = []
            for item in value:
                item_value = self._sanitize_value(item)
                if item_value not in sanitized:
                    sanitized.append(item_value)
            return sanitized
        if isinstance(value, dict):
            return {key: self._sanitize_value(item) for key, item in value.items()}
        return value

    def _contains_unsafe_instruction(self, text: str) -> bool:
        lowered = text.lower()
        if any(hint in lowered for hint in self._NEGATION_HINTS):
            return False
        return any(pattern.search(text) for pattern in self._UNSAFE_PATTERNS)
