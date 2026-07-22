# Contributing

Thanks for helping improve Mars Cost Router. This is an independent, unofficial
project. Keep changes small, public, and free of credentials, private prompts,
raw protocol captures, and evaluation evidence.

1. Open an issue before proposing a policy or behavior change.
2. Preserve explicit `model`, `reasoning_effort`, and `fork_turns` settings in
   every lane and keep final review at the root.
3. Run `python scripts/validate_plugin.py` and
   `python -m unittest discover -s tests -v`.
4. Describe user-visible changes and their evidence scope in the pull request.

Keep the plugin surface instruction-only: metadata, policy, and skill. Public
claims must identify requested settings, treat provider/runtime metadata as the
authority for effective execution, and reserve billing, realized savings, and
comparative quality conclusions for supporting evidence.
By contributing, you agree that your contribution is licensed under the MIT
License.

Repository: <https://github.com/userbox020/mars-cost-router>
