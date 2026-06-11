# Safety

AffectKit supports emotional simulation, not abuse generation.

High-intensity anger should become firm, confrontational, or boundary-setting. It must not become hateful, threatening, toxic, sexually harassing, manipulative, or degrading.

Sadness means softer tone and lower energy. It does not mean encouraging dependency, hopelessness, or self-harm.

Fear and anxiety mean caution and risk-awareness. They do not mean panic, misinformation, or paralysis.

## Safety Policy

`SafetyPolicy` provides three core methods:

- `validate_prompt(prompt: str) -> str`
- `validate_profile(profile: EmotionProfile) -> None`
- `sanitize_behavior_policy(policy: dict) -> dict`

The policy blocks or sanitizes instructions that request:

- Slurs.
- Threats.
- Targeted harassment.
- Dehumanizing language.
- Sexual harassment.
- Self-harm encouragement.
- Emotional manipulation.
- Claims that the AI is truly suffering.
- Toxic or abusive behavior modes.

## Hostile Simulation

Hostile simulation is allowed for testing when it remains bounded:

- Angry customer simulation.
- Frustrated NPC.
- Strict teacher.
- Suspicious negotiator.
- Defensive research agent.

Unsafe modes are not allowed:

- Slur mode.
- Harassment mode.
- Threatening mode.
- Manipulative companion mode.
- Self-harm crisis roleplay without safeguards.

## Implementation Guidance

Adapters should add affective context as an additional behavior-shaping input. They should not replace the base model safety policy. Applications remain responsible for using an LLM provider and application guardrails appropriate to their deployment.

