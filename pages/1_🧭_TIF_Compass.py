"""T,I,F Compass — Evaluate any AI output with real LLM analysis."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.tif_calculator import classify_zone, ZONE_INFO
from components.visualizations import create_radar_chart, create_comparison_bar

st.set_page_config(page_title="T,I,F Compass", page_icon="🧭", layout="wide")

st.markdown("# 🧭 The T,I,F Compass")
st.markdown("*Evaluate any AI output using three independent dimensions — powered by Groq LLM*")
st.divider()

# API Key in sidebar
with st.sidebar:
    # Try secrets first (hidden from users), fallback to manual input
    groq_key = st.secrets.get("GROQ_API_KEY", "")
    if groq_key and groq_key != "REPLACE_WITH_NEW_KEY_AFTER_REVOKING":
        st.success("API key loaded from secrets (hidden)")
    else:
        groq_key = st.text_input("🔑 Groq API Key", type="password",
                                 help="Free at console.groq.com. Never stored.")
        if not groq_key:
            st.warning("Enter your Groq API key (free at console.groq.com)")
        else:
            st.success("Key loaded")

    model = st.selectbox("Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
        "mixtral-8x7b-32768",
    ], help="All free on Groq")

# Mode selector
mode = st.radio("Mode:", ["🤖 AI Auto-Analysis (Groq)", "🖐 Manual Sliders"], horizontal=True)

col_input, col_viz = st.columns([1, 1])

with col_input:
    st.markdown("### Paste an AI Response to Evaluate")
    ai_text = st.text_area(
        "AI output to assess",
        placeholder="Paste any AI-generated text here...\n\nExample: 'The prevalence of Chagas disease in Manabi province is approximately 2.3% of the rural population...'",
        height=180,
    )

    context = st.text_input("Domain/context (optional)",
                            placeholder="e.g., medicine, law, Ecuador policy, technology...")

    if mode == "🤖 AI Auto-Analysis (Groq)":
        analyze_btn = st.button("🧭 Analyze with T,I,F Compass", type="primary",
                                disabled=not groq_key or not ai_text)

        if analyze_btn and groq_key and ai_text:
            with st.spinner("Analyzing with Groq LLM (free, ~2 sec)..."):
                try:
                    from components.llm import analyze_with_groq
                    result = analyze_with_groq(ai_text, groq_key, context, model)
                    st.session_state["tif_result"] = result
                    st.session_state["tif_mode"] = "auto"
                except Exception as e:
                    st.error(f"Error: {e}")

        # Show claim-by-claim analysis if available
        if st.session_state.get("tif_mode") == "auto" and "tif_result" in st.session_state:
            r = st.session_state["tif_result"]

            if r.get("error_types"):
                st.error(f"⚠️ **Errors detected:** {', '.join(r['error_types'])}")
                if r.get("error_explanation"):
                    st.markdown(f"*{r['error_explanation']}*")

            if r.get("key_claims"):
                st.markdown("#### Claim-by-Claim Analysis")
                for j, claim in enumerate(r["key_claims"]):
                    ct = claim.get("T", 0.5)
                    ci = claim.get("I", 0.5)
                    cf = claim.get("F", 0.1)
                    czone = classify_zone(ct, ci, cf)
                    z = ZONE_INFO[czone]
                    st.markdown(f"""
                    <div style="background: {z['color']}10; border-left: 4px solid {z['color']};
                                padding: 0.8rem; border-radius: 8px; margin: 0.3rem 0; font-size: 0.9rem;">
                        {z['emoji']} <strong>{claim.get('claim', '')[:100]}</strong><br>
                        <code>T={ct:.2f} I={ci:.2f} F={cf:.2f}</code>
                        <span style="color: {z['color']}; font-weight:600;"> → {z['name']}</span><br>
                        <small style="color: #64748b;">{claim.get('note', '')}</small>
                    </div>
                    """, unsafe_allow_html=True)

            # Honest rewrite
            if r.get("honest_version") and r["honest_version"] != ai_text:
                st.markdown("#### ✅ Honest Version (rewritten with uncertainty)")
                st.markdown(f"""
                <div style="background: #f0fdf4; border: 1px solid #86efac;
                            border-radius: 10px; padding: 1rem; font-size: 0.9rem;">
                {r['honest_version']}
                </div>
                """, unsafe_allow_html=True)

    else:
        # Manual mode
        st.markdown("### Assess the Three Dimensions")
        st.caption("Move each slider independently. They do NOT need to add up to 1.")
        st.session_state["tif_mode"] = "manual"

# Get T, I, F values
if mode == "🤖 AI Auto-Analysis (Groq)" and st.session_state.get("tif_result"):
    r = st.session_state["tif_result"]
    t, i, f = r["T"], r["I"], r["F"]
else:
    if mode == "🖐 Manual Sliders":
        with col_input:
            t = st.slider("**T (Truth)** — How much is supported?", 0.0, 1.0, 0.5, 0.05)
            i = st.slider("**I (Indeterminacy)** — How much is unknown?", 0.0, 1.0, 0.3, 0.05)
            f = st.slider("**F (Falsity)** — How much is contradicted?", 0.0, 1.0, 0.1, 0.05)
    else:
        t, i, f = 0.5, 0.3, 0.1

# Visualization column
with col_viz:
    zone_key = classify_zone(t, i, f)
    zone = ZONE_INFO[zone_key]

    st.markdown(f"""
    <div style="background: {zone['color']}15; border: 2px solid {zone['color']};
                border-radius: 16px; padding: 1.5rem; text-align: center; margin-bottom: 1rem;">
        <div style="font-size: 3rem;">{zone['emoji']}</div>
        <div style="font-size: 1.5rem; font-weight: 800; color: {zone['color']};">{zone['name']}</div>
        <div style="font-size: 1rem; font-weight: 600; margin-top: 0.5rem;">{zone['action']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Show reason if auto
    if mode == "🤖 AI Auto-Analysis (Groq)" and st.session_state.get("tif_result"):
        r = st.session_state["tif_result"]
        if r.get("zone_reason"):
            st.info(f"**Why this zone:** {r['zone_reason']}")
        rec = r.get("recommendation", "")
        rec_map = {
            "trust": ("🟢", "You can generally trust this"),
            "investigate": ("🟡", "Investigate before relying on this"),
            "consult_expert": ("🟠", "Consult a domain expert"),
            "do_not_use": ("🔴", "Do NOT use for decisions"),
        }
        if rec in rec_map:
            emoji, text = rec_map[rec]
            st.markdown(f"**Recommendation:** {emoji} {text}")

    fig = create_radar_chart(t, i, f, zone["color"])
    st.plotly_chart(fig, use_container_width=True)

    fig_bar = create_comparison_bar(t, i, f)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# Zone details
st.markdown(f"### {zone['emoji']} Zone: {zone['name']}")
st.markdown(f"**{zone['description']}**")
st.markdown("**What to do:**")
for item in zone["what_to_do"]:
    st.markdown(f"- {item}")

confidence = max(0, t - i - f)
st.divider()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Truth (T)", f"{t:.2f}")
with c2:
    st.metric("Indeterminacy (I)", f"{i:.2f}")
with c3:
    st.metric("Falsity (F)", f"{f:.2f}")
with c4:
    st.metric("Confidence C(σ)", f"{confidence:.2f}", help="C = max(0, T - I - F)")

st.caption("From *The Third Answer* by Leyva-Vazquez & Smarandache (2026) | Powered by Groq (free)")
