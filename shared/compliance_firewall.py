"""
compliance_firewall.py — Pluggable bar-rule firewall.

Checks text against jurisdiction-specific bar rules for advertising/solicitation
risk, confidentiality breaches, and professional-conduct violations.

Usage:
    from shared.compliance_firewall import ComplianceFirewall

    fw = ComplianceFirewall(config_path="~/.ailawfirm_uk/config.toml")
    results = fw.check("Best advocate in London — free consultation!")
    for r in results:
        print(f"{r.risk}: {r.finding}")
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskLevel(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class ComplianceFinding:
    rule: str
    risk: RiskLevel
    finding: str
    recommendation: str


class ComplianceFirewall:
    """Pluggable bar-rule firewall. Loads rules from the firm's config.toml."""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.rules = self._load_rules()

    def _load_rules(self) -> list[dict]:
        """Load bar rules from the jurisdiction's rules file specified in config."""
        # Stub — resolves {{JURISDICTION_BAR_RULES}} from config.toml
        return []

    def check(
        self, text: str, context: Optional[dict] = None
    ) -> list[ComplianceFinding]:
        """Run all loaded rules against the input text. Returns findings sorted by risk."""
        findings: list[ComplianceFinding] = []
        for rule in self.rules:
            result = self._apply_rule(rule, text, context)
            if result:
                findings.append(result)
        findings.sort(
            key=lambda f: [RiskLevel.HIGH, RiskLevel.MEDIUM, RiskLevel.LOW].index(
                f.risk
            )
        )
        return findings

    def _apply_rule(
        self, rule: dict, text: str, context: Optional[dict]
    ) -> Optional[ComplianceFinding]:
        """Apply a single rule pattern against text. Returns a finding if triggered."""
        for pattern in rule.get("patterns", []):
            if pattern.lower() in text.lower():
                return ComplianceFinding(
                    rule=rule["name"],
                    risk=RiskLevel[rule.get("risk", "LOW")],
                    finding=rule.get("finding_template", "").format(match=pattern),
                    recommendation=rule.get("recommendation", ""),
                )
        return None
