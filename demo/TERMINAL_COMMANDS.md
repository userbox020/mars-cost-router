# Terminal commands for the recording

Use these commands as shown in an offline, sanitized recording. Keep live
evaluation and personal plugin/account output outside the capture.

```sh
codex plugin marketplace add userbox020/mars-cost-router
codex plugin add mars-cost-router@mars-plugins
```

The published walkthrough remains a version-labeled 0.3.1 presentation. For the
current judge path, stay in the cloned repository root and use the corrected
launch documented in the README:

```sh
codex features list
codex --enable multi_agent \
  -c 'features.multi_agent_v2.enabled=true' \
  -c 'features.multi_agent_v2.hide_spawn_agent_metadata=false'
```

Multi-agent V2 is under development and is required for the current five-field
spawn surface. The fixed evidence and tested release path use Codex CLI 0.144.5.
The command's feature configuration and `features list` were checked
provider-free on installed Codex CLI 0.144.6. The provider-free check reported
`multi_agent` as stable and `true`, and `multi_agent_v2` as under development and
`true`; no child, runtime spawn, model request, or provider call was made. Open
the plugin browser or `@` surface and select Mars Cost Router. In interfaces that
expose Codex skills, `$mars-cost-router:mars-cost-router` is the fully qualified
skill syntax.

For the static policy shot, display a redacted local copy or the published policy view. The presentation payload is:

```json
{
  "task_name": "focused_check",
  "message": "Inspect one bounded area. Return findings only. Do not delegate or spawn another agent.",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "medium",
  "fork_turns": "none"
}
```

Present the payload as requested settings and native provider/runtime metadata as
the authority for effective child settings.
