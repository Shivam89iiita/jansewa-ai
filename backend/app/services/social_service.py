"""
Social media listener service — X/Twitter scanning + analysis.

PRIMARY:   Knowledge Base social_analysis (offline sentiment, misinfo, crisis)
OPTIONAL:  Twitter API for real data; Gemini for deep analysis
FALLBACK:  KB analysis + mock data always works
"""

import json
import logging
from typing import Optional

from app.services.sentiment_service import analyze_sentiment_vader, calculate_virality
from app.knowledge_base.social_analysis import (
    analyze_social_post as kb_analyze_post,
    analyze_social_batch,
)

logger = logging.getLogger(__name__)


async def scan_social_media(
    city_name: str,
    ward_names: list[str],
    bearer_token: Optional[str] = None,
) -> list[dict]:
    """
    Scan X (Twitter) for governance-related posts.
    Falls back to mock data if API unavailable.
    All posts are analysed by KB first, Gemini optionally.
    """
    try:
        import tweepy
        from app.config import settings

        token = bearer_token or getattr(settings, "TWITTER_BEARER_TOKEN", None)
        if not token:
            logger.info("No Twitter bearer token — using mock data with KB analysis")
            return _mock_social_data()

        client = tweepy.Client(bearer_token=token)

        keywords = [
            "water problem", "road pothole", "no electricity",
            "garbage", "drainage", "corruption", "municipal",
            "paani nahi", "bijli nahi", "sadak kharab",
        ]
        location_terms = " OR ".join([f'"{n}"' for n in ward_names[:5]])
        keyword_terms = " OR ".join(keywords[:10])
        query = f"({keyword_terms}) ({city_name} OR {location_terms}) -is:retweet lang:en OR lang:hi"

        tweets = client.search_recent_tweets(
            query=query,
            max_results=50,
            tweet_fields=["created_at", "public_metrics", "lang"],
        )

        results = []
        if tweets.data:
            for tweet in tweets.data:
                analysis = await analyze_social_post(tweet.text)
                results.append({
                    "platform": "twitter",
                    "post_text": tweet.text,
                    "post_url": f"https://twitter.com/i/status/{tweet.id}",
                    "created_at": str(tweet.created_at),
                    "likes": tweet.public_metrics.get("like_count", 0),
                    "shares": tweet.public_metrics.get("retweet_count", 0),
                    "replies": tweet.public_metrics.get("reply_count", 0),
                    **analysis,
                })
        return results

    except Exception as e:
        logger.error(f"Social media scan failed: {e}")
        return _mock_social_data()


async def analyze_social_post(post_text: str) -> dict:
    """
    Analyze a single social media post.
    KB analysis first → VADER sentiment → optional Gemini deep analysis.
    """
    # ── STEP 1: KB analysis (always works) ───────────────
    kb_result = kb_analyze_post(post_text)

    # ── STEP 2: VADER sentiment (fast, local) ────────────
    vader_result = analyze_sentiment_vader(post_text)
    virality = calculate_virality(vader_result.get("scores", {}), post_text)

    # Build combined result from KB + VADER
    combined = {
        "sentiment": vader_result["sentiment"],
        "sentiment_score": vader_result["sentiment_score"],
        "virality_score": max(virality, int(kb_result.get("virality_score", 0) * 100)),
        "is_complaint": kb_result.get("is_governance_related", False),
        "category": kb_result.get("category", "Other"),
        "extracted_ward": None,
        "extracted_location": kb_result.get("location_mentioned"),
        "is_misinformation": kb_result["misinformation_risk"]["risk_level"] == "high",
        "misinfo_confidence": kb_result["misinformation_risk"]["score"],
        "misinfo_explanation": (
            f"Misinformation indicators: {kb_result['misinformation_risk']['misinfo_indicators']}"
            if kb_result["misinformation_risk"]["risk_level"] == "high"
            else None
        ),
        "crisis_detected": kb_result.get("crisis_detected", {}),
        "suggested_counter_statement": None,
        "source": "knowledge_base+vader",
    }

    # ── STEP 3: Optional Gemini deep analysis ────────────
    try:
        import google.generativeai as genai
        from app.config import settings

        if not getattr(settings, "GEMINI_API_KEY", None):
            return combined

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Analyze this social media post about local governance:

POST: \"{post_text}\"

Return JSON:
{{
    "is_complaint": true/false,
    "category": "Water Supply/Road/Electricity/Drainage/Garbage/Health/Safety/Other/None",
    "extracted_ward": null or ward number if mentioned,
    "extracted_location": "location name if mentioned or null",
    "is_misinformation": true/false,
    "misinfo_confidence": 0.0 to 1.0,
    "misinfo_explanation": "why it might be misinformation, or null",
    "suggested_counter_statement": "if misinfo, draft a factual response, or null"
}}
Return ONLY the JSON.
"""
        response = model.generate_content(prompt)
        cleaned = response.text.strip().strip("`").strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
        llm_result = json.loads(cleaned)

        # Merge Gemini data into combined result
        if llm_result.get("extracted_ward"):
            combined["extracted_ward"] = llm_result["extracted_ward"]
        if llm_result.get("extracted_location"):
            combined["extracted_location"] = llm_result["extracted_location"]
        if llm_result.get("suggested_counter_statement"):
            combined["suggested_counter_statement"] = llm_result["suggested_counter_statement"]
        combined["source"] = "knowledge_base+vader+gemini"
    except Exception as e:
        logger.warning(f"Gemini social analysis unavailable, using KB+VADER: {e}")

    return combined


def _mock_social_data() -> list[dict]:
    """Return mock social data for development / demo."""
    from datetime import datetime, timedelta
    import random

    posts = [
        {
            "text": "3 days no water in Shanti Nagar Ward 12! When will the municipality fix this? #WaterCrisis",
            "sentiment": "ANGRY", "sentiment_score": -0.85, "category": "Water Supply",
            "ward": 12, "is_misinfo": False,
        },
        {
            "text": "Great job by Ward 5 team — pothole on MG Road fixed within 24 hours! 👏",
            "sentiment": "POSITIVE", "sentiment_score": 0.78, "category": "Road/Pothole",
            "ward": 5, "is_misinfo": False,
        },
        {
            "text": "Councillor stole 50 crore from drainage project fund! No work done! #Corruption",
            "sentiment": "ANGRY", "sentiment_score": -0.92, "category": "Drainage",
            "ward": 8, "is_misinfo": True,
        },
        {
            "text": "Garbage not collected for a week in Rajendra Nagar. Terrible smell everywhere.",
            "sentiment": "NEGATIVE", "sentiment_score": -0.65, "category": "Garbage",
            "ward": 3, "is_misinfo": False,
        },
        {
            "text": "New LED street lights installed in Ward 1. Feels much safer now at night.",
            "sentiment": "POSITIVE", "sentiment_score": 0.82, "category": "Electricity",
            "ward": 1, "is_misinfo": False,
        },
        {
            "text": "Dengue cases rising in Ward 7 due to open drains. Nobody cares!",
            "sentiment": "ANGRY", "sentiment_score": -0.78, "category": "Health",
            "ward": 7, "is_misinfo": False,
        },
        {
            "text": "Municipality claims 100% complaints resolved this month — total lies! #FakeStats",
            "sentiment": "ANGRY", "sentiment_score": -0.88, "category": "Other",
            "ward": None, "is_misinfo": True,
        },
        {
            "text": "Thank you Ward 10 councillor for quick action on broken water pipeline.",
            "sentiment": "POSITIVE", "sentiment_score": 0.71, "category": "Water Supply",
            "ward": 10, "is_misinfo": False,
        },
    ]

    results = []
    for i, p in enumerate(posts):
        results.append({
            "platform": "twitter",
            "post_text": p["text"],
            "post_url": f"https://twitter.com/i/status/mock_{i}",
            "author_handle": f"@citizen_{random.randint(100,999)}",
            "created_at": str(datetime.utcnow() - timedelta(hours=random.randint(1, 72))),
            "likes": random.randint(5, 500),
            "shares": random.randint(1, 200),
            "replies": random.randint(0, 50),
            "sentiment": p["sentiment"],
            "sentiment_score": p["sentiment_score"],
            "virality_score": random.randint(20, 90),
            "is_complaint": p["category"] != "Other",
            "category": p["category"],
            "extracted_ward": p["ward"],
            "extracted_location": None,
            "is_misinformation": p["is_misinfo"],
            "misinfo_confidence": 0.85 if p["is_misinfo"] else 0.0,
            "misinfo_explanation": "Unverified claim with no evidence" if p["is_misinfo"] else None,
            "suggested_counter_statement": (
                "The municipality's financial records are publicly auditable. "
                "Please refer to the transparency portal for verified data."
            ) if p["is_misinfo"] else None,
        })
    return results
