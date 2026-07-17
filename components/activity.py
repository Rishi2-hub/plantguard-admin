import html

import streamlit as st


def recent_activity() -> None:
    activities = [
        {
            "icon": "🌿",
            "background": "#DCFCE7",
            "title": "Treatment Updated",
            "description": "Tomato Late Blight dosage was updated.",
            "time": "2 min ago",
        },
        {
            "icon": "👨‍🌾",
            "background": "#DBEAFE",
            "title": "New Farmer Registered",
            "description": "Ram Bahadur joined PlantGuard.",
            "time": "18 min ago",
        },
        {
            "icon": "⚠️",
            "background": "#FEF3C7",
            "title": "Disease Alert",
            "description": "Multiple Late Blight cases were detected.",
            "time": "1 hr ago",
        },
        {
            "icon": "🔒",
            "background": "#FEE2E2",
            "title": "Failed Login Attempt",
            "description": "An invalid admin login was detected.",
            "time": "2 hrs ago",
        },
    ]

    rows = ""

    for activity in activities:
        rows += f"""
<div class="activity-item">
    <div
        class="activity-icon"
        style="background:{activity['background']};"
    >
        {activity['icon']}
    </div>

    <div class="activity-content">
        <div class="activity-title">
            {html.escape(activity['title'])}
        </div>

        <div class="activity-description">
            {html.escape(activity['description'])}
        </div>
    </div>

    <div class="activity-time">
        {html.escape(activity['time'])}
    </div>
</div>
"""

    st.html(
        f"""
<div class="dashboard-panel">
    <div class="panel-header">
        <div>
            <div class="panel-title">
                Recent Activity
            </div>

            <div class="panel-subtitle">
                Latest PlantGuard system activity
            </div>
        </div>

        <div class="panel-action">
            View All
        </div>
    </div>

    <div class="activity-list">
        {rows}
    </div>
</div>
"""
    )