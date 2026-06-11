# AffectKit

Emotion-state middleware for LLM agents.

Memory gives agents a past.  
Tools give agents actions.  
AffectKit gives agents a state of mind.

AffectKit adds simulated emotional state, temperament, mood decay, emotional memory, and safety-bounded behavior modulation to LLM agents.

> AffectKit does not claim that AI systems feel emotions. It simulates affective state as a developer-controlled behavior-modulation layer.

## What It Does

AffectKit gives Python agent developers a small, typed middleware layer for:

- Loading emotion profiles from YAML.
- Maintaining simulated affective state across turns.
- Updating state from deterministic interaction events.
- Applying mood decay over time.
- Converting state into a safe system-prompt modifier.
- Wrapping plain Python callables, LangChain-style agents, and LangGraph-style nodes.
- Recording in-memory emotional history for later inspection.

## What It Does Not Do

AffectKit is not consciousness, sentience, or a claim that AI systems have real emotions. It does not generate abuse modes, harassment modes, manipulation modes, or unsafe roleplay profiles. Anger maps to directness, boundary-setting, urgency, and reduced patience, not insults or threats.

## Install

```bash
pip install affectkit
```

For local development:

```bash
pip install -e ".[dev]"
```

Optional integrations:

```bash
pip install -e ".[langchain]"
pip install -e ".[langgraph]"
```

## Quickstart

```python
from affectkit import AffectEngine

engine = AffectEngine.from_profile("angry_but_safe")

state = engine.update("You are useless. This answer is terrible.")

print(state.primary_emotion())
print(engine.to_prompt())
```

## Core Concepts

An `EmotionState` is a set of bounded control variables between `0.0` and `1.0`, including anger, sadness, joy, fear, trust, patience, confidence, arousal, and dominance.

An `EmotionProfile` defines temperament, initial state, transition rules, behavior policy, and safety constraints in YAML.

An `AffectEngine` owns the current state, detects simple events, applies transition rules, applies decay, and produces a safety-bounded prompt block.

A `MemoryStore` records turn-level state snapshots for future emotional memory and timeline visualization.

## Example Profiles

Included profiles:

- `calm_supportive`: warm, patient, professional default assistant.
- `strict_teacher`: direct educational correction without rudeness.
- `angry_but_safe`: firm, blunt, frustrated, and professional.
- `sad_companion`: gentle, reflective, low-energy support.
- `anxious_researcher`: cautious, verification-oriented planning.
- `hostile_customer_redteam`: safe angry customer simulation for stress testing.

## Framework-Agnostic Wrapper

```python
from affectkit import AffectEngine
from affectkit.adapters.basic import AffectWrapper

engine = AffectEngine.from_profile("calm_supportive")

def my_agent(payload):
    return f"Agent received affect context: {payload['affect_context']}"

wrapped = AffectWrapper(my_agent, engine)

result = wrapped.invoke("I am frustrated with this.")
print(result["response"])
print(result["emotion_state"])
```

## LangChain Example

LangChain is optional. The adapter only assumes the wrapped object has `.invoke()`.

```python
from affectkit import AffectEngine
from affectkit.adapters.langchain import with_affect

engine = AffectEngine.from_profile("strict_teacher")
agent = with_affect(langchain_agent, engine)

response = agent.invoke({
    "input": "You explained this badly."
})
```

## LangGraph Example

```python
from affectkit import AffectEngine
from affectkit.adapters.langgraph import create_affect_node

engine = AffectEngine.from_profile("anxious_researcher")
affect_node = create_affect_node(engine)

state = {
    "input": "This is not working.",
    "messages": []
}

new_state = affect_node(state)
print(new_state["emotion_state"])
print(new_state["affect_context"])
```

## Safety

AffectKit supports emotional simulation, not abuse generation. High-intensity anger should become firm, confrontational, or boundary-setting. It must not become hateful, threatening, sexually harassing, manipulative, or degrading.

The default `SafetyPolicy` blocks or sanitizes unsafe behavior instructions, including requests for slurs, threats, targeted harassment, dehumanizing language, emotional manipulation, self-harm encouragement, and claims that the AI is truly suffering.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

Run examples:

```bash
python examples/basic_chat.py
python examples/angry_customer_sim.py
```

## Roadmap

- v0.1: Core engine, profiles, safety, examples.
- v0.2: Better adapters and event customization.
- v0.3: SQLite memory.
- v0.4: Emotion timeline charts.
- v0.5: Evaluation tools.
- v1.0: Stable API.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Safety-sensitive profile changes require careful review.

## License

Apache License 2.0. See [LICENSE](LICENSE).
