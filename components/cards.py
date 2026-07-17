import html

import streamlit as st


def stat_card(
    title: str,
    value: str,
    subtitle: str,
    icon: str,
    accent_color: str,
    icon_background: str,
) -> None:
    st.html(
        f"""
<div
    class="stat-card"
    style="border-top:5px solid {accent_color};"
>
    <div class="stat-card-header">
        <div
            class="stat-card-icon"
            style="
                background:{icon_background};
                color:{accent_color};
            "
        >
            {icon}
        </div>

        <div class="stat-card-title">
            {html.escape(str(title))}
        </div>
    </div>

    <div class="stat-card-value">
        {html.escape(str(value))}
    </div>

    <div
        class="stat-card-subtitle"
        style="color:{accent_color};"
    >
        {html.escape(str(subtitle))}
    </div>
</div>
"""
    )