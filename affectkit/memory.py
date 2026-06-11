"""In-memory interaction history for AffectKit."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class InteractionRecord:
    """Single interaction record with state snapshots."""

    turn_id: int
    user_input: str
    agent_output: str
    emotion_state_before: dict[str, float]
    emotion_state_after: dict[str, float]
    detected_events: list[str]
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn_id": self.turn_id,
            "user_input": self.user_input,
            "agent_output": self.agent_output,
            "emotion_state_before": dict(self.emotion_state_before),
            "emotion_state_after": dict(self.emotion_state_after),
            "detected_events": list(self.detected_events),
            "timestamp": self.timestamp,
        }


class MemoryStore:
    """Simple in-memory store for interaction records."""

    def __init__(self) -> None:
        self._records: list[InteractionRecord] = []

    def add(
        self,
        user_input: str,
        agent_output: str,
        emotion_state_before: dict[str, float],
        emotion_state_after: dict[str, float],
        detected_events: list[str],
    ) -> InteractionRecord:
        record = InteractionRecord(
            turn_id=len(self._records) + 1,
            user_input=user_input,
            agent_output=agent_output,
            emotion_state_before=dict(emotion_state_before),
            emotion_state_after=dict(emotion_state_after),
            detected_events=list(detected_events),
        )
        self._records.append(record)
        return record

    def last(self, n: int) -> list[InteractionRecord]:
        if n <= 0:
            return []
        return self._records[-n:]

    def to_list(self) -> list[dict[str, Any]]:
        return [record.to_dict() for record in self._records]

    def clear(self) -> None:
        self._records.clear()

    def __len__(self) -> int:
        return len(self._records)

