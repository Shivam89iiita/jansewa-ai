"""
Local NLP & Keyword Classification Engine
==========================================
Zero-dependency text analysis — no external APIs.
- Category classification from keywords (Hindi + English + transliterated)
- Severity detection from urgency phrases
- Location extraction
- Duration parsing
- Impact estimation
- Emergency detection
- Text summarization
- Duplicate detection via Jaccard similarity
"""

import re
import logging
from typing import Optional
from collections import Counter

from app.knowledge_base.complaint_categories import (
    CATEGORIES,
    get_subcategory_match,
)
from app.knowledge_base.ward_database import get_ward_by_location

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# SEVERITY / URGENCY KEYWORDS
# ─────────────────────────────────────────────────────────

EMERGENCY_KEYWORDS = [
    # English
    "emergency", "urgent", "immediately", "life threatening", "dying",
    "collapse", "collapsing", "fire", "flood", "electrocution",
    "accident", "death", "dead", "unconscious", "ambulance",
    "gas leak", "chemical spill", "explosion", "drowning",
    # Hindi / Transliterated
    "emergency", "turant", "jaldi karo", "khatarnak", "maut",
    "aag lagi", "bijli ka jhatka", "baarh", "hadsa", "mar gaya",
    "gir gaya", "jaan ka khatra", "bachao", "madad karo",
    "tatkaal", "bahut zaruri",
]

HIGH_URGENCY_KEYWORDS = [
    "critical", "severe", "dangerous", "hazardous", "unbearable",
    "serious", "major", "extreme", "desperate", "worst",
    "health risk", "children suffering", "elderly affected",
    "bahut bura", "khatarnak", "gambhir", "bahut pareshan",
    "bachche beemar", "boodhe pareshan", "asahaniya",
]

DURATION_PATTERNS = [
    # English
    (r"(\d+)\s*(?:day|days|din)\s*(?:ago|se|since)?", "days"),
    (r"(\d+)\s*(?:week|weeks|hafte)\s*(?:ago|se|since)?", "weeks"),
    (r"(\d+)\s*(?:month|months|mahine)\s*(?:ago|se|since)?", "months"),
    (r"(\d+)\s*(?:hour|hours|ghante)\s*(?:ago|se|since)?", "hours"),
    (r"since\s*(\d+)\s*(?:day|days)", "days"),
    (r"past\s*(\d+)\s*(?:day|days)", "days"),
    # Hindi / Transliterated
    (r"(\d+)\s*din\s*(?:se|ho\s*gaye)", "days"),
    (r"(\d+)\s*hafte\s*se", "weeks"),
    (r"(\d+)\s*mahine\s*se", "months"),
    (r"(\d+)\s*ghante\s*se", "hours"),
    (r"kaafi\s*din\s*se", "many_days"),  # "many days"
    (r"bahut\s*din\s*se", "many_days"),
    (r"lamba\s*samay\s*se", "long_time"),
]

IMPACT_KEYWORDS = {
    "ward": [
        "entire ward", "whole ward", "poora ward", "ward level", "all residents",
        "sabhi log", "samast ward", "poora mohalla", "entire area",
    ],
    "colony": [
        "colony", "society", "apartment", "building", "complex",
        "residential area", "mohalla", "basti", "nagar", "vihar",
        "hundreds of families", "sainkdon parivaar",
    ],
    "street": [
        "street", "road", "lane", "gali", "marg", "sadak",
        "our street", "hamari gali", "hamare yahan",
    ],
    "family": [
        "family", "our house", "my home", "hamara ghar", "parivar",
        "ghar mein", "mere ghar", "hamare ghar",
    ],
    "individual": [
        "i", "me", "my", "main", "mera", "mujhe", "personally",
    ],
}


# ─────────────────────────────────────────────────────────
# STOPWORDS (English + Hindi transliterated)
# ─────────────────────────────────────────────────────────

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "shall", "should", "may", "might", "can", "could",
    "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "this", "that", "these", "those", "it", "its", "i", "we",
    "you", "he", "she", "they", "me", "us", "him", "her", "them",
    "my", "our", "your", "his", "their", "and", "but", "or",
    "not", "no", "so", "if", "about", "up", "out", "than",
    "very", "just", "also", "please", "kindly", "sir", "madam",
    "ji", "ji", "sahab", "sahib", "mam",
    # Hindi transliterated
    "hai", "hain", "ho", "tha", "thi", "the", "ka", "ki", "ke",
    "ko", "se", "mein", "par", "pe", "ne", "aur", "ya", "bhi",
    "nahi", "na", "koi", "kuch", "yeh", "woh", "yahan", "wahan",
    "kab", "kaise", "kyon", "kyunki", "lekin", "magar", "phir",
    "abhi", "ab", "tab", "jab", "bahut", "zyada", "kam", "sab",
    "apna", "apni", "apne", "ek", "do", "teen", "char",
    "kripaya", "please",
}


# ─────────────────────────────────────────────────────────
# MAIN CLASSIFICATION FUNCTION
# ─────────────────────────────────────────────────────────

def classify_complaint(raw_text: str) -> dict:
    """
    Complete offline NLP analysis of a complaint.
    Returns structured data identical to what Gemini API would return.
    """
    text = raw_text.strip()
    text_lower = text.lower()

    # 1. Category classification
    sub_match = get_subcategory_match(text)
    if sub_match and sub_match["match_score"] > 0:
        category = sub_match["category_name"]
        category_hi = sub_match["category_name_hi"]
        category_confidence = min(1.0, sub_match["match_score"] / 30.0)
        department = sub_match["department"]
        department_hi = sub_match["department_hi"]
        severity = sub_match["severity"]
        urgency = sub_match["urgency"]
        sla_hours = sub_match["sla_hours"]
        subcategory = sub_match["subcategory_name"]
    else:
        category = "Other"
        category_hi = "अन्य"
        category_confidence = 0.1
        department = "General Administration"
        department_hi = "सामान्य प्रशासन विभाग"
        severity = "LOW"
        urgency = 40
        sla_hours = 96
        subcategory = "General"

    # 2. Emergency detection
    is_emergency = any(kw in text_lower for kw in EMERGENCY_KEYWORDS)
    if is_emergency:
        severity = "CRITICAL"
        urgency = max(urgency, 95)

    # 3. High urgency detection
    is_high_urgency = any(kw in text_lower for kw in HIGH_URGENCY_KEYWORDS)
    if is_high_urgency and severity not in ("CRITICAL",):
        severity = "HIGH"
        urgency = max(urgency, 80)

    # 4. Duration extraction
    duration_days = _extract_duration(text_lower)

    # 5. Impact estimation
    affected_estimate = _estimate_impact(text_lower)

    # 6. Location extraction
    ward_info = get_ward_by_location(text)
    location_text = ward_info["name"] if ward_info else _extract_location(text)
    ward_number = ward_info["id"] if ward_info else _extract_ward_number(text)

    # 7. Generate summaries
    summary_en = _generate_summary(text, category, subcategory, location_text)
    summary_hi = _generate_summary_hindi(category_hi, subcategory, location_text)

    # 8. Extract severity keywords
    severity_keywords = _extract_severity_keywords(text_lower)

    return {
        "summary_english": summary_en,
        "summary_hindi": summary_hi,
        "category": category,
        "category_hindi": category_hi,
        "subcategory": subcategory,
        "category_confidence": round(category_confidence, 2),
        "location_text": location_text,
        "ward_number": ward_number,
        "duration_days": duration_days,
        "severity_keywords": severity_keywords,
        "affected_estimate": affected_estimate,
        "is_emergency": is_emergency,
        "severity": severity,
        "urgency_score": urgency,
        "sla_hours": sla_hours,
        "requires_department": department,
        "requires_department_hi": department_hi,
        "source": "knowledge_base",
    }


# ─────────────────────────────────────────────────────────
# DUPLICATE DETECTION (Jaccard + keyword overlap)
# ─────────────────────────────────────────────────────────

def check_duplicate_local(
    new_text: str,
    existing_complaints: list[dict],
    threshold: float = 0.55,
) -> Optional[dict]:
    """
    Check for duplicates using Jaccard similarity + keyword overlap.
    No external API needed.
    """
    new_tokens = _tokenize(new_text)
    if not new_tokens:
        return None

    new_set = set(new_tokens)
    new_counter = Counter(new_tokens)

    best_match = None
    best_score = 0.0

    for existing in existing_complaints:
        existing_text = existing.get("summary", "") or existing.get("title", "")
        existing_tokens = _tokenize(existing_text)
        if not existing_tokens:
            continue

        existing_set = set(existing_tokens)

        # Jaccard similarity
        intersection = new_set & existing_set
        union = new_set | existing_set
        jaccard = len(intersection) / len(union) if union else 0

        # Weighted keyword overlap (shared non-stopword terms)
        content_words = intersection - STOPWORDS
        keyword_score = len(content_words) / max(len(new_set - STOPWORDS), 1)

        # Composite
        score = 0.5 * jaccard + 0.5 * keyword_score

        if score > best_score and score >= threshold:
            best_score = score
            best_match = {
                "is_duplicate": True,
                "duplicate_of_id": existing.get("id"),
                "similarity_score": round(score, 2),
                "reason": f"Matching keywords: {', '.join(sorted(content_words)[:8])}",
                "source": "knowledge_base",
            }

    return best_match


# ─────────────────────────────────────────────────────────
# TEXT SUMMARIZATION (extractive, keyword-based)
# ─────────────────────────────────────────────────────────

def summarize_text(text: str, max_words: int = 30) -> str:
    """Simple extractive summarization — pick the most informative sentence."""
    sentences = re.split(r'[.!?।\n]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    if not sentences:
        return text[:150].strip()

    if len(sentences) == 1:
        words = sentences[0].split()
        return " ".join(words[:max_words])

    # Score sentences by content word density
    scored = []
    for sent in sentences:
        tokens = _tokenize(sent)
        content_tokens = [t for t in tokens if t not in STOPWORDS]
        score = len(content_tokens) / max(len(tokens), 1)
        scored.append((score, sent))

    scored.sort(key=lambda x: -x[0])
    top = scored[0][1]
    words = top.split()
    return " ".join(words[:max_words])


# ─────────────────────────────────────────────────────────
# PRIVATE HELPERS
# ─────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    """Simple tokenizer — lowercase, split on non-alphanumeric."""
    return [
        w for w in re.findall(r'[a-zA-Z\u0900-\u097F]+', text.lower())
        if len(w) > 1
    ]


def _extract_duration(text: str) -> int | None:
    """Extract how long the problem has existed (in days)."""
    for pattern, unit in DURATION_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if unit in ("many_days", "long_time"):
                return 15  # default estimate for vague durations
            try:
                num = int(match.group(1))
                if unit == "hours":
                    return max(1, num // 24)
                elif unit == "weeks":
                    return num * 7
                elif unit == "months":
                    return num * 30
                else:
                    return num
            except (ValueError, IndexError):
                continue
    return None


def _estimate_impact(text: str) -> str:
    """Estimate the scale of impact."""
    for level in ["ward", "colony", "street", "family", "individual"]:
        keywords = IMPACT_KEYWORDS.get(level, [])
        if any(kw in text for kw in keywords):
            return level
    return "individual"


def _extract_location(text: str) -> str | None:
    """Extract location names from text."""
    # Look for "near X", "at X", "in X" patterns
    patterns = [
        r"(?:near|at|in|behind|opposite|next to)\s+([A-Z][a-zA-Z\s]{3,25})",
        r"(?:ke paas|ke saamne|ke peechhe)\s+(\S+(?:\s+\S+)?)",
        r"ward\s*(?:no\.?\s*)?(\d+)",
    ]
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _extract_ward_number(text: str) -> int | None:
    """Extract ward number from text."""
    match = re.search(r'ward\s*(?:no\.?\s*)?(\d+)', text, re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            pass
    return None


def _extract_severity_keywords(text: str) -> list[str]:
    """Extract words that indicate severity."""
    found = []
    for kw in EMERGENCY_KEYWORDS + HIGH_URGENCY_KEYWORDS:
        if kw in text:
            found.append(kw)
    return found[:10]


def _generate_summary(
    text: str,
    category: str,
    subcategory: str,
    location: str | None,
) -> str:
    """Generate a brief English summary."""
    core = summarize_text(text, max_words=20)
    loc_str = f" in {location}" if location else ""
    return f"{category} issue ({subcategory}){loc_str}: {core}"


def _generate_summary_hindi(
    category_hi: str,
    subcategory: str,
    location: str | None,
) -> str:
    """Generate a brief Hindi summary."""
    loc_str = f"{location} में" if location else ""
    return f"{loc_str} {category_hi} की समस्या ({subcategory})"
