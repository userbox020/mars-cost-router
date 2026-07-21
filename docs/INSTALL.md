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

## Troubleshooting

| Issue | What to do |
| --- | --- |
| Plugin is not listed | Confirm the marketplace was added, run `codex plugin list`, refresh the marketplace and plugin with the commands above, then start a new Codex session. |
| Installed version is stale | Remove the plugin, run `codex plugin marketplace upgrade mars-plugins`, add the plugin again, and confirm the version with `codex plugin list`. |
| New version is not visible | Start a new Codex session after installation or refresh so discovery reloads the plugin. |
| Requested model is unavailable | Stop and report availability. Do not silently substitute another model or treat unavailability as escalation. |
| Plugin browser, `@`, or skill surface is missing | Use the plugin-management surface supported by the current Codex interface. Surface availability varies; `$mars-cost-router` applies only where skills are exposed. |
| Request fields or scope are malformed | Correct the call before spawning or retry the corrected call in the same appropriate lane. |
| Permission is denied or authorization is absent | Return to root or user clarification; selecting another lane does not supply authority. |

## First use

Use the installed `mars-cost-router` skill for the authoritative decision,
escalation, ownership, and acceptance guidance. Use [Playbooks](PLAYBOOKS.md) for
adaptable end-to-end templates. Correct malformed requests before spawning;
permission or authorization problems return to root or user clarification.
