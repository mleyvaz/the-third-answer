"""The Four Zones — Interactive 3D zone explorer."""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.tif_calculator import classify_zone, ZONE_INFO

st.set_page_config(page_title="Four Zones", page_icon="🗺", layout="wide")

st.markdown("# 🗺 The Four Zones")
st.markdown("*Every AI output falls into one of four epistemic territories (Chapter 2)*")
st.divider()

# === 3D ZONE MAP ===
st.markdown("### 3D Zone Map — Truth, Indeterminacy, Falsity")
st.caption("Each point in this space represents an epistemic state. The zones are regions, not lines.")

# Generate sample points for each zone
np.random.seed(42)
n = 60

zone_points = {
    "Consensus": {"T": np.random.uniform(0.6, 0.95, n), "I": np.random.uniform(0.02, 0.30, n), "F": np.random.uniform(0.02, 0.25, n), "color": "#22c55e", "symbol": "circle"},
    "Ambiguity": {"T": np.random.uniform(0.15, 0.55, n), "I": np.random.uniform(0.50, 0.95, n), "F": np.random.uniform(0.05, 0.40, n), "color": "#eab308", "symbol": "diamond"},
    "Contradiction": {"T": np.random.uniform(0.45, 0.90, n), "I": np.random.uniform(0.05, 0.35, n), "F": np.random.uniform(0.40, 0.90, n), "color": "#f97316", "symbol": "square"},
    "Ignorance": {"T": np.random.uniform(0.02, 0.25, n), "I": np.random.uniform(0.02, 0.30, n), "F": np.random.uniform(0.02, 0.25, n), "color": "#6b7280", "symbol": "x"},
}

fig3d = go.Figure()

for zone_name, data in zone_points.items():
    info = ZONE_INFO.get(zone_name.lower(), ZONE_INFO.get("ambiguity"))
    fig3d.add_trace(go.Scatter3d(
        x=data["T"], y=data["I"], z=data["F"],
        mode="markers",
        marker=dict(
            size=4,
            color=data["color"],
            opacity=0.6,
            symbol=data["symbol"],
        ),
        name=f"{info['emoji']} {zone_name}",
        hovertemplate=f"<b>{zone_name}</b><br>T=%{{x:.2f}}<br>I=%{{y:.2f}}<br>F=%{{z:.2f}}<extra></extra>",
    ))

# Add labeled center points
centers = [
    ("Consensus", 0.80, 0.12, 0.08, "#22c55e"),
    ("Ambiguity", 0.35, 0.75, 0.20, "#eab308"),
    ("Contradiction", 0.70, 0.15, 0.65, "#f97316"),
    ("Ignorance", 0.10, 0.10, 0.10, "#6b7280"),
]
for name, t, i, f, color in centers:
    fig3d.add_trace(go.Scatter3d(
        x=[t], y=[i], z=[f],
        mode="markers+text",
        marker=dict(size=10, color=color, opacity=1, line=dict(width=2, color="white")),
        text=[name],
        textposition="top center",
        textfont=dict(size=12, color=color),
        showlegend=False,
        hoverinfo="skip",
    ))

fig3d.update_layout(
    scene=dict(
        xaxis=dict(title="Truth (T)", range=[0, 1], backgroundcolor="rgba(248,250,252,0.8)"),
        yaxis=dict(title="Indeterminacy (I)", range=[0, 1], backgroundcolor="rgba(248,250,252,0.8)"),
        zaxis=dict(title="Falsity (F)", range=[0, 1], backgroundcolor="rgba(248,250,252,0.8)"),
        camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)),
    ),
    height=600,
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(
        yanchor="top", y=0.99, xanchor="left", x=0.01,
        bgcolor="rgba(255,255,255,0.8)",
        font=dict(size=13),
    ),
)

st.plotly_chart(fig3d, use_container_width=True)
st.caption("Rotate the 3D map by dragging. Each cloud represents a zone. Note: T+I+F is NOT constrained to 1 — the zones can overlap in the T+F > 1 region (paraconsistency).")

# === INTERACTIVE PROBE ===
st.divider()
st.markdown("### Probe a Point")
st.caption("Set T, I, F values and see which zone they fall into")

col_t, col_i, col_f, col_result = st.columns([1, 1, 1, 1])
with col_t:
    probe_t = st.slider("T (Truth)", 0.0, 1.0, 0.55, 0.05, key="probe_t")
with col_i:
    probe_i = st.slider("I (Indeterminacy)", 0.0, 1.0, 0.30, 0.05, key="probe_i")
with col_f:
    probe_f = st.slider("F (Falsity)", 0.0, 1.0, 0.45, 0.05, key="probe_f")
with col_result:
    zk = classify_zone(probe_t, probe_i, probe_f)
    zone = ZONE_INFO[zk]
    is_para = (probe_t + probe_f) > 1.0
    st.markdown(f"""
    <div style="background:{zone['color']}20; border:3px solid {zone['color']};
                border-radius:16px; padding:1.2rem; text-align:center; margin-top:0.5rem;">
        <div style="font-size:2.5rem;">{zone['emoji']}</div>
        <div style="font-size:1.3rem; font-weight:800; color:{zone['color']};">{zone['name']}</div>
        <div style="font-size:0.85rem; margin-top:4px;">{zone['action']}</div>
        {'<div style="color:#f97316; font-weight:700; margin-top:6px;">⚠ Paraconsistent (T+F=' + f"{probe_t+probe_f:.2f}" + ')</div>' if is_para else ''}
    </div>
    """, unsafe_allow_html=True)

st.divider()

# === ZONE DETAILS ===
st.markdown("### Zone Details")

for key, zone in ZONE_INFO.items():
    with st.expander(f"{zone['emoji']} {zone['name']} — {zone['action']}", expanded=False):
        st.markdown(f"**{zone['description']}**")
        st.markdown("**What to do:**")
        for item in zone["what_to_do"]:
            st.markdown(f"- {item}")

st.divider()

# === EXAMPLES ===
st.markdown("### Examples from the Book")

examples = [
    {"question": "What is the boiling point of water at sea level?", "zone": "Consensus",
     "t": 0.95, "i": 0.02, "f": 0.01,
     "explanation": "One of the most well-established facts in physical science."},
    {"question": "Long-term cognitive effects of a medication approved 18 months ago?", "zone": "Ambiguity",
     "t": 0.35, "i": 0.75, "f": 0.10,
     "explanation": "Short-term trials exist (moderate T). No long-term data yet (very high I)."},
    {"question": "Does remote work increase or decrease productivity?", "zone": "Contradiction",
     "t": 0.65, "i": 0.25, "f": 0.60,
     "explanation": "Evidence FOR: increased focus time. Evidence AGAINST: reduced collaboration. The real information is in the tension."},
    {"question": "Predict a complex geopolitical negotiation with no precedent.", "zone": "Ignorance",
     "t": 0.10, "i": 0.85, "f": 0.05,
     "explanation": "No reliable predictive model. The AI generates text but it is not grounded."},
]

for ex in examples:
    zk_ex = classify_zone(ex["t"], ex["i"], ex["f"])
    zone_ex = ZONE_INFO[zk_ex]
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Q:** *{ex['question']}*")
            st.markdown(f"{ex['explanation']}")
        with col2:
            st.markdown(f"""
            <div style="text-align:center; padding:0.5rem; border-radius:8px; background:{zone_ex['color']}15; border:1px solid {zone_ex['color']};">
                {zone_ex['emoji']} <b style="color:{zone_ex['color']};">{zone_ex['name']}</b><br>
                <code>T={ex['t']} I={ex['i']} F={ex['f']}</code>
            </div>""", unsafe_allow_html=True)
        st.divider()

st.caption("From *The Third Answer* by Leyva-Vazquez & Smarandache (2026), Chapter 2")
