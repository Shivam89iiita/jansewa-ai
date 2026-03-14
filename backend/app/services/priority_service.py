"""
Priority scoring engine — 5-factor weighted composite.

PRIMARY:   KB priority_rules + ward_database for enriched scoring
ENHANCED:  DB queries for recurrence + vulnerability data
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.complaint import Complaint
from app.models.ward import Ward

from app.knowledge_base.priority_rules import calculate_priority_kb, ESCALATION_RULES
from app.knowledge_base.ward_database import get_ward_vulnerability_score
from app.knowledge_base.governance_policies import get_sla, get_escalation_target

logger = logging.getLogger(__name__)

# Category base urgency scores
CATEGORY_URGENCY: dict[str, int] = {
    "Water Supply": 85,
    "Health": 90,
    "Public Safety": 95,
    "Electricity": 75,
    "Drainage": 80,
    "Road/Pothole": 60,
    "Garbage": 65,
    "Other": 40,
}


async def calculate_priority_score(
    complaint_data: dict,
    db: AsyncSession,
) -> dict:
    """
    Calculate composite priority score (0-100) using 5 weighted factors.

    Formula:
        Score = 0.30×Urgency + 0.25×Impact + 0.20×Recurrence
              + 0.15×Sentiment + 0.10×Vulnerability
    """

    # ── FACTOR 1: URGENCY (30%) ──────────────────────────
    category = complaint_data.get("category", "Other")
    urgency = CATEGORY_URGENCY.get(category, 40)

    if complaint_data.get("is_emergency"):
        urgency = min(100, urgency + 15)

    duration = complaint_data.get("duration_days") or 0
    if duration > 7:
        urgency = min(100, urgency + 10)
    elif duration > 3:
        urgency = min(100, urgency + 5)

    # ── FACTOR 2: IMPACT (25%) ───────────────────────────
    impact_map = {
        "individual": 20,
        "family": 35,
        "street": 55,
        "colony": 75,
        "ward": 95,
    }
    impact = impact_map.get(
        complaint_data.get("affected_estimate", "individual"), 20
    )

    # ── FACTOR 3: RECURRENCE (20%) ───────────────────────
    ward_id = complaint_data.get("ward_id")
    recurrence = 0
    if ward_id:
        try:
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            stmt = (
                select(func.count())
                .select_from(Complaint)
                .where(
                    Complaint.ward_id == ward_id,
                    Complaint.created_at >= thirty_days_ago,
                )
            )
            category_id = complaint_data.get("category_id")
            if category_id:
                stmt = stmt.where(Complaint.category_id == category_id)

            result = await db.execute(stmt)
            count = result.scalar() or 0
            recurrence = min(100, count * 15)
        except Exception as e:
            logger.warning(f"Recurrence calculation failed: {e}")

    # ── FACTOR 4: SENTIMENT (15%) ────────────────────────
    sentiment_score_raw = complaint_data.get("area_sentiment", 50)
    sentiment_priority = max(0, 100 - int((sentiment_score_raw + 1) * 50))

    # ── FACTOR 5: VULNERABILITY (10%) ────────────────────
    vulnerability = 30
    if ward_id:
        try:
            stmt = select(Ward).where(Ward.id == ward_id)
            result = await db.execute(stmt)
            ward = result.scalar_one_or_none()
            if ward and ward.is_vulnerable:
                vulnerability = 90
        except Exception as e:
            logger.warning(f"Vulnerability check failed: {e}")

    # ── COMPOSITE SCORE ──────────────────────────────────
    final_score = int(
        0.30 * urgency
        + 0.25 * impact
        + 0.20 * recurrence
        + 0.15 * sentiment_priority
        + 0.10 * vulnerability
    )

    if final_score >= 80:
        level = "CRITICAL"
    elif final_score >= 60:
        level = "HIGH"
    elif final_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "urgency_score": urgency,
        "impact_score": impact,
        "recurrence_score": recurrence,
        "sentiment_score": int(sentiment_priority),
        "vulnerability_score": vulnerability,
        "final_priority_score": final_score,
        "priority_level": level,
        "scoring_breakdown": {
            "urgency": f"{urgency} × 0.30 = {0.30 * urgency:.1f}",
            "impact": f"{impact} × 0.25 = {0.25 * impact:.1f}",
            "recurrence": f"{recurrence} × 0.20 = {0.20 * recurrence:.1f}",
            "sentiment": f"{int(sentiment_priority)} × 0.15 = {0.15 * sentiment_priority:.1f}",
            "vulnerability": f"{vulnerability} × 0.10 = {0.10 * vulnerability:.1f}",
        },
        # ── KB enrichment ────────────────────────────────
        "sla": get_sla(level.lower()),
        "escalation_target": get_escalation_target(
            category, 0  # initial — 0 hours elapsed
        ),
        "escalation_rules_matched": _match_escalation_rules(complaint_data, final_score),
        "source": "db+knowledge_base",
    }


def _match_escalation_rules(complaint_data: dict, score: int) -> list:
    """Check which KB escalation rules apply."""
    matched = []
    for rule in ESCALATION_RULES:
        try:
            conditions = rule.get("conditions", {})
            if conditions.get("severity") in ("critical",) and score >= 80:
                matched.append(rule["name"])
            elif conditions.get("severity") == "high" and score >= 60:
                matched.append(rule["name"])
            elif conditions.get("is_emergency") and complaint_data.get("is_emergency"):
                matched.append(rule["name"])
        except Exception:
            pass
    return matched
