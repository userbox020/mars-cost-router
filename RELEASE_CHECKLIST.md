# Release Checklist

## 0.3.2 release gates

- [x] Synchronize current package version `0.3.2` across marketplace and plugin
      metadata, validator, tests, README badge, changelog, and issue template,
      while retaining the separately versioned `0.3.1` walkthrough links.
- [x] Run `python scripts/validate_plugin.py` successfully for the local candidate.
- [x] Run the complete focused unit test suite successfully (14 tests).
- [x] Run `node video/verify.mjs` successfully.
- [x] Parse every workspace JSON file, including the contract fixture,
      with the Python standard library.
- [x] Confirm fixed-v1.2 evidence files are unchanged and `docs/EVIDENCE.md`
      exactly excludes the 0.3.2 guidance from that evidence.
- [x] Confirm the installed package shape and policy lane values are unchanged.
- [x] Complete local claim and simplification review without adding enforcement,
      runtime, telemetry, quality-equivalence, or savings claims.

The published 0.3.1 walkthrough remains the intentional current overview. No
0.3.2 media or video-evidence claim is made by this candidate.

- [ ] Confirm hosted CI passes on the pushed `0.3.2` commit.
- [ ] Confirm a clean remote marketplace refresh/install reports `0.3.2`.
- [ ] Tag and publish `0.3.2`.
- [ ] Verify public package, documentation, and retained 0.3.1 walkthrough links
      after publication.

## 0.3.1 release gates

- [x] Synchronize version `0.3.1` across package metadata, marketplace metadata,
      validator, tests, README badge, changelog, issue template, and release URLs.
- [x] Run `python scripts/validate_plugin.py` successfully for the local candidate.
- [x] Run the complete local unit test suite successfully (31 tests).
- [x] Parse every tracked JSON file with the Python standard library.
- [x] Confirm fixed-v1.2 public evidence values, hashes, arithmetic, and caveats
      remain unchanged.
- [x] Complete local claim review, including video-source affirmative and
      unsupported-claim checks.
- [x] Verify the local `mars-cost-router-explainer-0.3.1.mp4` media, streams,
      subtitles, duration, and SHA-256
      `78EC16F2CB6E76B0362FB178D867CE59FF780133A9B9D0B62EAFF5D2FBB431B6`.
- [x] Confirm hosted CI passes on the pushed `0.3.1` commit.
- [x] Confirm a clean remote marketplace refresh/install reports `0.3.1`.
- [x] Tag and publish `0.3.1`.
- [x] Upload `mars-cost-router-explainer-0.3.1.mp4` to the `0.3.1` release.
- [x] Verify the public asset SHA-256 is
      `78EC16F2CB6E76B0362FB178D867CE59FF780133A9B9D0B62EAFF5D2FBB431B6`
      and verify its duration, streams, and subtitles after download.
- [x] Confirm the README and Project Story release-asset links return HTTP 200.

## 0.3.0 completed release checklist

- [x] Confirm marketplace and plugin versions match the changelog.
- [x] Run `python scripts/validate_plugin.py`.
- [x] Run `python -m unittest discover -s tests -v`.
- [x] Parse every tracked JSON file with the Python standard library.
- [x] Validate both closed `public-evidence/` summaries against their exact
      arithmetic, caveats, dates, hashes, and official source URLs.
- [x] Review the tree for secrets, local paths, evidence, captures, and generated
      files.
- [x] Confirm the plugin contains no hooks, MCP configuration, executables, or
      runtime telemetry.
- [x] Confirm public claims describe requested settings, not effective routing,
      actual cost, savings, or equivalent quality.
- [x] Confirm the actual GitHub Actions validation matrix passes on the hosted
      repository, not only in local simulation.
- [x] Test remote marketplace registration and installation from the hosted
      repository in a clean environment.
- [x] Check the final author, homepage, repository, and interface website URLs
      against the intended public repository after publication.
- [x] Link an actual hosted video, or ensure the README clearly labels the
      walkthrough as a script or recording plan rather than a hosted video.
- [x] Upload and verify a social-preview PNG on the hosted repository.
- [x] Record basic project/plugin name-clearance search notes and resolve obvious
      conflicts; do not present this check as legal clearance.
- [x] Finalize release notes and public documentation before tagging.
