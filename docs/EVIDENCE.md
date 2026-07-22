# Evidence and interpretation

## Fixed v1.2: descriptive record

Record classification: **`descriptive-synthetic`**.

The fixed-v1.2 record contains three precommitted pairs of four fixed read-only tasks using Codex CLI 0.144.5. The comparison is a selective Terra/Sol policy against an all-Sol/high baseline.

| Recorded observation | Selective Terra/Sol policy | All-Sol/high baseline |
| --- | ---: | ---: |
| Deterministic checks | 12 / 12 | 12 / 12 |
| Observed automatic retries | 0 | 0 |
| Observed reroutes | 0 | 0 |
| Child tokens | 356,116 | 356,494 |
| Root tokens | 372,590 | 412,418 |
| Total tokens | 728,706 | 768,912 |
| Median wall duration | 45.094 s | 53.328 s |

Child-token totals were nearly flat: 356,116 versus 356,494, a recorded difference of -378 (-0.11%). Most of the recorded total-token difference occurred at the root: root totals were 372,590 versus 412,418. The total-token difference was -40,206 (-5.23%). Token and duration observations are order- and cache-confounded. They describe this fixed read-only series.

<p align="center">
  <img src="../assets/evidence/fixed-v1.2-performance.svg" alt="Fixed v1.2 descriptive comparison with stacked child and root token bars plus separate 12 of 12 deterministic-check panels for both treatments." width="1000" />
</p>

> **What this demonstrates:** The record supports the listed deterministic
> checks and descriptive token, timing, retry, and reroute observations for the
> fixed series. Actual billing, realized savings, causal efficiency, general or
> comparative quality, and effective route identity require separate
> authoritative evidence. Provider/runtime metadata remains the authority for
> effective execution.

The [sanitized fixed-v1.2 machine-readable summary](../public-evidence/fixed-v1.2-summary.json) is the public source for these values. Raw local evidence remains private.

Fixed-v1.2 covers the policy version before the optional child return contracts
in 0.3.1 and the 0.3.2 root-first decision ladder. Cause-specific escalation,
ownership and dependency rules, root acceptance guidance, minimum-context
privacy guidance, and delegation playbooks are product guidance outside this
fixed-series evaluation.

## Dated rate comparison

As of **2026-07-17**, the recorded Standard API rate source lists Terra at a 50 index versus Sol at a 100 index across the recorded categories.

<p align="center">
  <img src="../assets/evidence/rate-index.svg" alt="Dated Standard API rate index: Terra 50 and Sol 100." width="1000" />
</p>

This index represents dated listed Standard API rates. Invoices, bill forecasts,
and ChatGPT credits use separate evidence sources. Recheck the current source
before publication or use.

See the [sanitized rate-index machine-readable summary](../public-evidence/rate-index-2026-07-17.json). Raw local evidence remains private.

## Heldout-v2

Heldout-v2 is an unexecuted evaluation design with offline evaluator components
implemented through Step 3. Its status is pre-freeze and pre-authorization, so
the results presented here come exclusively from fixed-v1.2.

## Public source record

The two sanitized machine-readable summaries above are the published source
records for this presentation. Provenance keeps two identities separate: the
`frozen_suite` hash binds the frozen suite inputs, while the
`source_series_summary` hash identifies the result source used for the
descriptive summary. See the [sanitized fixed-v1.2 summary](../public-evidence/fixed-v1.2-summary.json).
Raw local evidence stays private and redacted.
