from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_plugin import (
    ValidationError,
    _validate_v2_launch_guides,
    validate_repository,
)


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = Path(".agents/plugins/marketplace.json")
MANIFEST = Path("plugins/mars-cost-router/.codex-plugin/plugin.json")
POLICY = Path("plugins/mars-cost-router/policy/default.json")
SKILL = Path("plugins/mars-cost-router/skills/mars-cost-router/SKILL.md")
FIXTURE = Path("tests/fixtures/skill-contract-v1.json")
FIXED_SUMMARY = Path("public-evidence/fixed-v1.2-summary.json")
PLAYBOOKS = Path("docs/PLAYBOOKS.md")
V2_LAUNCH_GUIDES = (
    Path("README.md"),
    Path("PROJECT_STORY.md"),
    Path("docs/INSTALL.md"),
    Path("demo/TERMINAL_COMMANDS.md"),
)
CURRENT_VERSION = "0.3.2"
WALKTHROUGH_VERSION = "0.3.1"


class PluginValidationTests(unittest.TestCase):
    def copy_repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        destination = Path(temporary.name) / "repository"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(
                ".git",
                "__pycache__",
                "*.pyc",
                ".cdp-profile",
                "audio-work",
                "benchmark-gpu",
                "benchmark-software",
                "frames",
                "inputs",
                "out",
                "sparse-smoke",
            ),
        )
        return temporary, destination

    def assert_text_rejected(self, relative: Path, transform) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        path = root / relative
        content = path.read_text(encoding="utf-8")
        mutated = transform(content)
        self.assertNotEqual(content, mutated)
        path.write_text(mutated, encoding="utf-8")
        with self.assertRaises(ValidationError):
            validate_repository(root)

    def assert_json_rejected(self, relative: Path, mutation) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        path = root / relative
        value = json.loads(path.read_text(encoding="utf-8"))
        mutation(value)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        with self.assertRaises(ValidationError):
            validate_repository(root)

    def test_public_repository_validates(self) -> None:
        result = validate_repository(ROOT)
        self.assertEqual(
            {"name": "mars-cost-router", "version": CURRENT_VERSION},
            {"name": result["name"], "version": result["version"]},
        )

    def test_contract_fixture_is_versioned_and_grouped(self) -> None:
        fixture = json.loads((ROOT / FIXTURE).read_text(encoding="utf-8"))
        self.assertEqual(1, fixture["schema_version"])
        self.assertEqual(
            {
                str(SKILL).replace("\\", "/"),
                "docs/PLAYBOOKS.md",
                "docs/INSTALL.md",
                "docs/PRIVACY.md",
                "docs/ARCHITECTURE.md",
                "docs/EVIDENCE.md",
                "README.md",
                "PROJECT_STORY.md",
                "demo/TERMINAL_COMMANDS.md",
            },
            set(fixture["files"]),
        )
        for contract in fixture["files"].values():
            self.assertEqual({"ordered_sections", "required_anchors"}, set(contract))

    def test_rejects_fixture_schema_anchor_and_order_mutations(self) -> None:
        mutations = {
            "schema": lambda value: value.__setitem__("schema_version", 2),
            "anchor": lambda value: value["files"][str(SKILL).replace("\\", "/")][
                "required_anchors"
            ].append("missing contract anchor"),
            "order": lambda value: value["files"][str(SKILL).replace("\\", "/")][
                "ordered_sections"
            ].reverse(),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                self.assert_json_rejected(FIXTURE, mutation)

    def test_rejects_generic_anchor_removal_and_section_reordering(self) -> None:
        self.assert_text_rejected(
            SKILL,
            lambda text: text.replace(
                "Within a parallel batch, assign at most one child writer to each file or area.",
                "Assign writers as needed.",
                1,
            ),
        )
        first = "## Handle failure and escalation by cause"
        second = "## Decompose and assign ownership"
        self.assert_text_rejected(
            SKILL,
            lambda text: text.replace(first, "SECTION_SWAP", 1)
            .replace(second, first, 1)
            .replace("SECTION_SWAP", second, 1),
        )
        for relative in (
            Path("README.md"),
            Path("PROJECT_STORY.md"),
            Path("docs/EVIDENCE.md"),
        ):
            with self.subTest(classification=relative):
                self.assert_text_rejected(
                    relative,
                    lambda text: text.replace(
                        "Record classification: **`descriptive-synthetic`**.",
                        "Record classification: descriptive.",
                        1,
                    ),
                )

        sources = {
            relative.as_posix(): (ROOT / relative).read_text(encoding="utf-8")
            for relative in V2_LAUNCH_GUIDES
        }
        bad_combination = dict(sources)
        bad_combination["README.md"] = bad_combination["README.md"].replace(
            "codex --enable multi_agent \\",
            "codex --enable multi_agent " + "--enable multi_" + "agent_v2 \\",
            1,
        )
        with self.assertRaisesRegex(ValidationError, "combines parent multi_agent_v2"):
            _validate_v2_launch_guides(bad_combination)

        missing_table_enable = dict(sources)
        missing_table_enable["README.md"] = missing_table_enable["README.md"].replace(
            "features.multi_agent_v2.enabled=true",
            "features.multi_agent_v2.enabled=false",
            1,
        )
        with self.assertRaisesRegex(ValidationError, "table-shaped V2 launch command"):
            _validate_v2_launch_guides(missing_table_enable)

    def test_skill_lane_table_and_templates_follow_policy(self) -> None:
        policy = json.loads((ROOT / POLICY).read_text(encoding="utf-8"))
        skill = (ROOT / SKILL).read_text(encoding="utf-8")
        rows = re.findall(
            r"^\| (economy|balanced|premium) \| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|$",
            skill,
            re.MULTILINE,
        )
        self.assertEqual(
            policy["lanes"],
            {
                lane: {"model": model, "reasoning_effort": effort, "fork_turns": fork}
                for lane, model, effort, fork in rows
            },
        )
        templates = [
            json.loads(payload)
            for payload in re.findall(
                r"^### (?:Economy|Balanced|Premium) exact input\n\n```json\n(\{.*?\})\n```$",
                skill,
                re.MULTILINE | re.DOTALL,
            )
        ]
        self.assertEqual(3, len(templates))
        for template in templates:
            self.assertEqual(
                {"task_name", "message", "model", "reasoning_effort", "fork_turns"},
                set(template),
            )
            self.assertIn("Do not delegate or spawn another agent.", template["message"])

    def test_rejects_structural_skill_mutations(self) -> None:
        mutations = {
            "wrong lane": lambda text: text.replace(
                "| economy | `gpt-5.6-terra` |", "| economy | `gpt-5.6-sol` |", 1
            ),
            "omitted field": lambda text: text.replace(
                ',\n  "fork_turns": "none"', "", 1
            ),
            "nested delegation": lambda text: text.replace(
                "Do not delegate or spawn another agent.", "Return the result.", 1
            ),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                self.assert_text_rejected(SKILL, mutation)

    def test_playbook_requests_are_structural_templates(self) -> None:
        playbooks = (ROOT / PLAYBOOKS).read_text(encoding="utf-8")
        requests = [
            json.loads(payload)
            for payload in re.findall(r"```json\n(\{.*?\})\n```", playbooks, re.DOTALL)
        ]
        self.assertEqual(4, len(requests))
        for request in requests:
            self.assertEqual(
                {"task_name", "message", "model", "reasoning_effort", "fork_turns"},
                set(request),
            )
            self.assertRegex(request["message"], r"<[A-Z][A-Z0-9_]*>")
            self.assertIn("Do not delegate or spawn another agent.", request["message"])

    def test_rejects_structural_playbook_mutations(self) -> None:
        mutations = {
            "wrong lane": lambda text: text.replace(
                '"reasoning_effort": "low"', '"reasoning_effort": "high"', 1
            ),
            "omitted field": lambda text: text.replace(',\n  "fork_turns": "none"', "", 1),
            "nested delegation": lambda text: text.replace(
                "Do not delegate or spawn another agent.", "Return findings.", 1
            ),
            "placeholder": lambda text: text.replace("<SYMBOL>", "<symbol>", 1),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                self.assert_text_rejected(PLAYBOOKS, mutation)

    def test_rejects_runtime_key_and_runtime_file(self) -> None:
        self.assert_json_rejected(POLICY, lambda value: value.__setitem__("hooks", []))
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        hook = root / "plugins/mars-cost-router/hooks/hook.py"
        hook.parent.mkdir(parents=True)
        hook.write_text("print('not allowed')\n", encoding="utf-8")
        with self.assertRaises(ValidationError):
            validate_repository(root)

    def test_rejects_evidence_hash_arithmetic_and_caveat_mutations(self) -> None:
        mutations = {
            "status": lambda value: value.__setitem__("status", "descriptive"),
            "hash": lambda value: value.__setitem__(
                "frozen_suite_aggregate_sha256", "0" * 64
            ),
            "arithmetic": lambda value: value["treatments"]["selective_terra_sol"][
                "tokens"
            ].__setitem__("total", 728707),
            "caveat": lambda value: value["caveats"].pop(),
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                self.assert_json_rejected(FIXED_SUMMARY, mutation)

    def test_rejects_unsafe_claim_secret_and_local_path(self) -> None:
        additions = (
            "without " + "compromising quality",
            "$" + "mars-cost-router",
            "sk-" + "x" * 32,
            "C:" + "/Us" + "ers/example/private",
        )
        for addition in additions:
            with self.subTest(addition=addition[:12]):
                self.assert_text_rejected(
                    Path("CHANGELOG.md"), lambda text, value=addition: text + f"\n{value}\n"
                )

    def test_ignored_internal_and_generated_files_do_not_change_validation(self) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        before = validate_repository(root)
        paths = (
            root / ".git/objects/aa/object",
            root / "scripts/__pycache__/module.pyc",
            root / "video/out/explainer.mp4",
        )
        for path in paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"C:" + b"/Us" + b"ers/private\nsk-" + b"x" * 32)
        self.assertEqual(before, validate_repository(root))

    def test_ci_is_pinned_read_only_and_checks_video(self) -> None:
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        for phrase in (
            "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
            "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065",
            "actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020",
            'node-version: "24"',
            "run: node video/verify.mjs",
            "persist-credentials: false",
            "contents: read",
        ):
            self.assertIn(phrase, workflow)

    def test_current_version_and_walkthrough_surfaces(self) -> None:
        release_url = (
            "https://github.com/userbox020/mars-cost-router/releases/download/"
            f"{WALKTHROUGH_VERSION}/mars-cost-router-explainer-"
            f"{WALKTHROUGH_VERSION}.mp4"
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        story = (ROOT / "PROJECT_STORY.md").read_text(encoding="utf-8")
        self.assertIn(f"![Version {CURRENT_VERSION}]", readme)
        self.assertIn(f"Watch the {WALKTHROUGH_VERSION} walkthrough", readme)
        self.assertIn(f"Watch the {WALKTHROUGH_VERSION} walkthrough", story)
        self.assertIn(release_url, readme)
        self.assertIn(release_url, story)
        self.assertIn(
            f"## {CURRENT_VERSION} - 2026-07-21",
            (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            f"placeholder: {CURRENT_VERSION}",
            (ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
