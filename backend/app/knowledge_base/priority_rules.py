"""
Priority Rules Engine (Knowledge-Base Driven)
==============================================
Deterministic priority scoring using internal rules — no AI API.
Uses ward vulnerability data, category severity, and text-derived signals.
"""

import logging
from typing import Optional

from app.knowledge_base.complaint_categories import CATEGORIES, get_category_by_name
from app.knowledge_base.ward_database import (
    get_ward,
    get_ward_vulnerability_score,
    INFRASTRUCTURE_BENCHMARKS,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# ESCALATION RULES
# ─────────────────────────────────────────────────────────

ESCALATION_RULES = [
    {
        "name": "Critical-Emergency",
        "condition": lambda d: d.get("is_emergency") is True,
        "priority_boost": 25,
        "auto_escalate": True,
        "escalate_to": "LEADER",
        "sla_override_hours": 4,
    },
    {
        "name": "Vulnerable-Ward-Critical",
        "condition": lambda d: d.get("ward_vulnerability", 0) >= 70 and d.get("severity") == "CRITICAL",
        "priority_boost": 20,
        "auto_escalate": True,
        "escalate_to": "DEPARTMENT_HEAD",
        "sla_override_hours": 6,
    },
    {
        "name": "Multi-Complaint-Spike",
        "condition": lambda d: d.get("recurrence_count", 0) >= 10,
        "priority_boost": 15,
        "auto_escalate": True,
        "escalate_to": "DEPARTMENT_HEAD",
        "sla_override_hours": 12,
    },
    {
        "name": "Elderly-Children-Impact",
        "condition": lambda d: any(
            kw in d.get("text_lower", "")
            for kw in ["elderly", "children", "disabled", "boodhe", "bachche", "viklang",
                       "senior citizen", "pregnant", "garbhwati"]
        ),
        "priority_boost": 10,
        "auto_escalate": False,
        "escalate_to": None,
        "sla_override_hours": None,
    },
    {
        "name": "Health-Epidemic",
        "condition": lambda d: d.get("category") in ("Health", "Health / Medical") and
                               any(kw in d.get("text_lower", "")
                                   for kw in ["dengue", "malaria", "cholera", "epidemic",
                                              "outbreak", "spreading", "fail raha"]),
        "priority_boost": 25,
        "auto_escalate": True,
        "escalate_to": "LEADER",
        "sla_override_hours": 4,
    },
    {
        "name": "Infrastructure-Danger",
        "condition": lambda d: any(
            kw in d.get("text_lower", "")
            for kw in ["collapse", "collapsing", "falling", "caving in",
                       "sinkhole", "gir raha", "toot raha", "dhah raha"]
        ),
        "priority_boost": 20,
        "auto_escalate": True,
        "escalate_to": "LEADER",
        "sla_override_hours": 4,
    },
    {
        "name": "Long-Pending",
        "condition": lambda d: (d.get("duration_days") or 0) > 30,
        "priority_boost": 15,
        "auto_escalate": True,
        "escalate_to": "DEPARTMENT_HEAD",
        "sla_override_hours": 24,
    },
]


# ─────────────────────────────────────────────────────────
# SEASONAL ADJUSTMENTS
# ─────────────────────────────────────────────────────────

SEASONAL_PRIORITY_BOOSTS = {
    # month: {category: boost}
    6: {"drainage": 15, "road_pothole": 10, "health": 10},     # June monsoon
    7: {"drainage": 20, "road_pothole": 15, "health": 15},     # July monsoon peak
    8: {"drainage": 20, "road_pothole": 15, "health": 15},     # August
    9: {"drainage": 10, "road_pothole": 10, "health": 10},     # September
    4: {"water_supply": 15},                                     # Summer starts
    5: {"water_supply": 20, "electricity": 10},                  # Peak summer
    10: {"health": 10},                                          # Post-monsoon dengue
    11: {"electricity": 5},                                      # Early winter
    12: {"electricity": 10, "public_safety": 5},                 # Winter
    1: {"electricity": 10, "public_safety": 5},                  # Winter
}


# ─────────────────────────────────────────────────────────
# TIME-OF-DAY ADJUSTMENTS
# ─────────────────────────────────────────────────────────

def _time_of_day_boost(category: str, hour: int) -> int:
    """Extra urgency for night-time safety/electricity complaints."""
    if 20 <= hour or hour <= 5:  # 8 PM to 5 AM
        if category in ("electricity", "public_safety"):
            return 10
    return 0


# ─────────────────────────────────────────────────────────
# MAIN PRIORITY CALCULATION
# ─────────────────────────────────────────────────────────

def calculate_priority_kb(
    complaint_data: dict,
    recurrence_count: int = 0,
    current_month: Optional[int] = None,
    current_hour: Optional[int] = None,
) -> dict:
    """
    Calculate composite priority score using ONLY knowledge base rules.
    No external API needed.

    Input complaint_data keys:
      - category (str)
      - severity (str)
      - urgency_score (int)
      - is_emergency (bool)
      - duration_days (int|None)
      - affected_estimate (str)
      - ward_number (int|None)
      - text_lower (str) — lowercased raw text

    Returns same format as the API-based priority service.
    """
    from datetime import datetime

    month = current_month or datetime.now().month
    hour = current_hour or datetime.now().hour

    # ── FACTOR 1: BASE URGENCY (from KB category) ───────
    urgency = complaint_data.get("urgency_score", 40)
    category = complaint_data.get("category", "Other")
    category_key = _category_to_key(category)

    # ── FACTOR 2: IMPACT ────────────────────────────────
    impact_map = {"individual": 20, "family": 35, "street": 55, "colony": 75, "ward": 95}
    impact = impact_map.get(complaint_data.get("affected_estimate", "individual"), 20)

    # ── FACTOR 3: RECURRENCE ────────────────────────────
    recurrence = min(100, recurrence_count * 12)

    # ── FACTOR 4: WARD VULNERABILITY ────────────────────
    ward_id = complaint_data.get("ward_number")
    vulnerability = 30
    ward_vuln_score = 0
    if ward_id:
        ward_vuln_score = get_ward_vulnerability_score(ward_id)
        vulnerability = ward_vuln_score

    # ── FACTOR 5: SENTIMENT (text-based estimation) ─────
    text_lower = complaint_data.get("text_lower", "")
    negative_words = [
        "angry", "frustrated", "fed up", "disgusted", "horrible",
        "terrible", "pathetic", "worst", "useless", "corrupt",
        "gussa", "pareshan", "thak gaye", "ghatiya", "bekaar",
    ]
    neg_count = sum(1 for w in negative_words if w in text_lower)
    sentiment_priority = min(100, neg_count * 20 + 20)

    # ── SEASONAL BOOST ──────────────────────────────────
    seasonal = SEASONAL_PRIORITY_BOOSTS.get(month, {})
    seasonal_boost = seasonal.get(category_key, 0)

    # ── TIME-OF-DAY BOOST ───────────────────────────────
    tod_boost = _time_of_day_boost(category_key, hour)

    # ── DURATION DECAY BOOST ────────────────────────────
    duration = complaint_data.get("duration_days") or 0
    duration_boost = 0
    if duration > 30:
        duration_boost = 15
    elif duration > 14:
        duration_boost = 10
    elif duration > 7:
        duration_boost = 5

    # ── COMPOSITE SCORE ─────────────────────────────────
    base_score = (
        0.30 * urgency
        + 0.22 * impact
        + 0.18 * recurrence
        + 0.15 * sentiment_priority
        + 0.15 * vulnerability
    )

    final_score = int(
        min(100, base_score + seasonal_boost + tod_boost + duration_boost)
    )

    # ── APPLY ESCALATION RULES ──────────────────────────
    escalation_context = {
        **complaint_data,
        "ward_vulnerability": ward_vuln_score,
        "recurrence_count": recurrence_count,
        "text_lower": text_lower,
    }

    triggered_rules = []
    sla_hours = complaint_data.get("sla_hours", 96)
    escalate_to = None

    for rule in ESCALATION_RULES:
        try:
            if rule["condition"](escalation_context):
                final_score = min(100, final_score + rule["priority_boost"])
                triggered_rules.append(rule["name"])
                if rule["auto_escalate"]:
                    escalate_to = rule["escalate_to"]
                if rule["sla_override_hours"]:
                    sla_hours = min(sla_hours, rule["sla_override_hours"])
        except Exception:
            continue

    # ── DETERMINE LEVEL ─────────────────────────────────
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
        "sentiment_score": sentiment_priority,
        "vulnerability_score": vulnerability,
        "seasonal_boost": seasonal_boost,
        "time_of_day_boost": tod_boost,
        "duration_boost": duration_boost,
        "final_priority_score": final_score,
        "priority_level": level,
        "sla_hours": sla_hours,
        "escalate_to": escalate_to,
        "triggered_rules": triggered_rules,
        "scoring_breakdown": {
            "urgency": f"{urgency} × 0.30 = {0.30 * urgency:.1f}",
            "impact": f"{impact} × 0.22 = {0.22 * impact:.1f}",
            "recurrence": f"{recurrence} × 0.18 = {0.18 * recurrence:.1f}",
            "sentiment": f"{sentiment_priority} × 0.15 = {0.15 * sentiment_priority:.1f}",
            "vulnerability": f"{vulnerability} × 0.15 = {0.15 * vulnerability:.1f}",
            "seasonal": f"+{seasonal_boost}",
            "time_of_day": f"+{tod_boost}",
            "duration": f"+{duration_boost}",
            "rules": ", ".join(triggered_rules) or "none",
        },
        "source": "knowledge_base",
    }


def _category_to_key(category_name: str) -> str:
    """Map category display name to internal key."""
    mapping = {
        "water supply": "water_supply",
        "road / pothole": "road_pothole",
        "road/pothole": "road_pothole",
        "electricity": "electricity",
        "drainage / sewage": "drainage",
        "drainage": "drainage",
        "garbage / sanitation": "garbage",
        "garbage": "garbage",
        "health / medical": "health",
        "health": "health",
        "public safety": "public_safety",
        "other": "other",
        "other / general": "other",
    }
    return mapping.get(category_name.lower().strip(), "other")
