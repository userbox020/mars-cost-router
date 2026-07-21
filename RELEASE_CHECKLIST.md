# Release Checklist

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
