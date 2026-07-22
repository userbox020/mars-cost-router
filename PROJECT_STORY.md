# Mars Cost Router — Project Story

> **An independent, instruction-driven delegation policy for Codex.**
> Route by risk and effort; verify at the root.

## About the project

Mars Cost Router is an instruction-driven Codex plugin for **risk- and
effort-based bounded subagent delegation**. It presents three explicit request
lanes—economy, balanced, and premium—so the root can request different model and
reasoning settings for a bounded lookup than for a security review or difficult
debugging task. The root classifies each task, submits the native request, and
uses provider/runtime metadata as the authority for effective execution.

The project is deliberately small. It is a skill, a versioned JSON policy, and
plugin metadata. This static, instruction-only package makes each requested
decision visible and keeps quality control where it can be reviewed: in narrow
task definitions, deliberate escalation, native runtime fields, and final root
verification.

The core is an inspectable decision protocol: decide whether delegation is
worthwhile, let risk take precedence, assign non-overlapping bounded work in
dependency order, recover by cause, and verify acceptance at the root using
native Codex fields.

Mars is the project brand. This independent, unofficial project treats OpenAI,
Codex, and provider metadata as external authorities.

> **Judge summary:** Mars packages a transparent three-lane request policy in an
> instruction-only plugin, with integration and verification at the root. Release
> 0.3.2 has a verified marketplace path and cross-platform validation. Fixed-v1.2
> evidence records requested settings and descriptive fixed-suite outcomes;
> provider/runtime metadata remains the authority for effective execution.

## Inspiration

The project began with a simple orchestration problem: **using the premium lane
for every delegated task is easy, but the decision is invisible**.

A root agent may delegate file discovery, a focused implementation, and a
security-sensitive review during the same session. Their risk, uncertainty, and
reasoning needs vary, so an explicit decision makes the workflow easier to
explain and evaluate.

I wanted a policy that could answer four questions before every child request:

1. Is delegation worthwhile?
2. What is the smallest self-contained task?
3. Which lane matches its risk and effort?
4. What evidence must the root verify afterward?

That became the core principle: **route by risk and effort; verify at the
root**.

## What it does

Mars provides three requested settings:

| Lane | Intended work | Requested settings |
| --- | --- | --- |
| **Economy** | bounded inspection, lookup, low-risk checks | `gpt-5.6-terra`, `low`, `fork_turns: "none"` |
| **Balanced** | focused implementation, tests, documentation, review | `gpt-5.6-terra`, `medium`, `fork_turns: "none"` |
| **Premium** | security boundaries, difficult debugging, broad uncertainty | `gpt-5.6-sol`, `high`, `fork_turns: "none"` |

The root keeps tiny or tightly coupled work, then applies Premium risk
precedence, the all-condition Economy rule, or the Balanced delegated default.
The skill calls for bounded, self-contained child messages. It assigns exclusive
writer scopes, waits for reviewed prerequisites, and keeps nested delegation
prohibited. Weak, conflicting, malformed, unavailable, unauthorized, or newly
risky work returns to the root for cause-specific review, with substitutions
requiring an explicit reviewed decision.

The skill also offers optional requested formats for read-only locators, focused
edit handoffs, and review findings. Four concise
[playbooks](docs/PLAYBOOKS.md) show how to adapt the protocol for a lookup,
implementation, security review, or dependent task as advisory request guidance.

Mars manages review risk by making scope, escalation criteria, and root
verification explicit. Each lane's returned work receives its own acceptance
review.

## How I built it

The public repository is organized as an installable Codex marketplace:

- `.agents/plugins/marketplace.json` publishes the marketplace entry.
- `.codex-plugin/plugin.json` defines the plugin metadata and interface copy.
- `SKILL.md` contains the root-agent delegation policy.
- `policy/default.json` keeps lane settings versioned and machine-readable.
- `scripts/validate_plugin.py` closes the public package shape and checks
  metadata, runtime boundaries, local-path and secret hygiene, evidence
  arithmetic, and public claim scope.
- `tests/test_plugin.py` exercises valid packaging and fail-closed mutations.
- GitHub Actions runs the validator, unit tests, Node.js 24 video-source
  verifier, and Python compile step on Windows and Linux with Python 3.10 and
  3.13.

The installed package contains three files: plugin metadata, one versioned
policy, and one skill. Its static surface keeps the policy directly inspectable;
runtime hooks, MCP configuration, telemetry, receipts, and mutable project state
remain outside the package.

I also built the deterministic source project for a 2:20 explainer under
`video/`. It renders 4,200 frame-addressed 1080p frames over 140 seconds. It
generates local narration and an original procedural audio bed, verifies caption
and scene bounds, and uses GPU-assisted capture and encoding when available. The
source uses repository assets and sanitized examples, keeping account
screens, private prompts, and downloaded media outside the render path.
[Watch the 0.3.1 walkthrough](https://github.com/userbox020/mars-cost-router/releases/download/0.3.1/mars-cost-router-explainer-0.3.1.mp4).

## Judge installation and testing path

### 1. Clone and install the plugin

Python 3.10+ is required for the core validator, unit tests, and compile check.
Node.js 24+ is required only for video-source verification and is optional for
core package validation.

```sh
git clone https://github.com/userbox020/mars-cost-router.git
cd mars-cost-router
codex plugin marketplace add userbox020/mars-cost-router
codex plugin add mars-cost-router@mars-plugins
codex plugin list
codex features list
```

From that cloned repository root, start a new interactive session with:

```sh
codex --enable multi_agent \
  -c 'features.multi_agent_v2.enabled=true' \
  -c 'features.multi_agent_v2.hide_spawn_agent_metadata=false'
```

Multi-agent V2 is under development and is required for the five-field spawn
surface. Fixed evidence and the tested release path use Codex CLI 0.144.5. This
current judge command's feature configuration and `codex features list` were
checked provider-free on installed Codex CLI 0.144.6. The provider-free check
reported `multi_agent` as stable and `true`, and `multi_agent_v2` as under
development and `true`. That check did not launch a child, runtime spawn, model
request, or provider call. Open the plugin browser or `@` surface, select **Mars
Cost Router**, and use `$mars-cost-router:mars-cost-router` where the interface
exposes skills. Keep inspection and validation commands in this clone.

### 2. Inspect the policy

Open:

- [`plugins/mars-cost-router/skills/mars-cost-router/SKILL.md`](plugins/mars-cost-router/skills/mars-cost-router/SKILL.md)
- [`plugins/mars-cost-router/policy/default.json`](plugins/mars-cost-router/policy/default.json)

The complete packaged policy, request templates, and all three requested lane
settings are visible there. For a native spawn, inspect `task_name`, `message`,
`model`, `reasoning_effort`, and `fork_turns`; provider/runtime metadata remains
the authority for effective execution.

### 3. Run the public checks

```sh
python scripts/validate_plugin.py
python -m unittest discover -s tests -v
node video/verify.mjs
python -m compileall -q scripts tests
```

The Node command is the video-source check and may be skipped for core package
validation. The hosted GitHub Actions matrix runs all four checks on Windows and
Linux runners with Python 3.10 and 3.13 plus Node.js 24.

### 4. Review the evidence scope

Read [`docs/EVIDENCE.md`](docs/EVIDENCE.md), the
[`fixed-v1.2` summary](public-evidence/fixed-v1.2-summary.json), and the
[`2026-07-17` rate index](public-evidence/rate-index-2026-07-17.json). They show
the recorded values, provenance hashes, arithmetic, and interpretation scope in
a sanitized public record.

## What the fixed suite recorded

The public fixed-v1.2 record compares a selective Terra/Sol policy with an
all-Sol/high baseline across three precommitted pairs of four fixed read-only
tasks. Both treatments passed **12/12 deterministic checks** and had
zero observed automatic retries and reroutes.

Record classification: **`descriptive-synthetic`**.

For a recorded metric \(x\), the descriptive percentage difference is:

$$
\Delta_x =
\frac{x_{\text{selective}} - x_{\text{baseline}}}
     {x_{\text{baseline}}}
\times 100\%.
$$

| Metric | Selective policy | Baseline | Recorded difference |
| --- | ---: | ---: | ---: |
| Child tokens | 356,116 | 356,494 | -378 / -0.11% |
| Total tokens | 728,706 | 768,912 | -40,206 / -5.23% |
| Median duration | 45.094 s | 53.328 s | descriptive only |

Most of the recorded total-token difference occurred at the root rather than in
child tokens.

> **Evidence scope:** These are descriptive observations from one fixed
> read-only series with order and cache confounding. They support the recorded
> checks, tokens, timings, retries, and reroutes for that series. Actual billing,
> realized savings, causal speed or cost effects, general quality, and effective
> model identity require separate authoritative evidence.

## Challenges I faced

### Keeping an instruction honest

The biggest architectural challenge was keeping policy guidance distinct from
runtime authority. Mars guides a root to request explicit settings; native child
metadata records effective runtime detail when available. The documentation,
validator, and video preserve that distinction.

### Measuring orchestration instead of only children

The fixed record showed why root behavior matters. Child-token totals were
nearly flat while most of the recorded total difference occurred at the root.
That changed the story from “pick the lower-listed-rate child lane” to “make the
entire delegation decision reviewable.”

### Publishing sanitized evidence

I created sanitized summaries with separate hashes for the frozen suite inputs
and the summarized result source, then added scans and tests that keep raw
prompts, local paths, identifiers, and evaluator material private.

### Building a reproducible demo

A normal screen recording could reveal notifications, account data, or local
paths. The explainer is designed to be generated entirely from repository
assets and sanitized examples. During pre-publication verification, the renderer
detected stale frames, floating-point frame-identity errors, and clipped
captions.

### Making the package easy to judge

The plugin needed to be install-first rather than explanation-first. I tested a
clean remote marketplace installation, added a cross-platform CI matrix, kept
the package surface static, and documented a short path from install to
policy inspection to evidence review.

## What I learned

- **Routing is an orchestration decision broader than a model field.** Scope,
  escalation, integration, and verification can dominate the outcome.
- **Requested settings and effective settings are different facts.** Useful
  evidence labels each source and its authority.
- **Quality claims need evidence.** The plugin requires bounded tasks and root
  review; the fixed read-only suite reports deterministic checks for each arm.
- **Executable evidence scope is easier to maintain.** The public validator
  checks arithmetic, provenance, package boundaries, and claim language.
- **A smaller trust surface is a feature.** An instruction-only plugin is easy
  to inspect, remove, and reason about.

## What is next

The next step is broader, independently reviewable evaluation across more task
families, environments, and orderings. Future work can also compare requested
lanes with native child metadata where the interface exposes it, while keeping
API rates, token counts, ChatGPT credits, and actual billing evidence separate.

The long-term goal is to make every delegation choice easier to inspect,
challenge, and improve.

---

- **Repository:** <https://github.com/userbox020/mars-cost-router>
- **License:** MIT
- **Tested with:** Codex CLI 0.144.5
