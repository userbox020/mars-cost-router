# Mars Cost Router — Project Story

> **An independent, instruction-driven delegation policy for Codex.**
> Route by risk and effort; verify at the root.

## About the project

Mars Cost Router is an instruction-driven Codex plugin for **risk- and
effort-based bounded subagent delegation**. It presents three explicit request
lanes—economy, balanced, and premium—so the root can request different model and
reasoning settings for a bounded lookup than for a security review or difficult
debugging task.

The project is deliberately small. It is a skill, a versioned JSON policy, and
plugin metadata—not a hidden proxy or runtime control plane. Mars does not
rewrite calls or claim that a requested route became the effective route.
Instead, it makes the decision visible and keeps quality control where it can be
reviewed: in narrow task definitions, deliberate escalation, and final root
verification.

The innovation is not hidden model selection. It is an inspectable decision
protocol: decide whether delegation is worthwhile, let risk take precedence,
assign non-overlapping bounded work in dependency order, recover by cause, and
verify acceptance at the root using native Codex fields.

Mars is the project name, not a model. This is an independent, unofficial
project and is not affiliated with or endorsed by OpenAI.

> **Judge summary:** Mars packages a transparent three-lane request policy, not
> an automated router. The installed plugin is instruction-only and keeps
> integration and verification at the root. The published 0.3.1 release passed
> remote installation and hosted cross-platform validation. Its fixed read-only
> evidence is descriptive only and supports neither quality-equivalence nor
> savings claims.

## Inspiration

The project began with a simple orchestration problem: **using the premium lane
for every delegated task is easy, but the decision is invisible**.

A root agent may delegate file discovery, a focused implementation, and a
security-sensitive review during the same session. Those tasks do not have the
same risk, uncertainty, or reasoning needs. Treating them identically can make
an agent workflow harder to explain and evaluate.

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
The skill calls for bounded, self-contained child messages. It directs the root
to avoid overlapping parallel writer scopes, wait for reviewed prerequisites,
and prohibit nested delegation. Weak, conflicting, malformed, unavailable,
unauthorized, or newly risky work returns to the root for cause-specific review
rather than silent substitution.

The skill also offers optional requested formats for read-only locators, focused
edit handoffs, and review findings. Four concise
[playbooks](docs/PLAYBOOKS.md) show how to adapt the protocol for a lookup,
implementation, security review, or dependent task without claiming runtime
enforcement.

This is how Mars manages review risk: it does not claim the lanes are
equivalent; it makes scope, escalation criteria, and root verification explicit.

## How I built it

The public repository is organized as an installable Codex marketplace:

- `.agents/plugins/marketplace.json` publishes the marketplace entry.
- `.codex-plugin/plugin.json` defines the plugin metadata and interface copy.
- `SKILL.md` contains the root-agent delegation policy.
- `policy/default.json` keeps lane settings versioned and machine-readable.
- `scripts/validate_plugin.py` closes the public package shape and rejects
  unexpected metadata, runtime features, local paths, secrets, arithmetic
  mutations, and unsupported headline claims.
- `tests/test_plugin.py` exercises both valid packaging and negative cases.
- GitHub Actions runs the validator and tests on Windows and Linux with Python
  3.10 and 3.13.

The installed plugin has no hook, executable runtime, MCP configuration,
telemetry collector, receipt store, or mutable project-wide state. That reduces
the trust surface and keeps the policy inspectable.

I also built the deterministic source project for a 2:20 explainer under
`video/`. It renders 4,200 frame-addressed 1080p frames over 140 seconds. It
generates local narration and an original procedural audio bed, verifies caption
and scene bounds, and uses GPU-assisted capture and encoding when available. No
account screen, private prompt, or downloaded media is required.
[Watch the 0.3.1 walkthrough](https://github.com/userbox020/mars-cost-router/releases/download/0.3.1/mars-cost-router-explainer-0.3.1.mp4).

## Judge installation and testing path

### 1. Install the plugin

```sh
codex plugin marketplace add userbox020/mars-cost-router
codex plugin add mars-cost-router@mars-plugins
```

Start a new Codex session, open the plugin browser or `@` surface, and select
**Mars Cost Router**. Where the interface exposes skills, use
`$mars-cost-router`.

### 2. Inspect the policy

Open:

- [`plugins/mars-cost-router/skills/mars-cost-router/SKILL.md`](plugins/mars-cost-router/skills/mars-cost-router/SKILL.md)
- [`plugins/mars-cost-router/policy/default.json`](plugins/mars-cost-router/policy/default.json)

The complete packaged policy, request templates, and all three requested lane
settings are visible there.

### 3. Run the public checks

```sh
python scripts/validate_plugin.py
python -m unittest discover -s tests -v
```

The hosted GitHub Actions matrix runs the same checks on Windows and Linux
runners with Python 3.10 and 3.13.

### 4. Review the evidence boundaries

Read [`docs/EVIDENCE.md`](docs/EVIDENCE.md), the
[`fixed-v1.2` summary](public-evidence/fixed-v1.2-summary.json), and the
[`2026-07-17` rate index](public-evidence/rate-index-2026-07-17.json). They show
the recorded values, provenance hashes, arithmetic, and limitations without
publishing private prompts or raw local evidence.

## What the fixed suite recorded

The public fixed-v1.2 record compares a selective Terra/Sol policy with an
all-Sol/high baseline across three precommitted pairs of four fixed read-only
tasks. Both treatments passed **12/12 deterministic checks** and had
zero observed automatic retries and reroutes.

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

Most of the recorded total-token difference occurred at the root, not in child
tokens. Because order and cache effects were not isolated, the duration is a
recorded timing observation—not evidence that the policy is faster or causes
lower latency.

These are descriptive observations from this fixed read-only series. The runs
are order- and cache-confounded. They do not establish causal token or latency
improvement, general quality, quality equivalence, API-dollar or ChatGPT-credit
savings, billing outcomes, or proof that requested and effective routes matched.

## Challenges I faced

### Keeping an instruction honest

The biggest architectural challenge was resisting the temptation to describe a
policy as enforcement. Mars can guide a root to request explicit settings, but
it cannot prove the effective child route. The documentation, validator, and
video all preserve that distinction.

### Measuring orchestration instead of only children

The fixed record showed why root behavior matters. Child-token totals were
nearly flat while most of the recorded total difference occurred at the root.
That changed the story from “pick the lower-listed-rate child lane” to “make the
entire delegation decision reviewable.”

### Publishing evidence without leaking evidence

Raw prompts, local paths, identifiers, and evaluator material do not belong in
a public submission. I created sanitized summaries with separate hashes for the
frozen suite inputs and the summarized result source, then added scans and tests
to keep private material out of the repository.

### Building a reproducible demo

A normal screen recording could reveal notifications, account data, or local
paths. The explainer is designed to be generated entirely from repository
assets and sanitized examples. During pre-publication verification, the renderer
detected stale frames, floating-point frame-identity errors, and clipped
captions.

### Making the package easy to judge

The plugin needed to be install-first rather than explanation-first. I tested a
clean remote marketplace installation, added a cross-platform CI matrix, kept
the runtime surface non-executable, and documented a short path from install to
policy inspection to evidence review.

## What I learned

- **Routing is an orchestration decision, not just a model field.** Scope,
  escalation, integration, and verification can dominate the outcome.
- **Requested settings and effective settings are different facts.** A useful
  tool should say which one it knows.
- **Quality claims need evidence, not a slogan.** The plugin requires bounded
  tasks and root review; the project evaluates its fixed read-only suite with
  deterministic checks rather than claiming that the lanes are equivalent.
- **Evidence is strongest when its limits are executable.** The public validator
  checks arithmetic, provenance, package boundaries, and claim language instead
  of leaving caveats only in prose.
- **A smaller trust surface is a feature.** An instruction-only plugin is easy
  to inspect, remove, and reason about.

## What is next

The next step is broader, independently reviewable evaluation across more task
families, environments, and orderings. Future work can also compare requested
lanes with native child metadata where the interface exposes it, while keeping
API rates, token counts, ChatGPT credits, and actual billing evidence separate.

The long-term goal is not to hide routing behind automation. It is to make every
delegation choice easier to inspect, challenge, and improve.

---

- **Repository:** <https://github.com/userbox020/mars-cost-router>
- **License:** MIT
- **Tested with:** Codex CLI 0.144.5
