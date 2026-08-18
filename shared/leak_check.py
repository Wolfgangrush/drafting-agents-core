"""
leak_check.py — Cross-layer leak detection and boundary enforcement.

Checks output for internal paths, personal identifiers, AAAK codes, and other
sensitive tokens that should never leave the local environment.

Usage:
    from shared.leak_check import LeakCheck

    lc = LeakCheck()
    hits = lc.scan("some text that might contain ~/Desktop/mempalace/...")
    if hits:
        raise LeakError(f"Leak detected: {hits}")
"""

import re
from typing import Optional


class LeakError(Exception):
    pass


class LeakCheck:
    """Cross-layer boundary enforcement. Prevents internal data from leaking into outputs."""

    # Patterns that must never appear in any output destined for GitHub or APIs
    FORBIDDEN_PATTERNS: list[tuple[str, str]] = [
        # Palace / internal paths
        ("PALACE_PATH", r"~?/?(\.localstore|Desktop/localstore)"),
        ("CLAUDE_PROJECTS", r"~/\.claude/projects"),
        # AAAK personal code leak (word-boundary match)
        (
            "AAAK_CODE",
            r"\b(CMA|MRO|VJP|CK|SAM|GAG|HCFR|PK|MVA|RSH|GAR|APK|GMA|ATR|YCN|CYW)\b",
        ),
        # Real names / personal email
        ("REAL_NAME", r"(?i)(rushikesh|mahajan)"),
        ("PERSONAL_EMAIL", r"(?i)@gmail\.com"),
        ("NAGPUR_REFERENCE", r"(?i)(nagpur|bombay\s*high)"),
    ]

    def scan(
        self, text: str, extra_patterns: Optional[list[tuple[str, str]]] = None
    ) -> list[tuple[str, str]]:
        """Scan text for forbidden patterns. Returns list of (pattern_label, match) tuples."""
        patterns = self.FORBIDDEN_PATTERNS + (extra_patterns or [])
        hits: list[tuple[str, str]] = []
        for label, pattern in patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                hits.append((label, str(m)))
        return hits

    def scan_files(
        self, root_dir: str, exclude_dirs: Optional[list[str]] = None
    ) -> list[tuple[str, str, str]]:
        """Recursively scan all text files in root_dir. Returns (file, label, match) tuples."""
        from pathlib import Path

        exclude = set(exclude_dirs or [])
        hits: list[tuple[str, str, str]] = []
        root = Path(root_dir)

        for path in root.rglob("*"):
            if path.is_file() and not any(p in exclude for p in path.parts):
                try:
                    content = path.read_text()
                    for label, match in self.scan(content):
                        hits.append((str(path), label, match))
                except (UnicodeDecodeError, OSError):
                    continue
        return hits

    @staticmethod
    def assert_clean(text: str, context: str = "") -> None:
        """Scan and raise LeakError if any forbidden pattern is found."""
        lc = LeakCheck()
        hits = lc.scan(text)
        if hits:
            labels = [h[0] for h in hits]
            raise LeakError(f"Leak detected in {context}: {labels}")
