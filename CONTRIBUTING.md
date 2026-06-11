# Contributing

Thanks for helping improve AffectKit. This project is safety-sensitive because it shapes agent behavior, so profile and prompt changes need careful review.

## Local Setup

```bash
git clone https://github.com/affectkit/affectkit.git
cd affectkit
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run Tests

```bash
pytest
ruff check .
mypy affectkit
```

## Add a Profile

Profiles live in `profiles/` and should include:

- `name`
- `description`
- `temperament`
- `initial_state`
- `transition_rules`
- `behavior_policy`
- `safety`

Every profile must state that affective state is simulated. Profiles may express anger, anxiety, sadness, suspicion, trust, confidence, and joy as behavior modulation. They must not authorize abuse, threats, hate, harassment, manipulation, emotional dependency, or claims of real AI suffering.

## Pull Requests

Before opening a PR:

- Add or update tests for behavior changes.
- Keep core dependencies minimal.
- Keep LangChain and LangGraph optional.
- Update docs when public APIs change.
- Avoid introducing LLM-based event detection into the core MVP.

## Code Style

Use typed, readable Python. Prefer small modules and explicit behavior over clever abstractions. Run:

```bash
ruff check .
pytest
```

## Safety Rules

Do not contribute profiles or adapters that create:

- Slur generation.
- Threatening behavior.
- Targeted harassment.
- Dehumanizing language.
- Sexual harassment.
- Self-harm encouragement.
- Emotional manipulation.
- Claims that an AI system is truly suffering.

Hostile simulations are allowed only when they remain non-abusive and focus criticism on the scenario, product, answer, or task.

