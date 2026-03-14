"""
AI-powered communication generator — bilingual (English + Hindi).

PRIMARY:   Knowledge Base response_templates (always works offline)
OPTIONAL:  Gemini API for more natural / creative phrasing
FALLBACK:  KB templates never fail
"""

import json
import logging

from app.knowledge_base.response_templates import render_communication

logger = logging.getLogger(__name__)

_gemini_available = False


def _try_gemini():
    """Check if Gemini is available."""
    global _gemini_available
    try:
        from app.config import settings
        _gemini_available = bool(getattr(settings, "GEMINI_API_KEY", None))
    except Exception:
        _gemini_available = False
    return _gemini_available


async def generate_communication(
    comm_type: str,
    complaint_data: dict,
    format: str = "whatsapp",
) -> dict:
    """
    Generate official public communication in Hindi + English.

    comm_type: ACKNOWLEDGMENT | PROGRESS | COMPLETION | CRISIS_RESPONSE | WEEKLY_DIGEST
    format:    whatsapp | social_media | official_notice

    Strategy: KB templates first → optionally polish with Gemini.
    """
    # ── STEP 1: Render from Knowledge Base templates (always works) ──
    kb_result = render_communication(
        comm_type=comm_type,
        format=format,
        data=complaint_data,
        language="both",
    )

    # ── STEP 2: Try Gemini for a more polished / creative version ──
    _try_gemini()
    if _gemini_available:
        gemini_result = await _gemini_enhance(comm_type, complaint_data, format)
        if gemini_result:
            gemini_result["source"] = "knowledge_base+gemini"
            return gemini_result

    # Return KB result — already fully functional
    return kb_result


async def _gemini_enhance(
    comm_type: str,
    complaint_data: dict,
    format: str,
) -> dict | None:
    """Optional Gemini enhancement for more natural language."""
    format_instructions = {
        "whatsapp": (
            "Keep it under 200 words. Use emojis sparingly (✅, 📍, 🔧). "
            "Simple language. Include ward name and complaint ID."
        ),
        "social_media": (
            "Keep it under 280 characters for X/Twitter. Professional but approachable. "
            "Include relevant hashtags."
        ),
        "official_notice": (
            "Formal tone. Include reference number, department name, "
            "officer in charge, and expected timeline."
        ),
    }

    type_instructions = {
        "ACKNOWLEDGMENT": f"""
Generate an acknowledgment message for a citizen complaint.
Complaint details: {json.dumps(complaint_data, default=str)}
Tone: Empathetic, professional, reassuring.
Include: complaint ID, category, that it has been received and assigned.
""",
        "PROGRESS": f"""
Generate a progress update for ongoing work.
Complaint details: {json.dumps(complaint_data, default=str)}
Tone: Informative, transparent.
Include: what work has been done, current status, expected completion date.
""",
        "COMPLETION": f"""
Generate a work completion announcement.
Complaint details: {json.dumps(complaint_data, default=str)}
Tone: Positive, grateful.
Include: what was done, verification status, thank the citizen.
Mention that before/after proof is available on the public portal.
""",
        "CRISIS_RESPONSE": f"""
Generate a crisis response / counter-statement.
Issue details: {json.dumps(complaint_data, default=str)}
Tone: Calm, factual, authoritative.
Include: acknowledge the concern, provide facts, state what action is being taken.
Do NOT be defensive. Be transparent.
""",
        "WEEKLY_DIGEST": f"""
Generate a weekly governance digest.
Stats: {json.dumps(complaint_data, default=str)}
Tone: Proud but humble. Data-driven.
Include: total complaints received, resolved, in-progress, top issues, trust score.
""",
    }

    prompt = f"""
You are a professional government communication writer for Indian local governance.

Task: Generate a {comm_type} communication.

{type_instructions.get(comm_type, "")}

Format: {format}
{format_instructions.get(format, "")}

Generate in BOTH languages.

Return JSON:
{{
    "content_english": "...",
    "content_hindi": "..."
}}

Make it sound HUMAN — not robotic.
Return ONLY the JSON object.
"""

    try:
        import google.generativeai as genai
        from app.config import settings

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)
        cleaned = response.text.strip().strip("`").strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
        return json.loads(cleaned)
    except Exception as e:
        logger.warning(f"Gemini communication enhancement failed: {e}")
        return None
