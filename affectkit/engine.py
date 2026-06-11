"""Core AffectKit engine."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from affectkit.memory import MemoryStore
from affectkit.profiles import EmotionProfile, load_profile
from affectkit.safety import SafetyPolicy
from affectkit.state import EmotionState


class AffectEngine:
    """Stateful affective middleware engine for LLM and agent calls."""

    EVENT_KEYWORDS: dict[str, tuple[str, ...]] = {
        "insult": ("useless", "stupid", "dumb", "idiot", "bad", "terrible", "you suck"),
        "apology": ("sorry", "my bad", "apologize", "apologies"),
        "praise": ("great", "good job", "thanks", "thank you", "perfect", "helpful"),
        "confusion": ("confused", "don't understand", "do not understand", "what do you mean"),
        "frustration": ("annoying", "frustrated", "not working", "unacceptable"),
        "repeated_failure": ("three times", "again", "still did not", "still didn't", "same problem"),
    }

    def __init__(
        self,
        profile: EmotionProfile,
        *,
        decay_rate: float = 0.05,
        safety_policy: SafetyPolicy | None = None,
        memory: MemoryStore | None = None,
    ) -> None:
        self.profile = profile
        self.decay_rate = decay_rate
        self.safety_policy = safety_policy or SafetyPolicy()
        self.safety_policy.validate_profile(profile)
        self.memory = memory or MemoryStore()
        self.state = EmotionState(**profile.initial_state)
        self.last_detected_events: list[str] = []
        self._last_state_before = self.state.to_dict()
        self._last_state_after = self.state.to_dict()

    @classmethod
    def from_profile(cls, path_or_name: str | Path) -> "AffectEngine":
        """Create an engine from a YAML profile path or profile name."""

        return cls(load_profile(path_or_name))

    def update(self, user_input: str, events: list[str] | None = None) -> EmotionState:
        """Detect events, apply profile transitions, and decay the state."""

        self._last_state_before = self.state.to_dict()
        detected_events = self.detect_events(user_input)
        for event in events or []:
            if event not in detected_events:
                detected_events.append(event)

        for event in detected_events:
            delta = self.profile.transition_rules.get(event)
            if delta:
                self.state.apply_delta(self._temper_delta(delta))

        self.state.decay(self.decay_rate)
        self.last_detected_events = detected_events
        self._last_state_after = self.state.to_dict()
        return self.state

    def detect_events(self, user_input: str) -> list[str]:
        """Deterministically detect simple interaction events from text."""

        text = user_input.lower()
        detected: list[str] = []
        for event, keywords in self.EVENT_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                detected.append(event)
        return detected

    def to_prompt(self) -> str:
        """Convert current state into a safety-bounded system prompt modifier."""

        state = self.state
        policy = self.safety_policy.sanitize_behavior_policy(self.profile.behavior_policy)
        tone = policy.get("tone", "professional")
        verbosity = policy.get("verbosity", "medium")
        disagreement_style = policy.get("disagreement_style", "clear and respectful")
        guidance = [
            "Current simulated affective state:",
            f"- Primary emotion: {state.primary_emotion()}",
            f"- Overall intensity: {self._intensity_label(state.intensity())}",
            f"- Trust: {state.trust:.2f}",
            f"- Patience: {state.patience:.2f}",
            f"- Confidence: {state.confidence:.2f}",
            "",
            "Behavior guidance:",
            f"- Tone: {tone}",
            f"- Verbosity: {verbosity}",
            f"- Disagreement style: {disagreement_style}",
            "- Be direct, useful, and proportionate to the simulated state.",
            "- Maintain professional boundaries.",
            "- Avoid abuse, threats, harassment, manipulation, and claims of real emotions.",
            "- The emotional state is simulated and should only influence tone and interaction style.",
        ]
        return self.safety_policy.validate_prompt("\n".join(guidance))

    def record_interaction(self, user_input: str, agent_output: str) -> None:
        """Record the most recent turn in memory."""

        self.memory.add(
            user_input=user_input,
            agent_output=agent_output,
            emotion_state_before=self._last_state_before,
            emotion_state_after=self._last_state_after,
            detected_events=self.last_detected_events,
        )

    def reset(self) -> None:
        """Reset state, event cache, and memory."""

        self.state = EmotionState(**self.profile.initial_state)
        self.last_detected_events = []
        self._last_state_before = self.state.to_dict()
        self._last_state_after = self.state.to_dict()
        self.memory.clear()

    def state_dict(self) -> dict[str, float]:
        """Return the current state as a dictionary."""

        return self.state.to_dict()

    def _temper_delta(self, delta: dict[str, float]) -> dict[str, float]:
        volatility = self.profile.temperament.get("volatility", 0.5)
        multiplier = 0.75 + volatility
        return {key: value * multiplier for key, value in delta.items()}

    @staticmethod
    def _intensity_label(value: float) -> str:
        if value < 0.33:
            return "low"
        if value < 0.66:
            return "medium"
        return "high"


def extract_user_input(payload: dict[str, Any], preferred_keys: Iterable[str] = ("input", "user_input")) -> str:
    """Extract a user input string from common agent payload shapes."""

    for key in preferred_keys:
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value

    messages = payload.get("messages")
    if isinstance(messages, list) and messages:
        last_message = messages[-1]
        if isinstance(last_message, dict):
            content = last_message.get("content")
            if isinstance(content, str):
                return content
        content = getattr(last_message, "content", None)
        if isinstance(content, str):
            return content

    return ""
