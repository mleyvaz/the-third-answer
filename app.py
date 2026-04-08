"""
The Third Answer — Interactive Companion App
Why AI Doesn't Know What It Doesn't Know — And How Ancient Logic Can Fix It

By Maikel Yelandi Leyva-Vazquez, PhD & Florentin Smarandache, PhD
"""
import streamlit as st

st.set_page_config(
    page_title="The Third Answer",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-title { font-size: 2.8rem; font-weight: 800; color: #1e293b; line-height: 1.2; }
    .subtitle { font-size: 1.2rem; color: #64748b; margin-top: -10px; }
    .zone-card {
        padding: 1.5rem; border-radius: 12px; margin: 0.5rem 0;
        border-left: 5px solid; background: #f8fafc;
    }
    .quote { font-style: italic; color: #475569; padding: 1rem;
             border-left: 4px solid #94a3b8; margin: 1rem 0; }
    .metric-big { font-size: 3rem; font-weight: 800; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/compass.png", width=60)
    st.markdown("### The Third Answer")
    st.caption("Interactive companion to the book")
    st.divider()
    st.markdown("""
    **Navigate:**
    - **Home** — What is The Third Answer?
    - **T,I,F Compass** — Evaluate any AI output
    - **Four Zones** — Map your assessment
    - **Error Detector** — Identify AI error types
    - **Prompt Templates** — Ready-to-use prompts
    - **The Honest Machine** — Interactive demo
    - **🏷 Nutrition Label** — Generate Epistemic Nutrition Labels
    """)
    st.divider()
    st.caption("Leyva-Vazquez & Smarandache, 2026")

# Main content
st.markdown('<p class="main-title">🧭 The Third Answer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Why AI Doesn\'t Know What It Doesn\'t Know — And How Ancient Logic Can Fix It</p>', unsafe_allow_html=True)

st.markdown("")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### The Problem

    AI systems speak with the same confidence whether they are retrieving a well-established
    fact or fabricating a plausible fiction. They have **no mechanism for signaling when they
    are on uncertain ground**.

    This is not a bug that will be patched. It is a **structural feature** of how these
    systems work — what we call *the architecture of overconfidence*.

    ### The Solution

    A framework from 1995 — **neutrosophic logic** — gives every claim three independent
    dimensions instead of one:

    | Dimension | What it measures |
    |-----------|-----------------|
    | **T (Truth)** | How much is supported by evidence |
    | **I (Indeterminacy)** | How much is genuinely unknown |
    | **F (Falsity)** | How much is contradicted by evidence |

    These three needles are **independent** — they don't need to add up to 1.
    This is what makes the framework fundamentally different from probability.
    """)

    st.markdown("""
    <div class="quote">
    "The only true wisdom is in knowing you know nothing." — Socrates<br><br>
    "El mundo indio no concibe dualismos que excluyen. Concibe dualidades que incluyen." — Rodolfo Kusch
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### The Four Zones")

    zones = [
        ("🟢 Consensus", "#22c55e", "T high, I low, F low", "TRUST"),
        ("🟡 Ambiguity", "#eab308", "I high", "INVESTIGATE"),
        ("🟠 Contradiction", "#f97316", "T high AND F high", "EXPLORE BOTH SIDES"),
        ("⚫ Ignorance", "#6b7280", "All low or I overwhelming", "STOP"),
    ]

    for name, color, condition, action in zones:
        st.markdown(f"""
        <div class="zone-card" style="border-left-color: {color};">
            <strong>{name}</strong><br>
            <small style="color: #64748b;">{condition}</small><br>
            <span style="color: {color}; font-weight: 600;">{action}</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Quick stats from the book
st.markdown("### Why This Matters")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("AI Error Rate (medical)", "10-30%", help="Stanford 2024 study on AI clinical advice")
with c2:
    st.metric("Fabricated Legal Cases", "6 in 1 brief", help="Schwartz v. Mata, 2023")
with c3:
    st.metric("Users Who Can't Detect", "~70%", help="Users cannot distinguish AI confidence from accuracy")
with c4:
    st.metric("The Missing Dimension", "I", help="Indeterminacy — what current AI cannot express")

st.divider()

st.markdown("""
### How to Use This App

1. **🧭 T,I,F Compass** — Paste any AI output and assess its Truth, Indeterminacy, and Falsity
2. **🗺 Four Zones** — See which zone your assessment falls into and what action to take
3. **🔍 Error Detector** — Learn to identify the 4 types of AI errors (Chapter 1)
4. **📋 Prompt Templates** — Copy ready-made prompts that force AI to express uncertainty
5. **🤖 The Honest Machine** — See what AI outputs would look like WITH the Third Answer
6. **🏷 Nutrition Label** — Generate visual Epistemic Nutrition Labels for any AI output

---
**Book:** *The Third Answer: Why AI Doesn't Know What It Doesn't Know — And How Ancient Logic Can Fix It*
**Authors:** Maikel Yelandi Leyva-Vazquez, PhD & Florentin Smarandache, PhD
**Year:** 2026 | ISBN: [pending]
""")
