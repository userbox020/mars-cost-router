# Architecture

![Delegation flow](../assets/diagrams/delegation-flow.svg)

Mars Cost Router is a non-executable plugin presentation: a skill, a versioned policy, and package metadata. Its policy gives the root agent three explicit request shapes:

| Lane | Requested model | Requested reasoning effort | Turn context |
| --- | --- | --- | --- |
| Economy | `gpt-5.6-terra` | `low` | `fork_turns: "none"` |
| Balanced | `gpt-5.6-terra` | `medium` | `fork_turns: "none"` |
| Premium | `gpt-5.6-sol` | `high` | `fork_turns: "none"` |

## Boundaries

- The root decides whether delegation is worthwhile.
- The root writes the native child request; the plugin does not rewrite it.
- Every child request should explicitly include model, reasoning effort, and `fork_turns`.
- The root remains responsible for integration, conflict resolution, and final verification.
- Native metadata may be inspected when effective settings matter. A requested setting is not proof of an effective setting.

Optional return formats are advisory SKILL guidance, not a runtime schema or enforcement mechanism.

## Why no hook

Mars Cost Router deliberately has no packaged runtime hook. That keeps the installed surface small and avoids representing an instruction as an enforcement mechanism. There is no executable plugin runtime, project-wide mutable state, receipt store, or telemetry collector.

## Privacy boundary

`task_name` is a generic label, not a routing command. Keep prompts, paths, filenames, user data, rationale, credentials, secrets, and sensitive content out of it. Put only the bounded task context needed to complete work in the child message.

For installation and use, see [Install](INSTALL.md). For evidence boundaries, see [Evidence](EVIDENCE.md).
