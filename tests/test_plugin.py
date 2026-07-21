from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_plugin import ValidationError, validate_repository


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = Path(".agents/plugins/marketplace.json")
MANIFEST = Path("plugins/mars-cost-router/.codex-plugin/plugin.json")
POLICY = Path("plugins/mars-cost-router/policy/default.json")
SKILL = Path("plugins/mars-cost-router/skills/mars-cost-router/SKILL.md")
FIXED_SUMMARY = Path("public-evidence/fixed-v1.2-summary.json")
RATE_INDEX = Path("public-evidence/rate-index-2026-07-17.json")


class PluginValidationTests(unittest.TestCase):
    def copy_repository(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        destination = Path(temporary.name) / "repository"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        return temporary, destination

    @staticmethod
    def mutate_json(root: Path, relative: Path, mutation) -> None:
        path = root / relative
        value = json.loads(path.read_text(encoding="utf-8"))
        mutation(value)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def assert_mutation_rejected(self, relative: Path, mutation) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        self.mutate_json(root, relative, mutation)
        with self.assertRaises(ValidationError):
            validate_repository(root)

    def test_public_repository_validates(self) -> None:
        result = validate_repository(ROOT)
        self.assertEqual("mars-cost-router", result["name"])
        self.assertEqual("0.3.0", result["version"])

    def test_rejects_missing_evidence_asset(self) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        (root / "assets/evidence/fixed-v1.2-performance.svg").unlink()
        with self.assertRaises(ValidationError):
            validate_repository(root)

    def test_public_manifest_and_evidence_identity(self) -> None:
        manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        self.assertEqual(
            {"name": "userbox020", "url": "https://github.com/userbox020"},
            manifest["author"],
        )
        self.assertEqual(
            "https://github.com/userbox020/mars-cost-router#readme",
            manifest["homepage"],
        )
        fixed = json.loads((ROOT / FIXED_SUMMARY).read_text(encoding="utf-8"))
        self.assertEqual("descriptive-synthetic", fixed["status"])
        self.assertNotIn("immutable_aggregate_sha256", fixed)
        self.assertEqual(
            "05e010d3805a4b2c16dd4a97cf39342cd1fe091af834c4df67fe110bc76c2361",
            fixed["source_series_summary_sha256"],
        )
        expected_caveat = (
            "Three precommitted pairs of four fixed read-only tasks are summarized descriptively."
        )
        old_wording = "synthetic " + "read-only tasks"
        self.assertIn(expected_caveat, fixed["caveats"])
        self.assertFalse(any(old_wording in caveat for caveat in fixed["caveats"]))
        self.assertEqual(728706, fixed["treatments"]["selective_terra_sol"]["tokens"]["total"])
        rate = json.loads((ROOT / RATE_INDEX).read_text(encoding="utf-8"))
        self.assertEqual("rate-comparison-only", rate["status"])
        self.assertEqual({"gpt-5.6-terra": 50, "gpt-5.6-sol": 100}, rate["indices"])

    def test_rejects_unknown_marketplace_metadata(self) -> None:
        self.assert_mutation_rejected(
            MARKETPLACE,
            lambda value: value["plugins"][0].__setitem__("compatibility", "invented"),
        )

    def test_rejects_marketplace_path_escape(self) -> None:
        self.assert_mutation_rejected(
            MARKETPLACE,
            lambda value: value["plugins"][0]["source"].__setitem__("path", "../plugin"),
        )

    def test_rejects_version_mismatch(self) -> None:
        self.assert_mutation_rejected(
            MANIFEST, lambda value: value.__setitem__("version", "0.3.1")
        )

    def test_rejects_manifest_metadata_mutation(self) -> None:
        self.assert_mutation_rejected(
            MANIFEST,
            lambda value: value["author"].__setitem__("url", "https://example.invalid"),
        )

    def test_manifest_long_description_has_exact_qualifier(self) -> None:
        manifest = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        qualifier = "Independent and unofficial; Mars is the project name, not a model."
        self.assertTrue(manifest["interface"]["longDescription"].startswith(qualifier))

    def test_rejects_lane_mutation(self) -> None:
        self.assert_mutation_rejected(
            POLICY,
            lambda value: value["lanes"]["balanced"].__setitem__("reasoning_effort", "high"),
        )

    def test_rejects_fixed_aggregate_mutation(self) -> None:
        self.assert_mutation_rejected(
            FIXED_SUMMARY,
            lambda value: value.__setitem__("frozen_suite_aggregate_sha256", "0" * 64),
        )

    def test_rejects_source_summary_hash_mutation(self) -> None:
        self.assert_mutation_rejected(
            FIXED_SUMMARY,
            lambda value: value.__setitem__("source_series_summary_sha256", "0" * 64),
        )

    def test_rejects_provenance_explanation_mutation(self) -> None:
        self.assert_mutation_rejected(
            FIXED_SUMMARY,
            lambda value: value["provenance"].__setitem__(
                "source_series_summary_sha256", "Unbound result."
            ),
        )

    def test_rejects_fixed_token_arithmetic_mutation(self) -> None:
        self.assert_mutation_rejected(
            FIXED_SUMMARY,
            lambda value: value["treatments"]["selective_terra_sol"]["tokens"].__setitem__(
                "total", 728707
            ),
        )

    def test_rejects_fixed_caveat_mutation(self) -> None:
        self.assert_mutation_rejected(
            FIXED_SUMMARY,
            lambda value: value["caveats"].pop(),
        )

    def test_rejects_old_fixed_caveat_wording(self) -> None:
        old_wording = "synthetic " + "read-only tasks"
        self.assert_mutation_rejected(
            FIXED_SUMMARY,
            lambda value: value["caveats"].__setitem__(
                0,
                value["caveats"][0].replace("fixed read-only tasks", old_wording),
            ),
        )

    def test_rejects_rate_source_mutation(self) -> None:
        self.assert_mutation_rejected(
            RATE_INDEX,
            lambda value: value["official_source_urls"].__setitem__(0, "https://example.invalid"),
        )

    def test_rejects_rate_index_mutation(self) -> None:
        self.assert_mutation_rejected(
            RATE_INDEX,
            lambda value: value["indices"].__setitem__("gpt-5.6-terra", 51),
        )

    def test_rejects_hook_added_to_plugin(self) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        hook = root / "plugins/mars-cost-router/hooks/hook.py"
        hook.parent.mkdir(parents=True)
        hook.write_text("print('not allowed')\n", encoding="utf-8")
        with self.assertRaises(ValidationError):
            validate_repository(root)

    def test_rejects_invalid_skill_frontmatter(self) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        path = root / SKILL
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace("name: mars-cost-router", "name: other", 1), encoding="utf-8")
        with self.assertRaises(ValidationError):
            validate_repository(root)

    def test_rejects_absolute_local_path(self) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        path = root / "CHANGELOG.md"
        local_path = "C:" + "/Us" + "ers/example/private"
        path.write_text(
            path.read_text(encoding="utf-8") + f"\n{local_path}\n",
            encoding="utf-8",
        )
        with self.assertRaises(ValidationError):
            validate_repository(root)

    def test_git_internals_are_excluded_from_scan_and_count(self) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        before = validate_repository(root)
        object_path = root / ".git/objects/aa/binary-object"
        object_path.parent.mkdir(parents=True)
        secret_like = b"sk-" + b"x" * 32
        local_path = b"C:" + b"/Us" + b"ers/example/private"
        object_path.write_bytes(b"\x00\xff" + secret_like + b"\n" + local_path)
        (root / ".git/config").write_text(
            "[remote \"origin\"]\nurl = private-local-value\n",
            encoding="utf-8",
        )
        after = validate_repository(root)
        self.assertEqual(before["files"], after["files"])
        self.assertEqual(before, after)

    def test_python_caches_are_excluded_from_scan_and_count(self) -> None:
        temporary, root = self.copy_repository()
        self.addCleanup(temporary.cleanup)
        before = validate_repository(root)
        cache_path = root / "scripts/__pycache__/validate_plugin.cpython-313.pyc"
        cache_path.parent.mkdir(parents=True)
        unix_path = b"/ho" + b"me/runner/private"
        unsupported_claim = b"without " + b"compromising quality"
        cache_path.write_bytes(unix_path + b"\n" + unsupported_claim)
        (root / "generated.pyc").write_bytes(b"sk-" + b"x" * 32)
        after = validate_repository(root)
        self.assertEqual(before["files"], after["files"])
        self.assertEqual(before, after)

    def test_ci_actions_are_pinned_and_read_only(self) -> None:
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        self.assertIn(
            "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
            workflow,
        )
        self.assertIn(
            "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065",
            workflow,
        )
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("timeout-minutes: 10", workflow)
        self.assertIn("contents: read", workflow)

    def test_rejects_unsupported_headline_claim(self) -> None:
        claims = (
            "without " + "compromising quality",
            "save " + "tokens",
            "guaranteed " + "savings",
            "GPT 5.6 " + "Mars",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                temporary, root = self.copy_repository()
                self.addCleanup(temporary.cleanup)
                path = root / "CHANGELOG.md"
                path.write_text(
                    path.read_text(encoding="utf-8") + f"\n{claim}\n",
                    encoding="utf-8",
                )
                with self.assertRaises(ValidationError):
                    validate_repository(root)


if __name__ == "__main__":
    unittest.main()
