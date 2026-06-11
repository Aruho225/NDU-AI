"""Call reports table for the dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.call_analytics import contact_number
from ui.dashboard_layout import section_panel


def render_reports_table(calls: list[dict]) -> None:
    with section_panel("Caller reports", "Who called, direction, status, and duration"):
        if not calls:
            st.caption("No calls to report in this period.")
            return

        rows = []
        for call in calls:
            direction = call.get("direction", "")
            rows.append(
                {
                    "Type": "Inbound" if direction == "inbound" else "Outbound",
                    "Contact": contact_number(call),
                    "Status": call.get("status", "—"),
                    "Duration (s)": call.get("duration_seconds", 0),
                    "When": (call.get("created_at") or "—").replace("T", " ")[:16],
                }
            )
        frame = pd.DataFrame(rows)
        st.dataframe(frame, use_container_width=True, hide_index=True, height=360)
        st.download_button(
            "Download CSV report",
            data=frame.to_csv(index=False).encode("utf-8"),
            file_name="ndu_call_report.csv",
            mime="text/csv",
            use_container_width=True,
            key="dash_report_csv",
        )
