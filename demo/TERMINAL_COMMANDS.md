# Terminal commands for the recording

Use these commands as shown. Do not add a live evaluation or show personal plugin/account output.

```sh
codex plugin marketplace add userbox020/mars-cost-router
codex plugin add mars-cost-router@mars-plugins
```

Then start a new Codex session. Open the plugin browser or `@` surface and select Mars Cost Router. In interfaces that expose Codex skills, `$mars-cost-router` is the skill syntax.

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

Do not claim the payload proves effective child settings.
