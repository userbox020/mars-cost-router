# Architecture

![Delegation flow](../assets/diagrams/delegation-flow.svg)

Mars Cost Router is a static plugin package: a skill, a versioned policy, and
package metadata. Its policy gives the root agent three explicit request shapes:

| Lane | Requested model | Requested reasoning effort | Turn context |
| --- | --- | --- | --- |
| Economy | `gpt-5.6-terra` | `low` | `fork_turns: "none"` |
| Balanced | `gpt-5.6-terra` | `medium` | `fork_turns: "none"` |
| Premium | `gpt-5.6-sol` | `high` | `fork_turns: "none"` |

## Ownership and trust boundary

- The root decides whether delegation is worthwhile.
- The root writes and submits the native child request.
- Every child request should explicitly include model, reasoning effort, and `fork_turns`.
- Each child receives an independently checkable scope. Within a parallel batch, at most one child writer owns each file or area; overlapping work is re-scoped or serialized under root review.
- Only independent work runs in parallel; dependent work waits until prerequisite evidence is reviewed.
- The root unconditionally retains cross-cutting integration, conflict resolution, final architectural or product decisions, final verification, and final claims.
- Commits, publication, deployment, credential access, and destructive actions may be delegated only when the user explicitly authorizes that exact bounded action and existing safety guidance permits it.
- Native metadata is the authority when effective settings matter; the policy
  fields record requested settings.

Optional return formats are advisory SKILL guidance. Runtime responses retain
their native schema and authority.

## Static package surface

Mars Cost Router packages only metadata, a versioned policy, and a skill. Runtime
hooks, executable code, project-wide mutable state, receipts, and telemetry stay
outside the installed surface, keeping the instruction directly inspectable.

## Privacy boundary

`task_name` serves only as a generic label. Keep prompts, paths, filenames, user
data, rationale, credentials, secrets, and sensitive content out of it. Put only
the bounded task context needed to complete work in the child message.

For installation and use, see [Install](INSTALL.md). For evidence interpretation,
see [Evidence](EVIDENCE.md).
