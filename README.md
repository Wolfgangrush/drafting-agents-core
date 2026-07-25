<div align="center">

<img src="docs/banner.png" width="820"/>

**Shared Claude Code agents powering the wolfgang_rush AI Law Firm across six jurisdictions.**

Visit the live site: [wolfgangrush.github.io](https://wolfgangrush.github.io)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/Claude%20Code-agent%20library-8A2BE2" alt="Claude Code agent library"/>
  <img src="https://img.shields.io/badge/jurisdictions-UK%20%C2%B7%20EU%20%C2%B7%20SG%20%C2%B7%20AU%20%C2%B7%20DIFC%20%C2%B7%20USA-blue" alt="Jurisdictions"/>
</p>


<div align="center">

<img src="docs/banner.png" width="820"/>

**Shared Claude Code agents powering the wolfgang_rush AI Law Firm across six jurisdictions.**

Visit the live site: [wolfgangrush.github.io](https://wolfgangrush.github.io)

</div>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/Claude%20Code-agent%20library-8A2BE2" alt="Claude Code agent library"/>
  <img src="https://img.shields.io/badge/jurisdictions-UK%20%C2%B7%20EU%20%C2%B7%20SG%20%C2%B7%20AU%20%C2%B7%20DIFC%20%C2%B7%20USA-blue" alt="Jurisdictions"/>
</p>


# Drafting Agents Core — shared agent library for the wolfgang_rush AI Law Firm family

**v0.1.0 · Claude Code native · MIT licensed · 2026**

Shared Claude Code skill library used by all foreign wolfgang_rush AI Law Firms (UK · EU · Singapore · Australia · Dubai-DIFC · USA). Each firm imports these agents via local clone + `config.toml`. India AI Law Firm uses its own wolfgang_rush plugin architecture and is out of scope for this repo.

## What's inside

| # | Agent | What it does |
|---|---|---|
| 1 | Receptionist (brain) | Intent classification · routes user requests to the right specialist |
| 2 | Matter Manager | Holds active matters — parties, prayers, hearings, orders, draft state |
| 3 | Citation Clerk | Parses jurisdiction-specific citations · 2-source verification |
| 4 | Court Registrar | Knows the court hierarchy for the configured jurisdiction |
| 5 | Drafting Assistant | Connects to wolfgang_rush drafting plugins (separate, MIT, optional) |
| 6 | Compliance Officer | Bar-rule firewall · advertising/solicitation risk · data-protection flags |
| 7 | Risk Assessor | 3×3 risk matrix — auto-classifies every session by application, use, technology |
| 8 | Audit Clerk | Always-on AI audit log · 90-day retention · ICS export · never transmitted |
| 9 | Transparency Gate | Client-disclosure gate · human-in-the-loop · no bulk-execute, no auto-emit |
| 10 | Direct Access Detector | Public-access / direct-access scheme safeguards |

## Shared utilities

| Utility | Purpose |
|---|---|
| `compliance_firewall.py` | Pluggable bar-rule firewall — per-jurisdiction rule sets |
| `audit_logger.py` | 90-day retention audit logging · ICS export |
| `leak_check.py` | Cross-layer leak detection · boundary enforcement |
| `pseudonymisation.py` | PII pseudonymisation gateway interface |

## Integration

Each firm imports these agents via local clone as a sibling directory. See `examples/integrating-into-a-firm/` for the 3-step quickstart.

```bash
git clone https://github.com/Wolfgangrush/drafting-agents-core
cd your-firm/
./setup.sh  # auto-clones drafting-agents-core as sibling if not present
```

## Jurisdiction support

Agents use `{{JURISDICTION_*}}` placeholders that each firm resolves via its `~/.ailawfirm_<country>/config.toml`. See `jurisdiction_loader/` for the config-loading helper.

## Roadmap

See [ROADMAP.md](ROADMAP.md). v0.1 = Claude Code native. v0.3+ = multi-LLM adapter (OpenAI · paid Gemini · **DeepSeek V4 Pro** · Ollama for local Llama 3.3 70B / Qwen 2.5 72B · BYOM for in-firm LLMs) when demand signal lands.

## License

MIT — see [LICENSE](LICENSE). Copyright wolfgang_rush, 2026.

## Maintainer

[wolfgang_rush](https://github.com/Wolfgangrush) — publisher. 2026.
