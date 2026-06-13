"""
declaration_emitter.py — Jurisdiction-specific AI-use declaration generator.

Emits a parallel declaration artifact alongside any AI-assisted draft, in the
format required by the matter's jurisdiction. Companion to the transparency_gate
SKILL — invoked AFTER Gate 1 (Client Disclosure) returns YES.

Supported jurisdictions (v0.1):
    - IN-SC-Reg43-2026  — India · Supreme Court · Regulation 43(3) declaration

Planned (v0.2):
    - US-ABA-Op512-Client-Consent       — ABA Formal Op 512, Mod Rule 1.4
    - US-FedCourt-AI-Certification      — federal court standing-order AI cert
    - UK-BSB-rC19                       — BSB Handbook rC19 client disclosure
    - EU-AIAct-Art50                    — EU AI Act Art 50 transparency
    - SG-LSRA / AU-FedCourt / DIFC      — to follow

Pipeline:
    matter_metadata
        ↓
    load jurisdiction config (./<firm>/_declarations/<code>.config.yaml)
        ↓
    load template (./<firm>/_declarations/<code>.template.md)
        ↓
    substitute placeholders
        ↓
    render to .docx (pandoc shell-out preferred; python-docx fallback)
        ↓
    emit .conformance.json manifest alongside .docx
        ↓
    log emission event to ~/.ailawfirm_<country>/audit_logs/transparency_gate/
        ↓
    return paths

Usage from a drafter agent:

    from agents.transparency_gate.declaration_emitter import emit_declaration

    artifact = emit_declaration(
        jurisdiction_code="IN-SC-Reg43-2026",
        firm_path=Path("~/Desktop/AIO/lawtech-resources/ai-law-firm/india"),
        matter_metadata={
            "COURT_NAME": "Hon'ble High Courts of India",
            "CASE_NUMBER": "Writ Petition No. ____ of 2026",
            ...
        },
        output_dir=Path("./out/matter-XYZ/"),
    )

    print(artifact.declaration_docx_path)
    print(artifact.conformance_manifest_path)
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

WRCS_AILF_VERSION = "0.1"
DRAFTING_AGENTS_CORE_VERSION = "0.1"
TEMPLATE_VERSION_PATTERN = re.compile(r"\{\{([A-Z_][A-Z0-9_]*)\}\}")


@dataclass
class DeclarationArtifact:
    """Paths and metadata returned by emit_declaration()."""

    jurisdiction_code: str
    declaration_md_path: Path
    declaration_docx_path: Path
    conformance_manifest_path: Path
    audit_log_path: Path
    generated_at: str
    wrcs_ailf_level: int
    template_version: str
    unresolved_placeholders: list[str] = field(default_factory=list)


def _parse_yaml_min(path: Path) -> dict[str, Any]:
    """Minimal YAML reader — uses PyYAML if installed, else a flat-key fallback.

    The config.yaml shape is structured enough that a real YAML parser is
    preferred; this fallback keeps the module import-clean on a vanilla
    Python install for the v0.1 stub.
    """
    try:
        import yaml  # type: ignore[import-not-found]

        with path.open() as f:
            return yaml.safe_load(f)
    except ImportError:
        logger.warning("PyYAML not installed; using shallow fallback parser.")
        config: dict[str, Any] = {}
        current_top: str | None = None
        with path.open() as f:
            for raw in f:
                line = raw.rstrip()
                if not line or line.lstrip().startswith("#"):
                    continue
                if not line.startswith(" ") and ":" in line:
                    key, _, value = line.partition(":")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if value:
                        config[key] = value
                        current_top = None
                    else:
                        config[key] = {}
                        current_top = key
        return config


def _load_jurisdiction_config(firm_path: Path, jurisdiction_code: str) -> dict[str, Any]:
    """Load the per-jurisdiction declaration config from the firm's _declarations dir."""
    config_path = firm_path / "_declarations" / f"{jurisdiction_code}.config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(
            f"Declaration config not found: {config_path}\n"
            f"Available jurisdictions for this firm: "
            f"{[p.stem.replace('.config', '') for p in (firm_path / '_declarations').glob('*.config.yaml')]}"
        )
    return _parse_yaml_min(config_path)


def _load_template(firm_path: Path, jurisdiction_code: str) -> str:
    """Load the declaration template markdown body."""
    template_path = firm_path / "_declarations" / f"{jurisdiction_code}.template.md"
    if not template_path.exists():
        raise FileNotFoundError(f"Declaration template not found: {template_path}")
    return template_path.read_text()


def _substitute_placeholders(
    template_body: str, matter_metadata: dict[str, str]
) -> tuple[str, list[str]]:
    """Replace {{PLACEHOLDER}} tokens with matter_metadata values.

    Returns (rendered_body, list_of_unresolved_placeholders).
    Unresolved placeholders are left intact in the body for visibility,
    NOT silently swapped for empty strings — that hides errors.
    """
    unresolved: list[str] = []

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in matter_metadata:
            return str(matter_metadata[key])
        unresolved.append(key)
        return match.group(0)

    rendered = TEMPLATE_VERSION_PATTERN.sub(replace, template_body)
    return rendered, sorted(set(unresolved))


def _render_md_to_docx(md_body: str, out_path: Path) -> None:
    """Render markdown body to .docx. Prefers pandoc; falls back to a warning.

    The fallback writes a .md file alongside if pandoc is unavailable, so the
    pipeline does not silently lose the artifact.
    """
    md_intermediate = out_path.with_suffix(".md")
    md_intermediate.write_text(md_body)

    if shutil.which("pandoc") is None:
        logger.warning(
            "pandoc not found on PATH — .docx not rendered. .md written at %s",
            md_intermediate,
        )
        return

    subprocess.run(
        ["pandoc", str(md_intermediate), "-o", str(out_path), "--from=markdown", "--to=docx"],
        check=True,
    )


def _compute_sha256(path: Path) -> str:
    """SHA-256 of a file, hex-encoded."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_conformance_manifest(
    jurisdiction_code: str,
    config: dict[str, Any],
    declaration_docx_path: Path,
    matter_metadata: dict[str, str],
    generated_at: str,
) -> dict[str, Any]:
    """Construct the wolfgang_rush AI Law Firm conformance manifest.

    Manifest is filed alongside every emitted declaration. Public registry of
    third-party firms' manifests lives at Wolfgangrush/ailf-conformance-standard.
    """
    return {
        "$schema": "https://raw.githubusercontent.com/Wolfgangrush/ailf-conformance-standard/main/MANIFEST.schema.json",
        "manifest_version": WRCS_AILF_VERSION,
        "jurisdiction_code": jurisdiction_code,
        "wrcs_ailf_level": int(config.get("conformance", {}).get("wrcs_ailf_minimum_level", 1))
        if isinstance(config.get("conformance"), dict)
        else 1,
        "drafting_agents_core_version": DRAFTING_AGENTS_CORE_VERSION,
        "generated_at": generated_at,
        "matter": {
            "court": matter_metadata.get("COURT_NAME", ""),
            "case_number": matter_metadata.get("CASE_NUMBER", ""),
            "filing_party": matter_metadata.get("PARTY_FILER_NAME", ""),
            "filing_date": matter_metadata.get("FILING_DATE", ""),
        },
        "ai_tool": {
            "name": matter_metadata.get("AI_TOOL_NAME", ""),
            "version": matter_metadata.get("AI_TOOL_VERSION", ""),
            "provider": matter_metadata.get("AI_TOOL_PROVIDER", ""),
            "deployment_mode": matter_metadata.get("AI_TOOL_DEPLOYMENT_MODE", ""),
            "privacy_primitive": matter_metadata.get("PRIVACY_PRIMITIVE", ""),
        },
        "declaration_artifact": {
            "path": str(declaration_docx_path),
            "sha256": _compute_sha256(declaration_docx_path)
            if declaration_docx_path.exists()
            else "",
        },
        "publisher": {
            "organisation": "wolfgang_rush",
            "license": "MIT",
            "repository": "github.com/Wolfgangrush",
        },
    }


def _write_audit_log(
    firm_country_lower: str, jurisdiction_code: str, artifact: DeclarationArtifact
) -> Path:
    """Append the emission event to the firm's transparency_gate audit log."""
    audit_dir = Path.home() / f".ailawfirm_{firm_country_lower}" / "audit_logs" / "transparency_gate"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_path = audit_dir / "declaration_emissions.jsonl"
    entry = {
        "event": "DECLARATION_EMITTED",
        "timestamp": artifact.generated_at,
        "jurisdiction_code": jurisdiction_code,
        "declaration_docx_path": str(artifact.declaration_docx_path),
        "conformance_manifest_path": str(artifact.conformance_manifest_path),
        "wrcs_ailf_level": artifact.wrcs_ailf_level,
        "unresolved_placeholders": artifact.unresolved_placeholders,
    }
    with audit_path.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return audit_path


def emit_declaration(
    jurisdiction_code: str,
    firm_path: Path,
    matter_metadata: dict[str, str],
    output_dir: Path,
) -> DeclarationArtifact:
    """Emit a jurisdiction-specific declaration alongside an AI-assisted draft.

    Args:
        jurisdiction_code: e.g. "IN-SC-Reg43-2026"
        firm_path: path to the AI law firm root (e.g. .../ai-law-firm/india)
        matter_metadata: mapping of template placeholders to values
        output_dir: directory where declaration .docx + manifest .json land

    Returns:
        DeclarationArtifact with paths to every emitted file.

    Raises:
        FileNotFoundError: if the jurisdiction config or template is missing.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    config = _load_jurisdiction_config(firm_path, jurisdiction_code)
    template_body = _load_template(firm_path, jurisdiction_code)

    generated_at = datetime.now(timezone.utc).isoformat()
    matter_metadata = {
        **matter_metadata,
        "GENERATED_AT_ISO": generated_at,
        "DRAFTING_AGENTS_CORE_VERSION": DRAFTING_AGENTS_CORE_VERSION,
        "WRCS_AILF_LEVEL": str(matter_metadata.get("WRCS_AILF_LEVEL", "1")),
    }

    rendered_body, unresolved = _substitute_placeholders(template_body, matter_metadata)

    safe_code = jurisdiction_code.lower().replace("-", "_")
    declaration_md_path = output_dir / f"declaration_{safe_code}.md"
    declaration_docx_path = output_dir / f"declaration_{safe_code}.docx"
    conformance_manifest_path = output_dir / f"declaration_{safe_code}.conformance.json"

    declaration_md_path.write_text(rendered_body)
    _render_md_to_docx(rendered_body, declaration_docx_path)

    manifest = _build_conformance_manifest(
        jurisdiction_code=jurisdiction_code,
        config=config,
        declaration_docx_path=declaration_docx_path,
        matter_metadata=matter_metadata,
        generated_at=generated_at,
    )
    manifest["unresolved_placeholders"] = unresolved
    conformance_manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    manifest_sha = _compute_sha256(conformance_manifest_path)

    # Patch the manifest SHA into the rendered .md/.docx footer if it was
    # unresolved at render time. Stable second pass — only writes if changed.
    if "CONFORMANCE_MANIFEST_SHA256" in unresolved:
        patched_body = rendered_body.replace(
            "{{CONFORMANCE_MANIFEST_SHA256}}", manifest_sha
        )
        declaration_md_path.write_text(patched_body)
        _render_md_to_docx(patched_body, declaration_docx_path)
        unresolved = [p for p in unresolved if p != "CONFORMANCE_MANIFEST_SHA256"]

    country_lower = str(config.get("country", "india")).lower()
    artifact = DeclarationArtifact(
        jurisdiction_code=jurisdiction_code,
        declaration_md_path=declaration_md_path,
        declaration_docx_path=declaration_docx_path,
        conformance_manifest_path=conformance_manifest_path,
        audit_log_path=Path(),  # filled in below
        generated_at=generated_at,
        wrcs_ailf_level=manifest["wrcs_ailf_level"],
        template_version="IN-SC-Reg43-2026 v0.1",
        unresolved_placeholders=unresolved,
    )
    artifact.audit_log_path = _write_audit_log(country_lower, jurisdiction_code, artifact)
    return artifact
