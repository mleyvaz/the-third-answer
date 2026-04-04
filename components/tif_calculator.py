"""Core T,I,F logic from The Third Answer framework."""


def classify_zone(t, i, f):
    """Classify a T,I,F triple into one of the Four Zones.

    Rules (from Chapter 2):
    - Consensus: T high, I low, F low
    - Ambiguity: I high (overrides others when I > 0.5)
    - Contradiction: T high AND F high
    - Ignorance: all low, or I overwhelming
    """
    if i > 0.5:
        if t < 0.3 and f < 0.3:
            return "ignorance"
        return "ambiguity"
    if t > 0.5 and f > 0.4:
        return "contradiction"
    if t > 0.5 and i < 0.35 and f < 0.3:
        return "consensus"
    if f > 0.5 and t < 0.3:
        return "consensus_false"
    if t < 0.3 and f < 0.3 and i < 0.3:
        return "ignorance"
    if i > 0.35:
        return "ambiguity"
    if t > 0.3 and f > 0.3:
        return "contradiction"
    return "ambiguity"


ZONE_INFO = {
    "consensus": {
        "name": "Consensus",
        "emoji": "🟢",
        "color": "#22c55e",
        "action": "TRUST — but verify sources for critical decisions",
        "description": "Evidence supports the claim. Little uncertainty. Negligible counter-evidence. The ground is solid.",
        "what_to_do": [
            "You can generally rely on this information",
            "For high-stakes decisions, verify the primary source",
            "Check if the consensus is recent (knowledge evolves)",
        ],
    },
    "consensus_false": {
        "name": "Consensus (Against)",
        "emoji": "🔴",
        "color": "#ef4444",
        "action": "REJECT — the evidence contradicts this claim",
        "description": "Strong evidence against the claim. This is likely false or misleading.",
        "what_to_do": [
            "Do not rely on this information",
            "The AI may be presenting misinformation confidently",
            "Verify with authoritative sources",
        ],
    },
    "ambiguity": {
        "name": "Ambiguity",
        "emoji": "🟡",
        "color": "#eab308",
        "action": "INVESTIGATE — the evidence is insufficient",
        "description": "High indeterminacy. The data doesn't exist yet, or is too sparse to resolve. You are in fog.",
        "what_to_do": [
            "Do NOT accept the AI's answer at face value",
            "Look for primary sources and recent research",
            "Consider consulting a domain expert",
            "The AI may be generating plausible-sounding text without reliable basis",
        ],
    },
    "contradiction": {
        "name": "Contradiction",
        "emoji": "🟠",
        "color": "#f97316",
        "action": "INVESTIGATE BOTH SIDES — the evidence conflicts",
        "description": "Both T and F are high. Evidence supports AND contradicts the claim. Different sources point in opposite directions.",
        "what_to_do": [
            "Do not let the AI pick one side for you",
            "Ask: What is the evidence FOR? What is the evidence AGAINST?",
            "The real information is in the tension between positions",
            "Seek the most recent meta-analyses or systematic reviews",
        ],
    },
    "ignorance": {
        "name": "Ignorance",
        "emoji": "⚫",
        "color": "#6b7280",
        "action": "STOP — the AI is operating in the dark",
        "description": "T, I, and F are all low or I is overwhelming. The system has no meaningful information. The text is not grounded in anything.",
        "what_to_do": [
            "Do NOT use this output for any decision",
            "The AI has generated text, but the text is not grounded",
            "Seek human expertise in this domain",
            "This is where 'confident ignorance' is most dangerous",
        ],
    },
}


ERROR_TYPES = {
    "fabrication": {
        "name": "Fabrication",
        "emoji": "🔴",
        "description": "The AI invents something that doesn't exist and presents it as fact.",
        "example": "Citing a legal case that was never filed, or a paper that was never published.",
        "detectability": "Medium — can be caught with a database check",
        "severity": "High",
    },
    "distortion": {
        "name": "Distortion",
        "emoji": "🟠",
        "description": "The AI takes a real fact and warps it — sometimes slightly, sometimes dramatically.",
        "example": "'Moderate evidence of benefit' becomes 'strong evidence of benefit'.",
        "detectability": "Low — requires reading the original source",
        "severity": "High",
    },
    "conflation": {
        "name": "Conflation",
        "emoji": "🟡",
        "description": "The AI merges two true things into one false thing.",
        "example": "A real author paired with a book they didn't write.",
        "detectability": "Medium — caught by verifying individual claims",
        "severity": "Medium",
    },
    "confident_ignorance": {
        "name": "Confident Ignorance",
        "emoji": "⚫",
        "description": "The AI doesn't have reliable information but produces a response anyway, with no signal of uncertainty.",
        "example": "Inventing prevalence statistics for a rare disease in a remote province.",
        "detectability": "Very Low — produces no signal that verification is needed",
        "severity": "Very High — the most dangerous type",
    },
}


PROMPT_TEMPLATES = {
    "general_tif": {
        "name": "General T,I,F Assessment",
        "prompt": """Before answering my question, I want you to assess the epistemic quality of your response using three independent dimensions:

- Truth (T): How much of your answer is supported by strong evidence? (0.0 to 1.0)
- Indeterminacy (I): How much genuine uncertainty exists? (0.0 to 1.0)
- Falsity (F): How much counter-evidence or contradiction exists? (0.0 to 1.0)

These three values are INDEPENDENT — they do not need to add up to 1.

After your answer, provide:
T = [value] | I = [value] | F = [value]
Zone: [Consensus / Ambiguity / Contradiction / Ignorance]
Confidence note: [1-2 sentences explaining WHY you assigned these values]

My question: {question}""",
    },
    "medical": {
        "name": "Medical / Health Query",
        "prompt": """I'm going to ask you a health-related question. Before answering, I need you to be epistemically honest using the Third Answer framework:

For your response, assess:
- T (Truth): How well-supported is this by peer-reviewed medical evidence?
- I (Indeterminacy): How much is still unknown or under-researched?
- F (Falsity): Is there contradicting evidence from credible medical sources?

CRITICAL RULES:
- If I > 0.5, explicitly state: "This topic has significant medical uncertainty. Consult a healthcare professional."
- If T > 0.3 AND F > 0.3, explicitly state: "There is conflicting medical evidence on this topic."
- Never present uncertain medical information with confidence.

Provide at the end:
T = [value] | I = [value] | F = [value]
Zone: [Consensus / Ambiguity / Contradiction / Ignorance]
Recommendation: [Trust / Investigate / Consult Professional / Do Not Use]

My question: {question}""",
    },
    "education": {
        "name": "Education / Academic",
        "prompt": """You are an epistemic tutor. When answering my question, model intellectual honesty:

For each key claim in your answer, indicate your epistemic state:
- "I'm fairly certain about this" (T > 0.7, I < 0.2)
- "This is debated among experts" (T > 0.3 AND F > 0.3)
- "I'm not confident about this — verify with your instructor" (I > 0.5)
- "I don't have reliable information on this" (T < 0.2, I > 0.6)

At the end, provide overall:
T = [value] | I = [value] | F = [value]
Zone: [Consensus / Ambiguity / Contradiction / Ignorance]

My question: {question}""",
    },
    "policy": {
        "name": "Policy / Legal Analysis",
        "prompt": """I need an analysis of a policy/legal topic. Use the Third Answer framework to be transparent about certainty:

Assess your response:
- T: How much is supported by established law, regulation, or strong precedent?
- I: How much involves unresolved legal questions, pending legislation, or jurisdictional ambiguity?
- F: How much is contradicted by competing legal interpretations or recent changes?

Flag explicitly:
- Areas where the law is settled (Consensus zone)
- Areas where legal interpretation varies (Contradiction zone)
- Areas where the legal landscape is evolving (Ambiguity zone)

Provide: T = [value] | I = [value] | F = [value]
Zone: [Consensus / Ambiguity / Contradiction / Ignorance]

My question: {question}""",
    },
    "research": {
        "name": "Research / Scientific",
        "prompt": """As a research assistant, apply epistemic rigor to your answer using the T,I,F framework:

For each claim, assess:
- T (Truth): Strength of supporting evidence (sample sizes, replication, meta-analyses)
- I (Indeterminacy): Open questions, methodological limitations, gaps in literature
- F (Falsity): Contradicting studies, failed replications, competing theories

IMPORTANT:
- Distinguish between "well-replicated finding" (T high) and "single study" (I high)
- Flag the replication crisis where relevant
- If citing studies, note if they are pre-prints vs peer-reviewed

Provide: T = [value] | I = [value] | F = [value]
Zone: [Consensus / Ambiguity / Contradiction / Ignorance]
Evidence quality: [Strong / Moderate / Weak / Insufficient]

My question: {question}""",
    },
}
