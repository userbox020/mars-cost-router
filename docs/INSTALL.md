# Install Mars Cost Router

## Prerequisites

- Codex CLI **0.144.5**, the version tested by this project.
- Python **3.10+** for the validator, unit tests, and compile check.
- Node.js **24+** for video-source verification. Node is optional for core
  package validation.
- An account and environment where the requested models are available. Confirm
  availability separately for the account, CLI, and interface.

## Install from the marketplace repository

```sh
codex plugin marketplace add userbox020/mars-cost-router
codex plugin add mars-cost-router@mars-plugins
```

## Launch the current judge session

From the cloned repository root, inspect the available feature states and launch
a new interactive session with the table-shaped V2 configuration:

```sh
codex features list
codex --enable multi_agent \
  -c 'features.multi_agent_v2.enabled=true' \
  -c 'features.multi_agent_v2.hide_spawn_agent_metadata=false'
```

Multi-agent V2 is under development and is required for the five-field spawn
surface. Fixed evidence and the tested release path use Codex CLI 0.144.5. The
current judge command's feature configuration and `features list` were checked
provider-free on installed Codex CLI 0.144.6. The provider-free check reported
`multi_agent` as stable and `true`, and `multi_agent_v2` as under development and
`true`. That check did not launch a child, runtime spawn, model request, or
provider call.

## Open the plugin

Use the plugin browser or the `@` surface in your Codex interface and select
**Mars Cost Router**. Where Codex exposes skills,
`$mars-cost-router:mars-cost-router` activates the skill in a prompt. The exact
discovery surface varies by Codex version and interface; installation always
uses the marketplace commands above, and the current judge launch uses the
table-shaped command in the preceding section.

## Refresh

Use the documented marketplace refresh sequence, then start a new session.
Refresh keeps the marketplace registered:

```sh
codex plugin remove mars-cost-router@mars-plugins
codex plugin marketplace upgrade mars-plugins
codex plugin add mars-cost-router@mars-plugins
```

Confirm the installed version in the plugin list before relying on a policy change.

## Uninstall

```sh
codex plugin remove mars-cost-router@mars-plugins
codex plugin marketplace remove mars-plugins
```

Complete uninstall removes both the plugin and marketplace entry. Start a new
session after removal so the discovery surface reloads.

## Troubleshooting

| Issue | What to do |
| --- | --- |
| Plugin is not listed | Confirm the marketplace was added, run `codex plugin list`, refresh the marketplace and plugin with the commands above, then start a new Codex session. |
| Installed version is stale | Remove the plugin, run `codex plugin marketplace upgrade mars-plugins`, add the plugin again, and confirm the version with `codex plugin list`. |
| New version is not visible | Start a new Codex session after installation or refresh so discovery reloads the plugin. |
| Requested model is unavailable | Stop and report availability. Do not silently substitute another model or treat unavailability as escalation. |
| Plugin browser, `@`, or skill surface is missing | Use the plugin-management surface supported by the current Codex interface. Surface availability varies; `$mars-cost-router:mars-cost-router` applies only where skills are exposed. |
| Request fields or scope are malformed | Correct the call before spawning or retry the corrected call in the same appropriate lane. |
| Permission is denied or authorization is absent | Return to root or user clarification; selecting another lane does not supply authority. |

## First use

Use the installed `mars-cost-router` skill for the authoritative decision,
escalation, ownership, and acceptance guidance. Use [Playbooks](PLAYBOOKS.md) for
adaptable end-to-end templates. Correct malformed requests before spawning;
permission or authorization problems return to root or user clarification.

## Trust boundary

Installation adds a static skill, policy, and metadata package. The skill records
requested spawn settings; native provider/runtime metadata remains the authority
for effective execution.
