"""
Governance Policies Knowledge Base
====================================
SLA definitions, escalation chains, department routing, shift schedules,
holiday calendars, and operational rules — fully self-contained.
"""

from datetime import datetime, time
from typing import Optional


# ─────────────────────────────────────────────────────────
# DEPARTMENT ROUTING
# ─────────────────────────────────────────────────────────

DEPARTMENTS = {
    "Water Supply": {
        "name_en": "Water Supply & Sewerage",
        "name_hi": "जल आपूर्ति एवं सीवरेज",
        "code": "WSS",
        "head": "Executive Engineer (Water)",
        "phone": "+91-11-23456001",
        "email": "water@mcd.gov.in",
        "escalation_chain": [
            {"level": 1, "role": "Junior Engineer", "hours": 0},
            {"level": 2, "role": "Assistant Engineer", "hours": 12},
            {"level": 3, "role": "Executive Engineer", "hours": 24},
            {"level": 4, "role": "Superintending Engineer", "hours": 48},
            {"level": 5, "role": "Additional Commissioner", "hours": 72},
        ],
    },
    "Road & Pothole": {
        "name_en": "Roads & Infrastructure",
        "name_hi": "सड़क एवं अवसंरचना",
        "code": "RNI",
        "head": "Executive Engineer (Roads)",
        "phone": "+91-11-23456002",
        "email": "roads@mcd.gov.in",
        "escalation_chain": [
            {"level": 1, "role": "Junior Engineer", "hours": 0},
            {"level": 2, "role": "Assistant Engineer", "hours": 24},
            {"level": 3, "role": "Executive Engineer", "hours": 48},
            {"level": 4, "role": "Superintending Engineer", "hours": 72},
            {"level": 5, "role": "Additional Commissioner", "hours": 96},
        ],
    },
    "Electricity": {
        "name_en": "Electrical & Street Lighting",
        "name_hi": "विद्युत एवं स्ट्रीट लाइटिंग",
        "code": "ELS",
        "head": "Executive Engineer (Electrical)",
        "phone": "+91-11-23456003",
        "email": "electricity@mcd.gov.in",
        "escalation_chain": [
            {"level": 1, "role": "Lineman", "hours": 0},
            {"level": 2, "role": "Junior Engineer", "hours": 6},
            {"level": 3, "role": "Assistant Engineer", "hours": 12},
            {"level": 4, "role": "Executive Engineer", "hours": 24},
            {"level": 5, "role": "Superintending Engineer", "hours": 48},
        ],
    },
    "Drainage & Sewage": {
        "name_en": "Drainage & Sanitation",
        "name_hi": "नाला एवं स्वच्छता",
        "code": "DNS",
        "head": "Executive Engineer (Drainage)",
        "phone": "+91-11-23456004",
        "email": "drainage@mcd.gov.in",
        "escalation_chain": [
            {"level": 1, "role": "Sanitary Inspector", "hours": 0},
            {"level": 2, "role": "Assistant Engineer", "hours": 8},
            {"level": 3, "role": "Executive Engineer", "hours": 24},
            {"level": 4, "role": "Superintending Engineer", "hours": 48},
            {"level": 5, "role": "Additional Commissioner", "hours": 72},
        ],
    },
    "Garbage & Sanitation": {
        "name_en": "Solid Waste Management",
        "name_hi": "ठोस अपशिष्ट प्रबंधन",
        "code": "SWM",
        "head": "Chief Sanitary Inspector",
        "phone": "+91-11-23456005",
        "email": "swm@mcd.gov.in",
        "escalation_chain": [
            {"level": 1, "role": "Sanitary Inspector", "hours": 0},
            {"level": 2, "role": "Chief Sanitary Inspector", "hours": 12},
            {"level": 3, "role": "Health Officer", "hours": 24},
            {"level": 4, "role": "Additional Commissioner", "hours": 48},
        ],
    },
    "Health & Sanitation": {
        "name_en": "Public Health",
        "name_hi": "जन स्वास्थ्य",
        "code": "PHD",
        "head": "Medical Officer of Health",
        "phone": "+91-11-23456006",
        "email": "health@mcd.gov.in",
        "escalation_chain": [
            {"level": 1, "role": "Health Inspector", "hours": 0},
            {"level": 2, "role": "Medical Officer", "hours": 4},
            {"level": 3, "role": "Chief Medical Officer", "hours": 12},
            {"level": 4, "role": "Commissioner (Health)", "hours": 24},
        ],
    },
    "Public Safety": {
        "name_en": "Public Safety & Emergency",
        "name_hi": "जन सुरक्षा एवं आपातकाल",
        "code": "PSE",
        "head": "Safety Commissioner",
        "phone": "+91-11-23456007",
        "email": "safety@mcd.gov.in",
        "escalation_chain": [
            {"level": 1, "role": "Ward Safety Officer", "hours": 0},
            {"level": 2, "role": "Zonal Safety Officer", "hours": 2},
            {"level": 3, "role": "Deputy Commissioner", "hours": 6},
            {"level": 4, "role": "Commissioner", "hours": 12},
        ],
    },
    "General Administration": {
        "name_en": "General Administration",
        "name_hi": "सामान्य प्रशासन",
        "code": "GAD",
        "head": "Ward Officer",
        "phone": "+91-11-23456000",
        "email": "admin@mcd.gov.in",
        "escalation_chain": [
            {"level": 1, "role": "Ward Clerk", "hours": 0},
            {"level": 2, "role": "Ward Officer", "hours": 24},
            {"level": 3, "role": "Zonal Deputy Commissioner", "hours": 48},
            {"level": 4, "role": "Additional Commissioner", "hours": 72},
        ],
    },
}


# ─────────────────────────────────────────────────────────
# SLA DEFINITIONS (hours)
# ─────────────────────────────────────────────────────────

SLA_POLICY = {
    "critical": {
        "response_hours": 1,
        "resolution_hours": 6,
        "update_frequency_hours": 2,
        "max_extensions": 1,
        "extension_hours": 4,
    },
    "high": {
        "response_hours": 4,
        "resolution_hours": 24,
        "update_frequency_hours": 6,
        "max_extensions": 2,
        "extension_hours": 12,
    },
    "medium": {
        "response_hours": 12,
        "resolution_hours": 72,
        "update_frequency_hours": 24,
        "max_extensions": 2,
        "extension_hours": 24,
    },
    "low": {
        "response_hours": 24,
        "resolution_hours": 168,  # 7 days
        "update_frequency_hours": 48,
        "max_extensions": 3,
        "extension_hours": 48,
    },
}


# ─────────────────────────────────────────────────────────
# SHIFT SCHEDULES
# ─────────────────────────────────────────────────────────

SHIFTS = {
    "morning": {"start": time(6, 0), "end": time(14, 0), "label": "Morning Shift"},
    "afternoon": {"start": time(14, 0), "end": time(22, 0), "label": "Afternoon Shift"},
    "night": {"start": time(22, 0), "end": time(6, 0), "label": "Night Shift"},
}

EMERGENCY_TEAMS = {
    "water_tanker": {"available_24x7": True, "response_minutes": 60},
    "electrical_emergency": {"available_24x7": True, "response_minutes": 30},
    "drainage_emergency": {"available_24x7": True, "response_minutes": 45},
    "medical_emergency": {"available_24x7": True, "response_minutes": 15},
    "fire_safety": {"available_24x7": True, "response_minutes": 10},
}


# ─────────────────────────────────────────────────────────
# GAZETTED HOLIDAYS (Delhi / Central Govt 2024-2025 pattern)
# ─────────────────────────────────────────────────────────

GAZETTED_HOLIDAYS = [
    {"date": "2025-01-26", "name": "Republic Day", "name_hi": "गणतंत्र दिवस"},
    {"date": "2025-03-14", "name": "Holi", "name_hi": "होली"},
    {"date": "2025-03-31", "name": "Id-ul-Fitr", "name_hi": "ईद-उल-फित्र"},
    {"date": "2025-04-06", "name": "Ram Navami", "name_hi": "राम नवमी"},
    {"date": "2025-04-10", "name": "Mahavir Jayanti", "name_hi": "महावीर जयंती"},
    {"date": "2025-04-14", "name": "Dr. Ambedkar Jayanti", "name_hi": "डॉ. अंबेडकर जयंती"},
    {"date": "2025-04-18", "name": "Good Friday", "name_hi": "गुड फ्राइडे"},
    {"date": "2025-05-01", "name": "May Day", "name_hi": "मई दिवस"},
    {"date": "2025-05-12", "name": "Buddha Purnima", "name_hi": "बुद्ध पूर्णिमा"},
    {"date": "2025-06-07", "name": "Eid-ul-Adha", "name_hi": "ईद-उल-अज़हा"},
    {"date": "2025-07-06", "name": "Muharram", "name_hi": "मुहर्रम"},
    {"date": "2025-08-15", "name": "Independence Day", "name_hi": "स्वतंत्रता दिवस"},
    {"date": "2025-08-16", "name": "Janmashtami", "name_hi": "जन्माष्टमी"},
    {"date": "2025-09-05", "name": "Milad-un-Nabi", "name_hi": "मिलाद-उन-नबी"},
    {"date": "2025-10-02", "name": "Gandhi Jayanti", "name_hi": "गांधी जयंती"},
    {"date": "2025-10-02", "name": "Dussehra", "name_hi": "दशहरा"},
    {"date": "2025-10-20", "name": "Diwali", "name_hi": "दीवाली"},
    {"date": "2025-10-21", "name": "Diwali Holiday", "name_hi": "दीवाली अवकाश"},
    {"date": "2025-11-05", "name": "Guru Nanak Jayanti", "name_hi": "गुरु नानक जयंती"},
    {"date": "2025-12-25", "name": "Christmas", "name_hi": "क्रिसमस"},
]


# ─────────────────────────────────────────────────────────
# CATEGORY → DEPARTMENT ROUTING MAP
# ─────────────────────────────────────────────────────────

CATEGORY_TO_DEPARTMENT = {
    "Water Supply": "Water Supply",
    "Road & Pothole": "Road & Pothole",
    "Electricity": "Electricity",
    "Drainage & Sewage": "Drainage & Sewage",
    "Garbage & Sanitation": "Garbage & Sanitation",
    "Health & Sanitation": "Health & Sanitation",
    "Public Safety": "Public Safety",
    "Other": "General Administration",
}


# ─────────────────────────────────────────────────────────
# TRUST SCORE POLICY
# ─────────────────────────────────────────────────────────

TRUST_SCORE_WEIGHTS = {
    "resolution_rate": 0.30,
    "avg_resolution_time_vs_sla": 0.25,
    "citizen_satisfaction": 0.20,
    "transparency_score": 0.15,
    "complaint_recurrence": 0.10,
}

TRUST_SCORE_THRESHOLDS = {
    "excellent": {"min": 80, "label": "Excellent", "label_hi": "उत्कृष्ट", "color": "#22c55e"},
    "good":      {"min": 60, "label": "Good", "label_hi": "अच्छा", "color": "#3b82f6"},
    "average":   {"min": 40, "label": "Average", "label_hi": "औसत", "color": "#f59e0b"},
    "poor":      {"min": 20, "label": "Poor", "label_hi": "खराब", "color": "#ef4444"},
    "critical":  {"min": 0,  "label": "Critical", "label_hi": "गंभीर", "color": "#991b1b"},
}


# ─────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────

def get_department(category: str) -> dict:
    """Route a complaint category to the responsible department."""
    dept_key = CATEGORY_TO_DEPARTMENT.get(category, "General Administration")
    return DEPARTMENTS.get(dept_key, DEPARTMENTS["General Administration"])


def get_escalation_target(category: str, hours_elapsed: float) -> dict:
    """Determine current escalation level based on elapsed time."""
    dept = get_department(category)
    chain = dept["escalation_chain"]
    current = chain[0]
    for step in chain:
        if hours_elapsed >= step["hours"]:
            current = step
    return {
        "level": current["level"],
        "role": current["role"],
        "department": dept["name_en"],
        "department_hi": dept["name_hi"],
        "phone": dept["phone"],
        "email": dept["email"],
    }


def get_sla(priority: str) -> dict:
    """Get SLA timings for a priority level."""
    return SLA_POLICY.get(priority.lower(), SLA_POLICY["medium"])


def is_holiday(date_str: Optional[str] = None) -> bool:
    """Check if a date is a gazetted holiday."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    return any(h["date"] == date_str for h in GAZETTED_HOLIDAYS)


def is_working_hours(hour: Optional[int] = None) -> bool:
    """Check if within standard working hours (9am-5pm)."""
    if hour is None:
        hour = datetime.now().hour
    return 9 <= hour < 17


def get_current_shift(hour: Optional[int] = None) -> dict:
    """Get current shift details."""
    if hour is None:
        hour = datetime.now().hour
    if 6 <= hour < 14:
        return SHIFTS["morning"]
    elif 14 <= hour < 22:
        return SHIFTS["afternoon"]
    else:
        return SHIFTS["night"]


def calculate_effective_sla(priority: str, is_holiday_flag: bool = False) -> int:
    """
    Adjust SLA hours for holidays / non-working hours.
    Holidays add 50% buffer to resolution time.
    """
    sla = get_sla(priority)
    base_hours = sla["resolution_hours"]
    if is_holiday_flag:
        base_hours = int(base_hours * 1.5)
    return base_hours


def get_trust_label(score: float) -> dict:
    """Return Trust-Score label & colour for a numeric score."""
    for key in ("excellent", "good", "average", "poor", "critical"):
        if score >= TRUST_SCORE_THRESHOLDS[key]["min"]:
            return TRUST_SCORE_THRESHOLDS[key]
    return TRUST_SCORE_THRESHOLDS["critical"]
