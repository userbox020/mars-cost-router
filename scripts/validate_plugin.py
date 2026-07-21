#!/usr/bin/env python3
"""Validate the public Mars Cost Router package using only the standard library."""

from __future__ import annotations

import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_REL = Path("plugins/mars-cost-router")
PLUGIN_ROOT = ROOT / PLUGIN_REL
MARKETPLACE_PATH = ROOT / ".agents/plugins/marketplace.json"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin/plugin.json"
POLICY_PATH = PLUGIN_ROOT / "policy/default.json"
SKILL_PATH = PLUGIN_ROOT / "skills/mars-cost-router/SKILL.md"
FIXED_SUMMARY_PATH = ROOT / "public-evidence/fixed-v1.2-summary.json"
RATE_INDEX_PATH = ROOT / "public-evidence/rate-index-2026-07-17.json"
VERSION = "0.3.0"
REPOSITORY_URL = "https://github.com/userbox020/mars-cost-router"
HOMEPAGE_URL = f"{REPOSITORY_URL}#readme"
LONG_DESCRIPTION = (
    "Independent and unofficial; Mars is the project name, not a model. "
    "Adds a delegation skill with explicit economy, balanced, and premium model, "
    "effort, and context settings for Codex."
)

EXPECTED_PLUGIN_FILES = {
    Path(".codex-plugin/plugin.json"),
    Path("policy/default.json"),
    Path("skills/mars-cost-router/SKILL.md"),
}
EXPECTED_LANES = {
    "economy": {
        "model": "gpt-5.6-terra",
        "reasoning_effort": "low",
        "fork_turns": "none",
    },
    "balanced": {
        "model": "gpt-5.6-terra",
        "reasoning_effort": "medium",
        "fork_turns": "none",
    },
    "premium": {
        "model": "gpt-5.6-sol",
        "reasoning_effort": "high",
        "fork_turns": "none",
    },
}
EXPECTED_FALLBACKS = {
    "economy": ["balanced", "premium"],
    "balanced": ["premium"],
    "premium": [],
}
FIXED_CAVEATS = [
    "Three precommitted pairs of four synthetic read-only tasks are summarized descriptively.",
    "No causal, general-quality, quality-equivalence, or quality-superiority conclusion is supported.",
    "No cost, billing, ChatGPT-credit, or savings conclusion is supported.",
    "Token and duration observations are order- and cache-confounded.",
    "Zero observed retries or reroutes does not prove none occurred or that requested and effective routes matched.",
]
RATE_CAVEATS = [
    "The indices compare listed Standard API rates only.",
    "The comparison is not an invoice, bill prediction, cost calculation, or savings claim.",
]
OFFICIAL_RATE_URLS = [
    "https://developers.openai.com/api/docs/pricing",
    "https://developers.openai.com/api/docs/models/gpt-5.6-sol",
    "https://developers.openai.com/api/docs/models/gpt-5.6-terra",
]


class ValidationError(ValueError):
    """Raised when the repository does not conform to the public package contract."""


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_object_without_duplicates,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be a JSON object")
    return value


def _require_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    mapping = _require_mapping(value, label)
    actual = set(mapping)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValidationError(f"{label} keys are not closed; missing={missing}, extra={extra}")
    return mapping


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return value


def _require_int(value: Any, label: str, minimum: int = 0) -> int:
    if type(value) is not int or value < minimum:
        raise ValidationError(f"{label} must be an integer of at least {minimum}")
    return value


def _require_percent(value: Any, label: str) -> float:
    if type(value) not in (int, float) or not -100 <= value <= 100:
        raise ValidationError(f"{label} must be a percentage from -100 through 100")
    return float(value)


def _iter_public_tree():
    """Yield repository entries without generated caches or Git internals."""

    ignored_directories = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }
    ignored_suffixes = {".pyc", ".pyo", ".pyd"}
    for current, directories, files in os.walk(ROOT, followlinks=False):
        directories[:] = [name for name in directories if name not in ignored_directories]
        current_path = Path(current)
        for name in directories:
            yield current_path / name
        for name in files:
            if name != ".git" and Path(name).suffix.casefold() not in ignored_suffixes:
                yield current_path / name


def _validate_tree() -> None:
    required = (
        MARKETPLACE_PATH,
        MANIFEST_PATH,
        POLICY_PATH,
        SKILL_PATH,
        FIXED_SUMMARY_PATH,
        RATE_INDEX_PATH,
    )
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise ValidationError(f"missing required files: {missing}")

    actual_plugin_files = {
        path.relative_to(PLUGIN_ROOT) for path in PLUGIN_ROOT.rglob("*") if path.is_file()
    }
    if actual_plugin_files != EXPECTED_PLUGIN_FILES:
        missing_files = sorted(str(path) for path in EXPECTED_PLUGIN_FILES - actual_plugin_files)
        extra_files = sorted(str(path) for path in actual_plugin_files - EXPECTED_PLUGIN_FILES)
        raise ValidationError(
            f"plugin package structure differs; missing={missing_files}, extra={extra_files}"
        )

    root_resolved = ROOT.resolve()
    for path in _iter_public_tree():
        if path.is_symlink():
            raise ValidationError(f"symlinks are not allowed in the public tree: {path.relative_to(ROOT)}")
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError as exc:
            raise ValidationError(f"path escapes repository root: {path}") from exc

    for path in (PLUGIN_ROOT / relative for relative in EXPECTED_PLUGIN_FILES):
        if path.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            raise ValidationError(f"installed plugin file must not be executable: {path.relative_to(ROOT)}")


def _validate_marketplace(marketplace: Any) -> dict[str, Any]:
    marketplace = _require_keys(
        marketplace, {"name", "interface", "plugins"}, "marketplace"
    )
    if marketplace["name"] != "mars-plugins":
        raise ValidationError("marketplace.name must be mars-plugins")
    interface = _require_keys(marketplace["interface"], {"displayName"}, "marketplace.interface")
    if interface["displayName"] != "Mars Plugins":
        raise ValidationError("marketplace displayName must be Mars Plugins")
    plugins = marketplace["plugins"]
    if not isinstance(plugins, list) or len(plugins) != 1:
        raise ValidationError("marketplace.plugins must contain exactly one entry")
    plugin = _require_keys(
        plugins[0], {"name", "version", "source", "policy", "category"}, "marketplace plugin"
    )
    if plugin["name"] != "mars-cost-router" or plugin["version"] != VERSION:
        raise ValidationError("marketplace plugin identity or version is invalid")
    if plugin["category"] != "Productivity":
        raise ValidationError("marketplace category must be Productivity")
    source = _require_keys(plugin["source"], {"source", "path"}, "marketplace source")
    if source != {"source": "local", "path": "./plugins/mars-cost-router"}:
        raise ValidationError("marketplace must use the confined local plugin source")
    source_path = (ROOT / source["path"]).resolve()
    try:
        source_path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValidationError("marketplace source escapes the repository") from exc
    if source_path != PLUGIN_ROOT.resolve():
        raise ValidationError("marketplace source does not resolve to the plugin package")
    install = _require_keys(
        plugin["policy"], {"installation", "authentication"}, "marketplace policy"
    )
    if install != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
        raise ValidationError("marketplace install policy is invalid")
    return plugin


def _validate_manifest(manifest: Any) -> dict[str, Any]:
    manifest = _require_keys(
        manifest,
        {
            "name",
            "version",
            "description",
            "author",
            "homepage",
            "repository",
            "license",
            "keywords",
            "skills",
            "interface",
        },
        "plugin manifest",
    )
    if manifest["name"] != "mars-cost-router" or manifest["version"] != VERSION:
        raise ValidationError("plugin manifest identity or version is invalid")
    _require_string(manifest["description"], "plugin description")
    author = _require_keys(manifest["author"], {"name", "url"}, "plugin author")
    if author != {"name": "userbox020", "url": "https://github.com/userbox020"}:
        raise ValidationError("plugin author is invalid")
    if manifest["homepage"] != HOMEPAGE_URL:
        raise ValidationError("plugin homepage is invalid")
    if manifest["repository"] != REPOSITORY_URL:
        raise ValidationError("plugin repository is invalid")
    if manifest["license"] != "MIT":
        raise ValidationError("plugin license must be MIT")
    keywords = manifest["keywords"]
    if not isinstance(keywords, list) or not keywords or not all(
        isinstance(item, str) and item for item in keywords
    ):
        raise ValidationError("plugin keywords must be a non-empty string list")
    if manifest["skills"] != "./skills/":
        raise ValidationError("plugin skills path must be ./skills/")
    interface = _require_keys(
        manifest["interface"],
        {
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
            "capabilities",
            "defaultPrompt",
            "brandColor",
            "websiteURL",
        },
        "plugin interface",
    )
    expected_scalars = {
        "displayName": "Mars Cost Router",
        "developerName": "Mars Cost Router contributors",
        "category": "Productivity",
        "brandColor": "#C1440E",
        "websiteURL": HOMEPAGE_URL,
    }
    for key, expected in expected_scalars.items():
        if interface[key] != expected:
            raise ValidationError(f"plugin interface {key} is invalid")
    _require_string(interface["shortDescription"], "interface shortDescription")
    if interface["longDescription"] != LONG_DESCRIPTION:
        raise ValidationError("plugin interface longDescription is invalid")
    if interface["capabilities"] != ["Interactive"]:
        raise ValidationError("plugin interface capabilities are invalid")
    prompts = interface["defaultPrompt"]
    if not isinstance(prompts, list) or len(prompts) != 1:
        raise ValidationError("plugin interface defaultPrompt must contain one prompt")
    _require_string(prompts[0], "interface defaultPrompt entry")
    return manifest


def _validate_policy(policy: Any) -> None:
    policy = _require_keys(
        policy,
        {"version", "policy_id", "effective_date", "execution_mode", "lanes", "fallback_order"},
        "routing policy",
    )
    if type(policy["version"]) is not int or policy["version"] != 3:
        raise ValidationError("routing policy version must be integer 3")
    if policy["policy_id"] != "mars-cost-router-explicit-v3":
        raise ValidationError("routing policy_id is invalid")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(policy["effective_date"])):
        raise ValidationError("routing policy effective_date must use YYYY-MM-DD")
    if policy["execution_mode"] != "model_directed":
        raise ValidationError("routing policy execution_mode must be model_directed")
    lanes = _require_keys(policy["lanes"], set(EXPECTED_LANES), "routing lanes")
    for lane, expected in EXPECTED_LANES.items():
        actual = _require_keys(
            lanes[lane], {"model", "reasoning_effort", "fork_turns"}, f"{lane} lane"
        )
        if actual != expected:
            raise ValidationError(f"{lane} lane settings differ from the public policy")
    fallback = _require_keys(
        policy["fallback_order"], set(EXPECTED_FALLBACKS), "fallback order"
    )
    if fallback != EXPECTED_FALLBACKS:
        raise ValidationError("fallback order differs from the public policy")


def _parse_frontmatter(skill: str) -> dict[str, str]:
    lines = skill.splitlines()
    if not lines or lines[0] != "---":
        raise ValidationError("skill must start with YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValidationError("skill frontmatter is not closed") from exc
    frontmatter: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            raise ValidationError(f"invalid skill frontmatter line: {line}")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in frontmatter or not key or not value:
            raise ValidationError("skill frontmatter has duplicate or empty fields")
        frontmatter[key] = value
    if set(frontmatter) != {"name", "description"}:
        raise ValidationError("skill frontmatter permits only name and description")
    if frontmatter["name"] != "mars-cost-router":
        raise ValidationError("skill frontmatter name must be mars-cost-router")
    return frontmatter


def _validate_skill(skill: str) -> None:
    frontmatter = _parse_frontmatter(skill)
    _require_string(frontmatter["description"], "skill frontmatter description")
    row_pattern = re.compile(
        r"^\| (economy|balanced|premium) \| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|$",
        re.MULTILINE,
    )
    rows = {
        lane: {"model": model, "reasoning_effort": effort, "fork_turns": fork_turns}
        for lane, model, effort, fork_turns in row_pattern.findall(skill)
    }
    if rows != EXPECTED_LANES:
        raise ValidationError("skill lane table differs from the routing policy")

    template_pattern = re.compile(
        r"^### (Economy|Balanced|Premium) exact input\n\n```json\n(\{.*?\})\n```$",
        re.MULTILINE | re.DOTALL,
    )
    templates: dict[str, Any] = {}
    for lane, payload in template_pattern.findall(skill):
        try:
            templates[lane.lower()] = json.loads(
                payload, object_pairs_hook=_object_without_duplicates
            )
        except json.JSONDecodeError as exc:
            raise ValidationError(f"invalid {lane} spawn template JSON: {exc}") from exc
    if set(templates) != set(EXPECTED_LANES):
        raise ValidationError("skill must contain exactly one spawn template per lane")
    template_keys = {"task_name", "message", "model", "reasoning_effort", "fork_turns"}
    for lane, expected in EXPECTED_LANES.items():
        template = _require_keys(templates[lane], template_keys, f"{lane} spawn template")
        if any(template[key] != value for key, value in expected.items()):
            raise ValidationError(f"{lane} spawn template differs from the routing policy")
        if "Do not delegate or spawn another agent." not in str(template["message"]):
            raise ValidationError(f"{lane} spawn template must prohibit nested delegation")

    required_claim_boundaries = (
        "Instruction-driven and evidence-limited",
        "does not enforce or independently verify",
        "requested lane is not evidence",
        "REQUIRED — NEVER INHERIT",
        "Inheritance or omission of any of these three fields is invalid.",
        "Do not set `agent_type` or `service_tier`.",
        "The root owns scope, integration, conflict resolution, final verification",
        "describe only evidence actually observed",
    )
    normalized = re.sub(r"\s+", " ", skill)
    for statement in required_claim_boundaries:
        if statement not in normalized:
            raise ValidationError(f"skill is missing required boundary: {statement}")


def _validate_fixed_summary(summary: Any) -> None:
    summary = _require_keys(
        summary,
        {
            "schema_version",
            "status",
            "frozen_suite_aggregate_sha256",
            "source_series_summary_sha256",
            "provenance",
            "cli_version",
            "series",
            "treatments",
            "recorded_deltas_selective_minus_baseline",
            "caveats",
        },
        "fixed-v1.2 public summary",
    )
    if summary["schema_version"] != 1 or type(summary["schema_version"]) is not int:
        raise ValidationError("fixed-v1.2 summary schema_version must be integer 1")
    if summary["status"] != "descriptive-synthetic":
        raise ValidationError("fixed-v1.2 summary status must be descriptive-synthetic")
    expected_hashes = {
        "frozen_suite_aggregate_sha256": (
            "96b06474481b7fc4eeec612b4845f4eeb4cb8eed38b7e3fc69dd67c75c1d7bff"
        ),
        "source_series_summary_sha256": (
            "05e010d3805a4b2c16dd4a97cf39342cd1fe091af834c4df67fe110bc76c2361"
        ),
    }
    for field, expected in expected_hashes.items():
        value = summary[field]
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValidationError(f"fixed-v1.2 {field} must be lowercase SHA-256")
        if value != expected:
            raise ValidationError(f"fixed-v1.2 {field} differs from the frozen record")
    provenance = _require_keys(
        summary["provenance"], set(expected_hashes), "fixed-v1.2 provenance"
    )
    expected_provenance = {
        "frozen_suite_aggregate_sha256": "Binds the frozen suite inputs.",
        "source_series_summary_sha256": (
            "Identifies the result source summarized by this sanitized file."
        ),
    }
    if provenance != expected_provenance:
        raise ValidationError("fixed-v1.2 provenance explanations are invalid")
    if summary["cli_version"] != "0.144.5":
        raise ValidationError("fixed-v1.2 CLI version must be 0.144.5")

    series = _require_keys(summary["series"], {"pairs", "tasks_per_pair"}, "fixed series")
    pairs = _require_int(series["pairs"], "fixed series pairs", 1)
    tasks = _require_int(series["tasks_per_pair"], "fixed series tasks_per_pair", 1)
    if (pairs, tasks) != (3, 4):
        raise ValidationError("fixed series must contain three pairs of four tasks")

    expected_treatments = {
        "selective_terra_sol": {
            "checks": (12, 12),
            "tokens": {"child": 356116, "root": 372590, "total": 728706},
            "duration": 45094,
        },
        "all_sol_high_baseline": {
            "checks": (12, 12),
            "tokens": {"child": 356494, "root": 412418, "total": 768912},
            "duration": 53328,
        },
    }
    treatments = _require_keys(
        summary["treatments"], set(expected_treatments), "fixed treatments"
    )
    treatment_keys = {
        "deterministic_checks",
        "observed_automatic_retries",
        "observed_reroutes",
        "tokens",
        "median_wall_duration_ms",
    }
    for name, expected in expected_treatments.items():
        treatment = _require_keys(treatments[name], treatment_keys, f"{name} treatment")
        checks = _require_keys(
            treatment["deterministic_checks"], {"passed", "total"}, f"{name} checks"
        )
        passed = _require_int(checks["passed"], f"{name} checks passed")
        total = _require_int(checks["total"], f"{name} checks total", 1)
        if passed > total or (passed, total) != expected["checks"]:
            raise ValidationError(f"{name} deterministic check result is invalid")
        for field in ("observed_automatic_retries", "observed_reroutes"):
            if _require_int(treatment[field], f"{name} {field}") != 0:
                raise ValidationError(f"{name} {field} must be zero")
        tokens = _require_keys(
            treatment["tokens"], {"child", "root", "total"}, f"{name} tokens"
        )
        for field in ("child", "root", "total"):
            _require_int(tokens[field], f"{name} {field} tokens")
        if tokens["child"] + tokens["root"] != tokens["total"]:
            raise ValidationError(f"{name} child and root tokens do not sum to total")
        if tokens != expected["tokens"]:
            raise ValidationError(f"{name} token record differs from fixed-v1.2")
        duration = _require_int(
            treatment["median_wall_duration_ms"], f"{name} median duration", 1
        )
        if duration > 86_400_000 or duration != expected["duration"]:
            raise ValidationError(f"{name} median duration differs from fixed-v1.2")

    routed = treatments["selective_terra_sol"]
    baseline = treatments["all_sol_high_baseline"]
    delta_inputs = {
        "child_tokens": (routed["tokens"]["child"], baseline["tokens"]["child"]),
        "root_tokens": (routed["tokens"]["root"], baseline["tokens"]["root"]),
        "total_tokens": (routed["tokens"]["total"], baseline["tokens"]["total"]),
        "median_wall_duration_ms": (
            routed["median_wall_duration_ms"],
            baseline["median_wall_duration_ms"],
        ),
    }
    deltas = _require_keys(
        summary["recorded_deltas_selective_minus_baseline"],
        set(delta_inputs),
        "fixed recorded deltas",
    )
    for name, (routed_value, baseline_value) in delta_inputs.items():
        delta = _require_keys(deltas[name], {"absolute", "percent"}, f"{name} delta")
        if type(delta["absolute"]) is not int:
            raise ValidationError(f"{name} absolute delta must be an integer")
        percent = _require_percent(delta["percent"], f"{name} percent delta")
        expected_absolute = routed_value - baseline_value
        expected_percent = round(expected_absolute / baseline_value * 100, 2)
        if delta["absolute"] != expected_absolute or percent != expected_percent:
            raise ValidationError(f"{name} delta does not match the recorded values")

    if summary["caveats"] != FIXED_CAVEATS:
        raise ValidationError("fixed-v1.2 caveats must match the closed public caveat set")


def _validate_rate_index(rate_index: Any) -> None:
    rate_index = _require_keys(
        rate_index,
        {
            "schema_version",
            "status",
            "effective_date",
            "retrieved_date",
            "rate_plan",
            "indices",
            "official_source_urls",
            "chatgpt_credits",
            "recheck_requirement",
            "caveats",
        },
        "public rate index",
    )
    if rate_index["schema_version"] != 1 or type(rate_index["schema_version"]) is not int:
        raise ValidationError("rate index schema_version must be integer 1")
    if rate_index["status"] != "rate-comparison-only":
        raise ValidationError("rate index status must be rate-comparison-only")
    if rate_index["effective_date"] != "2026-07-17":
        raise ValidationError("rate index effective_date is invalid")
    if rate_index["retrieved_date"] != "2026-07-18":
        raise ValidationError("rate index retrieved_date is invalid")
    if rate_index["rate_plan"] != "Standard API":
        raise ValidationError("rate index plan must be Standard API")
    indices = _require_keys(
        rate_index["indices"], {"gpt-5.6-terra", "gpt-5.6-sol"}, "rate indices"
    )
    for model, value in indices.items():
        if not 0 < _require_int(value, f"{model} rate index", 1) <= 100:
            raise ValidationError(f"{model} rate index is outside the supported range")
    if indices != {"gpt-5.6-terra": 50, "gpt-5.6-sol": 100}:
        raise ValidationError("rate indices must preserve the dated Terra 50 / Sol 100 ratio")
    if rate_index["official_source_urls"] != OFFICIAL_RATE_URLS:
        raise ValidationError("rate index official source URLs differ from the dated record")
    if rate_index["chatgpt_credits"] != "excluded":
        raise ValidationError("rate index must explicitly exclude ChatGPT credits")
    if rate_index["recheck_requirement"] != (
        "Recheck the official sources before publication or use."
    ):
        raise ValidationError("rate index must retain the source recheck requirement")
    if rate_index["caveats"] != RATE_CAVEATS:
        raise ValidationError("rate index caveats must match the closed public caveat set")


def _walk_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(key)
            keys.extend(_walk_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.extend(_walk_keys(nested))
    return keys


def _validate_no_runtime_features(documents: tuple[Any, ...]) -> None:
    forbidden_keys = {"hooks", "hook", "mcp", "mcpservers", "executables", "commands"}
    for key in (key.casefold() for document in documents for key in _walk_keys(document)):
        if key in forbidden_keys:
            raise ValidationError(f"forbidden hook/MCP/executable metadata key: {key}")


def _validate_public_files() -> int:
    patterns = {
        "Windows user path": re.compile(rb"[A-Za-z]:[\\/]Users[\\/]", re.IGNORECASE),
        "workspace-local path": re.compile(rb"[A-Za-z]:[\\/]_Work[\\/]", re.IGNORECASE),
        "Unix user path": re.compile(rb"/(?:Users|home)/[^/\s]+/"),
        "private key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "OpenAI-style secret": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
        "GitHub token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
        "AWS access key": re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    }
    unsupported_claims = (
        "without " + "compromising quality",
        "save " + "tokens",
        "guaranteed " + "savings",
        "GPT 5.6 " + "Mars",
    )
    files = [path for path in _iter_public_tree() if path.is_file()]
    for path in files:
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise ValidationError(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc
        for label, pattern in patterns.items():
            if pattern.search(content):
                raise ValidationError(f"{label} found in {path.relative_to(ROOT)}")
        lowered = content.lower()
        for claim in unsupported_claims:
            if claim.lower().encode("utf-8") in lowered:
                raise ValidationError(
                    f"unsupported headline claim {claim!r} found in {path.relative_to(ROOT)}"
                )
        if path.suffix.casefold() == ".json":
            _load_json(path)
    return len(files)


def validate_repository(root: Path | None = None) -> dict[str, int | str]:
    """Validate a repository tree and return a compact success summary."""

    global ROOT, PLUGIN_ROOT, MARKETPLACE_PATH, MANIFEST_PATH, POLICY_PATH, SKILL_PATH
    global FIXED_SUMMARY_PATH, RATE_INDEX_PATH
    if root is not None:
        ROOT = Path(root).resolve()
        PLUGIN_ROOT = ROOT / PLUGIN_REL
        MARKETPLACE_PATH = ROOT / ".agents/plugins/marketplace.json"
        MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin/plugin.json"
        POLICY_PATH = PLUGIN_ROOT / "policy/default.json"
        SKILL_PATH = PLUGIN_ROOT / "skills/mars-cost-router/SKILL.md"
        FIXED_SUMMARY_PATH = ROOT / "public-evidence/fixed-v1.2-summary.json"
        RATE_INDEX_PATH = ROOT / "public-evidence/rate-index-2026-07-17.json"

    _validate_tree()
    marketplace = _load_json(MARKETPLACE_PATH)
    manifest = _load_json(MANIFEST_PATH)
    policy = _load_json(POLICY_PATH)
    fixed_summary = _load_json(FIXED_SUMMARY_PATH)
    rate_index = _load_json(RATE_INDEX_PATH)
    marketplace_plugin = _validate_marketplace(marketplace)
    manifest = _validate_manifest(manifest)
    _validate_policy(policy)
    _validate_skill(SKILL_PATH.read_text(encoding="utf-8"))
    _validate_fixed_summary(fixed_summary)
    _validate_rate_index(rate_index)
    _validate_no_runtime_features((marketplace, manifest, policy))
    if marketplace_plugin["version"] != manifest["version"]:
        raise ValidationError("marketplace and plugin manifest versions differ")
    file_count = _validate_public_files()
    return {"name": manifest["name"], "version": manifest["version"], "files": file_count}


def main() -> int:
    try:
        result = validate_repository()
    except (ValidationError, OSError, UnicodeError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"validated {result['name']} {result['version']}: "
        f"{result['files']} public files; static instruction-only package"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
