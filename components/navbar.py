import html
from datetime import datetime

import streamlit as st


PAGE_DESCRIPTIONS = {
    "Dashboard": "Monitor PlantGuard activity and system performance.",
    "Treatments": "Manage plant disease treatments and dosage records.",
    "Farmers": "View and manage registered farmer accounts.",
    "Audit Logs": "Review security events and administrative activity.",
    "Add Admin": "Create a new administrator account.",
    "Settings": "Manage administrator preferences and security.",
}


def navbar(current_page: str) -> None:
    admin_name = st.session_state.get(
        "admin_name",
        "Administrator",
    )

    first_name = (
        str(admin_name).split()[0]
        if admin_name
        else "Admin"
    )

    today = datetime.now().strftime(
        "%A, %d %B %Y"
    )

    description = PAGE_DESCRIPTIONS.get(
        current_page,
        "PlantGuard Admin Console",
    )

    st.html(
        f"""
<div class="dashboard-navbar">
    <div class="navbar-left">
        <div class="dashboard-title">
            {html.escape(current_page)}
        </div>

        <div class="dashboard-subtitle">
            {html.escape(description)}
        </div>
    </div>

    <div class="navbar-right">
        <div class="date-card">
            📅 {html.escape(today)}
        </div>

        <div class="admin-badge">
            👤 {html.escape(first_name)}
        </div>
    </div>
</div>
"""
    )