# Evidence and claim boundaries

## Fixed v1.2: descriptive record

> [!CAUTION]
> **Descriptive only — root difference is confounded; 12/12 is not quality equivalence.** The observations below are order- and cache-confounded in a fixed synthetic, read-only series. They are not causal, general-quality, cost, billing, or savings proof.

The fixed-v1.2 record contains three precommitted pairs of four synthetic, read-only tasks using Codex CLI 0.144.5. The comparison is a selective Terra/Sol policy against an all-Sol/high baseline.

| Recorded observation | Selective Terra/Sol policy | All-Sol/high baseline |
| --- | ---: | ---: |
| Deterministic checks | 12 / 12 | 12 / 12 |
| Observed automatic retries | 0 | 0 |
| Observed reroutes | 0 | 0 |
| Child tokens | 356,116 | 356,494 |
| Root tokens | 372,590 | 412,418 |
| Total tokens | 728,706 | 768,912 |
| Median wall duration | 45.094 s | 53.328 s |

Child-token totals were nearly flat: 356,116 versus 356,494, a recorded difference of -378 (-0.11%). Most of the recorded total-token difference occurred at the root: root totals were 372,590 versus 412,418. The total-token difference was -40,206 (-5.23%). Token and duration observations are order- and cache-confounded. They are descriptive of this fixed synthetic series only.

![Fixed v1.2 descriptive comparison](../assets/evidence/fixed-v1.2-performance.svg)

Do not turn this record into a claim of causal efficiency, general quality, equal quality, cost savings, billing savings, or ChatGPT-credit savings. Zero observed retries or reroutes is not proof that none occurred or that an effective route matched a request.

The [sanitized fixed-v1.2 machine-readable summary](../public-evidence/fixed-v1.2-summary.json) is the public source for these values. Raw local evidence is not published.

## Dated rate comparison

As of **2026-07-17**, the recorded Standard API rate source lists Terra at a 50 index versus Sol at a 100 index across the recorded categories.

![Terra and Sol rate index](../assets/evidence/rate-index.svg)

This is an index of listed Standard API rates, not an invoice or a prediction of a user’s bill. It excludes ChatGPT credits and must be rechecked against the current source before publication or use.

See the [sanitized rate-index machine-readable summary](../public-evidence/rate-index-2026-07-17.json). Raw local evidence is not published.

## Heldout-v2

Heldout-v2 is an unexecuted evaluation design with offline evaluator components implemented through Step 3. It is not frozen, authorized, or run and contributes no results here.

## Public source record

The two sanitized machine-readable summaries above are the published source records for this presentation. Provenance keeps two identities separate: the `frozen_suite` hash binds the frozen suite inputs, while the `source_series_summary` hash identifies the result source used for the descriptive summary. See the [sanitized fixed-v1.2 summary](../public-evidence/fixed-v1.2-summary.json). Keep any raw local evidence private and redacted; it is not published by this repository.
