"""
Local Social Media Analysis — Knowledge Base
===============================================
Offline social media text analysis: sentiment, misinformation detection,
hashtag trending, and crisis identification — no external API required.

Replaces Gemini-based analysis in social_service.py.
"""

import re
import math
from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────────────────
# MISINFORMATION INDICATORS
# ─────────────────────────────────────────────────────────

MISINFORMATION_PHRASES_EN = [
    "i heard that", "someone told me", "forwarded as received",
    "whatsapp forward", "breaking news unverified", "sources say",
    "rumour", "rumor", "viral message", "fake news", "unconfirmed",
    "secret plan", "they are hiding", "government is hiding",
    "conspiracy", "exposed", "shocking truth", "they don't want you to know",
    "mainstream media won't tell you", "share before deleted",
    "100% true", "confirmed by insider", "leaked document",
]

MISINFORMATION_PHRASES_HI = [
    "suna hai ki", "kisi ne bataya", "forward kiya", "whatsapp pe aaya",
    "afwah", "jhoothi khabar", "viral message", "sach samne aaya",
    "chhupa rahe hain", "saazish", "share karo delete hone se pehle",
    "government chhupa rahi hai", "insider ne bataya",
    "shocking", "parda faash", "100% sach",
]

CREDIBILITY_BOOSTERS = [
    "official statement", "press release", "verified", "according to",
    "data shows", "report published", "government confirmed",
    "ward office", "councillor", "mcd", "sdmc", "ndmc", "edmc",
    "official", "adhikarik", "satyapit",
]


# ─────────────────────────────────────────────────────────
# SENTIMENT WORDS (supplementary to VADER)
# ─────────────────────────────────────────────────────────

POSITIVE_WORDS = {
    "en": [
        "thank", "thanks", "good", "great", "excellent", "fixed", "resolved",
        "working", "improved", "clean", "safe", "happy", "appreciate",
        "well done", "satisfied", "kudos", "progress", "better",
    ],
    "hi": [
        "dhanyavad", "shukriya", "accha", "bahut accha", "theek", "sudhaar",
        "kaam ho gaya", "saaf", "surakshit", "khush", "tarakki",
        "badiya", "shaandaar",
    ],
}

NEGATIVE_WORDS = {
    "en": [
        "bad", "worst", "terrible", "pathetic", "corrupt", "useless",
        "nothing done", "no action", "waste", "disgust", "angry",
        "shameful", "dirty", "dangerous", "broken", "failure",
        "negligence", "incompetent", "scam",
    ],
    "hi": [
        "bekar", "ghatiya", "bhrashtachar", "koi kaam nahi", "ganda",
        "kharab", "khatarnak", "toota", "nakaam", "laparwahi",
        "sharmnak", "bekaar", "dhoka", "gussa", "pareshan",
        "jhooth", "fraud",
    ],
}


# ─────────────────────────────────────────────────────────
# GOVERNANCE ISSUE HASHTAGS
# ─────────────────────────────────────────────────────────

GOVERNANCE_HASHTAGS = [
    "#jansewaai", "#mcd", "#sdmc", "#ndmc", "#edmc",
    "#delhimcd", "#pothole", "#watercrisis", "#garbageissue",
    "#drainageblock", "#streetlight", "#roaddamage",
    "#swachhbharat", "#smartcity", "#cleanindia",
    "#delhiroads", "#delhiwater", "#delhiflood",
    "#waterlogging", "#mosquito", "#dengue", "#pollution",
    "#encroachment", "#straydog",
    # Hindi tags
    "#sadak", "#paani", "#bijli", "#gaddha", "#nala",
    "#kuda", "#safai", "#suraksha",
]


# ─────────────────────────────────────────────────────────
# CRISIS KEYWORDS
# ─────────────────────────────────────────────────────────

CRISIS_KEYWORDS = [
    "flood", "collapse", "fire", "explosion", "stampede",
    "epidemic", "outbreak", "death", "fatality", "casualties",
    "riot", "protest", "strike", "bandh", "chakka jam",
    "building collapse", "wall collapse", "bridge collapse",
    "electrocution", "drowning", "gas leak",
    # Hindi
    "baadh", "dhah gaya", "aag", "dhamaka", "bhaagdad",
    "mahamari", "maut", "danga", "hadtal", "andolan",
    "bijli ka jhatka", "gas leak",
]


# ─────────────────────────────────────────────────────────
# ANALYSIS FUNCTIONS
# ─────────────────────────────────────────────────────────

def analyze_social_post(text: str) -> dict:
    """
    Comprehensive local analysis of a social media post.
    Returns structured dict — drop-in replacement for Gemini analysis.
    """
    text_lower = text.lower()
    words = re.findall(r'\w+', text_lower)
    word_set = set(words)

    result = {
        "sentiment": _detect_sentiment(text_lower, word_set),
        "is_governance_related": _is_governance_related(text_lower),
        "category": _detect_category(text_lower),
        "location_mentioned": _extract_location_from_social(text_lower),
        "misinformation_risk": _assess_misinformation(text_lower),
        "crisis_detected": _detect_crisis(text_lower),
        "virality_score": _estimate_virality(text, text_lower, word_set),
        "hashtags": _extract_hashtags(text),
        "source": "knowledge_base",
    }
    return result


def _detect_sentiment(text_lower: str, word_set: set) -> dict:
    """Rule-based sentiment with score."""
    pos_count = sum(1 for w in POSITIVE_WORDS["en"] + POSITIVE_WORDS["hi"] if w in text_lower)
    neg_count = sum(1 for w in NEGATIVE_WORDS["en"] + NEGATIVE_WORDS["hi"] if w in text_lower)

    total = pos_count + neg_count
    if total == 0:
        return {"label": "neutral", "score": 0.0, "positive": 0, "negative": 0}

    score = (pos_count - neg_count) / total  # -1 to +1
    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return {"label": label, "score": round(score, 2), "positive": pos_count, "negative": neg_count}


def _is_governance_related(text_lower: str) -> bool:
    """Check if post is about local governance issues."""
    gov_keywords = [
        "ward", "mcd", "sdmc", "ndmc", "edmc", "councillor", "parshad",
        "nagar nigam", "municipality", "civic body", "corporation",
        "pothole", "water supply", "garbage", "drainage", "sewer",
        "street light", "road", "sadak", "paani", "bijli", "nala",
        "kuda", "safai", "complaint", "shikayat",
    ]
    return any(kw in text_lower for kw in gov_keywords)


def _detect_category(text_lower: str) -> Optional[str]:
    """Map social post to a complaint category."""
    category_kw = {
        "Water Supply": ["water", "paani", "tanker", "pipeline", "tap", "nala", "supply"],
        "Road & Pothole": ["road", "pothole", "sadak", "gaddha", "footpath", "divider"],
        "Electricity": ["electricity", "bijli", "light", "street light", "power cut", "transformer"],
        "Drainage & Sewage": ["drain", "sewer", "nala", "sewage", "overflow", "manhole"],
        "Garbage & Sanitation": ["garbage", "kuda", "waste", "dump", "sanitation", "safai", "dhalao"],
        "Health & Sanitation": ["mosquito", "dengue", "malaria", "health", "disease", "epidemic", "fogging"],
        "Public Safety": ["stray", "collapse", "unsafe", "danger", "fire", "encroachment"],
    }
    best_cat = None
    best_score = 0
    for cat, kws in category_kw.items():
        score = sum(1 for kw in kws if kw in text_lower)
        if score > best_score:
            best_score = score
            best_cat = cat
    return best_cat


def _extract_location_from_social(text_lower: str) -> Optional[str]:
    """Try to extract location mentions."""
    # Look for common Delhi locality patterns
    patterns = [
        r'(?:in|at|near|of)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})',
        r'(ward\s*\d+)',
        r'(sector\s*\d+)',
    ]
    for pat in patterns:
        match = re.search(pat, text_lower if 'ward' in pat.lower() else text_lower.replace(text_lower, text_lower), re.IGNORECASE)
        if match:
            return match.group(1).strip()

    # Delhi area names
    delhi_areas = [
        "karol bagh", "chandni chowk", "sadar bazaar", "civil lines",
        "rohini", "dwarka", "janakpuri", "pitampura", "shalimar bagh",
        "lajpat nagar", "greater kailash", "sarojini nagar", "connaught place",
        "paharganj", "rajouri garden", "tilak nagar", "vikaspuri",
        "najafgarh", "narela", "alipur", "model town", "mukherjee nagar",
        "shahdara", "gandhi nagar", "krishna nagar", "mayur vihar",
    ]
    for area in delhi_areas:
        if area in text_lower:
            return area.title()
    return None


def _assess_misinformation(text_lower: str) -> dict:
    """Assess misinformation risk of a post."""
    misinfo_hits = sum(1 for p in MISINFORMATION_PHRASES_EN + MISINFORMATION_PHRASES_HI if p in text_lower)
    credibility_hits = sum(1 for p in CREDIBILITY_BOOSTERS if p in text_lower)

    if misinfo_hits == 0 and credibility_hits > 0:
        risk = "low"
        score = 0.1
    elif misinfo_hits == 0:
        risk = "low"
        score = 0.2
    elif misinfo_hits <= 1 and credibility_hits > 0:
        risk = "medium"
        score = 0.4
    elif misinfo_hits <= 2:
        risk = "medium"
        score = 0.5
    else:
        risk = "high"
        score = min(0.9, 0.3 + misinfo_hits * 0.15)

    # ALL-CAPS text increases suspicion
    import re as _re
    upper_ratio = len(_re.findall(r'[A-Z]', text_lower.swapcase())) / max(len(text_lower), 1)
    if upper_ratio > 0.5:
        score = min(1.0, score + 0.15)
        if risk == "low":
            risk = "medium"

    # Multiple exclamation marks
    if text_lower.count("!") > 3:
        score = min(1.0, score + 0.1)

    return {
        "risk_level": risk,
        "score": round(score, 2),
        "misinfo_indicators": misinfo_hits,
        "credibility_indicators": credibility_hits,
    }


def _detect_crisis(text_lower: str) -> dict:
    """Detect if post indicates a crisis situation."""
    crisis_hits = [kw for kw in CRISIS_KEYWORDS if kw in text_lower]
    is_crisis = len(crisis_hits) >= 1

    severity = "none"
    if len(crisis_hits) >= 3:
        severity = "critical"
    elif len(crisis_hits) >= 2:
        severity = "high"
    elif len(crisis_hits) >= 1:
        severity = "medium"

    return {
        "is_crisis": is_crisis,
        "severity": severity,
        "keywords_matched": crisis_hits[:5],
    }


def _estimate_virality(original_text: str, text_lower: str, word_set: set) -> float:
    """
    Estimate how viral / impactful a post might be.
    Score 0–1 based on emotional intensity, hashtags, call-to-action, etc.
    """
    score = 0.0

    # Emotional intensity
    neg_count = sum(1 for w in NEGATIVE_WORDS["en"] + NEGATIVE_WORDS["hi"] if w in text_lower)
    score += min(0.3, neg_count * 0.06)

    # Hashtag count
    hashtag_count = original_text.count("#")
    score += min(0.15, hashtag_count * 0.03)

    # Mentions / tags
    mention_count = original_text.count("@")
    score += min(0.15, mention_count * 0.05)

    # Exclamation / urgency
    score += min(0.1, original_text.count("!") * 0.02)

    # Call to action phrases
    cta_phrases = ["share", "retweet", "rt", "spread", "viral karo", "share karo", "tag"]
    cta_hits = sum(1 for p in cta_phrases if p in text_lower)
    score += min(0.15, cta_hits * 0.07)

    # Length bonus (longer = more detailed = more engagement)
    word_count = len(text_lower.split())
    if word_count > 50:
        score += 0.05
    if word_count > 100:
        score += 0.05

    # Photo / video mentions
    if any(w in text_lower for w in ["photo", "video", "pic", "image", "tasveer"]):
        score += 0.1

    return round(min(1.0, score), 2)


def _extract_hashtags(text: str) -> list:
    """Extract all hashtags from text."""
    return re.findall(r'#\w+', text)


# ─────────────────────────────────────────────────────────
# BATCH ANALYSIS (for social media scanning)
# ─────────────────────────────────────────────────────────

def analyze_social_batch(posts: list[dict]) -> dict:
    """
    Analyze a batch of social posts and produce aggregate report.

    Args:
        posts: List of {"text": "...", "author": "...", "timestamp": "...", ...}

    Returns:
        Aggregate analysis: trending issues, sentiment distribution, crisis alerts.
    """
    analyses = []
    sentiment_dist = {"positive": 0, "negative": 0, "neutral": 0}
    category_counts = {}
    crisis_alerts = []
    misinfo_alerts = []

    for post in posts:
        text = post.get("text", "")
        result = analyze_social_post(text)
        result["author"] = post.get("author", "unknown")
        result["timestamp"] = post.get("timestamp", "")
        analyses.append(result)

        # Aggregate
        sentiment_dist[result["sentiment"]["label"]] += 1

        cat = result.get("category")
        if cat:
            category_counts[cat] = category_counts.get(cat, 0) + 1

        if result["crisis_detected"]["is_crisis"]:
            crisis_alerts.append({
                "text_snippet": text[:200],
                "severity": result["crisis_detected"]["severity"],
                "author": post.get("author"),
            })

        if result["misinformation_risk"]["risk_level"] == "high":
            misinfo_alerts.append({
                "text_snippet": text[:200],
                "score": result["misinformation_risk"]["score"],
                "author": post.get("author"),
            })

    # Trending categories
    trending = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

    total = len(posts)
    return {
        "total_analyzed": total,
        "sentiment_distribution": sentiment_dist,
        "governance_related": sum(1 for a in analyses if a.get("is_governance_related")),
        "trending_categories": [{"category": c, "count": n} for c, n in trending],
        "crisis_alerts": crisis_alerts,
        "misinformation_alerts": misinfo_alerts,
        "avg_virality": round(sum(a["virality_score"] for a in analyses) / max(total, 1), 2),
        "individual_analyses": analyses,
        "source": "knowledge_base",
    }
