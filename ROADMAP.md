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

- Multi-LLM adapter: OpenAI · paid Gemini · **DeepSeek V4 Pro** · Ollama (local Llama 3.3 70B / Qwen 2.5 72B) · BYOM for in-firm LLMs
- True air-gap mode — no API calls, no telemetry, no network egress
- Model-agnostic skill execution layer

## Honest note on timelines
Solo-author OSS. Ships as time permits. Targets are indicative, not committed dates. Open an issue if a specific feature on a specific timeline matters to your work.

---

## 🌐 Family Status (honest · cross-firm)

The Wolfgang Rush AI Law Firm family ships across 7 jurisdictions. Honest status of the v0.2 legal-knowledge layer (statute corpus + drafting data) per firm:

| Firm | Statute corpus | Drafting corpus | Shared agents | GitHub |
|------|---|---|---|---|
| 🇮🇳 **India** | Native knowledge base · maintainer-curated | Wolfgang_rush plugins (14 Indian-litigation plugins · separate stack) | Not applicable — Indian-specific | ✅ LIVE |
| 🇪🇺 **EU** | ✅ 11 statutes · 8/8 Tier-1 | ✅ 26 templates · 9/9 Tier-1 | ✅ Migrated | ✅ LIVE |
| 🇦🇺 **Australia** | ✅ Complete | ✅ Complete | ✅ Migrated | ✅ LIVE |
| 🇦🇪 **Dubai-DIFC** | ✅ Complete | ✅ Complete | ✅ Migrated | ✅ LIVE |
| 🇸🇬 **Singapore** | ✅ Complete | ✅ Complete | ✅ Migrated | ✅ LIVE |
| 🇬🇧 **UK** | 🚧 v0.2 milestone | 🚧 v0.2 milestone | ✅ Migrated | ✅ LIVE (firm code) |
| 🇺🇸 **USA** | 🚧 v0.2 milestone | 🚧 v0.2 milestone | ✅ Migrated | ✅ LIVE (firm code) |

**Plus:**
- **AI Startup Firm — India v0.1** (legal-ops brain for founders)
- **GC In-House Brain** (multi-jurisdictional, 8 modules — 3 live · 5 shipping v0.2+)

Both share the same `drafting-agents-core` architecture pattern.

All firms migrated to this central agent library on 2026-05-20 (Path B-Lite) — single source of truth for the agent layer; jurisdictional knowledge stays per-firm.
