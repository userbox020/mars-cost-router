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
is optional.

## Decide whether and how to delegate

Apply this advisory precedence ladder before choosing a requested lane:

1. **Root / no delegation first.** Keep work at the root when it is tiny,
   tightly coupled to current edits, depends on rapidly changing root context,
   contains sensitive context that cannot be minimized safely, or costs more to
   specify and review than to complete directly.
2. **Premium if any trigger is present.** When delegation is worthwhile, request
   Premium for a security, authentication, credentials, sandbox, or permissions
   boundary; a production, destructive, or irreversible action; an architecture,
   cross-system, or data-integrity decision; broad uncertainty; or high
   consequence of error. Risk overrides activity labels such as review,
   documentation, or lookup.
3. **Economy only when all conditions hold.** The task must be bounded and
   independently checkable; deterministic and read-only, or a simple lookup;
   low consequence; governed by clear acceptance criteria; and require no
   sensitive context. If any condition fails, do not select Economy.
4. **Balanced is the delegated default.** When delegation is worthwhile, use
   Balanced if no Premium trigger is present and not all Economy conditions
   hold.

Do not select a lane from the task noun alone.

## Choose one lane

Every delegated call must explicitly set all three native V2 fields shown here:

| Lane | `model` | `reasoning_effort` | `fork_turns` |
| --- | --- | --- | --- |
| economy | `gpt-5.6-terra` | `low` | `none` |
| balanced | `gpt-5.6-terra` | `medium` | `none` |
| premium | `gpt-5.6-sol` | `high` | `none` |

## Handle failure and escalation by cause

`fallback_order` is advisory, reviewed escalation. It never means automatic
fallback, retry, or model substitution. The root owns each decision.

| Cause | Root-owned action |
| --- | --- |
| Weak evidence | Review it, then optionally issue a new self-contained next-lane request containing the unresolved gap and relevant observed evidence. Never blindly repeat the unchanged request. |
| Contradictory evidence | Review and reconcile the conflict before any new self-contained next-lane request; include the unresolved gap and relevant observed evidence. |
| Malformed or missing requested fields, or incorrectly scoped message | Correct the call before spawning, or retry in the same appropriate lane after correction. This is correction, not escalation. |
| Missing requirements, ambiguity, permission denial, or absent authorization | Return to root or user clarification. Lane escalation does not solve missing authority or requirements. |
| Requested model or tool unavailable | Stop and report the availability problem. Never silently substitute another model or treat unavailability as capability escalation. |
| Increased risk or new security/high-consequence boundary | Move to Premium or keep the work at the root. Required user authorization still applies. |
| Premium failure | Stop for root review or clarification; there is no lane above Premium. |
| De-escalation | Apply only to a newly isolated, independently checkable lower-risk subtask, never to the same failed task. |

## Decompose and assign ownership

Delegate only independently checkable units. Give each child one concrete
objective, exact scope expressed as questions or repository-relative paths in
the message, and acceptance criteria.

- Within a parallel batch, assign at most one child writer to each file or area.
  Re-scope overlapping work or serialize it under root review.
- Parallelize only independent tasks. Serialize dependencies, and do not start a
  dependent child before prerequisite evidence is reviewed.
- Keep cross-cutting integration, conflict resolution, final architectural or
  product decisions, and final claims at the root.
- Delegate commits, publication, deployment, credential access, or destructive
  actions only when the user explicitly authorizes that exact bounded action and
  existing safety guidance permits it.
- Children never delegate or spawn another agent.

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

## Optional child return contracts

These are optional requested formats. The package does not validate or enforce
a child response shape. Choose one only when it makes the handoff clearer.

### Read-only locator

For a bounded inspection or lookup, request one result per line as:

`relative/path:line — symbol — short finding`

Use repository-relative locations so the root can inspect each finding directly.

### Focused edit handoff

For implementation work, request an edit handoff or change summary containing:

- changed repository-relative paths;
- verification actually run and the observed result;
- skipped checks; and
- remaining risks.

For implementation or dependent work, request: `State whether the task is
complete. If partial or blocked, identify remaining work, verification gaps, and
any root decision needed.` Child status remains unverified until the root checks
the work; it is not proof of completion.

### Review

Request findings first, ordered **critical**, **high**, **medium**, then **low**.
Each finding should include a repository-relative location and a concrete impact
or action. If there are no findings, say `No findings` and identify verification
gaps.

### Clarity and safety override

Do not force brevity or omit material context for security, destructive or
production actions, ambiguity, conflicting evidence, missing verification, or
required user authorization. Never include credentials, private prompts,
home-directory paths, or unrelated local details.

## Review and integrate

The root unconditionally owns cross-cutting integration, conflict resolution,
final architectural or product decisions, final verification, and final claims.
Check each child response against its acceptance criteria.

### Root acceptance checklist

- Inspect cited locations and diffs.
- Confirm changed paths remained in assigned scope and ownership did not overlap.
- Distinguish checks actually run from skipped checks.
- Reconcile conflicting findings or edits.
- Rerun final relevant checks at the root.
- Treat `partial` or `blocked` as unresolved and report gaps and risks.
- At final reporting, describe only evidence actually observed.

If work is incomplete, risky, contradictory, or lacks evidence, repair it at the
root or issue a new self-contained call in an appropriate lane.
