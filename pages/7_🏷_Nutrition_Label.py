"""Epistemic Nutrition Label — Generate a visual T,I,F label for any AI output."""
import streamlit as st
import streamlit.components.v1 as components
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.tif_calculator import classify_zone, ZONE_INFO
from components.visualizations import create_radar_chart

st.set_page_config(page_title="Epistemic Nutrition Label", page_icon="🏷", layout="wide")

st.markdown("# 🏷 Epistemic Nutrition Label")
st.markdown("*The FDA regulates what you eat. This regulates the epistemic quality of what AI tells you.*")
st.divider()

# CSS is now embedded inline in render_label_html() for iframe rendering


def render_label_html(t, i, f, zone_key, claim_text="", source_info=""):
    """Generate the Epistemic Nutrition Label as a full standalone HTML page for iframe rendering."""
    zone = ZONE_INFO[zone_key]
    is_para = (t + f) > 1.0
    confidence = max(0.0, t - i - f)

    bar_color_t = "#22c55e"
    bar_color_i = "#eab308"
    bar_color_f = "#ef4444"

    para_html = ""
    if is_para:
        para_html = f'<div style="text-align:center;padding:6px 0;font-size:0.85rem;font-weight:700;color:#f97316;">&#9888; PARACONSISTENT (T+F = {t+f:.2f} &gt; 1.0)</div>'

    claim_html = ""
    if claim_text:
        short = claim_text[:80] + "..." if len(claim_text) > 80 else claim_text
        claim_html = f'<div style="padding:8px 0;font-size:0.85rem;color:#475569;border-bottom:1px solid #e2e8f0;font-style:italic;">&ldquo;{short}&rdquo;</div>'

    source_html = ""
    if source_info:
        source_html = f'<div style="font-size:0.75rem;color:#64748b;padding:4px 0;">{source_info}</div>'

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
body {{ margin:0; padding:10px; font-family:'Helvetica Neue',Arial,sans-serif; background:transparent; }}
.enl {{ max-width:400px; border:3px solid #1e293b; border-radius:12px; background:#fff; margin:0 auto; }}
.hdr {{ background:#1e293b; color:#fff; padding:12px 16px; border-radius:9px 9px 0 0; text-align:center; font-size:1.05rem; font-weight:800; letter-spacing:1px; }}
.bdy {{ padding:16px 20px; }}
.row {{ display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid #e2e8f0; }}
.lbl {{ font-weight:600; font-size:0.9rem; color:#334155; }}
.val {{ font-weight:800; font-size:1.05rem; }}
.bar-c {{ width:130px; height:14px; background:#e2e8f0; border-radius:7px; overflow:hidden; display:inline-block; vertical-align:middle; margin-right:6px; }}
.bar {{ height:100%; border-radius:7px; }}
.zone {{ text-align:center; padding:12px 0; margin-top:8px; border-top:2px solid #1e293b; }}
.ftr {{ background:#f8fafc; padding:8px 16px; border-radius:0 0 9px 9px; text-align:center; font-size:0.7rem; color:#94a3b8; }}
</style></head><body>
<div class="enl">
  <div class="hdr">EPISTEMIC NUTRITION LABEL</div>
  <div class="bdy">
    {claim_html}
    <div class="row"><span class="lbl">Truth (T)</span><span><span class="bar-c"><span class="bar" style="width:{t*100}%;background:{bar_color_t};"></span></span><span class="val" style="color:{bar_color_t};">{t:.2f}</span></span></div>
    <div class="row"><span class="lbl">Indeterminacy (I)</span><span><span class="bar-c"><span class="bar" style="width:{i*100}%;background:{bar_color_i};"></span></span><span class="val" style="color:{bar_color_i};">{i:.2f}</span></span></div>
    <div class="row"><span class="lbl">Falsity (F)</span><span><span class="bar-c"><span class="bar" style="width:{f*100}%;background:{bar_color_f};"></span></span><span class="val" style="color:{bar_color_f};">{f:.2f}</span></span></div>
    <div class="row"><span class="lbl">Confidence</span><span class="val" style="color:#334155;">{confidence:.2f}</span></div>
    {para_html}
    <div class="zone">
      <div style="font-size:2rem;">{zone['emoji']}</div>
      <div style="font-size:1.2rem;font-weight:800;color:{zone['color']};">{zone['name']}</div>
      <div style="font-size:0.8rem;color:#64748b;margin-top:4px;">{zone['action']}</div>
    </div>
    {source_html}
  </div>
  <div class="ftr">Powered by thirdanswer | Leyva-Vazquez &amp; Smarandache (2026)</div>
</div>
</body></html>"""


def show_label(t, i, f, zone_key, claim_text="", source_info=""):
    """Render the label using components.html (iframe) so CSS renders correctly."""
    html = render_label_html(t, i, f, zone_key, claim_text, source_info)
    components.html(html, height=420, scrolling=False)


# === TABS ===
tab_manual, tab_ai, tab_examples = st.tabs([
    "✏️ Manual (enter T,I,F)",
    "🤖 AI-Powered (paste text)",
    "📚 Gallery (pre-built examples)",
])

# --- TAB 1: Manual ---
with tab_manual:
    st.markdown("### Generate a label from T,I,F values")
    st.caption("Set the three dimensions manually — great for presentations, papers, or workshops")

    col_input, col_label = st.columns([1, 1])

    with col_input:
        claim = st.text_input("Claim or AI output (optional):",
                              placeholder="e.g., Coffee is good for your health")
        t_val = st.slider("Truth (T)", 0.0, 1.0, 0.55, 0.05)
        i_val = st.slider("Indeterminacy (I)", 0.0, 1.0, 0.30, 0.05)
        f_val = st.slider("Falsity (F)", 0.0, 1.0, 0.45, 0.05)
        source = st.text_input("Source info (optional):",
                               placeholder="e.g., 14 studies support, 9 contradict")

    with col_label:
        zone_key = classify_zone(t_val, i_val, f_val)
        show_label(t_val, i_val, f_val, zone_key, claim, source)

        st.markdown("")
        fig = create_radar_chart(t_val, i_val, f_val, ZONE_INFO[zone_key]["color"])
        st.plotly_chart(fig, use_container_width=True)

    # What to do
    zone = ZONE_INFO[zone_key]
    st.divider()
    st.markdown(f"### {zone['emoji']} {zone['name']} — What to do")
    for item in zone["what_to_do"]:
        st.markdown(f"- {item}")

# --- TAB 2: AI-Powered ---
with tab_ai:
    st.markdown("### Paste any AI output and get its Nutrition Label")
    st.caption("Uses Groq (free) to analyze the text and generate T,I,F values automatically")

    with st.sidebar:
        groq_key = st.secrets.get("GROQ_API_KEY", "")
        if not groq_key or groq_key == "REPLACE_WITH_NEW_KEY_AFTER_REVOKING":
            groq_key = st.text_input("🔑 Groq API Key", type="password",
                                     help="Free at console.groq.com", key="label_groq_key")

    ai_text = st.text_area(
        "Paste AI-generated text here:",
        height=200,
        placeholder="Paste any response from ChatGPT, Claude, Gemini, etc. and we'll generate its Epistemic Nutrition Label...",
    )

    ai_domain = st.selectbox("Domain context:", [
        "general", "medicine", "education", "policy", "technology", "research"
    ], key="label_domain")

    if st.button("🏷 Generate Nutrition Label", type="primary",
                 disabled=not groq_key or not ai_text):
        with st.spinner("Analyzing epistemic quality (~3 sec)..."):
            try:
                from components.llm import analyze_for_label
                result = analyze_for_label(ai_text, groq_key, ai_domain)
                st.session_state["label_result"] = result
                st.session_state["label_text"] = ai_text
            except AttributeError:
                # Fallback: use the existing generate_honest_response
                from components.llm import generate_honest_response
                result = generate_honest_response(
                    f"Analyze this text for epistemic quality: {ai_text[:500]}",
                    groq_key, ai_domain,
                    "llama-3.3-70b-versatile"
                )
                st.session_state["label_result"] = result
                st.session_state["label_text"] = ai_text
            except Exception as e:
                st.error(f"Error: {e}")

    if "label_result" in st.session_state:
        r = st.session_state["label_result"]
        t_v, i_v, f_v = r["T"], r["I"], r["F"]
        zk = classify_zone(t_v, i_v, f_v)

        col_l, col_r = st.columns([1, 1])
        with col_l:
            show_label(t_v, i_v, f_v, zk,
                       st.session_state.get("label_text", "")[:100])
        with col_r:
            fig = create_radar_chart(t_v, i_v, f_v, ZONE_INFO[zk]["color"])
            st.plotly_chart(fig, use_container_width=True)

            zone = ZONE_INFO[zk]
            st.markdown(f"### {zone['emoji']} {zone['name']}")
            st.markdown(f"**Action:** {zone['action']}")
            if r.get("what_i_dont_know"):
                st.warning(f"**What the AI didn't know:** {r['what_i_dont_know']}")

# --- TAB 3: Gallery ---
with tab_examples:
    st.markdown("### Gallery — Epistemic Nutrition Labels for Common AI Claims")
    st.caption("No API key needed — pre-computed labels from the book")

    gallery = [
        {
            "claim": "The MMR vaccine causes autism",
            "t": 0.02, "i": 0.03, "f": 0.95,
            "source": "Retracted (Wakefield 1998). Millions of children studied, no link found.",
        },
        {
            "claim": "Coffee is good for your health",
            "t": 0.55, "i": 0.30, "f": 0.45,
            "source": "14 meta-analyses support benefits; 9 show risks for specific populations.",
        },
        {
            "claim": "Remote work is more productive than office work",
            "t": 0.55, "i": 0.25, "f": 0.55,
            "source": "Stanford 2013 +13% (call center). Microsoft 2023 -18% (engineers). Depends on context.",
        },
        {
            "claim": "Quantum computing will break encryption within 5 years",
            "t": 0.15, "i": 0.65, "f": 0.30,
            "source": "Current: ~1000 noisy qubits. Need: millions of error-corrected. Most experts: 10-20+ years.",
        },
        {
            "claim": "GPT-4 passes the bar exam in the 90th percentile",
            "t": 0.70, "i": 0.20, "f": 0.35,
            "source": "OpenAI reported 90th percentile. Independent analyses show performance varies by section.",
        },
        {
            "claim": "The prevalence of Chagas disease in Manabi is 2.3%",
            "t": 0.20, "i": 0.70, "f": 0.15,
            "source": "National Ecuador ~1.4% (WHO). Province-specific data for Manabi is sparse.",
        },
    ]

    cols = st.columns(2)
    for idx, item in enumerate(gallery):
        zk = classify_zone(item["t"], item["i"], item["f"])
        with cols[idx % 2]:
            show_label(item["t"], item["i"], item["f"], zk,
                       item["claim"], item["source"])
            st.markdown("")

st.divider()
st.markdown("""
### Why an Epistemic Nutrition Label?

The FDA requires every food product to display its nutritional content: calories, fat, protein, sugar.
You don't need to be a nutritionist to read the label — **the format does the work**.

AI outputs have no equivalent. A model can respond with the same syntactic confidence whether
it is retrieving a well-replicated medical finding or fabricating a plausible-sounding statistic.
The user has no signal.

The Epistemic Nutrition Label fills this gap. Three bars — Truth, Indeterminacy, Falsity —
a zone classification, and a recommended action. **Readable in 5 seconds. Auditable. Standardizable.**

> *"The FDA regulates what you eat. Who regulates the epistemic quality of what AI tells you?"*

---
📖 From Chapter 7 of *The Third Answer* | 🔬 Implemented in `thirdanswer` Python library (`pip install thirdanswer`)
""")
st.caption("Powered by thirdanswer | Leyva-Vazquez & Smarandache (2026)")
