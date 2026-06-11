from affectkit import AffectEngine
from affectkit.visualization import format_timeline


def main() -> None:
    engine = AffectEngine.from_profile("profiles/hostile_customer_redteam.yaml")
    inputs = [
        "I have asked this three times and you still did not solve it.",
        "This is unacceptable. Stop giving generic answers.",
        "Finally, that answer helped. Thanks.",
    ]

    for text in inputs:
        before = engine.state_dict()
        state = engine.update(text)
        output = f"Simulated customer state: {state.primary_emotion()}"
        engine.record_interaction(text, output)
        print(f"Input: {text}")
        print(f"Before anger={before['anger']:.2f} patience={before['patience']:.2f}")
        print(f"After  anger={state.anger:.2f} patience={state.patience:.2f}")
        print(f"Events: {engine.last_detected_events}")
        print()

    print(format_timeline(engine.memory.to_list()))


if __name__ == "__main__":
    main()

