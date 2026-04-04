"""Prompt Templates for Uncertainty-Aware AI Use — Appendix B."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from components.tif_calculator import PROMPT_TEMPLATES

st.set_page_config(page_title="Prompt Templates", page_icon="📋", layout="wide")

st.markdown("# 📋 Prompt Templates")
st.markdown("*Ready-to-use prompts that force AI to express uncertainty (Appendix B)*")
st.divider()

st.info("**How to use:** Select a template, type your question, and copy the generated prompt. Paste it into ChatGPT, Claude, Gemini, or any AI chatbot.")

# Template selector
template_key = st.selectbox(
    "Select a domain template:",
    list(PROMPT_TEMPLATES.keys()),
    format_func=lambda x: PROMPT_TEMPLATES[x]["name"],
)

template = PROMPT_TEMPLATES[template_key]

st.markdown(f"### {template['name']}")

# User question
question = st.text_input(
    "Your question:",
    placeholder="Type the question you want to ask the AI...",
)

if question:
    filled_prompt = template["prompt"].replace("{question}", question)

    st.markdown("### Generated Prompt (copy this)")
    st.code(filled_prompt, language="text")

    st.download_button(
        "Download prompt as .txt",
        filled_prompt,
        file_name=f"tif_prompt_{template_key}.txt",
        mime="text/plain",
    )
else:
    st.markdown("### Template Preview")
    st.code(template["prompt"], language="text")

st.divider()

# All templates at a glance
st.markdown("### All Templates")

for key, tmpl in PROMPT_TEMPLATES.items():
    with st.expander(f"📋 {tmpl['name']}"):
        st.code(tmpl["prompt"], language="text")

st.divider()

st.markdown("""
### Why These Prompts Work

Standard prompts accept whatever the AI produces. These prompts:

1. **Force the AI to self-assess** — by requiring T, I, F values
2. **Make uncertainty visible** — the AI must name what it doesn't know
3. **Map to action zones** — Consensus, Ambiguity, Contradiction, Ignorance
4. **Domain-specific rules** — medical prompts enforce different standards than research prompts

> *"The machine will not tell you when it is guessing. After this book, you will not need it to."*
> — Preface, The Third Answer
""")

st.caption("From *The Third Answer* by Leyva-Vazquez & Smarandache (2026), Appendix B")
