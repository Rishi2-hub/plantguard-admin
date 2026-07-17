import pandas as pd
import streamlit as st


def initialize_audit_logs() -> None:
    if "audit_logs_data" not in st.session_state:
        st.session_state.audit_logs_data = [
            {
                "id": 1,
                "event": "Treatment Updated",
                "user": "Ritik Budhathoki",
                "ip_address": "192.168.1.10",
                "detail": "Updated Tomato Late Blight dosage",
                "timestamp": "2026-07-11 18:35",
                "level": "Info",
            },
            {
                "id": 2,
                "event": "Failed Login",
                "user": "Unknown",
                "ip_address": "103.22.45.12",
                "detail": "Invalid administrator credentials",
                "timestamp": "2026-07-11 16:48",
                "level": "Danger",
            },
            {
                "id": 3,
                "event": "Farmer Deactivated",
                "user": "Ritik Budhathoki",
                "ip_address": "192.168.1.10",
                "detail": "Deactivated farmer Hari Prasad",
                "timestamp": "2026-07-11 15:30",
                "level": "Warning",
            },
            {
                "id": 4,
                "event": "Admin Created",
                "user": "Super Admin",
                "ip_address": "192.168.1.10",
                "detail": "Created a new administrator account",
                "timestamp": "2026-07-11 14:15",
                "level": "Success",
            },
            {
                "id": 5,
                "event": "Farmer Registered",
                "user": "System",
                "ip_address": "192.168.1.20",
                "detail": "New farmer Sita Maya registered",
                "timestamp": "2026-07-11 13:05",
                "level": "Info",
            },
            {
                "id": 6,
                "event": "Rate Limit Triggered",
                "user": "System",
                "ip_address": "103.22.45.12",
                "detail": "Too many requests from the same IP address",
                "timestamp": "2026-07-11 12:40",
                "level": "Warning",
            },
        ]


def audit_logs_page() -> None:
    initialize_audit_logs()

    st.html(
        """
<div class="page-heading">
    <div>
        <div class="page-title">Audit Logs</div>
        <div class="page-subtitle">
            Review administrative activity, login events, and security records.
        </div>
    </div>

    <div class="page-badge">
        📜 Read-Only Records
    </div>
</div>
"""
    )

    logs = pd.DataFrame(
        st.session_state.audit_logs_data
    )

    search_col, event_col, level_col = st.columns(
        [2, 1, 1],
        gap="medium",
    )

    with search_col:
        search_text = st.text_input(
            "Search audit logs",
            placeholder="Search event, user, IP address, or detail...",
        )

    with event_col:
        event_options = ["All"] + sorted(
            logs["event"].unique().tolist()
        )

        event_filter = st.selectbox(
            "Event",
            event_options,
        )

    with level_col:
        level_filter = st.selectbox(
            "Level",
            [
                "All",
                "Info",
                "Success",
                "Warning",
                "Danger",
            ],
        )

    filtered = logs.copy()

    if search_text.strip():
        search_value = search_text.strip().lower()

        filtered = filtered[
            filtered.apply(
                lambda row: search_value
                in " ".join(row.astype(str)).lower(),
                axis=1,
            )
        ]

    if event_filter != "All":
        filtered = filtered[
            filtered["event"] == event_filter
        ]

    if level_filter != "All":
        filtered = filtered[
            filtered["level"] == level_filter
        ]

    total_logs = len(logs)

    warning_count = len(
        logs[logs["level"] == "Warning"]
    )

    danger_count = len(
        logs[logs["level"] == "Danger"]
    )

    summary1, summary2, summary3 = st.columns(
        3,
        gap="medium",
    )

    with summary1:
        st.html(
            f"""
<div class="summary-card">
    <div class="summary-icon summary-blue">📜</div>

    <div>
        <div class="summary-label">Total Logs</div>
        <div class="summary-value">{total_logs}</div>
    </div>
</div>
"""
        )

    with summary2:
        st.html(
            f"""
<div class="summary-card">
    <div class="summary-icon summary-warning">⚠</div>

    <div>
        <div class="summary-label">Warnings</div>
        <div class="summary-value">{warning_count}</div>
    </div>
</div>
"""
        )

    with summary3:
        st.html(
            f"""
<div class="summary-card">
    <div class="summary-icon summary-red">🚨</div>

    <div>
        <div class="summary-label">Security Alerts</div>
        <div class="summary-value">{danger_count}</div>
    </div>
</div>
"""
        )

    st.html(
        """
<div class="section-panel-heading">
    <div class="panel-title">System Activity</div>
    <div class="panel-subtitle">
        The newest records appear first.
    </div>
</div>
"""
    )

    icon_map = {
        "Info": "ℹ️",
        "Success": "✅",
        "Warning": "⚠️",
        "Danger": "🚨",
    }

    display_data = filtered.copy()

    display_data["icon"] = display_data["level"].map(
        icon_map
    )

    display_data = display_data[
        [
            "icon",
            "event",
            "user",
            "ip_address",
            "detail",
            "timestamp",
            "level",
        ]
    ].rename(
        columns={
            "icon": "",
            "event": "Event",
            "user": "User",
            "ip_address": "IP Address",
            "detail": "Detail",
            "timestamp": "Timestamp",
            "level": "Level",
        }
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
    )

    if filtered.empty:
        st.warning(
            "No audit logs match the selected filters."
        )

    st.html(
        """
<div class="audit-info-card">
    <div class="audit-info-icon">🔒</div>

    <div>
        <div class="audit-info-title">
            Audit records are read-only
        </div>

        <div class="audit-info-text">
            Administrative and security logs cannot be edited or deleted from this panel.
        </div>
    </div>
</div>
"""
    )