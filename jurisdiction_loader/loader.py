"""
loader.py — Jurisdiction config loader.

Each firm calls this to load its corpus paths into agents. Reads
~/.ailawfirm_<country>/config.toml and returns paths for statute_corpus,
drafting_corpus, audit_log_dir, and other jurisdiction-specific config.

Usage:
    from jurisdiction_loader import load_config

    config = load_config("uk")
    print(config["paths"]["statute_corpus"])  # ../uk/_statute_corpus/
"""

from pathlib import Path
from typing import Any


def _parse_toml(path: str) -> dict[str, Any]:
    """Minimal TOML parser for config.toml. Avoids external dependency for v0.1."""
    config: dict[str, Any] = {}
    current_section: str | None = None

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
                config[current_section] = {}
            elif "=" in line and current_section is not None:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                config[current_section][key] = value

    return config


def load_config(country: str) -> dict[str, Any]:
    """Load the firm config for a given country code.

    Reads ~/.ailawfirm_<country>/config.toml and returns a structured dict
    with jurisdiction, paths, and llm sections.
    """
    config_path = Path.home() / f".ailawfirm_{country}" / "config.toml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config not found at {config_path}. "
            f"Run './setup.sh' from your firm directory to create it."
        )

    return _parse_toml(str(config_path))


def resolve_placeholders(skill_body: str, config: dict[str, Any]) -> str:
    """Resolve {{JURISDICTION_*}} and {{COUNTRY_*}} placeholders in a skill body.

    Given a SKILL.md body with placeholders and a loaded config dict,
    returns the body with all placeholders substituted.
    """
    jurisdiction = config.get("jurisdiction", {})
    paths = config.get("paths", {})

    replacements = {
        "{{JURISDICTION_CITATION_FORMAT}}": jurisdiction.get("citation_format", ""),
        "{{JURISDICTION_COURT_HIERARCHY}}": jurisdiction.get("court_hierarchy", ""),
        "{{JURISDICTION_BAR_RULES}}": jurisdiction.get("bar_rules", ""),
        "{{JURISDICTION_TIMEZONE}}": jurisdiction.get("timezone", ""),
        "{{JURISDICTION_REGULATOR}}": jurisdiction.get("country", ""),
        "{{JURISDICTION_STATUTE_CORPUS_PATH}}": paths.get("statute_corpus", ""),
        "{{JURISDICTION_DRAFTING_CORPUS_PATH}}": paths.get("drafting_corpus", ""),
        "{{JURISDICTION_AI_CASELAW}}": jurisdiction.get("ai_caselaw", ""),
        "{{JURISDICTION_RISK_RUBRIC}}": jurisdiction.get("risk_rubric", ""),
        "{{JURISDICTION_TRANSPARENCY_RULE}}": jurisdiction.get("transparency_rule", ""),
        "{{JURISDICTION_DIRECT_ACCESS_RULES}}": jurisdiction.get(
            "direct_access_rules", ""
        ),
        "{{COUNTRY_LOWER}}": jurisdiction.get("country", "").lower()
        if jurisdiction.get("country")
        else "",
    }

    result = skill_body
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result
