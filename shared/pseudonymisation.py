"""
pseudonymisation.py — Interface for the PII pseudonymisation gateway.

This module defines the interface that agents use to pseudonymise PII before
any cloud-API call. The actual gateway implementation lives in a separate repo
(github.com/Wolfgangrush/pseudonymisation-gateway). This interface allows
agents to call pseudonymisation without hard-coding the gateway implementation.

Usage:
    from shared.pseudonymisation import Pseudonymiser

    p = Pseudonymiser(jurisdiction="uk")
    safe_text = p.pseudonymise("Client John Smith's NIN is AB123456C")
    # → "Client [NAME_01]'s NIN is [UK_NIN_01]"
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PseudonymisationResult:
    original: str
    pseudonymised: str
    map_entries: dict[str, str]  # {token: pseudonym} for reconstruction
    jurisdiction: str


class PseudonymiserInterface(ABC):
    """Abstract interface for PII pseudonymisation. Implementations live in
    the pseudonymisation-gateway repo (separate, MIT)."""

    @abstractmethod
    def pseudonymise(self, text: str) -> PseudonymisationResult: ...

    @abstractmethod
    def reveal(self, text: str, map_entries: dict[str, str]) -> str: ...


class Pseudonymiser(PseudonymiserInterface):
    """Default pseudonymiser — delegates to the gateway implementation.

    v0.1: Stub implementation. Loads the gateway module if installed.
    v0.2+: Direct integration with pseudonymisation-gateway Python package.
    """

    def __init__(self, jurisdiction: str):
        self.jurisdiction = jurisdiction
        self._gateway = self._load_gateway()

    def _load_gateway(self):
        """Attempt to load the pseudonymisation-gateway module."""
        try:
            # The gateway is a separate MIT-licensed repo.
            # It may or may not be installed alongside drafting-agents-core.
            import importlib

            return importlib.import_module("pseudonymisation_gateway")
        except ImportError:
            return None

    def pseudonymise(self, text: str) -> PseudonymisationResult:
        if self._gateway:
            return self._gateway.pseudonymise(text, jurisdiction=self.jurisdiction)
        # Stub: no-op (text passes through unmodified)
        return PseudonymisationResult(
            original=text,
            pseudonymised=text,
            map_entries={},
            jurisdiction=self.jurisdiction,
        )

    def reveal(self, text: str, map_entries: dict[str, str]) -> str:
        if self._gateway:
            return self._gateway.reveal(text, map_entries)
        return text
