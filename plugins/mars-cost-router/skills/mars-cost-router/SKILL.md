---
name: mars-cost-router
description: Choose explicit Codex model, reasoning, and context settings for worthwhile bounded delegation while keeping the root responsible for integration and verification.
---

# Mars Cost Router

> **Instruction-driven and evidence-limited:** this skill advises the root model
> to set native spawn fields. It does not enforce or independently verify those
> settings. A requested lane is not evidence of the child's effective model or
> reasoning effort; inspect native child metadata when that distinction matters.

Use this skill from a Sol or Terra root running Codex multi-agent V2. Delegation
is optional. Keep work at the root when it is tiny, tightly coupled to the
current edit, depends on rapidly changing context, or costs more to specify and
review than to complete directly.

## Choose one lane

Every delegated call must explicitly set all three native V2 fields shown here:

| Lane | `model` | `reasoning_effort` | `fork_turns` |
| --- | --- | --- | --- |
| economy | `gpt-5.6-terra` | `low` | `none` |
| balanced | `gpt-5.6-terra` | `medium` | `none` |
| premium | `gpt-5.6-sol` | `high` | `none` |

- Choose **economy** for bounded read-only inspection, deterministic lookup,
  inventory, or a quick low-risk sanity check.
- Choose **balanced** for normal implementation, focused tests, documentation,
  analysis, or review with known boundaries.
- Choose **premium** for security-sensitive boundaries, architecture and
  integration decisions, broad uncertainty, difficult debugging, or work that
  failed or returned weak evidence in a lower lane.

Escalate uncertainty, risk, contradictory evidence, and failed work only after
the root reviews the prior result.

## Build the native V2 call

**REQUIRED — NEVER INHERIT:** every `spawn_agent` call must include `model`,
`reasoning_effort`, and `fork_turns`. Inheritance or omission of any of these
three fields is invalid. Do not spawn until all required fields are present in
the pending tool call.

Use the exact five-field input shape for the selected lane. Replace only
`task_name` and `message`; keep the three required routing values unchanged.

### Economy exact input

```json
{
  "task_name": "check_one",
  "message": "Complete one bounded task. Return the requested result. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "low",
  "fork_turns": "none"
}
```

### Balanced exact input

```json
{
  "task_name": "check_two",
  "message": "Complete one bounded task. Return the requested result. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "medium",
  "fork_turns": "none"
}
```

### Premium exact input

```json
{
  "task_name": "check_three",
  "message": "Complete one bounded task. Return the requested result. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-sol",
  "reasoning_effort": "high",
  "fork_turns": "none"
}
```

Customize each call as follows:

1. Set `task_name` to a short, generic, privacy-safe label such as
   `focused_check`, `test_run`, or `implementation_pass`. It is only a label and
   does not select a lane. Never include prompts, paths, filenames, user data,
   rationale, credentials, secrets, or sensitive content.
2. Write a self-contained `message` containing one concrete objective, exact
   scope and known facts, permissions and forbidden operations, acceptance
   criteria, and a bounded return format.
3. Include this exact child constraint: `Do not delegate or spawn another agent.`
4. Keep the template's REQUIRED `model`, `reasoning_effort`, and `fork_turns`
   fields. Always use `fork_turns: "none"` so the child does not inherit root
   turns.
5. Do not set `agent_type` or `service_tier`.

### Pre-call checklist

Before each spawn, verify every box. If any box fails, fix the call before
spawning:

- [ ] `task_name` is generic and privacy-safe.
- [ ] `message` is self-contained and prohibits nested delegation.
- [ ] REQUIRED `model` is present and exactly matches the selected template.
- [ ] REQUIRED `reasoning_effort` is present and exactly matches the template.
- [ ] REQUIRED `fork_turns` is present and equals `"none"`.
- [ ] `agent_type` and `service_tier` are absent.
- [ ] No required field relies on an inherited or default value.

Do not ask a child to maintain project-wide state, commit, publish, deploy,
access credentials, or perform production/destructive work unless the user has
explicitly authorized that exact action and the root can keep it safe and
bounded.

## Review and integrate

The root owns scope, integration, conflict resolution, final verification, and
the final claim. Check each child response against its acceptance criteria. If
the work is incomplete, risky, contradictory, or lacks evidence, repair it at
the root or issue a new self-contained call in an appropriate lane. Run final
validation at the root and describe only evidence actually observed.
