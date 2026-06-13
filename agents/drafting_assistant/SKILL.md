# Drafting Assistant

<!--
  JURISDICTION PLACEHOLDERS — resolved by the firm's config.toml:
  - {{JURISDICTION_STATUTE_CORPUS_PATH}}: path to _statute_corpus/ for this firm
  - {{JURISDICTION_DRAFTING_CORPUS_PATH}}: path to _drafting_data/ for this firm
  - {{JURISDICTION_CITATION_FORMAT}}: e.g. "OSCOLA 4th ed." (UK)
  - {{JURISDICTION_COURT_HIERARCHY}}: path to a JSON map of courts
  - {{COUNTRY_LOWER}}: e.g. "uk", "eu", "singapore"
  No other jurisdiction-specific tokens in this skill.
-->

Connects to the wolfgang_rush drafting plugins (separate, MIT, optional). v0.1 = connection layer. v0.2+ = real templates per jurisdiction.

## Plugin Connection

The Drafting Assistant interfaces with wolfgang_rush drafting plugins. Plugins are installed separately and are jurisdiction-specific. This agent provides the connection layer — it routes drafting requests to the appropriate plugin and returns results.

## Operations (v0.1)

- **connect**: Verify the drafting plugin is installed and reachable
- **list_templates**: Return available templates for this jurisdiction
- **status**: Report plugin version, available templates, last update

## Operations (v0.2+ roadmap)

- **draft**: Generate a first draft from a template + matter context
- **review**: Check a draft against statutory requirements from `{{JURISDICTION_STATUTE_CORPUS_PATH}}`
- **format**: Apply `{{JURISDICTION_CITATION_FORMAT}}` and court-specific formatting from `{{JURISDICTION_DRAFTING_CORPUS_PATH}}`

## Human-in-the-Loop

Every drafting output requires explicit user confirmation before it can be finalised. The Transparency Gate must fire before any draft reaches a client. No bulk-execute. No auto-emit.

## Storage

Draft versions at `~/.ailawfirm_{{COUNTRY_LOWER}}/matters/<matter_id>/drafts/`. Never transmitted.
