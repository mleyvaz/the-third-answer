"""About the book and authors."""
import streamlit as st

st.set_page_config(page_title="About", page_icon="📖", layout="wide")

st.markdown("# 📖 About The Third Answer")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### The Book

    **The Third Answer: Why AI Doesn't Know What It Doesn't Know — And How Ancient Logic Can Fix It**

    *A Framework for Thinking Clearly in the Age of Confident Machines*

    **Authors:** Maikel Yelandi Leyva-Vazquez, PhD & Florentin Smarandache, PhD
    **Year:** 2026 | **ISBN:** [pending]

    ---

    ### Structure

    | Part | Chapter | Topic |
    |------|---------|-------|
    | **PART ONE: THE PROBLEM** | 1. The Confident Machine | Why AI can't say "I don't know" |
    | | 2. True, False, and the Third Answer | The T,I,F framework and Four Zones |
    | **PART TWO: THE ROOTS** | 3. The Monks Who Doubted | Scholastic philosophy and uncertainty |
    | | 4. Neither One Nor the Other | Latin American philosophy and complementarity |
    | **PART THREE: THE FRAMEWORK** | 5. A Compass for Uncertainty | The T,I,F Quick Reference |
    | | 6. When to Trust, When to Doubt, When to Abstain | Decision framework |
    | **PART FOUR: THE FUTURE** | 7. The Honest Machine | Building AI that expresses uncertainty |
    | **APPENDICES** | A. T,I,F Quick Reference Card | Pocket guide |
    | | B. Prompt Templates | Ready-to-use uncertainty-aware prompts |
    | | C. For the Technically Curious | Mathematical foundations |
    | | D. Further Reading | Annotated bibliography |
    """)

with col2:
    st.markdown("### Key Concepts")

    concepts = {
        "Architecture of Overconfidence": "AI uses the same mechanism for true and false statements. No internal switch between 'reliable mode' and 'guessing mode'.",
        "The Third Answer": "Between True and False lies a space that is not empty — it's full. T, I, F: Truth, Indeterminacy, Falsity.",
        "Four Zones": "Consensus, Ambiguity, Contradiction, Ignorance. Each requires a different action.",
        "Confident Ignorance": "The most dangerous AI error type: the model produces a response without reliable information AND without any signal of uncertainty.",
        "WYSIATI": "Kahneman's 'What You See Is All There Is' — the human version of the same flaw that afflicts LLMs.",
        "Paraconsistency": "The capacity to hold contradictory information without the system collapsing. T and F can BOTH be high.",
    }

    for concept, desc in concepts.items():
        with st.expander(concept):
            st.markdown(desc)

st.divider()

# Authors
st.markdown("### The Authors")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    #### Maikel Yelandi Leyva-Vazquez, PhD

    Professor and Researcher. Universidad Bolivariana del Ecuador & Universidad de Guayaquil (GIIAR).
    President of the Latin American Association of Neutrosophic Sciences. 291+ publications, 9,380+ citations.

    Research: Neutrosophic logic, Fuzzy Cognitive Maps, AI in Education, Machine Learning, Dynamic Epistemic Logic (LED).

    - [Google Scholar](https://scholar.google.com/citations?user=5VlnGwcAAAAJ)
    - [ORCID: 0000-0001-5401-0018](https://orcid.org/0000-0001-5401-0018)
    - [ResearchGate](https://www.researchgate.net/profile/Maikel-Leyva-Vazquez)
    """)

with col_b:
    st.markdown("""
    #### Florentin Smarandache, PhD

    Professor of Mathematics. University of New Mexico, Gallup Campus, USA.
    Creator of neutrosophic logic (1995). Thousands of published papers. Multiple journals and applications across dozens of disciplines.

    Research: Neutrosophy, NeutroGeometry, NeutroAlgebra, Mathematical Philosophy.

    - [ORCID: 0000-0002-5560-5926](https://orcid.org/0000-0002-5560-5926)
    - [UNM Page](https://fs.unm.edu/FlorentinSmarandache.htm)
    """)

st.divider()

st.markdown("""
### This App

This interactive web application is a companion to the book. It implements the frameworks
described in each chapter:

- **T,I,F Compass** → Chapter 2 (the three-needle compass)
- **Four Zones** → Chapter 2 (Consensus, Ambiguity, Contradiction, Ignorance)
- **Error Detector** → Chapter 1 (four types of AI error)
- **Prompt Templates** → Appendix B (uncertainty-aware prompts)
- **The Honest Machine** → Chapter 7 (before/after comparison)

Built with [Streamlit](https://streamlit.io) (Python).

---

*"The machine will not tell you when it is guessing. After this book, you will not need it to."*
""")
