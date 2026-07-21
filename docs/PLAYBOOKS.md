# Delegation playbooks

These are adaptable guidance for requested calls. They do not enforce a route or
prove completion, effective settings, or runtime behavior.

Every JSON block below is a request template, not a ready-to-run call. Replace
every `<PLACEHOLDER>` value with bounded, repository-specific content before
spawning, then review the complete request at the root.

## 1. Bounded read-only locator — Economy

**Root/no-delegation decision:** Keep a trivial lookup at the root. Delegate only
when a bounded search is independently checkable and worth specifying.

**Why this lane fits:** The work is deterministic, read-only, low consequence,
and has a clear location-based acceptance criterion.

**Request template:**

```json
{
  "task_name": "symbol_lookup",
  "message": "Complete one bounded read-only lookup for <SYMBOL> within <REPOSITORY_RELATIVE_SCOPE>. Acceptance criteria: <ACCEPTANCE_CRITERIA>. Return only repository-relative locations and short findings. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "low",
  "fork_turns": "none"
}
```

**Optional return format:** `relative/path:line — symbol — short finding`

**Root verification and acceptance:** Inspect every cited location and accept the
result only when the symbol and finding match the repository.

## 2. Focused implementation with tests — Balanced

**Root/no-delegation decision:** Keep a tiny or tightly coupled edit at the root.
Delegate when one writer can own a bounded implementation and its focused tests.

**Why this lane fits:** The task is normal implementation with clear scope and
acceptance criteria, without a Premium risk trigger or all Economy conditions.

**Request template:**

```json
{
  "task_name": "focused_implementation",
  "message": "Complete this bounded objective: <OBJECTIVE>. Work only within <REPOSITORY_RELATIVE_SCOPE>. Acceptance criteria: <ACCEPTANCE_CRITERIA>. Run relevant tests and report observed results and skipped checks. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "medium",
  "fork_turns": "none"
}
```

**Optional return format/status:** Provide an edit handoff with changed
repository-relative paths, checks actually run and observed results, skipped
checks, and remaining risks. State whether the task is complete. If partial or
blocked, identify remaining work, verification gaps, and any root decision needed.

**Root verification and acceptance:** Inspect the diff and assigned paths,
rerun relevant tests at the root, and treat `partial` or `blocked` as unresolved.

## 3. Authentication/security review — Premium

**Root/no-delegation decision:** Keep the review at the root if sensitive context
cannot be minimized safely. Otherwise delegate one bounded, sanitized review.

**Why this lane fits:** Authentication is a security boundary, so risk selects
Premium despite the `review` activity label.

**Request template:**

```json
{
  "task_name": "authentication_review",
  "message": "Review the bounded authentication scope <REPOSITORY_RELATIVE_SCOPE>. Answer <REVIEW_QUESTIONS>. Acceptance criteria: <ACCEPTANCE_CRITERIA>. Identify concrete security findings with repository-relative locations, impact, and action. Do not access credentials. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-sol",
  "reasoning_effort": "high",
  "fork_turns": "none"
}
```

**Optional return format:** Findings first in critical, high, medium, then low
order, each with a repository-relative location and concrete impact or action.
If none, say `No findings` and identify verification gaps.

**Root verification and acceptance:** Inspect cited code and tests, reconcile
conflicts, and rerun relevant security checks before accepting the review.

## 4. Mixed/dependent task — root decomposition

**Root/no-delegation decision:** The root first clarifies the mixed task and keeps
cross-cutting integration and final decisions. It may delegate isolated units.

**Why this lane fits:** Independent read-only searches may run in parallel, while
the dependent edit and test are serialized. This bounded implementation request
uses Balanced after prerequisite evidence is reviewed.

**Request template:**

```json
{
  "task_name": "dependent_edit",
  "message": "Using the reviewed prerequisite findings <REVIEWED_PREREQUISITE_FINDINGS>, complete this bounded objective: <OBJECTIVE>. Work only within <REPOSITORY_RELATIVE_SCOPE>. Acceptance criteria: <ACCEPTANCE_CRITERIA>. Report the next root decision needed before dependent tests proceed. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "medium",
  "fork_turns": "none"
}
```

**Optional return format/status:** Provide an edit handoff with changed path,
verification actually run, skipped checks, and risks. State whether the task is
complete. If partial or blocked, identify remaining work, verification gaps, and
the root decision needed before the dependent test.

**Root verification and acceptance:** Review independent search evidence before
starting the dependent edit, inspect its diff before running dependent tests,
then integrate and run final relevant checks at the root.
