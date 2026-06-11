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

## What Matters for This Project

AffectKit should be useful to serious Python and AI-agent developers. Contributions should protect these priorities:

- Clear positioning: AffectKit simulates affective state; it must not imply AI systems literally feel emotions.
- Small core: keep required dependencies limited to what the core library needs.
- Stable API shape: avoid breaking `EmotionState`, `EmotionProfile`, `AffectEngine`, adapters, and profile loading without a clear migration path.
- Safety boundaries: profiles and prompt modifiers must never enable abuse, threats, hate, manipulation, self-harm encouragement, or claims of real AI suffering.
- Deterministic core behavior: the MVP uses transparent event detection, not LLM-based hidden classification.
- Optional integrations: LangChain and LangGraph support must stay optional.
- Real tests: behavior changes need tests that fail before the fix and pass after it.
- Useful docs: public APIs, profiles, safety rules, and examples should be documented with runnable snippets.
- Packaging quality: keep `pyproject.toml`, extras, README install instructions, and CI working.
- Backward compatibility: prefer additive changes unless the project version and changelog clearly explain a breaking change.

## Commit Message Guide

Use short, specific commit messages. Prefer this format:

```text
type(scope): short imperative summary
```

Good commit types:

- `feat`: new user-facing capability.
- `fix`: bug fix.
- `docs`: documentation-only change.
- `test`: tests only.
- `refactor`: internal code change with no behavior change.
- `chore`: maintenance, tooling, metadata, or CI.
- `ci`: GitHub Actions or release automation.
- `security`: safety or vulnerability-related hardening.
- `profile`: built-in emotion profile changes.
- `example`: examples and demo scripts.

Examples:

```text
feat(engine): add deterministic frustration detection
fix(state): clamp decay outputs to valid range
docs(readme): add pip install instructions
test(safety): cover abusive mode sanitization
refactor(memory): simplify interaction record serialization
chore(package): update project metadata
ci(tests): run pytest across supported Python versions
security(safety): block manipulation instructions in profiles
profile(redteam): add safe hostile customer profile
example(langgraph): show affect node usage
```

Suggested commit names for common changes:

- New core engine feature: `feat(engine): add <capability>`
- Emotion state behavior change: `fix(state): correct <behavior>` or `feat(state): add <capability>`
- Safety rule change: `security(safety): block <unsafe behavior>`
- New YAML profile: `profile(<name>): add <purpose> profile`
- Profile tuning: `profile(<name>): tune <state or behavior>`
- LangChain adapter change: `feat(langchain): add <capability>` or `fix(langchain): handle <case>`
- LangGraph adapter change: `feat(langgraph): add <capability>` or `fix(langgraph): handle <case>`
- Documentation update: `docs(<area>): update <topic>`
- Example script: `example(<name>): demonstrate <workflow>`
- Test coverage: `test(<module>): cover <behavior>`
- CI update: `ci(tests): <change>`
- Packaging update: `chore(package): <change>`
- Release prep: `chore(release): prepare <version>`
- Breaking API change: `feat(api)!: change <public behavior>`

If a commit changes public behavior, mention tests in the PR description. If a commit changes safety behavior, explain the risk it reduces.

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
