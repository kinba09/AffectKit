from affectkit.memory import MemoryStore
from affectkit.visualization import format_timeline


def test_memory_store_add_last_to_list_and_clear() -> None:
    memory = MemoryStore()
    memory.add(
        user_input="hello",
        agent_output="hi",
        emotion_state_before={"anger": 0.0},
        emotion_state_after={"anger": 0.1},
        detected_events=["praise"],
    )
    assert len(memory) == 1
    assert memory.last(1)[0].user_input == "hello"
    assert memory.to_list()[0]["detected_events"] == ["praise"]
    memory.clear()
    assert len(memory) == 0


def test_timeline_renders_records() -> None:
    memory = MemoryStore()
    before = {
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
    after = {**before, "anger": 0.4, "patience": 0.3}
    memory.add("input", "output", before, after, ["frustration"])
    timeline = format_timeline(memory.to_list())
    assert "Emotion Timeline" in timeline
    assert "primary=frustration" in timeline

