"""
audit_logger.py — 90-day retention audit logger with ICS export.

Usage:
    from shared.audit_logger import AuditLogger

    logger = AuditLogger(storage_dir="~/.ailawfirm_uk/audit_logs/")
    logger.log(agent="citation_clerk", prompt_summary="validated AIR 1973 SC 1461",
               output_summary="Well-formed, VERIFIED")
    logger.export_ics("2026-05-01", "2026-05-20")
"""

import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional


class AuditLogger:
    """Always-on audit logger. 90-day default retention. ICS/CSV/JSON export."""

    def __init__(self, storage_dir: str, retention_days: int = 90):
        self.storage_dir = Path(storage_dir).expanduser()
        self.retention_days = retention_days
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        agent: str,
        prompt_summary: str,
        output_summary: str,
        session_id: Optional[str] = None,
        matter_id: Optional[str] = None,
        risk_classification: str = "LOW",
        user_confirmed: bool = False,
        citation_verified: Optional[bool] = None,
        transparency_gate_passed: bool = False,
    ) -> str:
        """Append an audit record. Returns the log_id."""
        record = {
            "log_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent,
            "session_id": session_id or "",
            "matter_id": matter_id or "",
            "prompt_summary": prompt_summary,
            "output_summary": output_summary,
            "risk_classification": risk_classification,
            "user_confirmed": user_confirmed,
            "citation_verified": citation_verified,
            "transparency_gate_passed": transparency_gate_passed,
        }
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = self.storage_dir / f"audit_{date_str}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(record) + "\n")
        return record["log_id"]

    def query(
        self, start_date: str, end_date: str, agent: Optional[str] = None
    ) -> list[dict]:
        """Query audit records in a date range, optionally filtered by agent."""
        results: list[dict] = []
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        current = start
        while current <= end:
            log_file = self.storage_dir / f"audit_{current.strftime('%Y-%m-%d')}.jsonl"
            if log_file.exists():
                with open(log_file) as f:
                    for line in f:
                        record = json.loads(line)
                        if agent and record.get("agent") != agent:
                            continue
                        results.append(record)
            current += timedelta(days=1)
        return results

    def export_csv(self, start_date: str, end_date: str, output_path: str) -> str:
        """Export audit records as CSV."""
        import csv

        records = self.query(start_date, end_date)
        with open(output_path, "w", newline="") as f:
            if records:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
        return output_path

    def export_json(self, start_date: str, end_date: str, output_path: str) -> str:
        """Export audit records as JSON array."""
        records = self.query(start_date, end_date)
        with open(output_path, "w") as f:
            json.dump(records, f, indent=2)
        return output_path

    def purge(self) -> int:
        """Enforce retention policy. Delete records older than retention_days. Returns count deleted."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        deleted = 0
        for f in self.storage_dir.glob("audit_*.jsonl"):
            try:
                date_str = f.stem.replace("audit_", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
                if file_date < cutoff:
                    f.unlink()
                    deleted += 1
            except (ValueError, OSError):
                continue
        return deleted

    def stats(self, start_date: str, end_date: str) -> dict:
        """Summary statistics for the date range."""
        records = self.query(start_date, end_date)
        agents = {}
        risks = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for r in records:
            agents[r["agent"]] = agents.get(r["agent"], 0) + 1
            risks[r.get("risk_classification", "LOW")] = (
                risks.get(r.get("risk_classification", "LOW"), 0) + 1
            )
        return {
            "total_queries": len(records),
            "by_agent": agents,
            "by_risk": risks,
            "date_range": f"{start_date} – {end_date}",
        }
