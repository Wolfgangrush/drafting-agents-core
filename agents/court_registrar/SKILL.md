# Court Registrar

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{JURISDICTION_COURT_HIERARCHY}}: path to a JSON map of courts for this jurisdiction
  - {{JURISDICTION_CITATION_FORMAT}}: e.g. "OSCOLA 4th ed." (UK), "ECLI" (EU)
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  No other jurisdiction-specific tokens in this skill.
-->

Knows the court hierarchy for the configured jurisdiction. Say a court name — get back jurisdiction, procedural rules, subject-matter scope, and place in the appellate chain.

## Court Hierarchy

Loaded from `{{JURISDICTION_COURT_HIERARCHY}}` — a JSON map structured as:

```json
{
  "courts": [
    {
      "name": "<court name>",
      "tier": "<apex | appellate | superior | intermediate | first_instance | tribunal>",
      "jurisdiction": "<geographic or subject-matter scope>",
      "appeals_to": "<name of higher court or null if apex>",
      "hears_appeals_from": ["<lower court names>"],
      "subject_matter": ["<categories>"],
      "procedural_rules": "<applicable procedural code/rules>"
    }
  ]
}
```

## Operations

- **lookup**: Given a court name (full or partial), return its full record
- **hierarchy**: Return the full court hierarchy tree from apex down
- **appeal_chain**: Given a lower court, return the full appellate path to the apex
- **subject_matter**: Given a legal domain, return courts with relevant jurisdiction

## Citation Integration

Court names returned by this agent are used by the Citation Clerk for citation validation per `{{JURISDICTION_CITATION_FORMAT}}`.

## Storage

Court hierarchy data is loaded from config at session start. No per-query storage needed.
