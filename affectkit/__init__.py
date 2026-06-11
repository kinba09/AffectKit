"""AffectKit public API."""

from affectkit.engine import AffectEngine
from affectkit.memory import InteractionRecord, MemoryStore
from affectkit.profiles import EmotionProfile, load_profile
from affectkit.safety import SafetyPolicy
from affectkit.state import EmotionState

__all__ = [
    "AffectEngine",
    "EmotionProfile",
    "EmotionState",
    "InteractionRecord",
    "MemoryStore",
    "SafetyPolicy",
    "load_profile",
]

__version__ = "0.1.0"

