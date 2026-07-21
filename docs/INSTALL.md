# Install Mars Cost Router

## Prerequisites

- Codex CLI **0.144.5**, the version tested by this project.
- An account and environment where the requested models are available. Availability can vary; installation does not probe it.

## Install from the marketplace repository

```sh
codex plugin marketplace add userbox020/mars-cost-router
codex plugin add mars-cost-router@mars-plugins
```

Start a new Codex session after installation so the plugin can be discovered.

## Open the plugin

Use the plugin browser or the `@` surface in your Codex interface and select **Mars Cost Router**. Where Codex exposes skills, `$mars-cost-router` is the skill syntax. The exact surface can vary by Codex version and interface; it is not an alternate installation command.

## Refresh

Use the documented marketplace refresh sequence, then start a new session:

```sh
codex plugin remove mars-cost-router@mars-plugins
codex plugin marketplace upgrade mars-plugins
codex plugin add mars-cost-router@mars-plugins
```

Confirm the installed version in the plugin list before relying on a policy change.

## First use

1. Keep tiny or tightly coupled work at the root.
2. For a bounded task, open Mars Cost Router and choose a lane by risk and effort.
3. Give the child a self-contained message, bounded acceptance criteria, and a prohibition on nested delegation.
4. Review the result and run final checks at the root.

Mars Cost Router guides requested settings. It does not enforce them or prove an effective route.
