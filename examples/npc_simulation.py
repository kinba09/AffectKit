from affectkit import AffectEngine


def main() -> None:
    engine = AffectEngine.from_profile("profiles/calm_supportive.yaml")

    scenes = [
        ("Player lies about the stolen key.", ["insult"]),
        ("Player helps the village repair the gate.", ["praise"]),
        ("Player attacks the guard.", ["frustration"]),
        ("Time passes.", []),
    ]

    for description, events in scenes:
        state = engine.update(description, events=events)
        print(description)
        print(
            f"primary={state.primary_emotion()} "
            f"trust={state.trust:.2f} anger={state.anger:.2f} patience={state.patience:.2f}"
        )
        print()


if __name__ == "__main__":
    main()

