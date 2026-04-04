"""Visualization components for The Third Answer app."""
import plotly.graph_objects as go


def create_radar_chart(t, i, f, zone_color="#22c55e"):
    """Create a radar chart showing T, I, F values."""
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[t, i, f, t],
        theta=["Truth (T)", "Indeterminacy (I)", "Falsity (F)", "Truth (T)"],
        fill="toself",
        fillcolor=f"rgba({int(zone_color[1:3],16)},{int(zone_color[3:5],16)},{int(zone_color[5:7],16)},0.3)",
        line=dict(color=zone_color, width=3),
        name="T,I,F Assessment",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(size=11)),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        height=350,
        margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_zone_gauge(t, i, f, zone_name, zone_color):
    """Create a visual gauge showing the dominant zone."""
    confidence = max(0, t - i - f)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=confidence,
        number=dict(suffix="", font=dict(size=40)),
        title=dict(text=f"Zone: {zone_name}", font=dict(size=18)),
        gauge=dict(
            axis=dict(range=[0, 1], tickwidth=1),
            bar=dict(color=zone_color),
            bgcolor="rgba(200,200,200,0.1)",
            steps=[
                dict(range=[0, 0.25], color="rgba(107,114,128,0.2)"),
                dict(range=[0.25, 0.5], color="rgba(234,179,8,0.2)"),
                dict(range=[0.5, 0.75], color="rgba(249,115,22,0.2)"),
                dict(range=[0.75, 1], color="rgba(34,197,94,0.2)"),
            ],
        ),
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=30, r=30, t=60, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_error_matrix():
    """Create the error typology matrix from Chapter 1."""
    fig = go.Figure()

    errors = [
        ("Fabrication", 0.5, 0.8, "🔴", 20),
        ("Distortion", 0.3, 0.75, "🟠", 18),
        ("Conflation", 0.5, 0.5, "🟡", 16),
        ("Confident\nIgnorance", 0.15, 0.95, "⚫", 22),
    ]

    for name, detect, severity, emoji, size in errors:
        fig.add_trace(go.Scatter(
            x=[detect], y=[severity],
            mode="markers+text",
            marker=dict(size=size * 3, opacity=0.7),
            text=[f"{emoji} {name}"],
            textposition="bottom center",
            textfont=dict(size=12),
            name=name,
            showlegend=False,
        ))

    fig.add_shape(type="rect", x0=0, y0=0.7, x1=0.35, y1=1,
                  fillcolor="rgba(239,68,68,0.1)", line=dict(width=0))
    fig.add_annotation(x=0.17, y=0.98, text="DANGER ZONE",
                       font=dict(color="red", size=10), showarrow=False)

    fig.update_layout(
        xaxis=dict(title="Detectability →", range=[0, 1], dtick=0.25),
        yaxis=dict(title="Severity →", range=[0, 1], dtick=0.25),
        height=400,
        margin=dict(l=60, r=30, t=30, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(245,245,245,0.5)",
    )
    return fig


def create_comparison_bar(t, i, f):
    """Create horizontal bar showing T vs I vs F proportions."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=["Assessment"],
        x=[t], name="Truth (T)",
        orientation="h", marker_color="#22c55e",
    ))
    fig.add_trace(go.Bar(
        y=["Assessment"],
        x=[i], name="Indeterminacy (I)",
        orientation="h", marker_color="#eab308",
    ))
    fig.add_trace(go.Bar(
        y=["Assessment"],
        x=[f], name="Falsity (F)",
        orientation="h", marker_color="#ef4444",
    ))

    fig.update_layout(
        barmode="group",
        height=120,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(orientation="h", y=1.3),
        xaxis=dict(range=[0, 1]),
    )
    return fig
