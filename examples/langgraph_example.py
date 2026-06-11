from affectkit import AffectEngine
from affectkit.adapters.langgraph import create_affect_node


def main() -> None:
    engine = AffectEngine.from_profile("profiles/anxious_researcher.yaml")
    affect_node = create_affect_node(engine)

    state = {
        "input": "This is not working and I do not understand the risk.",
        "messages": [],
    }
    new_state = affect_node(state)
    print(new_state["emotion_state"])
    print(new_state["detected_events"])
    print(new_state["affect_context"])


if __name__ == "__main__":
    main()

