# Direct Access Detector

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{JURISDICTION_DIRECT_ACCESS_RULES}}: e.g. "Public Access scheme (BSB rC123)", "Direct Access (state Bar rules)"
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  No other jurisdiction-specific tokens in this skill.
-->

Detects when a matter involves Public Access / Direct Access schemes and triggers jurisdiction-specific safeguards before AI is used.

## Trigger Conditions

A matter is flagged as Direct Access when:
1. The matter's metadata includes `access_type: "public_access" | "direct_access"`
2. The user describes a client relationship without a solicitor intermediary
3. The matter involves a lay client who has approached the barrister/advocate directly

## Protocol on Trigger

When a Direct Access matter is detected:

1. **Confirm client understanding**: The system prompts:
   > "This matter appears to involve Direct Access / Public Access. Has the client been informed of AI use in accordance with {{JURISDICTION_DIRECT_ACCESS_RULES}}? [y/N]"

2. **Enhanced risk classification**: Direct Access matters are automatically elevated by one tier in the Risk Assessor matrix (A→B, B→C)

3. **Additional transparency**: All outputs in Direct Access matters carry an additional disclosure note

4. **No delegation**: The human-in-the-loop gate cannot be bypassed for Direct Access matters — every AI-assisted action requires explicit confirmation

## Jurisdiction-Specific Rules

Loaded from `{{JURISDICTION_DIRECT_ACCESS_RULES}}`. Each jurisdiction defines:
- Whether Direct Access / Public Access is permitted
- What additional disclosures are required when AI is used
- Whether client consent must be in writing
- Any restrictions on AI use in Direct Access matters

## Storage

Direct Access determinations logged at `~/.ailawfirm_{{COUNTRY_LOWER}}/audit_logs/direct_access_detector/`. Never transmitted.
