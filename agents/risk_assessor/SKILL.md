# Risk Assessor

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{JURISDICTION_RISK_RUBRIC}}: path to the jurisdiction-specific risk matrix definition
  - {{JURISDICTION_BAR_RULES}}: path to bar-rules markdown
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  No other jurisdiction-specific tokens in this skill.
-->

Auto-classifies every AI-use session using a 3×3 risk matrix: application × use × technology. Warns on high-risk combinations. Logs classification to audit trail.

## 3×3 Risk Matrix

The risk rubric is pluggable via `{{JURISDICTION_RISK_RUBRIC}}`. The default matrix:

### Application (what the output is used for)
- **Tier A — Admin only**: Internal notes, calendar management, non-client-facing organisation
- **Tier B — General client work**: Standard commercial/contract drafting, research, template adaptation
- **Tier C — Court + vulnerable + protected characteristics**: Filings, hearings, vulnerable clients, special-category data, public-access cases

### Use (how the AI is being used)
- **Tier 1 — Spelling/grammar/formatting**: Surface-level, no legal reasoning
- **Tier 2 — Research/summarisation**: AI surfaces information; human verifies and decides
- **Tier 3 — Drafting + agentic**: AI generates substantive legal content or takes action

### Technology (what AI system is being used)
- **Tier a — Non-AI tools**: Spell-check, templates without reasoning
- **Tier b — Legal-specific AI (local)**: Purpose-built legal AI running locally
- **Tier c — Agentic cloud AI**: Cloud-based AI with autonomous capabilities

### Risk Classification
- **LOW (green)**: A1-2 + B1-2 + a-b combinations
- **MEDIUM (amber)**: Any C or 3 or c in isolation
- **HIGH (red)**: C3c (court+vulnerable + agentic + cloud AI) — requires documented justification

## Operations

- **classify**: Given a user request, classify it into the 3×3 matrix
- **warn**: If HIGH risk, surface the warning with the specific combination that triggered it
- **log**: Record the classification in the audit trail with timestamp, agent, user-confirmed flag

## Output Format

```
Session: <session_id>
Classification: <Tier>-<Tier>-<Tier> (e.g. B-2-b)
Risk Level: LOW / MEDIUM / HIGH
Warning: <if HIGH — specific combination and recommended mitigation>
Logged: YES <timestamp>
```

## Storage

Risk classification logs at `~/.ailawfirm_{{COUNTRY_LOWER}}/audit_logs/risk_assessor/`. Never transmitted.
