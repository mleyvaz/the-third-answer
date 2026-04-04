"""The Honest Machine — Ask questions and get honest T,I,F responses."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.tif_calculator import classify_zone, ZONE_INFO
from components.visualizations import create_radar_chart

st.set_page_config(page_title="The Honest Machine", page_icon="🤖", layout="wide")

st.markdown("# 🤖 The Honest Machine")
st.markdown("*Ask any question and get a response WITH uncertainty assessment — Chapter 7 in action*")
st.divider()

# API Key (hidden from users via secrets)
with st.sidebar:
    groq_key = st.secrets.get("GROQ_API_KEY", "")
    if groq_key and groq_key != "REPLACE_WITH_NEW_KEY_AFTER_REVOKING":
        pass  # Key loaded silently
    else:
        groq_key = st.text_input("🔑 Groq API Key", type="password",
                                 help="Free at console.groq.com")
    if not groq_key:
        st.success("Key loaded")

    model = st.selectbox("Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
        "mixtral-8x7b-32768",
    ])

# Tabs: Live demo vs Pre-built examples
tab_live, tab_examples = st.tabs(["🔴 Live Demo (ask anything)", "📚 Pre-built Examples (no key needed)"])

with tab_live:
    st.markdown("### Ask The Honest Machine")
    st.caption("The LLM answers your question AND tells you what it doesn't know")

    domain = st.selectbox("Domain:", ["general", "medicine", "education", "policy", "technology", "research"])

    question = st.text_input(
        "Your question:",
        placeholder="e.g., Is coffee good for your health? / What is the prevalence of Chagas in Manabi?",
    )

    if st.button("🤖 Ask The Honest Machine", type="primary", disabled=not groq_key or not question):
        with st.spinner("Generating honest response (~3 sec, free via Groq)..."):
            try:
                from components.llm import generate_honest_response
                result = generate_honest_response(question, groq_key, domain, model)
                st.session_state["honest_result"] = result
                st.session_state["honest_question"] = question
            except Exception as e:
                st.error(f"Error: {e}")

    if "honest_result" in st.session_state:
        r = st.session_state["honest_result"]
        t_val, i_val, f_val = r["T"], r["I"], r["F"]
        zone_key = classify_zone(t_val, i_val, f_val)
        zone = ZONE_INFO[zone_key]

        col_answer, col_assess = st.columns([2, 1])

        with col_answer:
            st.markdown(f"**Q:** *{st.session_state.get('honest_question', '')}*")
            st.divider()

            # The answer
            st.markdown("#### Answer")
            st.markdown(r.get("answer", ""))

            # What the machine doesn't know
            if r.get("what_i_dont_know"):
                st.warning(f"**What I don't know:** {r['what_i_dont_know']}")

            # Claim-by-claim
            if r.get("claims"):
                st.markdown("#### Claim-by-Claim Certainty")
                for claim in r["claims"]:
                    certainty = claim.get("certainty", "uncertain")
                    colors = {
                        "well-established": "🟢",
                        "debated": "🟠",
                        "uncertain": "🟡",
                        "contradicted": "🔴",
                        "unreliable": "⚫",
                    }
                    icon = colors.get(certainty, "🟡")
                    ct = claim.get("T", 0.5)
                    ci = claim.get("I", 0.5)
                    cf = claim.get("F", 0.1)
                    st.markdown(f"{icon} **{certainty.upper()}** — {claim.get('claim', '')}")
                    st.caption(f"T={ct:.2f} I={ci:.2f} F={cf:.2f}")

        with col_assess:
            # Zone card
            st.markdown(f"""
            <div style="background: {zone['color']}15; border: 2px solid {zone['color']};
                        border-radius: 16px; padding: 1.2rem; text-align: center;">
                <div style="font-size: 2.5rem;">{zone['emoji']}</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: {zone['color']};">{zone['name']}</div>
                <div style="font-size: 0.9rem; margin-top: 0.3rem;">{zone['action']}</div>
            </div>
            """, unsafe_allow_html=True)

            if r.get("zone_reason"):
                st.info(f"{r['zone_reason']}")

            # Radar
            fig = create_radar_chart(t_val, i_val, f_val, zone["color"])
            st.plotly_chart(fig, use_container_width=True)

            # Metrics
            st.metric("Truth (T)", f"{t_val:.2f}")
            st.metric("Indeterminacy (I)", f"{i_val:.2f}")
            st.metric("Falsity (F)", f"{f_val:.2f}")

            # Recommendation
            rec = r.get("recommendation", "investigate")
            rec_map = {
                "trust": ("🟢", "Trust this response"),
                "investigate": ("🟡", "Investigate further"),
                "consult_expert": ("🟠", "Consult an expert"),
                "do_not_use": ("🔴", "Do NOT use this"),
            }
            if rec in rec_map:
                emoji, text = rec_map[rec]
                st.markdown(f"### {emoji} {text}")

with tab_examples:
    st.markdown("### Pre-built Examples (no API key needed)")
    st.caption("See what honest AI responses look like — from Chapter 7")

    examples = [
        {
            "question": "What is the FDA-approved first-line treatment for type 2 diabetes with cardiovascular disease?",
            "domain": "Medicine",
            "standard": "The FDA-approved first-line treatment is metformin, combined with GLP-1 receptor agonists such as liraglutide or semaglutide, which have demonstrated cardiovascular benefits in clinical trials.",
            "honest": "The first-line treatment is metformin, often combined with GLP-1 agonists (liraglutide, semaglutide) with demonstrated cardiovascular benefits.\n\n**Well-established** — ADA 2024 guidelines, multiple large-scale trials (LEADER, SUSTAIN-6).",
            "t": 0.85, "i": 0.10, "f": 0.05,
        },
        {
            "question": "What is the prevalence of Chagas disease in Manabi province, Ecuador?",
            "domain": "Public Health",
            "standard": "The prevalence of Chagas disease in Manabi province is approximately 2.3% of the rural population, based on seroprevalence studies conducted in the coastal lowlands.",
            "honest": "National seroprevalence for Ecuador is ~1.4% (WHO). **Province-specific data for Manabi is sparse.** The '2.3%' figure may be interpolated — no large-scale seroprevalence study specific to Manabi was found.\n\n⚠️ **Verify with MSP Ecuador before use.**\n\n**What I don't know:** Whether a Manabi-specific study exists in the PAHO database.",
            "t": 0.25, "i": 0.65, "f": 0.10,
        },
        {
            "question": "Is remote work more productive than office work?",
            "domain": "Business",
            "standard": "Research shows that remote work increases productivity by 13% on average, according to a Stanford study.",
            "honest": "**Evidence FOR:** Stanford/Ctrip 2013 showed +13% (but for call center workers). Multiple surveys show higher self-reported output.\n\n**Evidence AGAINST:** Microsoft 2023 found reduced collaboration. 2024 study showed -18% for engineers. Amazon, Google reversed remote policies.\n\n**The contradiction IS the information.** The answer depends on work type, management, and how you measure productivity.",
            "t": 0.55, "i": 0.25, "f": 0.55,
        },
        {
            "question": "Will quantum computing break current encryption within 5 years?",
            "domain": "Technology",
            "standard": "Yes, quantum computing poses a significant threat to current encryption. Organizations should begin transitioning to post-quantum cryptography now.",
            "honest": "Shor's algorithm **can theoretically** break RSA/ECC. But current quantum computers (~1000 noisy qubits) are far from the scale needed. Most experts estimate **10-20+ years** for cryptographically relevant quantum computers.\n\n**What I don't know:** Whether a non-public breakthrough has occurred. Progress is non-linear.\n\nPost-quantum crypto transition is prudent regardless of timeline.",
            "t": 0.40, "i": 0.55, "f": 0.30,
        },
        {
            "question": "Does the MMR vaccine cause autism?",
            "domain": "Public Health",
            "standard": "The MMR vaccine does not cause autism. Multiple large-scale studies have found no link.",
            "honest": "The MMR vaccine **does not cause autism**. This is one of the most thoroughly investigated claims in modern medicine. Multiple studies (millions of children, multiple countries) found no link. The 1998 Wakefield study was **retracted for fraud**. The author lost his medical license.\n\n**This is Consensus zone** — as settled as medical science gets.",
            "t": 0.05, "i": 0.03, "f": 0.92,
        },
    ]

    for ex in examples:
        zone_key = classify_zone(ex["t"], ex["i"], ex["f"])
        zone = ZONE_INFO[zone_key]

        with st.expander(f"{zone['emoji']} **{ex['domain']}:** {ex['question']}"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown("#### ❌ Standard AI (no uncertainty)")
                st.markdown(f"""<div style="background:#fef2f2; border:1px solid #fca5a5;
                    border-radius:10px; padding:1rem; font-size:0.9rem;">{ex['standard']}</div>""",
                    unsafe_allow_html=True)

                st.markdown("#### ✅ Honest Machine (with T,I,F)")
                st.markdown(f"""<div style="background:#f0fdf4; border:1px solid #86efac;
                    border-radius:10px; padding:1rem; font-size:0.9rem;">{ex['honest']}</div>""",
                    unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div style="background:{zone['color']}15; border:2px solid {zone['color']};
                    border-radius:12px; padding:1rem; text-align:center;">
                    <div style="font-size:2rem;">{zone['emoji']}</div>
                    <strong style="color:{zone['color']};">{zone['name']}</strong><br>
                    <code>T={ex['t']:.2f} I={ex['i']:.2f} F={ex['f']:.2f}</code>
                </div>""", unsafe_allow_html=True)

                fig = create_radar_chart(ex["t"], ex["i"], ex["f"], zone["color"])
                st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("""
> *"The machine will not tell you when it is guessing. After this book, you will not need it to."*
> — Preface, The Third Answer
""")
st.caption("Powered by Groq (free) | Leyva-Vazquez & Smarandache (2026)")
