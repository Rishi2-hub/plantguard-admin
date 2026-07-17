import html

import streamlit as st
from streamlit_option_menu import option_menu

from login import logout


def sidebar() -> str:
    admin_name = st.session_state.get(
        "admin_name",
        "Administrator",
    )

    is_super_admin = st.session_state.get(
        "is_super_admin",
        False,
    )

    safe_admin_name = html.escape(str(admin_name))

    role_label = (
        "Super Admin"
        if is_super_admin
        else "Admin"
    )

    initials = "".join(
        part[0].upper()
        for part in str(admin_name).split()[:2]
        if part
    )

    options = [
        "Dashboard",
        "Treatments",
        "Farmers",
        "Audit Logs",
    ]

    icons = [
        "grid-fill",
        "capsule",
        "people-fill",
        "clipboard-data",
    ]

    if is_super_admin:
        options.append("Add Admin")
        icons.append("person-plus-fill")

    options.append("Settings")
    icons.append("gear-fill")

    with st.sidebar:
        st.html(
            """
<div class="sidebar-brand">
    <div class="sidebar-logo">🌿</div>

    <div>
        <div class="sidebar-brand-name">
            PlantGuard
        </div>

        <div class="sidebar-brand-subtitle">
            ADMIN CONSOLE
        </div>
    </div>
</div>
"""
        )

        st.html(
            """
<div class="sidebar-section-label">
    NAVIGATION
</div>
"""
        )

        selected = option_menu(
    menu_title=None,
    options=options,
    icons=icons,
    default_index=0,
    styles={
        "container": {
            "padding": "0",
            "background-color": "#0f1017",
        },
        "icon": {
            "color": "#979db8",
            "font-size": "18px",
        },
        "nav-link": {
            "font-size": "15px",
            "font-weight": "650",
            "text-align": "left",
            "margin": "5px 0",
            "padding": "12px 14px",
            "border-radius": "10px",
            "--hover-color": "#171b28",
            "color": "#a6abc4",
        },
        "nav-link-selected": {
            "background-color": "#0b351f",
            "color": "#22c55e",
            "border": "1px solid #14532d",
        },
    },
)

        st.html(
            f"""
<div class="sidebar-profile">
    <div class="sidebar-avatar">
        {html.escape(initials or "AD")}
    </div>

    <div>
        <div class="sidebar-profile-name">
            {safe_admin_name}
        </div>

        <div class="sidebar-profile-role">
            {role_label}
        </div>
    </div>
</div>
"""
        )

        if st.button(
            "🚪 Sign Out",
            use_container_width=True,
            key="sidebar_sign_out",
        ):
            logout()

    return selected