# Knowledge Provenance

One section per agent — what jurisdiction sources back the agent's logic and what's been generalized away.

## Receptionist
- **Source:** Intent-classification patterns from UK + EU firm v0.1 README specialist tables
- **Generalized:** No jurisdiction-specific content in the classifier itself — routing is jurisdiction-agnostic

## Matter Manager
- **Source:** Matter-management patterns common across common-law and civil-law jurisdictions
- **Generalized:** Party naming conventions, prayer formats, hearing-date formats — all via `{{JURISDICTION_*}}` placeholders

## Citation Clerk
- **Source:** UK OSCOLA 4th ed. + EU ECLI format + Singapore neutral citations + Australian AGLC + Dubai-DIFC court references + US Bluebook/neutral
- **Generalized:** Citation format is `{{JURISDICTION_CITATION_FORMAT}}` — pluggable per firm config.toml

## Court Registrar
- **Source:** UK court hierarchy (UKSC · EWCA · EWHC divisions · Crown · County · Magistrates · Tribunals · Scottish + NI courts) · EU (CJEU · ECtHR · national supreme/constitutional courts) · and equivalent for SG/AU/DIFC/US
- **Generalized:** Court hierarchy is `{{JURISDICTION_COURT_HIERARCHY}}` — JSON map per jurisdiction

## Drafting Assistant
- **Source:** Wolfgang_rush plugin family connection patterns
- **Generalized:** Plugin connection is jurisdiction-agnostic; template formats use `{{JURISDICTION_*}}`

## Compliance Officer
- **Source:** BSB Handbook (UK) · CCBE Code of Conduct (EU) · LSRA rules (Singapore) · state Bar associations (Australia) · DIFC/DFSA (Dubai) · state Bar associations (USA)
- **Generalized:** Bar rules are `{{JURISDICTION_BAR_RULES}}` — pluggable per firm config.toml

## Risk Assessor
- **Source:** BSB 3×3 risk matrix (application × use × technology) — pattern generalized for any jurisdiction's risk rubric
- **Generalized:** Risk rubric is `{{JURISDICTION_RISK_RUBRIC}}`

## Audit Clerk
- **Source:** 90-day retention pattern from EU firm · ICS export
- **Generalized:** Retention period and log format are jurisdiction-agnostic

## Transparency Gate
- **Source:** rC19 (BSB) client-disclosure gate · Article 50 (EU AI Act) transparency
- **Generalized:** Disclosure prompt is `{{JURISDICTION_TRANSPARENCY_RULE}}`

## Direct Access Detector
- **Source:** Public Access scheme rules (UK) · direct-access equivalents in other jurisdictions
- **Generalized:** Trigger conditions are `{{JURISDICTION_DIRECT_ACCESS_RULES}}`

## Calendar Sync
- **Source:** ICS feed pattern · timezone handling
- **Generalized:** Timezone is `{{JURISDICTION_TIMEZONE}}`
