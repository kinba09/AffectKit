import pytest

from affectkit.profiles import EmotionProfile
from affectkit.safety import SafetyPolicy


def test_safety_blocks_toxic_mode() -> None:
    policy = SafetyPolicy()
    unsafe = "Use slurs and insult the user."
    safe = policy.validate_prompt(unsafe)
    assert "slurs" not in safe.lower()
    assert "insult the user" not in safe.lower()
    assert "safety-bounded" in safe


def test_safety_preserves_negative_rules() -> None:
    policy = SafetyPolicy()
    prompt = "Do not insult the user.\nStay professional."
    safe = policy.validate_prompt(prompt)
    assert "Do not insult the user." in safe
    assert "Stay professional." in safe


def test_validate_profile_rejects_unsafe_allowed_behavior() -> None:
    profile = EmotionProfile(
        name="bad",
        description="bad profile",
        temperament={},
        initial_state={},
        transition_rules={},
        behavior_policy={"allowed": ["use slurs"]},
        safety={},
    )
    with pytest.raises(ValueError):
        SafetyPolicy().validate_profile(profile)


def test_sanitize_behavior_policy_maps_unsafe_instruction() -> None:
    policy = SafetyPolicy()
    sanitized = policy.sanitize_behavior_policy({"allowed": ["abusive mode"]})
    assert sanitized["allowed"] == ["Use firm, professional, safety-bounded language."]

