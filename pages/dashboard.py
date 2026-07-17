import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.activity import recent_activity
from components.cards import stat_card


def disease_frequency_chart() -> None:
    diseases = [
        "Tomato Late Blight",
        "Tomato Early Blight",
        "Potato Blight",
        "Bacterial Spot",
        "Spider Mites",
    ]

    cases = [18, 14, 10, 7, 5]

    colors = [
        "#DC2626",
        "#F59E0B",
        "#2563EB",
        "#7C3AED",
        "#16A34A",
    ]

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=cases,
            y=diseases,
            orientation="h",
            marker_color=colors,
            text=cases,
            textposition="outside",
            textfont=dict(
                color="#111827",
                size=13,
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Cases: %{x}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        height=380,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        margin=dict(
            l=170,
            r=50,
            t=20,
            b=40,
        ),
        font=dict(
            family="Arial",
            color="#111827",
        ),
        xaxis=dict(
            range=[0, 20],
            title="Number of Cases",
            showgrid=True,
            gridcolor="#E5E7EB",
            zeroline=False,
            tickfont=dict(
                color="#111827",
                size=12,
            ),
            title_font=dict(
                color="#111827",
                size=13,
            ),
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(
                color="#111827",
                size=13,
            ),
        ),
    )

    st.html(
        """
<div class="chart-heading">
    <div class="panel-title">
        Disease Frequency
    </div>

    <div class="panel-subtitle">
        Most frequently detected plant diseases
    </div>
</div>
"""
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


def dashboard() -> None:
    st.html(
        """
<div class="dashboard-heading">
    <h2>System Overview</h2>

    <p>
        Monitor farmers, diseases, treatments, and system alerts.
    </p>
</div>
"""
    )

    col1, col2, col3, col4 = st.columns(
        4,
        gap="medium",
    )

    with col1:
        stat_card(
            title="Total Farmers",
            value="24",
            subtitle="3 new this week",
            icon="👨‍🌾",
            accent_color="#2563EB",
            icon_background="#DBEAFE",
        )

    with col2:
        stat_card(
            title="Plant Diseases",
            value="15",
            subtitle="Covered diseases",
            icon="🌿",
            accent_color="#16A34A",
            icon_background="#DCFCE7",
        )

    with col3:
        stat_card(
            title="Active Treatments",
            value="45",
            subtitle="Treatment records",
            icon="💊",
            accent_color="#F59E0B",
            icon_background="#FEF3C7",
        )

    with col4:
        stat_card(
            title="System Alerts",
            value="2",
            subtitle="Needs attention",
            icon="🚨",
            accent_color="#DC2626",
            icon_background="#FEE2E2",
        )

    st.html(
        """
<div class="disease-alert">
    <div class="disease-alert-icon">
        ⚠️
    </div>

    <div class="disease-alert-content">
        <div class="disease-alert-title">
            Tomato Late Blight detected multiple times
        </div>

        <div class="disease-alert-description">
            Review the affected farmers and treatment recommendations.
        </div>
    </div>

    <div class="disease-alert-action">
        Review Alert
    </div>
</div>
"""
    )

    left, right = st.columns(
        [1.05, 1],
        gap="large",
    )

    with left:
        recent_activity()

    with right:
        disease_frequency_chart()