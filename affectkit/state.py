"""State primitives for simulated affective variables."""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import ClassVar

EMOTION_FIELDS: tuple[str, ...] = (
    "anger",
    "sadness",
    "joy",
    "fear",
    "trust",
    "surprise",
    "disgust",
    "patience",
    "confidence",
    "arousal",
    "dominance",
)

BASELINE_STATE: dict[str, float] = {
    "anger": 0.0,
    "sadness": 0.0,
    "joy": 0.0,
    "fear": 0.0,
    "trust": 0.5,
    "surprise": 0.0,
    "disgust": 0.0,
    "patience": 0.5,
    "confidence": 0.5,
    "arousal": 0.2,
    "dominance": 0.5,
}


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    """Clamp a float into the supported state range."""

    return min(max(float(value), lower), upper)


@dataclass
class EmotionState:
    """Bounded simulated emotional state for behavior modulation.

    Values are control variables in the inclusive range ``0.0`` to ``1.0``.
    They do not represent real emotion or consciousness.
    """

    anger: float = 0.0
    sadness: float = 0.0
    joy: float = 0.0
    fear: float = 0.0
    trust: float = 0.5
    surprise: float = 0.0
    disgust: float = 0.0
    patience: float = 0.75
    confidence: float = 0.5
    arousal: float = 0.2
    dominance: float = 0.5

    _PRIMARY_FIELDS: ClassVar[tuple[str, ...]] = (
        "anger",
        "sadness",
        "joy",
        "fear",
        "trust",
        "surprise",
        "disgust",
        "patience",
        "confidence",
    )

    _CORE_AFFECT_FIELDS: ClassVar[tuple[str, ...]] = (
        "anger",
        "sadness",
        "joy",
        "fear",
        "surprise",
        "disgust",
    )

    _VOLATILE_FIELDS: ClassVar[tuple[str, ...]] = (
        "anger",
        "sadness",
        "joy",
        "fear",
        "surprise",
        "disgust",
        "arousal",
    )

    def __post_init__(self) -> None:
        for field in fields(self):
            setattr(self, field.name, clamp(getattr(self, field.name)))

    def to_dict(self) -> dict[str, float]:
        """Return a plain dictionary representation."""

        return {field.name: getattr(self, field.name) for field in fields(self)}

    def copy(self) -> EmotionState:
        """Return a detached copy of the state."""

        return EmotionState(**self.to_dict())

    def primary_emotion(self) -> str:
        """Return the dominant readable state label."""

        if self.intensity() < 0.25:
            return "calm"
        if self.anger >= 0.35 and self.patience <= 0.4:
            return "frustration"
        core_primary = max(self._CORE_AFFECT_FIELDS, key=lambda key: self.to_dict()[key])
        if getattr(self, core_primary) >= 0.25:
            return core_primary
        if self.trust >= 0.6:
            return "trust"
        if self.patience >= 0.6:
            return "patience"
        if self.confidence >= 0.65:
            return "confidence"
        return max(self._PRIMARY_FIELDS, key=lambda key: self.to_dict()[key])

    def intensity(self) -> float:
        """Return a normalized overall intensity score."""

        volatile = [getattr(self, key) for key in self._VOLATILE_FIELDS]
        destabilizers = [
            max(0.0, BASELINE_STATE["trust"] - self.trust) * 2,
            max(0.0, BASELINE_STATE["patience"] - self.patience) * 2,
            max(0.0, BASELINE_STATE["confidence"] - self.confidence) * 2,
            max(0.0, self.dominance - 0.75),
        ]
        return clamp(max([*volatile, *destabilizers]))

    def apply_delta(self, delta: dict[str, float]) -> EmotionState:
        """Apply per-field changes and clamp all resulting values."""

        for key, change in delta.items():
            if key not in EMOTION_FIELDS:
                raise ValueError(f"Unknown emotion state field: {key}")
            setattr(self, key, clamp(getattr(self, key) + float(change)))
        return self

    def decay(self, rate: float) -> EmotionState:
        """Move state variables toward safe calm baselines."""

        rate = clamp(rate)
        for key in EMOTION_FIELDS:
            current = getattr(self, key)
            baseline = BASELINE_STATE[key]
            setattr(self, key, clamp(baseline + ((current - baseline) * (1.0 - rate))))
        return self

    def __repr__(self) -> str:
        values = ", ".join(f"{key}={value:.2f}" for key, value in self.to_dict().items())
        return f"EmotionState({values})"
