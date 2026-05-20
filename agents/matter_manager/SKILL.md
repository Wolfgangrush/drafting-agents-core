# Matter Manager

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  - {{JURISDICTION_COURT_HIERARCHY}}: path to a JSON map of courts for this jurisdiction
  - {{JURISDICTION_TIMEZONE}}: e.g. "Europe/London", "Europe/Brussels"
  No other jurisdiction-specific tokens in this skill.
-->

Holds every active matter — parties, prayers, hearings, orders, draft state. Walk into court, context comes back instantly.

## Matter Schema

Each matter is stored as a structured record at `~/.ailawfirm_{{COUNTRY_LOWER}}/matters/`:

```
matter_id: string (unique, e.g. "MAT-2026-0014")
title: string (e.g. "Smith v Jones [2026]")
parties:
  applicant/claimant: string
  respondent/defendant: string
  additional_parties: [string]
prayers: [string]  (reliefs sought)
hearings:
  - date: ISO8601
    court: string (from {{JURISDICTION_COURT_HIERARCHY}})
    type: string (mention, directions, trial, etc.)
    outcome: string | null
orders:
  - date: ISO8601
    type: string
    summary: string
draft_state:
  current_version: string
  last_modified: ISO8601
  status: enum (drafting | review | finalised | filed)
notes: string
created: ISO8601
modified: ISO8601
```

## Operations

- **create**: Initialise a new matter with minimum required fields (title, parties)
- **update**: Modify any field; timestamps auto-update
- **query**: Search by matter_id, party name, court, date range, status
- **hearing_add**: Append a hearing entry with date, court, type
- **order_add**: Append an order entry
- **context_snapshot**: Return the full current state of a matter for use by other agents

## Storage

All matter data stays local at `~/.ailawfirm_{{COUNTRY_LOWER}}/matters/`. Never transmitted. Never synced to third-party cloud.

## Timezone

All dates are stored as ISO8601 in `{{JURISDICTION_TIMEZONE}}`.
