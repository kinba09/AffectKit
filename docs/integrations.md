# Integrations

AffectKit is designed to work as middleware. The core package does not require LangChain or LangGraph.

## Basic Python Callable

```python
from affectkit import AffectEngine
from affectkit.adapters.basic import AffectWrapper

engine = AffectEngine.from_profile("calm_supportive")

def agent(payload):
    return payload["affect_context"]

wrapped = AffectWrapper(agent, engine)
result = wrapped.invoke("I am frustrated with this product.")
```

## LangChain

The LangChain adapter wraps any object with `.invoke()`. It stays thin and does not
import LangChain directly.

```python
from affectkit.adapters.langchain import with_affect

agent = with_affect(agent, engine)
response = agent.invoke({"input": "You explained this badly."})
```

The wrapper adds:

- `affect_context`
- `emotion_state`
- `detected_events`

`wrap_langchain_agent(agent, engine)` is also available as a more explicit alias
for the same behavior.

## LangGraph

The LangGraph adapter returns a node function:

```python
from affectkit.adapters.langgraph import create_affect_node

affect_node = create_affect_node(engine)
new_state = affect_node({"input": "This is not working.", "messages": []})
```

The returned state includes:

- `emotion_state`
- `affect_context`
- `detected_events`

## Custom Agents

For custom code, call the engine directly:

```python
state = engine.update(user_input)
affect_context = engine.to_prompt()
```

Pass `affect_context` into your model or agent alongside your normal system instructions.
