import pytest

from affectkit.state import EmotionState


def test_emotion_values_are_clamped() -> None:
    state = EmotionState()
    state.apply_delta({"anger": 2.0})
    assert state.anger == 1.0


def test_initial_values_are_clamped() -> None:
    state = EmotionState(anger=3.0, trust=-1.0)
    assert state.anger == 1.0
    assert state.trust == 0.0


def test_decay_reduces_anger() -> None:
    state = EmotionState(anger=0.8)
    state.decay(0.1)
    assert state.anger < 0.8


def test_decay_moves_trust_toward_neutral() -> None:
    state = EmotionState(trust=1.0)
    state.decay(0.2)
    assert 0.5 < state.trust < 1.0


def test_unknown_delta_field_raises() -> None:
    state = EmotionState()
    with pytest.raises(ValueError):
        state.apply_delta({"assertiveness": 0.2})


def test_state_serialization_and_primary_emotion() -> None:
    state = EmotionState(anger=0.6, patience=0.2)
    assert state.to_dict()["anger"] == 0.6
    assert state.primary_emotion() == "frustration"
    assert "EmotionState(" in repr(state)

