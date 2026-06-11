from affectkit import AffectEngine
from affectkit.adapters.basic import AffectWrapper
from affectkit.adapters.langgraph import create_affect_node


def test_event_detection_detects_insult_and_frustration() -> None:
    engine = AffectEngine.from_profile("profiles/angry_but_safe.yaml")
    events = engine.detect_events("You are useless and this is not working.")
    assert "insult" in events
    assert "frustration" in events


def test_insult_increases_anger() -> None:
    engine = AffectEngine.from_profile("profiles/angry_but_safe.yaml")
    before = engine.state.anger
    engine.update("You are useless.")
    assert engine.state.anger > before


def test_apology_increases_trust() -> None:
    engine = AffectEngine.from_profile("profiles/angry_but_safe.yaml")
    before = engine.state.trust
    engine.update("Sorry, my bad.")
    assert engine.state.trust > before


def test_to_prompt_contains_safe_simulation_boundary() -> None:
    engine = AffectEngine.from_profile("profiles/calm_supportive.yaml")
    prompt = engine.to_prompt()
    assert "Current simulated affective state" in prompt
    assert "The emotional state is simulated" in prompt


def test_basic_wrapper_returns_response_and_metadata() -> None:
    engine = AffectEngine.from_profile("profiles/calm_supportive.yaml")

    def agent(payload: dict) -> str:
        assert "affect_context" in payload
        assert "emotion_state" in payload
        return "ok"

    wrapped = AffectWrapper(agent, engine)
    result = wrapped.invoke("This is not working.")
    assert result["response"] == "ok"
    assert "emotion_state" in result
    assert "frustration" in result["detected_events"]
    assert len(engine.memory) == 1


def test_langgraph_node_output_shape() -> None:
    engine = AffectEngine.from_profile("profiles/anxious_researcher.yaml")
    node = create_affect_node(engine)
    state = node({"input": "I am confused. What do you mean?", "messages": []})
    assert "emotion_state" in state
    assert "affect_context" in state
    assert "detected_events" in state
    assert "confusion" in state["detected_events"]

