"""
AI service — NLP extraction & image analysis.

PRIMARY:   Internal Knowledge Base (keyword_classifier, complaint_categories)
OPTIONAL:  Google Gemini API for enhanced analysis
FALLBACK:  KB always works offline — zero external API dependency
"""

import json
import logging
from typing import Optional

from app.knowledge_base.keyword_classifier import (
    classify_complaint,
    check_duplicate_local,
    summarize_text,
)
from app.knowledge_base.complaint_categories import get_subcategory_match
from app.knowledge_base.governance_policies import get_department

logger = logging.getLogger(__name__)

_model = None
_gemini_available = False


def _get_model():
    """Lazy-init the Gemini model (optional enhancement)."""
    global _model, _gemini_available
    if _model is None:
        try:
            import google.generativeai as genai
            from app.config import settings

            if not getattr(settings, "GEMINI_API_KEY", None):
                logger.info("No GEMINI_API_KEY — running in KB-only mode")
                _gemini_available = False
                return None

            genai.configure(api_key=settings.GEMINI_API_KEY)
            _model = genai.GenerativeModel("gemini-1.5-flash")
            _gemini_available = True
        except Exception as e:
            logger.warning(f"Gemini init failed — KB-only mode: {e}")
            _gemini_available = False
    return _model


def _parse_json(text: str) -> dict:
    """Best-effort parse JSON from LLM output (strip markdown fences)."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
    if cleaned.endswith("```"):
        cleaned = cleaned.rsplit("```", 1)[0]
    cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("Failed to parse LLM JSON, returning raw text")
        return {"raw_response": text}


# ─────────────────────────────────────────────────────────
# Complaint NLP extraction
# ─────────────────────────────────────────────────────────

async def extract_complaint_details(
    raw_text: str,
    source_language: str = "auto",
) -> dict:
    """
    Extract structured information from raw complaint text.
    Works with Hindi, English, or any Indian regional language input.

    Strategy: KB classifier first → optionally enhance with Gemini.
    """
    # ── STEP 1: Knowledge-Base classification (always works) ──
    kb_result = classify_complaint(raw_text)
    dept = get_department(kb_result.get("category", "Other"))

    result = {
        "summary_english": kb_result.get("summary_en", raw_text[:200]),
        "summary_hindi": kb_result.get("summary_hi", ""),
        "category": kb_result.get("category", "Other"),
        "category_confidence": kb_result.get("confidence", 0.5),
        "location_text": kb_result.get("location"),
        "ward_number": kb_result.get("ward_number"),
        "duration_days": kb_result.get("duration_days"),
        "severity_keywords": kb_result.get("severity_keywords", []),
        "affected_estimate": kb_result.get("impact", "individual"),
        "is_emergency": kb_result.get("is_emergency", False),
        "requires_department": dept.get("name_en", "General Administration"),
        "source": "knowledge_base",
    }

    # ── STEP 2: Optional Gemini enhancement ──────────────
    model = _get_model()
    if model and _gemini_available:
        try:
            prompt = f"""
You are an AI assistant for a local governance complaint management system in India.

Analyze the following citizen complaint and extract structured information.
The complaint may be in Hindi, English, or any Indian regional language.

COMPLAINT TEXT: \"{raw_text}\"

Extract and return a JSON object with these fields:
{{
    "summary_english": "Brief summary in English (1-2 sentences)",
    "summary_hindi": "Brief summary in Hindi (1-2 sentences)",
    "category": "One of: Water Supply, Road/Pothole, Electricity, Drainage, Garbage, Health, Public Safety, Other",
    "category_confidence": 0.0 to 1.0,
    "location_text": "Extracted location/area/ward name from complaint or null",
    "ward_number": null or integer if mentioned,
    "duration_days": null or integer (how long the problem has existed),
    "severity_keywords": ["list", "of", "severity", "indicators"],
    "affected_estimate": "individual / family / street / colony / ward",
    "is_emergency": true or false,
    "requires_department": "Water Dept / Roads Dept / Electricity Dept / Health Dept / Sanitation Dept / General"
}}

Return ONLY the JSON object. No markdown, no explanation.
"""
            response = model.generate_content(prompt)
            gemini_data = _parse_json(response.text)

            # Merge: prefer Gemini for summaries & confidence, keep KB for structure
            if gemini_data.get("summary_english"):
                result["summary_english"] = gemini_data["summary_english"]
            if gemini_data.get("summary_hindi"):
                result["summary_hindi"] = gemini_data["summary_hindi"]
            if gemini_data.get("category_confidence", 0) > result["category_confidence"]:
                result["category"] = gemini_data.get("category", result["category"])
                result["category_confidence"] = gemini_data["category_confidence"]
            result["source"] = "knowledge_base+gemini"
        except Exception as e:
            logger.warning(f"Gemini enhancement failed, using KB result: {e}")

    return result


# ─────────────────────────────────────────────────────────
# Image complaint analysis
# ─────────────────────────────────────────────────────────

async def analyze_image_complaint(image_path: str) -> dict:
    """
    Analyze a complaint photo.
    Uses Gemini Vision if available, otherwise returns a KB-based placeholder
    prompting manual review.
    """
    model = _get_model()

    if model and _gemini_available:
        try:
            from PIL import Image as PILImage

            image = PILImage.open(image_path)

            prompt = """
You are analyzing a photo submitted as a citizen complaint to local government in India.

Describe:
1. What issue/problem is visible in this image?
2. Category: Water Supply, Road/Pothole, Electricity, Drainage, Garbage, Health, Public Safety, Other
3. Severity: Low, Medium, High, Critical
4. Estimated impact area (small/medium/large)
5. Brief description for official records (1-2 sentences)

Return as JSON:
{
    "issue_description": "...",
    "category": "...",
    "severity": "...",
    "impact_area": "...",
    "official_summary": "..."
}

Return ONLY the JSON object.
"""
            response = model.generate_content([prompt, image])
            result = _parse_json(response.text)
            result["source"] = "gemini_vision"
            return result
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")

    # ── KB fallback: extract what we can from filename / metadata ──
    return {
        "issue_description": "Photo submitted — analysis pending",
        "category": "Other",
        "severity": "Medium",
        "impact_area": "small",
        "official_summary": "Image submitted — requires manual review or Vision API",
        "source": "knowledge_base",
        "requires_manual_review": True,
    }


# ─────────────────────────────────────────────────────────
# Duplicate detection
# ─────────────────────────────────────────────────────────

async def check_duplicate(
    new_summary: str,
    existing_summaries: list[dict],
) -> Optional[dict]:
    """
    Compare a new complaint summary against existing ones.
    Uses KB Jaccard + keyword similarity first, Gemini as enhancement.
    """
    if not existing_summaries:
        return None

    # ── STEP 1: KB-based duplicate check ─────────────────
    existing_for_kb = [
        {"id": s["id"], "text": s["summary"]}
        for s in existing_summaries[:50]
    ]
    kb_dup = check_duplicate_local(new_summary, existing_for_kb, threshold=0.55)
    if kb_dup:
        kb_dup["source"] = "knowledge_base"
        return kb_dup

    # ── STEP 2: Optional Gemini for borderline cases ─────
    model = _get_model()
    if model and _gemini_available:
        summaries_text = "\n".join(
            [f"ID: {s['id']} — {s['summary']}" for s in existing_summaries[:20]]
        )
        prompt = f"""
Compare this new complaint with existing complaints and determine if it is a duplicate.

NEW COMPLAINT: "{new_summary}"

EXISTING COMPLAINTS:
{summaries_text}

Return JSON:
{{
    "is_duplicate": true or false,
    "duplicate_of_id": "id of matching complaint or null",
    "similarity_score": 0.0 to 1.0,
    "reason": "brief explanation"
}}
"""
        try:
            response = model.generate_content(prompt)
            result = _parse_json(response.text)
            result["source"] = "gemini"
            if result.get("is_duplicate") and result.get("similarity_score", 0) > 0.75:
                return result
        except Exception:
            pass

    return None
