"""
Communication Templates Knowledge Base
========================================
Bilingual (English + Hindi) templates for all governance communication types.
Fully self-contained — no AI API needed.

Template types:
  ACKNOWLEDGMENT, PROGRESS, COMPLETION, CRISIS_RESPONSE, WEEKLY_DIGEST

Formats:
  whatsapp, social_media, official_notice
"""

from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────────────────────
# TEMPLATE STORE
# ─────────────────────────────────────────────────────────

TEMPLATES = {
    "ACKNOWLEDGMENT": {
        "whatsapp": {
            "english": (
                "Dear Citizen,\n\n"
                "✅ Your complaint has been registered successfully.\n\n"
                "📋 Complaint ID: {complaint_id}\n"
                "📁 Category: {category}\n"
                "📍 Location: {location}\n"
                "⏰ Expected Resolution: Within {sla_hours} hours\n\n"
                "Our team has been notified and will take action promptly. "
                "You can track the status on the Jansewa AI Public Portal.\n\n"
                "Thank you for helping improve our ward. 🙏\n"
                "— Jansewa AI, {ward_name}"
            ),
            "hindi": (
                "प्रिय नागरिक,\n\n"
                "✅ आपकी शिकायत सफलतापूर्वक दर्ज कर ली गई है।\n\n"
                "📋 शिकायत आईडी: {complaint_id}\n"
                "📁 श्रेणी: {category_hi}\n"
                "📍 स्थान: {location}\n"
                "⏰ अपेक्षित समाधान: {sla_hours} घंटों के भीतर\n\n"
                "हमारी टीम को सूचित कर दिया गया है और शीघ्र कार्रवाई की जाएगी। "
                "आप जनसेवा AI पोर्टल पर स्थिति देख सकते हैं।\n\n"
                "हमारे वार्ड को बेहतर बनाने में सहयोग के लिए धन्यवाद। 🙏\n"
                "— जनसेवा AI, {ward_name}"
            ),
        },
        "social_media": {
            "english": (
                "🔔 Complaint #{complaint_id} registered — {category} issue in {ward_name}. "
                "Our team is on it! Expected resolution in {sla_hours}hrs. "
                "Track progress: {portal_url} #JansewaAI #GoodGovernance #Ward{ward_number}"
            ),
            "hindi": (
                "🔔 शिकायत #{complaint_id} दर्ज — {ward_name} में {category_hi} की समस्या। "
                "हमारी टीम कार्य कर रही है! {sla_hours} घंटों में समाधान अपेक्षित। "
                "#जनसेवाAI #सुशासन"
            ),
        },
        "official_notice": {
            "english": (
                "OFFICE OF THE WARD COUNCILLOR — {ward_name}\n"
                "Reference No.: {complaint_id}\n"
                "Date: {date}\n\n"
                "ACKNOWLEDGMENT OF COMPLAINT\n\n"
                "This is to acknowledge receipt of your complaint regarding {category} "
                "({subcategory}) in {location}.\n\n"
                "The matter has been forwarded to the {department} for immediate action.\n"
                "Expected timeline for resolution: {sla_hours} hours.\n\n"
                "For queries, contact the ward office at {councillor_phone}.\n\n"
                "Sd/-\nWard Councillor\n{councillor_name}"
            ),
            "hindi": (
                "वार्ड पार्षद कार्यालय — {ward_name}\n"
                "संदर्भ संख्या: {complaint_id}\n"
                "दिनांक: {date}\n\n"
                "शिकायत की पावती\n\n"
                "{location} में {category_hi} ({subcategory}) संबंधी आपकी शिकायत प्राप्त हुई है।\n\n"
                "यह मामला {department_hi} को तत्काल कार्रवाई हेतु भेजा गया है।\n"
                "समाधान की अपेक्षित समय-सीमा: {sla_hours} घंटे।\n\n"
                "प्रश्नों के लिए वार्ड कार्यालय से संपर्क करें: {councillor_phone}\n\n"
                "सही/-\nवार्ड पार्षद\n{councillor_name}"
            ),
        },
    },

    "PROGRESS": {
        "whatsapp": {
            "english": (
                "Dear Citizen,\n\n"
                "🔄 Update on your complaint #{complaint_id}:\n\n"
                "📁 Issue: {category} — {subcategory}\n"
                "📍 Location: {location}\n"
                "📊 Status: {status}\n"
                "👷 Assigned to: {assigned_to}\n\n"
                "Work is in progress. {progress_note}\n\n"
                "Expected completion: {expected_date}\n\n"
                "We remain committed to resolving this. Thank you for your patience.\n"
                "— Jansewa AI"
            ),
            "hindi": (
                "प्रिय नागरिक,\n\n"
                "🔄 आपकी शिकायत #{complaint_id} का अपडेट:\n\n"
                "📁 समस्या: {category_hi} — {subcategory}\n"
                "📍 स्थान: {location}\n"
                "📊 स्थिति: {status}\n"
                "👷 जिम्मेदार: {assigned_to}\n\n"
                "कार्य प्रगति पर है। {progress_note}\n\n"
                "अपेक्षित पूर्णता: {expected_date}\n\n"
                "हम इसे हल करने के लिए प्रतिबद्ध हैं। धैर्य के लिए धन्यवाद।\n"
                "— जनसेवा AI"
            ),
        },
        "social_media": {
            "english": (
                "🔄 Update: Complaint #{complaint_id} in {ward_name} — {category} work in progress. "
                "Team deployed! Expected completion: {expected_date}. "
                "#JansewaAI #TransparentGovernance"
            ),
            "hindi": (
                "🔄 अपडेट: {ward_name} में {category_hi} की शिकायत #{complaint_id} पर कार्य जारी। "
                "टीम लगाई गई है! अपेक्षित पूर्णता: {expected_date}। "
                "#जनसेवाAI #पारदर्शी_शासन"
            ),
        },
        "official_notice": {
            "english": (
                "PROGRESS REPORT — Complaint {complaint_id}\n"
                "Date: {date}\n"
                "Department: {department}\n\n"
                "Current Status: {status}\n"
                "Work commenced on: {start_date}\n"
                "Progress: {progress_note}\n"
                "Expected completion: {expected_date}\n\n"
                "Officer in charge: {assigned_to}\n"
                "Contact: {department_phone}"
            ),
            "hindi": (
                "प्रगति रिपोर्ट — शिकायत {complaint_id}\n"
                "दिनांक: {date}\n"
                "विभाग: {department_hi}\n\n"
                "वर्तमान स्थिति: {status}\n"
                "कार्य प्रारंभ: {start_date}\n"
                "प्रगति: {progress_note}\n"
                "अपेक्षित पूर्णता: {expected_date}\n\n"
                "प्रभारी अधिकारी: {assigned_to}\n"
                "संपर्क: {department_phone}"
            ),
        },
    },

    "COMPLETION": {
        "whatsapp": {
            "english": (
                "Dear Citizen,\n\n"
                "✅ Great news! Your complaint has been RESOLVED!\n\n"
                "📋 Complaint ID: {complaint_id}\n"
                "📁 Issue: {category}\n"
                "📍 Location: {location}\n"
                "🔧 Work Completed: {completion_note}\n"
                "✓ Verification Status: {verification_status}\n\n"
                "Before/after photos are available on the Public Portal.\n\n"
                "Your feedback matters! Rate our service at: {feedback_url}\n\n"
                "Thank you for your cooperation. Together we build a better ward! 🙏\n"
                "— Jansewa AI, {ward_name}"
            ),
            "hindi": (
                "प्रिय नागरिक,\n\n"
                "✅ अच्छी खबर! आपकी शिकायत का समाधान हो गया है!\n\n"
                "📋 शिकायत आईडी: {complaint_id}\n"
                "📁 समस्या: {category_hi}\n"
                "📍 स्थान: {location}\n"
                "🔧 कार्य पूर्ण: {completion_note}\n"
                "✓ सत्यापन: {verification_status}\n\n"
                "पूर्व/पश्चात तस्वीरें पोर्टल पर उपलब्ध हैं।\n\n"
                "आपकी प्रतिक्रिया मायने रखती है! सेवा रेट करें: {feedback_url}\n\n"
                "सहयोग के लिए धन्यवाद। मिलकर बेहतर वार्ड बनाएं! 🙏\n"
                "— जनसेवा AI, {ward_name}"
            ),
        },
        "social_media": {
            "english": (
                "✅ RESOLVED: {category} issue in {ward_name} (#{complaint_id}) fixed! "
                "Verified with before/after proof. View on portal → {portal_url} "
                "#JansewaAI #ComplaintResolved #GoodGovernance"
            ),
            "hindi": (
                "✅ समाधान: {ward_name} में {category_hi} समस्या (#{complaint_id}) ठीक! "
                "पूर्व/पश्चात प्रमाण सहित सत्यापित। पोर्टल पर देखें → {portal_url} "
                "#जनसेवाAI #शिकायत_समाधान"
            ),
        },
        "official_notice": {
            "english": (
                "COMPLETION CERTIFICATE — Complaint {complaint_id}\n"
                "Date: {date}\n"
                "Department: {department}\n\n"
                "This is to certify that the {category} issue reported at {location} "
                "has been resolved on {completion_date}.\n\n"
                "Work Details: {completion_note}\n"
                "Verification: {verification_status}\n"
                "4-Layer Score: {verification_score}%\n\n"
                "Officer in charge: {assigned_to}\n\n"
                "Sd/-\nWard Councillor\n{councillor_name}"
            ),
            "hindi": (
                "पूर्णता प्रमाणपत्र — शिकायत {complaint_id}\n"
                "दिनांक: {date}\n"
                "विभाग: {department_hi}\n\n"
                "यह प्रमाणित किया जाता है कि {location} में {category_hi} की समस्या का "
                "{completion_date} को समाधान कर दिया गया है।\n\n"
                "कार्य विवरण: {completion_note}\n"
                "सत्यापन: {verification_status}\n"
                "4-स्तरीय स्कोर: {verification_score}%\n\n"
                "प्रभारी अधिकारी: {assigned_to}\n\n"
                "सही/-\nवार्ड पार्षद\n{councillor_name}"
            ),
        },
    },

    "CRISIS_RESPONSE": {
        "whatsapp": {
            "english": (
                "⚠️ OFFICIAL STATEMENT — {ward_name}\n\n"
                "We are aware of the concerns regarding {issue_summary}.\n\n"
                "FACTS:\n{facts}\n\n"
                "ACTION BEING TAKEN:\n{actions}\n\n"
                "We are committed to full transparency. "
                "Verified data is available on the Public Portal: {portal_url}\n\n"
                "For verified updates, follow our official channels only.\n"
                "— Ward Councillor {councillor_name}"
            ),
            "hindi": (
                "⚠️ आधिकारिक बयान — {ward_name}\n\n"
                "हमें {issue_summary} से संबंधित चिंताओं की जानकारी है।\n\n"
                "तथ्य:\n{facts}\n\n"
                "की जा रही कार्रवाई:\n{actions}\n\n"
                "हम पूर्ण पारदर्शिता के लिए प्रतिबद्ध हैं। "
                "सत्यापित डेटा पोर्टल पर उपलब्ध है: {portal_url}\n\n"
                "सत्यापित अपडेट के लिए केवल आधिकारिक चैनल देखें।\n"
                "— वार्ड पार्षद {councillor_name}"
            ),
        },
        "social_media": {
            "english": (
                "⚠️ OFFICIAL: Regarding concerns about {issue_summary} in {ward_name} — "
                "We are taking immediate action. {short_action} "
                "Full facts on portal: {portal_url} "
                "#JansewaAI #FactCheck #Transparency"
            ),
            "hindi": (
                "⚠️ आधिकारिक: {ward_name} में {issue_summary} की चिंताओं पर — "
                "तत्काल कार्रवाई की जा रही है। {short_action} "
                "पूर्ण तथ्य पोर्टल पर: {portal_url} "
                "#जनसेवाAI #तथ्य_जांच"
            ),
        },
        "official_notice": {
            "english": (
                "OFFICIAL PRESS RELEASE\n"
                "Ward: {ward_name} | Date: {date}\n"
                "Subject: Response to Public Concerns — {issue_summary}\n\n"
                "The Ward Administration has taken note of public concerns regarding "
                "{issue_summary}.\n\n"
                "VERIFIED FACTS:\n{facts}\n\n"
                "ACTIONS TAKEN:\n{actions}\n\n"
                "Citizens are advised to refer to official channels for verified information. "
                "Spreading unverified information may cause unnecessary panic.\n\n"
                "All governance data is publicly auditable on the Jansewa AI Transparency Portal.\n\n"
                "Sd/-\nWard Councillor\n{councillor_name}\nDate: {date}"
            ),
            "hindi": (
                "आधिकारिक प्रेस विज्ञप्ति\n"
                "वार्ड: {ward_name} | दिनांक: {date}\n"
                "विषय: जनता की चिंताओं पर प्रतिक्रिया — {issue_summary}\n\n"
                "वार्ड प्रशासन ने {issue_summary} संबंधी जनता की चिंताओं का संज्ञान लिया है।\n\n"
                "सत्यापित तथ्य:\n{facts}\n\n"
                "की गई कार्रवाई:\n{actions}\n\n"
                "नागरिकों से अनुरोध है कि सत्यापित जानकारी के लिए केवल आधिकारिक चैनल देखें।\n\n"
                "सभी शासन डेटा जनसेवा AI पारदर्शिता पोर्टल पर सार्वजनिक रूप से उपलब्ध है।\n\n"
                "सही/-\nवार्ड पार्षद\n{councillor_name}\nदिनांक: {date}"
            ),
        },
    },

    "WEEKLY_DIGEST": {
        "whatsapp": {
            "english": (
                "📊 WEEKLY GOVERNANCE DIGEST — {ward_name}\n"
                "Week: {week_range}\n\n"
                "📋 Complaints Received: {total_complaints}\n"
                "✅ Resolved: {resolved} ({resolution_rate}%)\n"
                "🔄 In Progress: {in_progress}\n"
                "⏳ Pending: {pending}\n\n"
                "🏆 Top Issues:\n{top_issues}\n\n"
                "⭐ Ward Trust Score: {trust_score}/100\n\n"
                "Full dashboard: {portal_url}\n"
                "— Jansewa AI"
            ),
            "hindi": (
                "📊 साप्ताहिक शासन डाइजेस्ट — {ward_name}\n"
                "सप्ताह: {week_range}\n\n"
                "📋 प्राप्त शिकायतें: {total_complaints}\n"
                "✅ समाधान: {resolved} ({resolution_rate}%)\n"
                "🔄 प्रगति पर: {in_progress}\n"
                "⏳ लंबित: {pending}\n\n"
                "🏆 प्रमुख मुद्दे:\n{top_issues}\n\n"
                "⭐ वार्ड विश्वास स्कोर: {trust_score}/100\n\n"
                "पूर्ण डैशबोर्ड: {portal_url}\n"
                "— जनसेवा AI"
            ),
        },
        "social_media": {
            "english": (
                "📊 {ward_name} Weekly Report:\n"
                "✅ {resolved}/{total_complaints} complaints resolved ({resolution_rate}%)\n"
                "⭐ Trust Score: {trust_score}/100\n"
                "Top focus: {top_issue}\n"
                "Full data: {portal_url}\n"
                "#JansewaAI #WeeklyReport #Accountability"
            ),
            "hindi": (
                "📊 {ward_name} साप्ताहिक रिपोर्ट:\n"
                "✅ {resolved}/{total_complaints} शिकायतें हल ({resolution_rate}%)\n"
                "⭐ विश्वास स्कोर: {trust_score}/100\n"
                "प्रमुख: {top_issue}\n"
                "#जनसेवाAI #साप्ताहिक_रिपोर्ट"
            ),
        },
        "official_notice": {
            "english": (
                "WEEKLY GOVERNANCE REPORT\n"
                "Ward: {ward_name} | Period: {week_range}\n"
                "Prepared by: Jansewa AI Intelligence System\n\n"
                "SUMMARY:\n"
                "Total Complaints: {total_complaints}\n"
                "Resolved: {resolved} ({resolution_rate}%)\n"
                "In Progress: {in_progress}\n"
                "Pending: {pending}\n\n"
                "TOP ISSUES:\n{top_issues}\n\n"
                "WARD PERFORMANCE:\n"
                "Trust Score: {trust_score}/100\n"
                "Average Resolution Time: {avg_resolution} hours\n"
                "Citizen Satisfaction: {satisfaction}%\n\n"
                "RECOMMENDATIONS:\n{recommendations}\n\n"
                "Full data available at: {portal_url}"
            ),
            "hindi": (
                "साप्ताहिक शासन रिपोर्ट\n"
                "वार्ड: {ward_name} | अवधि: {week_range}\n"
                "तैयार: जनसेवा AI इंटेलिजेंस सिस्टम\n\n"
                "सारांश:\n"
                "कुल शिकायतें: {total_complaints}\n"
                "समाधान: {resolved} ({resolution_rate}%)\n"
                "प्रगति पर: {in_progress}\n"
                "लंबित: {pending}\n\n"
                "प्रमुख मुद्दे:\n{top_issues}\n\n"
                "वार्ड प्रदर्शन:\n"
                "विश्वास स्कोर: {trust_score}/100\n"
                "औसत समाधान समय: {avg_resolution} घंटे\n"
                "नागरिक संतुष्टि: {satisfaction}%\n\n"
                "सुझाव:\n{recommendations}\n\n"
                "पूर्ण डेटा: {portal_url}"
            ),
        },
    },
}


# ─────────────────────────────────────────────────────────
# TEMPLATE RENDERER
# ─────────────────────────────────────────────────────────

def render_communication(
    comm_type: str,
    format: str,
    data: dict,
    language: str = "both",
) -> dict:
    """
    Render a communication from templates.

    Args:
        comm_type: ACKNOWLEDGMENT | PROGRESS | COMPLETION | CRISIS_RESPONSE | WEEKLY_DIGEST
        format: whatsapp | social_media | official_notice
        data: Dict of placeholder values
        language: "english" | "hindi" | "both"

    Returns:
        {"content_english": "...", "content_hindi": "..."}
    """
    # Defaults so templates don't break on missing keys
    defaults = {
        "date": datetime.now().strftime("%d %B %Y"),
        "complaint_id": "N/A",
        "category": "General",
        "category_hi": "सामान्य",
        "subcategory": "General",
        "location": "Ward Area",
        "ward_name": "Ward",
        "ward_number": "",
        "sla_hours": 48,
        "status": "In Progress",
        "assigned_to": "Ward Team",
        "department": "General Administration",
        "department_hi": "सामान्य प्रशासन",
        "councillor_name": "Ward Councillor",
        "councillor_phone": "",
        "portal_url": "https://jansewa.ai/portal",
        "feedback_url": "https://jansewa.ai/feedback",
        "progress_note": "Team is working on the issue.",
        "expected_date": "Soon",
        "start_date": "",
        "completion_date": datetime.now().strftime("%d %B %Y"),
        "completion_note": "Issue has been addressed.",
        "verification_status": "Pending",
        "verification_score": "N/A",
        "department_phone": "",
        "issue_summary": "the reported concern",
        "facts": "• Details being compiled",
        "actions": "• Immediate investigation ordered",
        "short_action": "Action underway.",
        "total_complaints": 0,
        "resolved": 0,
        "in_progress": 0,
        "pending": 0,
        "resolution_rate": 0,
        "trust_score": "N/A",
        "top_issues": "• Data loading",
        "top_issue": "General",
        "week_range": "",
        "avg_resolution": "N/A",
        "satisfaction": "N/A",
        "recommendations": "• Continue monitoring",
    }

    # Merge defaults < user data
    ctx = {**defaults, **data}

    template_group = TEMPLATES.get(comm_type, TEMPLATES["ACKNOWLEDGMENT"])
    format_group = template_group.get(format, template_group.get("whatsapp"))

    result = {}
    if language in ("english", "both"):
        try:
            result["content_english"] = format_group["english"].format(**ctx)
        except KeyError as e:
            result["content_english"] = format_group["english"]  # raw template

    if language in ("hindi", "both"):
        try:
            result["content_hindi"] = format_group["hindi"].format(**ctx)
        except KeyError:
            result["content_hindi"] = format_group["hindi"]

    result["comm_type"] = comm_type
    result["format"] = format
    result["source"] = "knowledge_base"
    return result
