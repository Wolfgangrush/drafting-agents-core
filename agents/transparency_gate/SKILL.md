# Transparency Gate

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{JURISDICTION_TRANSPARENCY_RULE}}: e.g. "rC19 (BSB Handbook)", "Article 50 (EU AI Act)", "LSRA rules"
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  No other jurisdiction-specific tokens in this skill.
-->

Enforces two gates before any AI-generated content reaches a client or court: the client-disclosure gate and the human-in-the-loop gate. No bulk-execute. No auto-emit.

## Gate 1 — Client Disclosure (Transparency)

Before any client-facing artifact is finalised, the Transparency Gate prompts:

> "Has the client been informed of AI use per {{JURISDICTION_TRANSPARENCY_RULE}}? [y/N]"

- **YES** — logs the confirmation and proceeds
- **NO** — blocks the output; advises the user to obtain client consent before proceeding
- **NOT APPLICABLE** (internal use, non-client-facing) — logs the determination and proceeds

The gate logs: timestamp, matter_id, user response, artifact reference.

## Gate 2 — Human-in-the-Loop

Before any drafting or agentic action executes:

> "This action will [describe what will happen]. The output is AI-generated and must be verified. Proceed? [y/N]"

- **YES** — executes and logs confirmation
- **NO** — cancels the action

This gate fires on:
- Any drafting output (Drafting Assistant)
- Any citation that will be inserted into a filing (Citation Clerk)
- Any compliance determination that will be published (Compliance Officer)
- Any matter modification (Matter Manager)

## No Bulk-Execute / No Auto-Emit

- Every action requires individual confirmation
- No batch processing of multiple matters without per-matter gates
- No scheduled/autonomous actions that bypass the gates

## Output Format

For each gate event, log:
```
Gate: CLIENT_DISCLOSURE | HUMAN_IN_THE_LOOP
Timestamp: <ISO8601>
Matter: <matter_id | null>
Action: <description>
User Response: YES | NO | N/A
Proceeded: true | false
```

## Storage

Gate logs at `~/.ailawfirm_{{COUNTRY_LOWER}}/audit_logs/transparency_gate/`. Never transmitted.
