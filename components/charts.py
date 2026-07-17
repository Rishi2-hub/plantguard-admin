import pandas as pd
import plotly.express as px
import streamlit as st


def disease_frequency_chart():
    data = pd.DataFrame(
        {
            "Disease": [
                "Tomato Late Blight",
                "Tomato Early Blight",
                "Potato Blight",
                "Bacterial Spot",
                "Spider Mites",
            ],
            "Cases": [18, 14, 10, 7, 5],
        }
    )

    fig = px.bar(
        data,
        x="Cases",
        y="Disease",
        orientation="h",
        text="Cases",
    )

    fig.update_traces(
        marker_color=[
            "#DC2626",
            "#F59E0B",
            "#2563EB",
            "#7C3AED",
            "#16A34A",
        ],
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Cases: %{x}<extra></extra>",
    )

    fig.update_layout(
        height=355,
        margin=dict(l=10, r=25, t=5, b=10),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        xaxis=dict(
            title=None,
            showgrid=True,
            gridcolor="#E8EDF5",
            zeroline=False,
            tickfont=dict(color="#64748B"),
        ),
        yaxis=dict(
            title=None,
            autorange="reversed",
            tickfont=dict(color="#334155", size=12),
        ),
        font=dict(
            family="Arial",
            color="#172033",
        ),
    )

    st.markdown(
        """
        <div class="chart-panel-header">
            <div>
                <div class="panel-title">Disease Frequency</div>
                <div class="panel-subtitle">
                    Most commonly detected plant diseases
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )