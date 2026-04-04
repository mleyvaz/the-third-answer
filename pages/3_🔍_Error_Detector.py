"""AI Error Type Detector — Chapter 1 typology."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.tif_calculator import ERROR_TYPES
from components.visualizations import create_error_matrix

st.set_page_config(page_title="Error Detector", page_icon="🔍", layout="wide")

st.markdown("# 🔍 AI Error Type Detector")
st.markdown("*Not all AI errors are the same. Learn to identify the four types (Chapter 1)*")
st.divider()

# Error matrix visualization
st.markdown("### Error Typology Matrix")
st.caption("Based on detectability (how easy to catch) and severity (how dangerous)")

fig = create_error_matrix()
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Interactive detector
st.markdown("### Identify an Error")

ai_output = st.text_area(
    "Paste an AI output you suspect contains an error:",
    placeholder="Example: 'The 2019 case of Fernandez v. Avianca Airlines established that...'",
    height=100,
)

if ai_output:
    st.markdown("### Which type of error do you suspect?")

    selected = st.radio(
        "Select the error type that best matches:",
        list(ERROR_TYPES.keys()),
        format_func=lambda x: f"{ERROR_TYPES[x]['emoji']} {ERROR_TYPES[x]['name']}",
    )

    error = ERROR_TYPES[selected]

    st.markdown(f"""
    <div style="background: #f8fafc; border-radius: 12px; padding: 1.5rem;
                border-left: 5px solid {'#ef4444' if selected == 'confident_ignorance' else '#f97316'};">
        <h3>{error['emoji']} {error['name']}</h3>
        <p><strong>{error['description']}</strong></p>
        <p><em>Example: {error['example']}</em></p>
        <p>Detectability: <strong>{error['detectability']}</strong></p>
        <p>Severity: <strong>{error['severity']}</strong></p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# All four types detailed
st.markdown("### The Four Types of AI Error")

for key, error in ERROR_TYPES.items():
    with st.expander(f"{error['emoji']} {error['name']} — {error['severity']} severity"):
        st.markdown(f"**{error['description']}**")
        st.markdown(f"*Example: {error['example']}*")
        st.markdown(f"**Detectability:** {error['detectability']}")
        st.markdown(f"**Severity:** {error['severity']}")

        if key == "fabrication":
            st.markdown("""
            **How to detect:**
            - Search for the specific claim in authoritative databases
            - Check if cited papers/cases/people actually exist
            - Use Google Scholar, Westlaw, PubMed for verification
            """)
        elif key == "distortion":
            st.markdown("""
            **How to detect:**
            - Read the ORIGINAL source, not just the AI summary
            - Compare quantitative claims (percentages, dates, sample sizes)
            - Watch for hedging that disappeared (\"may\" became \"does\")
            """)
        elif key == "conflation":
            st.markdown("""
            **How to detect:**
            - Verify each individual claim separately
            - Check that author+work, drug+indication, company+event match
            - Be suspicious when the AI connects two real things too neatly
            """)
        elif key == "confident_ignorance":
            st.markdown("""
            **How to detect — this is the hardest one:**
            - Ask yourself: Is this a topic where reliable data EXISTS?
            - Check: Is this recent, niche, or region-specific?
            - Look for hedging language — if the AI shows ZERO doubt, be MORE suspicious
            - Apply the T,I,F compass: if I should be high but the AI acts like I=0, you found it
            """)

st.divider()

st.markdown("""
### The Key Insight

> *"The model uses the same mechanism to produce true statements and false statements.
> There is no internal switch that flips between 'reliable mode' and 'guessing mode.'"*
> — Chapter 1, The Third Answer

**Confident Ignorance** is the most dangerous because it produces **no signal that verification
is needed**. The other three types can be caught with diligence. Confident Ignorance requires
the T,I,F framework to even know where to look.
""")

st.caption("From *The Third Answer* by Leyva-Vazquez & Smarandache (2026), Chapter 1")
