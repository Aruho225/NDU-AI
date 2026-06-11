"""Call statistics and chart data for the dashboard."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from typing import Any, Optional

from ui.call_store import load_calls_in_range

SUCCESS_STATUSES = frozenset({"completed"})
FAILED_STATUSES = frozenset({"failed", "busy", "no-answer", "canceled"})


def classify_outcome(status: str) -> str:
    key = (status or "").lower()
    if key in SUCCESS_STATUSES:
        return "successful"
    if key in FAILED_STATUSES:
        return "failed"
    return "other"


def contact_number(call: dict[str, Any]) -> str:
    if call.get("direction") == "inbound":
        return call.get("from_number") or "Unknown"
    return call.get("to_number") or "Unknown"


def load_dashboard_calls(
    user_id: Optional[int],
    start: date,
    end: date,
) -> list[dict[str, Any]]:
    return load_calls_in_range(
        user_id=user_id,
        start_date=start.isoformat(),
        end_date=end.isoformat(),
        limit=500,
    )


def summarize_calls(calls: list[dict[str, Any]]) -> dict[str, Any]:
    inbound = [c for c in calls if c.get("direction") == "inbound"]
    outbound = [c for c in calls if c.get("direction") == "outbound"]
    successful = [c for c in calls if classify_outcome(c.get("status", "")) == "successful"]
    failed = [c for c in calls if classify_outcome(c.get("status", "")) == "failed"]
    durations = [int(c.get("duration_seconds") or 0) for c in successful]
    avg_duration = round(sum(durations) / len(durations), 1) if durations else 0
    total_minutes = round(sum(durations) / 60, 1)
    return {
        "total": len(calls),
        "inbound": len(inbound),
        "outbound": len(outbound),
        "successful": len(successful),
        "failed": len(failed),
        "with_recording": sum(1 for c in calls if c.get("recording_url")),
        "avg_duration_sec": avg_duration,
        "total_talk_minutes": total_minutes,
        "success_rate": round(len(successful) / len(calls) * 100, 1) if calls else 0,
    }


def daily_series(calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, dict[str, int]] = defaultdict(
        lambda: {"inbound": 0, "outbound": 0, "successful": 0, "failed": 0}
    )
    for call in calls:
        raw = (call.get("created_at") or "")[:10]
        if not raw:
            continue
        day = buckets[raw]
        direction = call.get("direction", "")
        if direction == "inbound":
            day["inbound"] += 1
        elif direction == "outbound":
            day["outbound"] += 1
        outcome = classify_outcome(call.get("status", ""))
        if outcome == "successful":
            day["successful"] += 1
        elif outcome == "failed":
            day["failed"] += 1
    return [{"date": key, **value} for key, value in sorted(buckets.items())]


def default_date_range() -> tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=30)
    return start, end


def parse_dates(start_value: date, end_value: date) -> tuple[date, date]:
    if start_value > end_value:
        return end_value, start_value
    return start_value, end_value
