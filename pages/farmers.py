import html

import pandas as pd
import streamlit as st


def initialize_farmers() -> None:
    """Create temporary farmer records for UI testing."""

    if "farmers_data" not in st.session_state:
        st.session_state.farmers_data = [
            {
                "id": 1,
                "name": "Ram Bahadur",
                "email": "ram@farm.com",
                "joined": "Jun 1, 2026",
                "language": "EN",
                "status": "Active",
            },
            {
                "id": 2,
                "name": "Sujan Thapa",
                "email": "sujan@gmail.com",
                "joined": "Jun 22, 2026",
                "language": "NE",
                "status": "Active",
            },
            {
                "id": 3,
                "name": "Krishna Paudel",
                "email": "krishna@farm.com",
                "joined": "May 15, 2026",
                "language": "NE",
                "status": "Inactive",
            },
            {
                "id": 4,
                "name": "Bibek Karki",
                "email": "bibek@gmail.com",
                "joined": "Jun 10, 2026",
                "language": "EN",
                "status": "Active",
            },
            {
                "id": 5,
                "name": "Puja Sharma",
                "email": "puja@farm.com",
                "joined": "Apr 30, 2026",
                "language": "NE",
                "status": "Inactive",
            },
        ]


def get_avatar_color(farmer_id: int) -> str:
    colors = [
        "#2563EB",
        "#16A34A",
        "#7C3AED",
        "#F97316",
        "#0891B2",
        "#DB2777",
    ]

    return colors[(farmer_id - 1) % len(colors)]


def farmers_page() -> None:
    initialize_farmers()

    farmers = pd.DataFrame(st.session_state.farmers_data)

    total_count = len(farmers)
    active_count = len(
        farmers[farmers["status"] == "Active"]
    )
    inactive_count = len(
        farmers[farmers["status"] == "Inactive"]
    )

    # Page header
    st.html(
        f"""
<div class="farmers-light-header">
    <div>
        <div class="farmers-light-title">
            Farmer Accounts
        </div>

        <div class="farmers-light-subtitle">
            {total_count} registered ·
            {active_count} active ·
            {inactive_count} inactive
        </div>
    </div>

    <div class="farmers-api-status">
        <span class="farmers-api-dot"></span>
        API ready
    </div>
</div>
"""
    )

    # Summary cards
    metric1, metric2, metric3 = st.columns(
        3,
        gap="medium",
    )

    with metric1:
        st.html(
            f"""
<div class="farmer-light-metric metric-total">
    <div class="farmer-light-metric-icon icon-blue">
        👨‍🌾
    </div>

    <div>
        <div class="farmer-light-metric-label">
            Total Farmers
        </div>

        <div class="farmer-light-metric-value">
            {total_count}
        </div>
    </div>
</div>
"""
        )

    with metric2:
        st.html(
            f"""
<div class="farmer-light-metric metric-active">
    <div class="farmer-light-metric-icon icon-green">
        ✓
    </div>

    <div>
        <div class="farmer-light-metric-label">
            Active
        </div>

        <div class="farmer-light-metric-value value-green">
            {active_count}
        </div>
    </div>
</div>
"""
        )

    with metric3:
        st.html(
            f"""
<div class="farmer-light-metric metric-inactive">
    <div class="farmer-light-metric-icon icon-red">
        ×
    </div>

    <div>
        <div class="farmer-light-metric-label">
            Inactive
        </div>

        <div class="farmer-light-metric-value value-red">
            {inactive_count}
        </div>
    </div>
</div>
"""
        )

    # Search and filter
    search_col, status_col, language_col = st.columns(
        [2, 1, 1],
        gap="medium",
    )

    with search_col:
        search_text = st.text_input(
            "Search farmers",
            placeholder="🔍 Search by name or email...",
            label_visibility="collapsed",
            key="farmers_light_search",
        )

    with status_col:
        status_filter = st.selectbox(
            "Status",
            ["All Status", "Active", "Inactive"],
            label_visibility="collapsed",
            key="farmers_light_status",
        )

    with language_col:
        language_filter = st.selectbox(
            "Language",
            ["All Languages", "EN", "NE"],
            label_visibility="collapsed",
            key="farmers_light_language",
        )

    filtered = farmers.copy()

    if search_text.strip():
        search_value = search_text.strip().lower()

        filtered = filtered[
            filtered.apply(
                lambda row: search_value
                in f"{row['name']} {row['email']}".lower(),
                axis=1,
            )
        ]

    if status_filter != "All Status":
        filtered = filtered[
            filtered["status"] == status_filter
        ]

    if language_filter != "All Languages":
        filtered = filtered[
            filtered["language"] == language_filter
        ]

    # Table heading
    st.html(
        """
<div class="farmers-table-title-card">
    <div>
        <div class="farmers-table-title">
            Registered Farmers
        </div>

        <div class="farmers-table-subtitle">
            Search and manage farmer account status.
        </div>
    </div>

    <div class="farmers-result-count">
        Filtered results
    </div>
</div>
"""
    )

    st.html(
        """
<div class="farmers-light-table-header">
    <div>Farmer</div>
    <div>Email</div>
    <div>Joined</div>
    <div>Language</div>
    <div>Status</div>
    <div>Action</div>
</div>
"""
    )

    if filtered.empty:
        st.html(
            """
<div class="farmers-light-empty">
    No farmer accounts match the selected filters.
</div>
"""
        )
        return

    # Farmer rows
    for _, row in filtered.iterrows():
        farmer_id = int(row["id"])

        selected_farmer = next(
            farmer
            for farmer in st.session_state.farmers_data
            if farmer["id"] == farmer_id
        )

        safe_name = html.escape(str(row["name"]))
        safe_email = html.escape(str(row["email"]))
        safe_joined = html.escape(str(row["joined"]))
        safe_language = html.escape(str(row["language"]))
        safe_status = html.escape(str(row["status"]))

        initials = "".join(
            part[0].upper()
            for part in str(row["name"]).split()[:2]
            if part
        )

        avatar_color = get_avatar_color(farmer_id)

        columns = st.columns(
            [1.7, 1.9, 1.25, 1, 1.1, 1.1],
            gap="small",
            vertical_alignment="center",
        )

        with columns[0]:
            st.html(
                f"""
<div class="farmer-light-name-cell">
    <div
        class="farmer-light-avatar"
        style="background:{avatar_color};"
    >
        {initials or "F"}
    </div>

    <div class="farmer-light-name">
        {safe_name}
    </div>
</div>
"""
            )

        with columns[1]:
            st.html(
                f"""
<div class="farmer-light-text-cell">
    {safe_email}
</div>
"""
            )

        with columns[2]:
            st.html(
                f"""
<div class="farmer-light-text-cell">
    {safe_joined}
</div>
"""
            )

        with columns[3]:
            language_name = (
                "English"
                if row["language"] == "EN"
                else "Nepali"
            )

            st.html(
                f"""
<div
    class="farmer-light-language"
    title="{language_name}"
>
    {safe_language}
</div>
"""
            )

        with columns[4]:
            status_class = (
                "farmer-light-status-active"
                if row["status"] == "Active"
                else "farmer-light-status-inactive"
            )

            st.html(
                f"""
<div class="farmer-light-status {status_class}">
    <span>●</span>
    {safe_status}
</div>
"""
            )

        with columns[5]:
            if row["status"] == "Active":
                if st.button(
                    "Deactivate",
                    key=f"farmer_light_deactivate_{farmer_id}",
                    use_container_width=True,
                    type="secondary",
                ):
                    selected_farmer["status"] = "Inactive"
                    st.success(
                        f"{row['name']} was deactivated."
                    )
                    st.rerun()

            else:
                if st.button(
                    "Reactivate",
                    key=f"farmer_light_reactivate_{farmer_id}",
                    use_container_width=True,
                    type="primary",
                ):
                    selected_farmer["status"] = "Active"
                    st.success(
                        f"{row['name']} was reactivated."
                    )
                    st.rerun()

        st.html(
            '<div class="farmer-light-row-divider"></div>'
        )