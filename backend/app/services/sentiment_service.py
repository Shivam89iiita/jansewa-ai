"""
Sentiment analysis service — VADER + KB enhancement.

PRIMARY:   VADER (local) + KB sentiment words (English + Hindi + transliterated)
OPTIONAL:  LLM deep analysis via Gemini
"""

import logging
from typing import Optional

from app.knowledge_base.social_analysis import POSITIVE_WORDS, NEGATIVE_WORDS

logger = logging.getLogger(__name__)


def _get_vader():
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    return SentimentIntensityAnalyzer()


def analyze_sentiment_vader(text: str) -> dict:
    """Quick sentiment via VADER (best for social media text)."""
    analyzer = _get_vader()
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.3:
        sentiment = "POSITIVE"
    elif compound <= -0.5:
        sentiment = "ANGRY"
    elif compound <= -0.15:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return {
        "sentiment": sentiment,
        "sentiment_score": compound,
        "scores": scores,
    }


def calculate_virality(vader_scores: dict, text: str) -> int:
    """Estimate virality potential (0-100) using VADER + KB words."""
    score = 0

    compound = vader_scores.get("compound", 0)
    if compound < -0.5:
        score += 40
    elif compound < -0.15:
        score += 20

    score += min(20, text.count("!") * 5)

    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if caps_ratio > 0.3:
        score += 15

    trigger_words = ["crore", "lakh", "corruption", "scam", "chor", "fraud"]
    for word in trigger_words:
        if word in text.lower():
            score += 15
            break

    # KB negative words boost (Hindi / transliterated)
    text_lower = text.lower()
    kb_neg_hits = sum(1 for w in NEGATIVE_WORDS.get("hi", []) if w in text_lower)
    score += min(15, kb_neg_hits * 5)

    return min(100, score)
