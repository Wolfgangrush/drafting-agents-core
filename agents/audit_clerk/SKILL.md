# Audit Clerk

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  - {{JURISDICTION_TIMEZONE}}: e.g. "Europe/London", "Europe/Brussels"
  No other jurisdiction-specific tokens in this skill.
-->

Always-on AI audit log — prompt + output + timestamp + user-confirmed flag. 90-day default retention with enforced deletion policy. Stored locally at `~/.ailawfirm_{{COUNTRY_LOWER}}/audit_logs/`, never transmitted.

## Audit Record Schema

Every AI interaction is logged as:

```json
{
  "log_id": "string (UUID)",
  "timestamp": "ISO8601 ({{JURISDICTION_TIMEZONE}})",
  "agent": "string (which specialist was called)",
  "session_id": "string",
  "matter_id": "string | null",
  "prompt_summary": "string (one-line summary of the user's request)",
  "output_summary": "string (one-line summary of the AI's response)",
  "risk_classification": "LOW | MEDIUM | HIGH",
  "user_confirmed": "boolean (did the user review and confirm?)",
  "citation_verified": "boolean | null (if citation was involved)",
  "transparency_gate_passed": "boolean (was client disclosure confirmed?)"
}
```

## Operations

- **log**: Append a new audit record (called by other agents automatically)
- **query**: Search audit logs by date range, agent, matter_id, risk level
- **export**: Export audit logs as ICS / CSV / JSON for compliance review
- **purge**: Enforce 90-day retention — auto-delete records older than 90 days
- **stats**: Summary statistics (queries per day, per agent, risk distribution)

## Retention Policy

- **Default**: 90 days from timestamp
- **Enforcement**: Purge job runs on session start — deletes records where `timestamp < (now - 90 days)`
- **Override**: Configurable via `audit.retention_days` in config.toml (must be >= 30)
- **Deletion**: Secure delete (overwrite before unlink)

## Storage

All audit logs at `~/.ailawfirm_{{COUNTRY_LOWER}}/audit_logs/`. Local SQLite. Never transmitted. Never synced to cloud.

## Compliance

This audit trail satisfies:
- Professional conduct record-keeping requirements
- AI-use disclosure obligations
- Regulatory inspection readiness
- Client challenge defence (documented AI use with human confirmation at each step)
