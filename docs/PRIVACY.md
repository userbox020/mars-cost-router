# Privacy and security

## Package boundary

Mars Cost Router has no runtime hooks, executable runtime, receipt store, telemetry collector, or mutable project-wide state. It is an instruction-driven skill and policy, not an enforcement layer.

## Safe delegation inputs

- Use a short, generic `task_name` such as `focused_check` or `test_run`.
- Do not include prompts, file paths, filenames, user data, rationale, credentials, secrets, or other sensitive content in `task_name`.
- Keep the child message self-contained and limited to the scope required for the task.
- Tell children not to delegate or spawn another agent.
- Do not ask a child to access credentials, publish, deploy, commit, or perform destructive work without explicit authorization and a bounded plan.

## Minimum-necessary context

- A self-contained child message does not mean copying the root transcript. Give
  only the objective, scope, relevant facts, constraints, and acceptance criteria
  needed for the bounded task.
- Keep a sensitive task at the root when redaction or minimization would break
  correctness.
- Reference sensitive material rather than reproducing it where the child can
  complete the task safely without the contents.

## Host and provider boundary

Mars Cost Router collects no telemetry. Codex, its host environment, and model
providers may process or retain task content under their own terms, settings,
and policies; Mars does not control those systems.

## Evidence hygiene

Local evaluation artifacts can contain thread identifiers, runtime metadata, or prompt content. Review and redact material before sharing it. Screenshots and video should use non-sensitive tasks, generic labels, and sanitized payloads.

## What to verify

The root should inspect child results against acceptance criteria and run final validation. If a route’s effective settings matter, inspect native metadata where available; never infer effective settings solely from the requested payload.
