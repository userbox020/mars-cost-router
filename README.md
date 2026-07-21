# Mars Cost Router

![Mars Cost Router — three deliberate routes meeting at a verified root](assets/brand/mars-cost-router-hero.svg)

> **An independent, instruction-driven delegation policy for Codex.**
> Route by risk and effort; verify at the root.

> **Unofficial:** Mars Cost Router is not affiliated with or endorsed by OpenAI. “Mars” is this project's brand, not a model.

[![Validate](https://github.com/userbox020/mars-cost-router/actions/workflows/validate.yml/badge.svg)](https://github.com/userbox020/mars-cost-router/actions/workflows/validate.yml) ![Version 0.3.0](https://img.shields.io/badge/version-0.3.0-AD4C32?style=flat-square) ![Tested with Codex CLI 0.144.5](https://img.shields.io/badge/tested-Codex%20CLI%200.144.5-27374D?style=flat-square) ![No runtime hooks](https://img.shields.io/badge/runtime-no%20hooks-536B55?style=flat-square) ![MIT](https://img.shields.io/badge/license-MIT-E3B341?style=flat-square)

Mars Cost Router is a small local plugin with a three-lane policy for bounded subagent delegation. It guides the root agent to write explicit child settings. It does not rewrite calls, enforce a route, collect telemetry, or replace root review.

Project: [userbox020/mars-cost-router](https://github.com/userbox020/mars-cost-router)

**Build Week judges:** [Read the Project Story and verification path](PROJECT_STORY.md).

## Quickstart

```sh
codex plugin marketplace add userbox020/mars-cost-router
codex plugin add mars-cost-router@mars-plugins
```

Start a **new Codex session**, open the plugin browser or `@` surface, and select Mars Cost Router. In surfaces that expose Codex skills, `$mars-cost-router` is the skill syntax. Surface availability can vary by Codex version and interface.

See the fuller [installation guide](docs/INSTALL.md).

## A policy, not a control plane

| Mars Cost Router does | Mars Cost Router does not |
| --- | --- |
| Provides explicit economy, balanced, and premium lane settings | Run executable hooks or rewrite `spawn_agent` calls |
| Keeps the root responsible for scope, integration, and verification | Enforce model selection or prove effective routing |
| Requires a bounded child message and no nested delegation | Report billing, ChatGPT credits, or runtime telemetry |

## Three deliberate lanes

| Lane | Good fit | Requested model and effort | Context |
| --- | --- | --- | --- |
| **Economy** | bounded inspection, lookup, low-risk checks | `gpt-5.6-terra` · `low` | `fork_turns: "none"` |
| **Balanced** | focused implementation, tests, documentation, review | `gpt-5.6-terra` · `medium` | `fork_turns: "none"` |
| **Premium** | security boundaries, difficult debugging, broad uncertainty | `gpt-5.6-sol` · `high` | `fork_turns: "none"` |

Terra is the lower-listed-rate lane under the dated Standard API rate source. The root should escalate only after reviewing weak, conflicting, or risky evidence.

## How it fits

![Delegation flow: policy informs root; root makes bounded child calls and verifies results](assets/diagrams/delegation-flow.svg)

The skill and versioned policy inform the root. The root writes the child request, receives the result, and owns final verification. Native child metadata, when available, is evidence to inspect—not a claim made by this package.

### Sanitized child request shape

```json
{
  "task_name": "focused_check",
  "message": "Inspect one bounded area. Return findings only. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "medium",
  "fork_turns": "none"
}
```

`task_name` is only a generic, privacy-safe label. Do not place prompts, paths, filenames, user data, rationale, credentials, or secrets in it.

## Watch the three-minute walkthrough

[Three-minute walkthrough script](demo/VIDEO_SCRIPT.md) · [Captions](demo/CAPTIONS.vtt) · [Recording checklist](demo/RECORDING_CHECKLIST.md) · [Terminal commands](demo/TERMINAL_COMMANDS.md)

Final video URL pending. The walkthrough uses static policy inspection and sanitized examples. It does not expose private prompts, thread IDs, or unredacted evidence.

## Fixed v1.2 descriptive evidence

> [!CAUTION]
> **Descriptive only — root difference is confounded; 12/12 is not quality equivalence.** This fixed synthetic, read-only series is order- and cache-confounded. It is not causal, general-quality, cost, billing, or savings proof.

![Fixed v1.2 descriptive comparison: grouped token composition and 12 of 12 checks in each treatment](assets/evidence/fixed-v1.2-performance.svg)

Three precommitted pairs of four synthetic, read-only tasks recorded against Codex CLI 0.144.5:

| Recorded observation | Selective Terra/Sol policy | All-Sol/high baseline |
| --- | ---: | ---: |
| Deterministic checks | 12 / 12 | 12 / 12 |
| Observed automatic retries | 0 | 0 |
| Observed reroutes | 0 | 0 |
| Child tokens | 356,116 | 356,494 |
| Root tokens | 372,590 | 412,418 |
| Total tokens | 728,706 | 768,912 |
| Median wall duration | 45.094 s | 53.328 s |

Child-token totals were nearly flat: **356,116** versus **356,494** (**-0.11% recorded**). Most of the recorded total-token difference occurred at the root; total tokens were **728,706** versus **768,912** (**-5.23% recorded**). These observations are order- and cache-confounded in a synthetic read-only suite. They are not causal evidence, a general-quality result, a cost result, a billing result, or a guarantee.

As of **2026-07-17**, the recorded Standard API rate source listed Terra at a 50 index versus Sol at 100 across the recorded categories. This is a rate comparison only; recheck the source before publishing or making a decision. It excludes ChatGPT credits.

![Dated API rate index: Terra 50 and Sol 100](assets/evidence/rate-index.svg)

Read the sanitized machine-readable summaries: [fixed-v1.2 summary](public-evidence/fixed-v1.2-summary.json) and [rate index](public-evidence/rate-index-2026-07-17.json). These summaries are the public record; raw local evidence is not published. Read definitions, provenance, and limits in [Evidence](docs/EVIDENCE.md). Heldout-v2 is an unexecuted evaluation design with offline evaluator components implemented through Step 3. It is not frozen, authorized, or run and contributes no results here.

## Limitations

- This is instruction-driven. A root can omit or misapply requested fields.
- A requested lane is not proof of the child’s effective model or reasoning effort.
- Availability depends on the account, CLI, and environment.
- Static validation does not establish runtime behavior, quality, cost, or routing outcomes.

## Security and privacy

The package has no runtime hooks, executable runtime, receipt store, or mutable project-wide state. Keep child messages scoped, do not put sensitive content in `task_name`, and redact local evidence before sharing it. See [Privacy and security](docs/PRIVACY.md).

## Development

Read [Architecture](docs/ARCHITECTURE.md), [Install](docs/INSTALL.md), and [Evidence](docs/EVIDENCE.md) before changing policy or public claims. This presentation intentionally distinguishes requested settings from observed runtime facts.

## License

MIT. See the repository license.
