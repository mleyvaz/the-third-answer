"""The Four Zones — Interactive zone explorer."""
import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.tif_calculator import ZONE_INFO

st.set_page_config(page_title="Four Zones", page_icon="🗺", layout="wide")

st.markdown("# 🗺 The Four Zones")
st.markdown("*Every AI output falls into one of four epistemic territories (Chapter 2)*")
st.divider()

# Interactive zone map
st.markdown("### Zone Map")

fig = go.Figure()

zones_plot = [
    ("Consensus", 0.8, 0.15, "#22c55e", "T high, I low, F low<br><b>ACTION: Trust</b>"),
    ("Ambiguity", 0.3, 0.75, "#eab308", "I high<br><b>ACTION: Investigate</b>"),
    ("Contradiction", 0.7, 0.7, "#f97316", "T high AND F high<br><b>ACTION: Explore both sides</b>"),
    ("Ignorance", 0.15, 0.15, "#6b7280", "All low or I overwhelming<br><b>ACTION: Stop</b>"),
]

for name, x, y, color, text in zones_plot:
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode="markers+text",
        marker=dict(size=80, color=color, opacity=0.4, line=dict(width=2, color=color)),
        text=[name],
        textposition="middle center",
        textfont=dict(size=14, color=color),
        hovertext=text,
        hoverinfo="text",
        showlegend=False,
    ))

fig.update_layout(
    xaxis=dict(title="Truth (T) — Evidence Support →", range=[0, 1]),
    yaxis=dict(title="Indeterminacy (I) / Falsity (F) →", range=[0, 1]),
    height=450,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(248,250,252,1)",
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Detailed zone cards
st.markdown("### Zone Details")

for key, zone in ZONE_INFO.items():
    with st.expander(f"{zone['emoji']} {zone['name']} — {zone['action']}", expanded=False):
        st.markdown(f"**{zone['description']}**")
        st.markdown("**What to do:**")
        for item in zone["what_to_do"]:
            st.markdown(f"- {item}")

st.divider()

# Examples from the book
st.markdown("### Examples from the Book")

examples = [
    {
        "question": "What is the boiling point of water at sea level?",
        "zone": "🟢 Consensus",
        "t": 0.95, "i": 0.02, "f": 0.01,
        "explanation": "One of the most well-established facts in physical science. No meaningful uncertainty. No counter-evidence.",
    },
    {
        "question": "What are the long-term cognitive effects of a medication approved 18 months ago?",
        "zone": "🟡 Ambiguity",
        "t": 0.35, "i": 0.75, "f": 0.10,
        "explanation": "Short-term trials showed some results (moderate T). No long-term data exists yet (very high I). No contradicting evidence (low F).",
    },
    {
        "question": "Does remote work increase or decrease productivity?",
        "zone": "🟠 Contradiction",
        "t": 0.65, "i": 0.25, "f": 0.60,
        "explanation": "Evidence FOR (T high): studies show increased focus time. Evidence AGAINST (F high): studies show reduced collaboration. The real information is in the tension.",
    },
    {
        "question": "Predict the outcome of a complex geopolitical negotiation with no precedent.",
        "zone": "⚫ Ignorance",
        "t": 0.10, "i": 0.85, "f": 0.05,
        "explanation": "No reliable predictive model exists (T low). Variables too numerous and poorly understood (I very high). The AI generates text but it is not grounded in anything.",
    },
    {
        "question": "Is coffee good for your health?",
        "zone": "🟠 Contradiction",
        "t": 0.70, "i": 0.30, "f": 0.45,
        "explanation": "Health benefits are real and well-documented (T=0.70). Risks are also real and documented (F=0.45). Long-term genetic factors still under-researched (I=0.30). Binary answer is impossible.",
    },
]

for ex in examples:
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**Q:** *{ex['question']}*")
            st.markdown(f"**Zone:** {ex['zone']}")
            st.markdown(f"{ex['explanation']}")
        with col2:
            st.markdown(f"T = **{ex['t']}** | I = **{ex['i']}** | F = **{ex['f']}**")
        st.divider()

st.caption("From *The Third Answer* by Leyva-Vazquez & Smarandache (2026), Chapter 2")
