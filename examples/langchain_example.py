from affectkit import AffectEngine
from affectkit.adapters.langchain import wrap_langchain_agent


class MockLangChainAgent:
    def invoke(self, payload: dict) -> dict:
        return {
            "output": "Replace MockLangChainAgent with a LangChain runnable or agent.",
            "received_affect_context": "affect_context" in payload,
        }


def main() -> None:
    engine = AffectEngine.from_profile("profiles/strict_teacher.yaml")
    agent = wrap_langchain_agent(MockLangChainAgent(), engine)

    response = agent.invoke({"input": "You explained this badly."})
    print(response)
    print(engine.state_dict())


if __name__ == "__main__":
    main()

