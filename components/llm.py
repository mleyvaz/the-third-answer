"""LLM integration via Groq (free, fast, no token cost for free tier)."""
import json
import re
from groq import Groq


SYSTEM_PROMPT = """You are an epistemic analysis engine implementing the Third Answer framework from neutrosophic logic.

For ANY text or claim given to you, you must:

1. Analyze its epistemic quality using three INDEPENDENT dimensions:
   - T (Truth): degree of evidence supporting the claim [0.0 to 1.0]
   - I (Indeterminacy): degree of genuine uncertainty [0.0 to 1.0]
   - F (Falsity): degree of evidence contradicting the claim [0.0 to 1.0]

   IMPORTANT: T + I + F do NOT need to equal 1. They are independent.

2. Classify into one of four zones:
   - "consensus": T > 0.5, I < 0.35, F < 0.3 (solid ground)
   - "ambiguity": I > 0.5 or (I > 0.35 and T < 0.6) (fog)
   - "contradiction": T > 0.3 AND F > 0.3 (crossfire)
   - "ignorance": T < 0.3, F < 0.3, or I overwhelming (darkness)

3. Identify if the text contains any of these error types:
   - "fabrication": invented facts presented as real
   - "distortion": real facts warped or exaggerated
   - "conflation": two true things merged into one false thing
   - "confident_ignorance": response on topic with insufficient data, showing no uncertainty

4. Provide a rewritten "honest" version that includes uncertainty markers.

You MUST respond in valid JSON only:
{
  "T": 0.0,
  "I": 0.0,
  "F": 0.0,
  "zone": "consensus|ambiguity|contradiction|ignorance",
  "zone_reason": "1-2 sentences explaining why this zone",
  "error_types": ["list of detected error types, or empty"],
  "error_explanation": "1-2 sentences if errors found, or empty string",
  "honest_version": "The text rewritten with uncertainty markers and T,I,F assessment embedded",
  "key_claims": [
    {"claim": "specific claim from the text", "T": 0.0, "I": 0.0, "F": 0.0, "note": "brief reason"}
  ],
  "recommendation": "trust|investigate|consult_expert|do_not_use"
}"""


def analyze_with_groq(text: str, api_key: str, context: str = "", model: str = "llama-3.3-70b-versatile") -> dict:
    """Send text to Groq for T,I,F analysis."""
    client = Groq(api_key=api_key)

    user_msg = f"Analyze this AI-generated text using the Third Answer framework:\n\n"
    if context:
        user_msg += f"Context/domain: {context}\n\n"
    user_msg += f"TEXT TO ANALYZE:\n\"\"\"\n{text}\n\"\"\"\n\nRespond ONLY in valid JSON."

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()

    # Extract JSON from response
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    # Try to find JSON object in response
    match = re.search(r'\{[\s\S]*\}', raw)
    if match:
        raw = match.group()

    result = json.loads(raw)

    # Ensure all required fields exist
    result.setdefault("T", 0.5)
    result.setdefault("I", 0.5)
    result.setdefault("F", 0.1)
    result.setdefault("zone", "ambiguity")
    result.setdefault("zone_reason", "")
    result.setdefault("error_types", [])
    result.setdefault("error_explanation", "")
    result.setdefault("honest_version", text)
    result.setdefault("key_claims", [])
    result.setdefault("recommendation", "investigate")

    # Clamp values
    for key in ["T", "I", "F"]:
        result[key] = max(0.0, min(1.0, float(result[key])))

    return result


def analyze_for_label(text: str, api_key: str, domain: str = "general", model: str = "llama-3.3-70b-versatile") -> dict:
    """Analyze pasted AI text and return T,I,F for the Nutrition Label."""
    result = analyze_with_groq(text, api_key, context=domain, model=model)
    result.setdefault("what_i_dont_know", result.get("zone_reason", ""))
    return result


def generate_honest_response(question: str, api_key: str, domain: str = "general", model: str = "llama-3.3-70b-versatile") -> dict:
    """Generate an honest response WITH T,I,F assessment built in."""
    client = Groq(api_key=api_key)

    system = """You answer questions honestly using the Third Answer framework.

For every response:
1. Answer the question as accurately as you can
2. For each key claim, indicate your certainty level:
   - "Well-established" (T > 0.8, I < 0.15)
   - "Likely but debated" (T > 0.5, I > 0.2 or F > 0.2)
   - "Uncertain" (I > 0.5)
   - "Contradicted" (T > 0.3 AND F > 0.3)
   - "I don't have reliable information" (I > 0.6, T < 0.3)
3. At the end, provide overall assessment

Respond in JSON:
{
  "answer": "Your detailed answer with inline uncertainty markers",
  "T": 0.0,
  "I": 0.0,
  "F": 0.0,
  "zone": "consensus|ambiguity|contradiction|ignorance",
  "zone_reason": "Why this zone",
  "claims": [
    {"claim": "...", "certainty": "well-established|debated|uncertain|contradicted|unreliable", "T": 0.0, "I": 0.0, "F": 0.0}
  ],
  "recommendation": "trust|investigate|consult_expert|do_not_use",
  "what_i_dont_know": "Explicit statement of what is unknown or uncertain"
}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Domain: {domain}\nQuestion: {question}\n\nRespond in JSON."},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()
    match = re.search(r'\{[\s\S]*\}', raw)
    if match:
        raw = match.group()

    result = json.loads(raw)
    for key in ["T", "I", "F"]:
        result.setdefault(key, 0.5)
        result[key] = max(0.0, min(1.0, float(result[key])))
    result.setdefault("zone", "ambiguity")
    result.setdefault("answer", "")
    result.setdefault("claims", [])
    result.setdefault("recommendation", "investigate")
    result.setdefault("what_i_dont_know", "")

    return result
