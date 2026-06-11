from pathlib import Path

import pytest
from pydantic import ValidationError

from affectkit.profiles import EmotionProfile, load_profile


def test_load_profile_by_name() -> None:
    profile = load_profile("calm_supportive")
    assert profile.name == "calm_supportive"
    assert profile.initial_state["trust"] > 0.5


def test_load_profile_by_path() -> None:
    profile = load_profile("profiles/angry_but_safe.yaml")
    assert profile.name == "angry_but_safe"
    assert "insult" in profile.transition_rules


def test_invalid_profile_validation_rejects_unknown_state() -> None:
    with pytest.raises(ValidationError):
        EmotionProfile(
            name="invalid",
            description="invalid profile",
            temperament={},
            initial_state={"assertiveness": 0.5},
            transition_rules={},
            behavior_policy={},
            safety={},
        )


def test_invalid_profile_file_rejects_out_of_range_value(tmp_path: Path) -> None:
    path = tmp_path / "invalid.yaml"
    path.write_text(
        """
name: invalid
description: invalid profile
temperament: {}
initial_state:
  anger: 2.0
transition_rules: {}
behavior_policy: {}
safety: {}
""",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError):
        load_profile(path)
