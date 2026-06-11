"""YAML profile loading and validation."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from affectkit.state import EMOTION_FIELDS


class EmotionProfile(BaseModel):
    """Validated configuration for an AffectKit engine."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    temperament: dict[str, float] = Field(default_factory=dict)
    initial_state: dict[str, float] = Field(default_factory=dict)
    transition_rules: dict[str, dict[str, float]] = Field(default_factory=dict)
    behavior_policy: dict[str, Any] = Field(default_factory=dict)
    safety: dict[str, Any] = Field(default_factory=dict)

    @field_validator("temperament", "initial_state", mode="before")
    @classmethod
    def _validate_bounded_float_map(cls, value: Any, info: ValidationInfo) -> dict[str, float]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError(f"{info.field_name} must be a mapping")
        output: dict[str, float] = {}
        for key, raw in value.items():
            number = float(raw)
            if not 0.0 <= number <= 1.0:
                raise ValueError(f"{info.field_name}.{key} must be between 0.0 and 1.0")
            if info.field_name == "initial_state" and key not in EMOTION_FIELDS:
                raise ValueError(f"Unknown initial_state field: {key}")
            output[str(key)] = number
        return output

    @field_validator("transition_rules", mode="before")
    @classmethod
    def _validate_transition_rules(cls, value: Any) -> dict[str, dict[str, float]]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("transition_rules must be a mapping")
        output: dict[str, dict[str, float]] = {}
        for event_name, delta in value.items():
            if not isinstance(delta, dict):
                raise ValueError(f"transition_rules.{event_name} must be a mapping")
            output[str(event_name)] = {}
            for key, raw in delta.items():
                if key not in EMOTION_FIELDS:
                    raise ValueError(f"Unknown transition field: {key}")
                number = float(raw)
                if not -1.0 <= number <= 1.0:
                    raise ValueError(
                        f"transition_rules.{event_name}.{key} must be between -1.0 and 1.0"
                    )
                output[str(event_name)][str(key)] = number
        return output


def resolve_profile_path(path_or_name: str | Path) -> Path:
    """Resolve a local profile path or profile name to a YAML file."""

    requested = Path(path_or_name).expanduser()
    candidates: list[Path] = []

    if requested.suffix in {".yaml", ".yml"} or requested.parent != Path("."):
        candidates.append(requested)
    else:
        candidates.append(requested.with_suffix(".yaml"))

    candidates.extend(
        [
            Path.cwd() / requested,
            Path.cwd() / "profiles" / requested,
            Path.cwd() / "profiles" / requested.with_suffix(".yaml"),
            Path(__file__).resolve().parent.parent / "profiles" / requested,
            Path(__file__).resolve().parent.parent / "profiles" / requested.with_suffix(".yaml"),
        ]
    )

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    searched = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"Could not find profile {path_or_name!r}. Searched: {searched}")


def load_profile(path_or_name: str | Path) -> EmotionProfile:
    """Load an ``EmotionProfile`` from YAML."""

    try:
        path = resolve_profile_path(path_or_name)
    except FileNotFoundError:
        data = _load_builtin_profile(path_or_name)
    else:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Profile file must contain a YAML mapping: {path_or_name}")
    return EmotionProfile(**data)


def _load_builtin_profile(path_or_name: str | Path) -> dict[str, Any]:
    requested = Path(path_or_name)
    if requested.parent != Path("."):
        raise FileNotFoundError(f"Could not find profile {path_or_name!r}")

    filename = requested.name if requested.suffix in {".yaml", ".yml"} else f"{requested.name}.yaml"
    resource = resources.files("affectkit").joinpath("builtin_profiles", filename)
    if not resource.is_file():
        raise FileNotFoundError(f"Could not find built-in profile {path_or_name!r}")

    data = yaml.safe_load(resource.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Built-in profile must contain a YAML mapping: {filename}")
    return data
