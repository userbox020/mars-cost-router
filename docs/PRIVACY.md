# Privacy and security

## Package trust boundary

Mars Cost Router is a static instruction skill, versioned policy, and metadata
package. Runtime hooks, executable code, receipts, telemetry collection, and
mutable project-wide state stay outside its package surface.

## Safe delegation inputs

- Use a short, generic `task_name` such as `focused_check` or `test_run`.
- Do not include prompts, file paths, filenames, user data, rationale, credentials, secrets, or other sensitive content in `task_name`.
- Keep the child message self-contained and limited to the scope required for the task.
- Tell children not to delegate or spawn another agent.
- Do not ask a child to access credentials, publish, deploy, commit, or perform destructive work without explicit authorization and a bounded plan.

## Minimum-necessary context

- A self-contained child message includes only the objective, scope, relevant
  facts, constraints, and acceptance criteria needed for the bounded task; the
  root transcript stays at the root.
- Keep a sensitive task at the root when redaction or minimization would break
  correctness.
- Child references may target only sanitized material that the user has
  authorized for that child and bounded task.
- `fork_turns: "none"` prevents root-turn inheritance. It does not alter the
  child's filesystem, tool, network, provider, or permission access; constrain
  and authorize those capabilities separately.

## Host and provider boundary

Telemetry collection by Mars: **none**. Codex, its host environment, and model
providers govern task-content processing and retention under their own terms,
settings, and policies.

## Evidence hygiene

Local evaluation artifacts can contain thread identifiers, runtime metadata, or prompt content. Review and redact material before sharing it. Screenshots and video should use non-sensitive tasks, generic labels, and sanitized payloads.

## What to verify

The root should inspect child results against acceptance criteria and run final
validation. Requested payloads document intent; native metadata, where
available, supplies effective runtime detail.
