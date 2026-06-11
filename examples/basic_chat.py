from affectkit import AffectEngine
from affectkit.adapters.basic import AffectWrapper


def my_agent(payload: dict) -> str:
    return (
        "I received your message with affective context. "
        f"Primary state: {payload['emotion_state']}"
    )


def main() -> None:
    engine = AffectEngine.from_profile("calm_supportive")
    wrapped = AffectWrapper(my_agent, engine)

    result = wrapped.invoke("I am frustrated with this product.")
    print(result["response"])
    print(result["affect_context"])
    print(result["detected_events"])


if __name__ == "__main__":
    main()
