# Roadmap

## v0.1 (today)
- Claude Code native — skills run via the Claude Code skill system
- 10 canonical agents, generalized for any jurisdiction via `{{JURISDICTION_*}}` placeholders
- Shared Python utilities: compliance_firewall, audit_logger, leak_check, pseudonymisation interface
- jurisdiction_loader: per-firm config resolver (~50 LOC Python)
- Used by 6 foreign AI Law Firms (UK · EU · Singapore · Australia · Dubai-DIFC · USA)
- India firm out of scope (uses Wolfgang_rush plugin architecture)

## v0.2 (next 1–2 months)
- Jurisdictional-corpus loader stabilized
- Per-agent test coverage 80%+
- Plugin marketplace listing (Anthropic) when approved
- Per-jurisdiction bar-rule packs for top regulator sets

## v0.3+ (when demand signal lands)
Unlock trigger: real downstream user (not the maintainer) requests local-LLM support, OR the maintainer's Sunday review endorses it as priority.

- Multi-LLM adapter: OpenAI · paid Gemini · Ollama (local Llama 3.3 70B / Qwen 2.5 72B) · BYOM for in-firm LLMs
- True air-gap mode — no API calls, no telemetry, no network egress
- Model-agnostic skill execution layer

## Honest note on timelines
Solo-author OSS. Ships as time permits. Targets are indicative, not committed dates. Open an issue if a specific feature on a specific timeline matters to your work.
