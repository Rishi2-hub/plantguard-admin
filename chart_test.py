def disease_frequency_chart() -> None:
    diseases = [
        "Tomato Late Blight",
        "Tomato Early Blight",
        "Potato Blight",
        "Bacterial Spot",
        "Spider Mites",
    ]

    cases = [18, 14, 10, 7, 5]

    figure = go.Figure(
        data=[
            go.Bar(
                x=cases,
                y=diseases,
                orientation="h",
                marker_color=[
                    "#DC2626",
                    "#F59E0B",
                    "#2563EB",
                    "#7C3AED",
                    "#16A34A",
                ],
                text=cases,
                textposition="outside",
            )
        ]
    )

    figure.update_layout(
        height=380,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        showlegend=False,
        margin=dict(l=170, r=50, t=20, b=40),
        xaxis=dict(
            range=[0, 20],
            title="Number of Cases",
            gridcolor="#E5E7EB",
            tickfont=dict(color="#111827"),
            title_font=dict(color="#111827"),
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
    <div class="panel-title">Disease Frequency</div>
    <div class="panel-subtitle">
        Most frequently detected plant diseases
    </div>
</div>
"""
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={"displayModeBar": False},
    )