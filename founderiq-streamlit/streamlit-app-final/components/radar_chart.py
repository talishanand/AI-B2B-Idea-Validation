import plotly.graph_objects as go

DIMENSIONS = [
    ("marketSize", "Market"),
    ("competitionAdvantage", "Advantage"),
    ("problemUrgency", "Urgency"),
    ("feasibility", "Feasibility"),
    ("revenuePotential", "Revenue"),
    ("differentiation", "Diff."),
    ("gtmFit", "GTM Fit"),
]


def render_radar_figure(radar: dict) -> go.Figure:
    labels = [label for _, label in DIMENSIONS]
    values = [max(0, min(100, radar.get(key, 0))) for key, _ in DIMENSIONS]
    # close the loop for a clean polygon
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            fillcolor="rgba(139,92,246,0.30)",
            line=dict(color="#a78bfa", width=2),
            marker=dict(color="#c4b5fd", size=6),
            name="Score",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(255,255,255,0.08)",
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.08)",
                linecolor="rgba(255,255,255,0.08)",
                tickfont=dict(color="#9c98a8", size=11),
            ),
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=20, b=20),
        height=320,
    )
    return fig
