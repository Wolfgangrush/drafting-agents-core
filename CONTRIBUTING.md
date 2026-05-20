# Contributing

## How to extend agents

1. Each agent lives in `agents/<agent_name>/SKILL.md` — the canonical Claude Code skill body
2. Jurisdiction-specific tokens use `{{JURISDICTION_*}}` placeholders
3. A firm's `config.toml` provides the substitution values
4. To add a new agent: create the folder, write the SKILL.md, add a smoke test in `tests/`

## How to add jurisdiction support

1. Add the jurisdiction's bar rules, court hierarchy, citation format, and timezone to the loader
2. No agent body changes needed — the placeholder system handles it
3. Submit a PR with the jurisdiction config schema addition

## PR process

1. Open an issue describing the change
2. Fork, branch, implement
3. Run `python3 -m ruff check . && python3 -m ruff format --check .` before pushing
4. PR against `main`

## Rules for public contributions

- No real names, no personal identifiers (this is a public repo)
- No AAAK codes or internal shorthand
- MIT license applies to all contributions
- By submitting a PR, you license your contribution under MIT

## License

MIT — see [LICENSE](LICENSE).
