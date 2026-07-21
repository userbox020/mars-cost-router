#!/usr/bin/env python3
"""Print a safe static illustration of the packaged routing policy."""

from __future__ import annotations

import json
from pathlib import Path

from validate_plugin import validate_repository


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "plugins/mars-cost-router/policy/default.json"


def main() -> int:
    result = validate_repository(ROOT)
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    print(f"Mars Cost Router {result['version']} - static policy illustration")
    print("lane      model           reasoning  fork_turns")
    print("--------- --------------- ---------- ----------")
    for lane in ("economy", "balanced", "premium"):
        settings = policy["lanes"][lane]
        print(
            f"{lane:<9} {settings['model']:<15} "
            f"{settings['reasoning_effort']:<10} {settings['fork_turns']}"
        )

    lane = "balanced"
    settings = policy["lanes"][lane]
    sample = {
        "task_name": "focused_check",
        "message": (
            "Inspect one bounded public artifact and return findings. "
            "Do not delegate or spawn another agent."
        ),
        **settings,
    }
    print(f"\nSample requested {lane} spawn payload:")
    print(json.dumps(sample, indent=2))
    print(
        "\nThis demo reads static files only. It does not spawn an agent, enforce "
        "routing, observe an effective model, collect telemetry, or estimate savings."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
