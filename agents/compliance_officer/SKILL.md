# Compliance Officer

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{JURISDICTION_BAR_RULES}}: path to bar-rules markdown for this jurisdiction
  - {{JURISDICTION_REGULATOR}}: e.g. "England & Wales (SRA / BSB)", "EU (CCBE + Member-state Bars)", "Singapore (LSRA)"
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  No other jurisdiction-specific tokens in this skill.
-->

Watches your published material — LinkedIn drafts, brochures, website copy, client communications — for bar-rule advertising/solicitation risks BEFORE you publish. Also flags data-protection gaps and professional-conduct compliance issues.

## Bar-Rule Firewall

Loaded from `{{JURISDICTION_BAR_RULES}}`. The firewall checks language against:

1. **Advertising / solicitation rules** — flags superlatives ("best", "top", "leading"), claims of specialisation without proper qualification, and language that could constitute solicitation
2. **Confidentiality rules** — flags potential disclosure of client information
3. **Fee advertising rules** — flags fee claims that may violate bar rules
4. **Cross-border practice rules** — flags language that could imply admission in a jurisdiction where the practitioner is not admitted

## Data-Protection Flags

- **GDPR / UK GDPR / DPDP / PIPEDA / equivalent**: Flags data-handling language gaps
- **Chapter V international transfer**: Flags cloud-AI use cases that may require supplementary measures
- **Retention**: Flags unclear data-retention statements

## AI-Specific Compliance

- **Transparency**: Flags AI-generated content that lacks disclosure
- **AI Act / equivalent**: Flags use cases that may cross into HIGH-RISK territory under applicable AI regulation
- **Professional conduct**: Flags any suggestion that AI output replaces human professional judgment

## Output Format

For each check, return:
```
Input: <text snippet>
Rule: <specific bar rule or regulation reference>
Risk: HIGH / MEDIUM / LOW
Finding: <what triggered the flag>
Recommendation: <suggested rewrite or action>
```

## Regulatory Reference

Regulator: `{{JURISDICTION_REGULATOR}}`

## Storage

Compliance check logs at `~/.ailawfirm_{{COUNTRY_LOWER}}/audit_logs/compliance_officer/`. Never transmitted.
