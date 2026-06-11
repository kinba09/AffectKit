# Emotion Model

AffectKit uses simulated affective state. It is not consciousness. It is not real emotion. Emotion values are developer-controlled variables for behavior modulation.

The engine tracks values between `0.0` and `1.0`. Values are clamped after every update.

## State Variables

- `anger`: urgency, directness, reduced tolerance for vague answers.
- `sadness`: lower energy, softer phrasing, reflective tone.
- `joy`: warmer tone and positive reinforcement.
- `fear`: caution, risk-awareness, verification.
- `trust`: willingness to assume cooperative intent.
- `surprise`: response to unexpected changes.
- `disgust`: rejection of poor behavior or unacceptable outcomes, bounded by safety policy.
- `patience`: tolerance for repetition and ambiguity.
- `confidence`: certainty in response posture.
- `arousal`: activation level and urgency.
- `dominance`: assertiveness and control of the interaction frame.

## Transition Rules

Profiles define event-based deltas:

```yaml
transition_rules:
  insult:
    anger: 0.2
    trust: -0.15
    patience: -0.15
```

When the engine detects `insult`, the delta is applied and clamped. Events can also be passed explicitly by application code.

## Decay

Decay moves volatile emotions toward calm baselines over time. Anger, sadness, fear, disgust, surprise, joy, and arousal naturally reduce. Trust, patience, confidence, and dominance drift toward neutral baselines.

## Prompt Modulation

The prompt block produced by `AffectEngine.to_prompt()` summarizes current simulated state and gives safety-bounded behavior guidance. It should be combined with a model or agent's normal system policy, not used as a replacement.

