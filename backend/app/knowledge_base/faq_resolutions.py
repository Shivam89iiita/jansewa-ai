"""
FAQ & Resolution Knowledge Base
=================================
Known solutions, standard operating procedures, and resolution steps
for every complaint subcategory — fully self-contained, no AI API needed.

Each entry maps (category, subcategory) → structured resolution data.
"""

from typing import Optional


# ─────────────────────────────────────────────────────────
# RESOLUTION DATABASE
# ─────────────────────────────────────────────────────────

RESOLUTIONS = {
    # ─── WATER SUPPLY ────────────────────────────────────
    ("Water Supply", "No Water Supply"): {
        "issue_en": "Complete absence of water supply",
        "issue_hi": "पानी की पूर्ण अनुपस्थिति",
        "steps": [
            "Verify water supply schedule for the area",
            "Check if main valve / pipeline is functional",
            "Dispatch water tanker for immediate relief",
            "Identify root cause (pipeline leak, pump failure, DJB issue)",
            "Coordinate repair with DJB if needed",
            "Restore pipeline supply and verify pressure",
        ],
        "steps_hi": [
            "क्षेत्र की जल आपूर्ति समय-सारणी सत्यापित करें",
            "मुख्य वाल्व / पाइपलाइन की जाँच करें",
            "तत्काल राहत के लिए टैंकर भेजें",
            "मूल कारण पहचानें (पाइपलाइन लीक, पंप खराबी, DJB समस्या)",
            "आवश्यक हो तो DJB से समन्वय करें",
            "पाइपलाइन आपूर्ति बहाल करें और दबाव सत्यापित करें",
        ],
        "required_resources": ["Water tanker", "Plumber team", "Pipeline repair kit"],
        "estimated_hours": 12,
        "prevention": "Regular pipeline inspection every 30 days; pressure monitoring sensors",
        "faq": [
            {"q": "When will water come?", "a": "A tanker has been dispatched. Pipeline repair is estimated within {sla} hours."},
            {"q": "Why is there no water?", "a": "The issue is being investigated — possible causes include pipeline leak, pump failure, or scheduled maintenance."},
        ],
    },
    ("Water Supply", "Low Pressure"): {
        "issue_en": "Very low water pressure in taps",
        "issue_hi": "नलों में बहुत कम पानी का दबाव",
        "steps": [
            "Check pressure readings at ward distribution point",
            "Identify if issue is localized or ward-wide",
            "Inspect for unauthorized connections / leaks",
            "Adjust distribution valve if needed",
            "Install booster pump if chronic issue",
        ],
        "steps_hi": [
            "वार्ड वितरण बिंदु पर दबाव रीडिंग जाँचें",
            "पहचानें कि समस्या स्थानीय है या वार्ड-व्यापी",
            "अनधिकृत कनेक्शन / लीक की जाँच करें",
            "आवश्यक हो तो वितरण वाल्व एडजस्ट करें",
            "स्थायी समस्या पर बूस्टर पंप लगाएं",
        ],
        "required_resources": ["Pressure gauge", "Plumber team"],
        "estimated_hours": 24,
        "prevention": "Monthly pressure audits; leak detection drives",
        "faq": [
            {"q": "Why is pressure low?", "a": "Could be due to increased demand, pipeline leak, or distribution issue. Our team is checking."},
        ],
    },
    ("Water Supply", "Contaminated Water"): {
        "issue_en": "Water is dirty, smelly, or contaminated",
        "issue_hi": "पानी गंदा, बदबूदार, या दूषित है",
        "steps": [
            "URGENT: Issue advisory to not use water until tested",
            "Collect water sample for lab testing",
            "Dispatch tanker with clean water immediately",
            "Inspect pipeline for sewage cross-contamination",
            "Flush and chlorinate the pipeline section",
            "Retest water quality (TDS, coliform, pH)",
            "Publish test results on portal",
        ],
        "steps_hi": [
            "तत्काल: जाँच तक पानी न पीने की सलाह जारी करें",
            "लैब परीक्षण के लिए पानी का नमूना लें",
            "तुरंत स्वच्छ पानी का टैंकर भेजें",
            "सीवेज क्रॉस-संदूषण के लिए पाइपलाइन जाँचें",
            "पाइपलाइन फ्लश और क्लोरीनेट करें",
            "पानी की गुणवत्ता पुनः परीक्षण करें",
            "परीक्षण परिणाम पोर्टल पर प्रकाशित करें",
        ],
        "required_resources": ["Water testing kit", "Clean tanker", "Chlorination equipment", "Lab coordination"],
        "estimated_hours": 6,
        "prevention": "Weekly water quality sampling; pipeline integrity checks",
        "faq": [
            {"q": "Is the water safe to drink?", "a": "Do NOT use the water until we confirm test results. A clean tanker is on the way."},
        ],
    },
    ("Water Supply", "Leaking Pipeline"): {
        "issue_en": "Water pipeline is leaking",
        "issue_hi": "पानी की पाइपलाइन में रिसाव",
        "steps": [
            "Locate exact leak point",
            "Shut off section valve to stop wastage",
            "Repair / replace damaged pipe section",
            "Restore supply and check for pressure",
            "Road repair if excavation was needed",
        ],
        "steps_hi": [
            "रिसाव बिंदु की सटीक स्थिति खोजें",
            "बर्बादी रोकने के लिए सेक्शन वाल्व बंद करें",
            "क्षतिग्रस्त पाइप सेक्शन मरम्मत / बदलें",
            "आपूर्ति बहाल करें और दबाव जाँचें",
            "खुदाई हुई हो तो सड़क मरम्मत करें",
        ],
        "required_resources": ["Plumber team", "Pipe section", "Excavation equipment"],
        "estimated_hours": 8,
        "prevention": "Pipeline age tracking; proactive replacement of old sections",
        "faq": [],
    },

    # ─── ROAD & POTHOLE ──────────────────────────────────
    ("Road & Pothole", "Pothole"): {
        "issue_en": "Potholes on road causing accidents / damage",
        "issue_hi": "सड़क पर गड्ढे जिनसे दुर्घटना / नुकसान",
        "steps": [
            "Mark pothole location with safety cones / barricades",
            "Assess pothole depth and road layer damage",
            "Clean debris from pothole",
            "Fill with cold-mix / hot-mix asphalt",
            "Compact and level the surface",
            "Mark for permanent repair if patch is temporary",
        ],
        "steps_hi": [
            "गड्ढे को सुरक्षा शंकु / बैरिकेड से चिह्नित करें",
            "गड्ढे की गहराई और सड़क परत क्षति का आकलन करें",
            "गड्ढे से मलबा साफ़ करें",
            "कोल्ड-मिक्स / हॉट-मिक्स डामर से भरें",
            "सतह को कॉम्पैक्ट और समतल करें",
            "अस्थायी पैच हो तो स्थायी मरम्मत हेतु चिह्नित करें",
        ],
        "required_resources": ["Road repair crew", "Asphalt mix", "Roller/compactor"],
        "estimated_hours": 48,
        "prevention": "Quarterly road condition surveys; proper drainage to prevent water damage",
        "faq": [
            {"q": "When will the pothole be fixed?", "a": "A temporary patch will be applied within 48 hours. Permanent repair may require a scheduled road project."},
        ],
    },
    ("Road & Pothole", "Road Damage"): {
        "issue_en": "Major road surface damage",
        "issue_hi": "सड़क की सतह में बड़ी क्षति",
        "steps": [
            "Safety barricading of damaged section",
            "Traffic diversion if needed",
            "Survey and estimate repair scope",
            "Schedule repair work (may need contractor)",
            "Execute repair — base layer + surface + markings",
            "Quality check with ward engineer",
        ],
        "steps_hi": [
            "क्षतिग्रस्त सेक्शन की सुरक्षा बैरिकेडिंग",
            "आवश्यक हो तो ट्रैफिक डायवर्शन",
            "सर्वे और मरम्मत गुंजाइश आकलन",
            "मरम्मत कार्य शेड्यूल करें",
            "मरम्मत — बेस लेयर + सतह + मार्किंग",
            "वार्ड इंजीनियर से गुणवत्ता जाँच",
        ],
        "required_resources": ["Road repair contractor", "Heavy equipment", "Traffic police coordination"],
        "estimated_hours": 120,
        "prevention": "Road quality standards enforcement; speed limit enforcement for heavy vehicles",
        "faq": [],
    },
    ("Road & Pothole", "Waterlogging"): {
        "issue_en": "Water accumulation on road after rain",
        "issue_hi": "बारिश के बाद सड़क पर पानी भराव",
        "steps": [
            "Deploy pump to remove standing water",
            "Clear blocked drains near waterlogged area",
            "Inspect road camber and drainage slope",
            "De-silt catch pits and chambers",
            "Long-term: Improve storm-water drainage",
        ],
        "steps_hi": [
            "खड़े पानी निकालने के लिए पंप लगाएं",
            "जलभराव क्षेत्र के पास अवरुद्ध नाले साफ़ करें",
            "सड़क कैम्बर और ड्रेनेज ढलान जाँचें",
            "कैच पिट और चैंबर डी-सिल्ट करें",
            "दीर्घकालिक: स्टॉर्म-वाटर ड्रेनेज सुधारें",
        ],
        "required_resources": ["Dewatering pump", "Drain cleaning crew", "De-silting machine"],
        "estimated_hours": 24,
        "prevention": "Pre-monsoon drain cleaning; road camber maintenance",
        "faq": [
            {"q": "Why does this area flood every year?", "a": "Typically caused by inadequate storm-water drains. We are working on a long-term drainage improvement plan."},
        ],
    },

    # ─── ELECTRICITY ─────────────────────────────────────
    ("Electricity", "Street Light Out"): {
        "issue_en": "Street light not working",
        "issue_hi": "सड़क की लाइट बंद है",
        "steps": [
            "Locate the exact pole number / GPS",
            "Check bulb / LED panel — replace if burned",
            "Check wiring and MCB / fuse",
            "Check timer / photo-sensor settings",
            "Test and restore functionality",
        ],
        "steps_hi": [
            "सटीक पोल नंबर / GPS पहचानें",
            "बल्ब / LED पैनल जाँचें — खराब हो तो बदलें",
            "वायरिंग और MCB / फ्यूज जाँचें",
            "टाइमर / फोटो-सेंसर सेटिंग जाँचें",
            "परीक्षण और कार्यक्षमता बहाल करें",
        ],
        "required_resources": ["Electrician", "LED panel / bulb", "Ladder truck"],
        "estimated_hours": 24,
        "prevention": "Monthly night patrol to identify non-working lights; LED upgrade program",
        "faq": [
            {"q": "When will the light be fixed?", "a": "Our electrician team will attend to it within 24 hours."},
        ],
    },
    ("Electricity", "Power Outage"): {
        "issue_en": "No electricity in the area",
        "issue_hi": "क्षेत्र में बिजली नहीं",
        "steps": [
            "Verify with DISCOM (BSES / Tata Power) about scheduled outage",
            "If unscheduled, report transformer / feeder issue to DISCOM",
            "Deploy DG set for critical facilities (hospital, school) if prolonged",
            "Monitor and update citizens on estimated restoration",
        ],
        "steps_hi": [
            "DISCOM (BSES / Tata Power) से शेड्यूल्ड आउटेज सत्यापित करें",
            "अनिर्धारित हो तो DISCOM को ट्रांसफॉर्मर / फीडर समस्या रिपोर्ट करें",
            "लंबी अवधि में DG सेट लगाएं",
            "नागरिकों को अनुमानित बहाली का अपडेट दें",
        ],
        "required_resources": ["DISCOM coordination", "DG set (backup)"],
        "estimated_hours": 6,
        "prevention": "Transformer health monitoring; demand-supply balancing",
        "faq": [
            {"q": "When will power come back?", "a": "We are coordinating with the power company. Estimated restoration: {sla} hours."},
        ],
    },
    ("Electricity", "Exposed Wires"): {
        "issue_en": "Dangerous exposed/hanging electrical wires",
        "issue_hi": "खतरनाक खुली / लटकती बिजली की तारें",
        "steps": [
            "URGENT: Barricade area immediately for safety",
            "Inform DISCOM to cut power to the line",
            "Secure or replace damaged cables",
            "Restore power and verify safety",
            "File incident report",
        ],
        "steps_hi": [
            "तत्काल: सुरक्षा के लिए क्षेत्र बैरिकेड करें",
            "DISCOM को लाइन की बिजली काटने के लिए सूचित करें",
            "क्षतिग्रस्त केबल सुरक्षित/बदलें",
            "बिजली बहाल करें और सुरक्षा सत्यापित करें",
            "घटना रिपोर्ट दर्ज करें",
        ],
        "required_resources": ["DISCOM emergency team", "Safety barricades", "Electrician"],
        "estimated_hours": 4,
        "prevention": "Quarterly cable inspection; anti-theft wire guards",
        "faq": [
            {"q": "Is it dangerous?", "a": "YES — stay away from the wires. Our team is en route to secure the area."},
        ],
    },

    # ─── DRAINAGE & SEWAGE ───────────────────────────────
    ("Drainage & Sewage", "Blocked Drain"): {
        "issue_en": "Drain is blocked causing overflow",
        "issue_hi": "नाला अवरुद्ध होने से उफान",
        "steps": [
            "Locate blockage point using inspection",
            "Deploy jetting machine / manual clearing",
            "Remove solid waste / debris causing blockage",
            "Restore drain flow and check downstream",
            "Sanitize the area",
        ],
        "steps_hi": [
            "निरीक्षण द्वारा अवरोध बिंदु खोजें",
            "जेटिंग मशीन / मैनुअल सफ़ाई लगाएं",
            "अवरोध कारण ठोस अपशिष्ट / मलबा हटाएं",
            "नाले का प्रवाह बहाल करें और डाउनस्ट्रीम जाँचें",
            "क्षेत्र को सैनिटाइज करें",
        ],
        "required_resources": ["Drain cleaning crew", "Jetting machine", "Sanitization team"],
        "estimated_hours": 12,
        "prevention": "Bi-weekly drain inspection; awareness against solid waste dumping",
        "faq": [],
    },
    ("Drainage & Sewage", "Sewage Overflow"): {
        "issue_en": "Raw sewage overflowing into streets / homes",
        "issue_hi": "गलियों / घरों में सीवेज का उफान",
        "steps": [
            "Deploy suction / jetting tanker immediately",
            "Identify overflow cause (blockage, pump failure, broken line)",
            "Repair the sewer line / pump",
            "Sanitize and disinfect affected area",
            "Health camp if residential contamination is severe",
        ],
        "steps_hi": [
            "तुरंत सक्शन / जेटिंग टैंकर लगाएं",
            "ओवरफ्लो कारण पहचानें (अवरोध, पंप खराबी, टूटी लाइन)",
            "सीवर लाइन / पंप मरम्मत करें",
            "प्रभावित क्षेत्र सैनिटाइज और कीटाणुरहित करें",
            "आवासीय संदूषण गंभीर हो तो स्वास्थ्य शिविर लगाएं",
        ],
        "required_resources": ["Suction tanker", "Plumber team", "Sanitization team", "Health team"],
        "estimated_hours": 8,
        "prevention": "Monthly sewer-line CCTV inspection; pumping station maintenance",
        "faq": [],
    },
    ("Drainage & Sewage", "Manhole Open/Damaged"): {
        "issue_en": "Manhole cover missing or damaged — safety hazard",
        "issue_hi": "मैनहोल का ढक्कन गायब या टूटा — सुरक्षा खतरा",
        "steps": [
            "URGENT: Place barricade / warning sign immediately",
            "Source replacement cover (standard/heavy-duty)",
            "Install new cover and secure it",
            "Paint safety markings around manhole",
        ],
        "steps_hi": [
            "तत्काल: बैरिकेड / चेतावनी चिह्न लगाएं",
            "रिप्लेसमेंट कवर (मानक/हैवी-ड्यूटी) की व्यवस्था",
            "नया कवर लगाएं और सुरक्षित करें",
            "मैनहोल के चारों ओर सेफ्टी मार्किंग करें",
        ],
        "required_resources": ["Manhole cover", "Labor crew", "Safety barricades"],
        "estimated_hours": 6,
        "prevention": "RFID tagging of covers; anti-theft locking mechanisms",
        "faq": [
            {"q": "Is it safe to walk near it?", "a": "NO — please stay away. We have placed barricades and a team is arriving to fix it."},
        ],
    },

    # ─── GARBAGE & SANITATION ────────────────────────────
    ("Garbage & Sanitation", "Garbage Not Collected"): {
        "issue_en": "Garbage not collected from the area",
        "issue_hi": "क्षेत्र से कूड़ा नहीं उठाया गया",
        "steps": [
            "Verify collection schedule for the area / block",
            "Check if collection vehicle was deployed",
            "Send backup vehicle if scheduled vehicle broke down",
            "Ensure door-to-door collection is complete",
            "Mark area as cleaned and verify",
        ],
        "steps_hi": [
            "क्षेत्र / ब्लॉक की कलेक्शन समय-सारणी सत्यापित करें",
            "कलेक्शन वाहन तैनात हुआ या नहीं जाँचें",
            "शेड्यूल्ड वाहन खराब हो तो बैकअप भेजें",
            "डोर-टू-डोर कलेक्शन पूर्ण सुनिश्चित करें",
            "क्षेत्र साफ़ चिह्नित करें और सत्यापित करें",
        ],
        "required_resources": ["Collection vehicle", "Sanitation workers"],
        "estimated_hours": 12,
        "prevention": "GPS tracking of vehicles; daily route compliance monitoring",
        "faq": [
            {"q": "When will garbage be picked up?", "a": "We are sending a collection vehicle today. Your area's regular schedule is {schedule}."},
        ],
    },
    ("Garbage & Sanitation", "Overflowing Dhalao"): {
        "issue_en": "Community garbage dump (dhalao) overflowing",
        "issue_hi": "सामुदायिक कूड़ा घर (ढलाव) उफ़ान पर",
        "steps": [
            "Deploy tipper truck to clear the dhalao",
            "Clean and disinfect the dhalao area",
            "Increase collection frequency for this site",
            "Install compactor if site chronically overflows",
        ],
        "steps_hi": [
            "ढलाव साफ़ करने के लिए टिपर ट्रक लगाएं",
            "ढलाव क्षेत्र साफ़ और कीटाणुरहित करें",
            "इस स्थल की कलेक्शन आवृत्ति बढ़ाएं",
            "बार-बार उफ़ान हो तो कम्पैक्टर लगाएं",
        ],
        "required_resources": ["Tipper truck", "Disinfection team"],
        "estimated_hours": 6,
        "prevention": "Capacity-based collection scheduling; segregation awareness drives",
        "faq": [],
    },
    ("Garbage & Sanitation", "Illegal Dumping"): {
        "issue_en": "Unauthorized garbage dumping at a location",
        "issue_hi": "किसी स्थान पर अनधिकृत कूड़ा फेंकना",
        "steps": [
            "Clean the illegal dump site",
            "Install 'No Dumping' signboard (bilingual)",
            "Install CCTV / light if recurring site",
            "Issue challans to offenders if identified",
            "Community awareness drive in the area",
        ],
        "steps_hi": [
            "अवैध डंप साइट साफ़ करें",
            "द्विभाषी 'कूड़ा न फेंकें' साइनबोर्ड लगाएं",
            "बार-बार हो तो CCTV / लाइट लगाएं",
            "पहचाने जाएं तो दोषियों पर चालान करें",
            "क्षेत्र में जन-जागरूकता अभियान",
        ],
        "required_resources": ["Cleaning crew", "Signboard", "CCTV (optional)"],
        "estimated_hours": 24,
        "prevention": "Regular patrolling; community shaming boards for violators",
        "faq": [],
    },

    # ─── HEALTH & SANITATION ─────────────────────────────
    ("Health & Sanitation", "Mosquito Breeding"): {
        "issue_en": "Mosquito menace / breeding sites",
        "issue_hi": "मच्छर प्रकोप / प्रजनन स्थल",
        "steps": [
            "Deploy fogging machine in affected area",
            "Identify and eliminate breeding sites (stagnant water)",
            "Apply larvicide in drains, ponds, containers",
            "Distribute mosquito nets if needed",
            "Awareness campaign for cover-water containers",
        ],
        "steps_hi": [
            "प्रभावित क्षेत्र में फॉगिंग मशीन लगाएं",
            "प्रजनन स्थल पहचानें और खत्म करें (ठहरा पानी)",
            "नालों, तालाबों में लार्विसाइड लगाएं",
            "आवश्यक हो तो मच्छरदानी वितरित करें",
            "पानी के बर्तन ढकने की जागरूकता अभियान",
        ],
        "required_resources": ["Fogging machine", "Larvicide", "Health inspector"],
        "estimated_hours": 24,
        "prevention": "Weekly anti-larval drives; drainage maintenance",
        "faq": [
            {"q": "When will fogging happen?", "a": "Fogging is scheduled for {date}. Keep windows open during fogging for best results."},
        ],
    },
    ("Health & Sanitation", "Food Safety"): {
        "issue_en": "Food hygiene / safety violation complaint",
        "issue_hi": "खाद्य स्वच्छता / सुरक्षा उल्लंघन शिकायत",
        "steps": [
            "Deploy food inspector to the establishment",
            "Collect food samples for testing",
            "Issue notice to establishment if violations found",
            "Seal establishment if critical violations",
            "Follow up on corrective actions",
        ],
        "steps_hi": [
            "प्रतिष्ठान पर खाद्य निरीक्षक भेजें",
            "परीक्षण हेतु खाद्य नमूने एकत्र करें",
            "उल्लंघन मिले तो प्रतिष्ठान को नोटिस जारी करें",
            "गंभीर उल्लंघन पर प्रतिष्ठान सील करें",
            "सुधारात्मक कार्रवाई पर अनुवर्ती कार्रवाई",
        ],
        "required_resources": ["Food inspector", "Sample collection kit", "Lab coordination"],
        "estimated_hours": 48,
        "prevention": "Quarterly food safety audits of all registered establishments",
        "faq": [],
    },
    ("Health & Sanitation", "Disease Outbreak"): {
        "issue_en": "Suspected disease outbreak report",
        "issue_hi": "संदिग्ध बीमारी प्रकोप की रिपोर्ट",
        "steps": [
            "URGENT: Deploy medical team for assessment",
            "Set up health camp in affected area",
            "Collect samples and coordinate with hospital lab",
            "Identify source of outbreak (water, food, vector)",
            "Contain the source — water supply testing, fogging, etc.",
            "Distribute ORS/medicines as first aid",
            "Daily monitoring until outbreak is contained",
            "Report to District Health Officer",
        ],
        "steps_hi": [
            "तत्काल: आकलन हेतु चिकित्सा दल भेजें",
            "प्रभावित क्षेत्र में स्वास्थ्य शिविर लगाएं",
            "नमूने एकत्र करें और अस्पताल लैब से समन्वय करें",
            "प्रकोप स्रोत पहचानें (पानी, भोजन, वेक्टर)",
            "स्रोत नियंत्रित करें",
            "प्राथमिक उपचार ORS/दवाइयाँ वितरित करें",
            "प्रकोप नियंत्रित होने तक दैनिक निगरानी",
            "जिला स्वास्थ्य अधिकारी को रिपोर्ट करें",
        ],
        "required_resources": ["Medical team", "Medicine kit", "Testing lab", "Ambulance"],
        "estimated_hours": 4,
        "prevention": "Water quality monitoring; vector control; sanitation drives",
        "faq": [],
    },

    # ─── PUBLIC SAFETY ───────────────────────────────────
    ("Public Safety", "Stray Animals"): {
        "issue_en": "Stray animal menace / aggressive animals",
        "issue_hi": "आवारा पशु उपद्रव / आक्रामक जानवर",
        "steps": [
            "Deploy animal control team",
            "Catch and relocate / shelter aggressive animals",
            "Coordinate with municipal animal shelter",
            "Issue rabies vaccination drive if dog bite reported",
        ],
        "steps_hi": [
            "पशु नियंत्रण दल भेजें",
            "आक्रामक जानवर पकड़ें और शेल्टर भेजें",
            "नगरपालिका पशु आश्रय से समन्वय करें",
            "कुत्ते ने काटा हो तो रेबीज टीकाकरण अभियान",
        ],
        "required_resources": ["Animal control team", "Transport vehicle", "Shelter coordination"],
        "estimated_hours": 24,
        "prevention": "ABC (Animal Birth Control) program; regular street drives",
        "faq": [
            {"q": "What to do if bitten by stray dog?", "a": "Wash the wound with soap, go to nearest PHC immediately for anti-rabies vaccine. It's FREE."},
        ],
    },
    ("Public Safety", "Unsafe Structure"): {
        "issue_en": "Dangerous / structurally unsafe building",
        "issue_hi": "खतरनाक / संरचनात्मक रूप से असुरक्षित भवन",
        "steps": [
            "URGENT: Evacuate occupants if imminent danger",
            "Barricade area and restrict access",
            "Deploy structural engineer for assessment",
            "Issue demolition / repair notice as per report",
            "Coordinate with police for evacuation if needed",
        ],
        "steps_hi": [
            "तत्काल: आसन्न खतरा हो तो निवासियों को खाली कराएं",
            "क्षेत्र बैरिकेड करें और प्रवेश प्रतिबंधित करें",
            "संरचनात्मक इंजीनियर आकलन हेतु भेजें",
            "रिपोर्ट अनुसार तोड़-फोड़ / मरम्मत नोटिस जारी करें",
            "आवश्यक हो तो पुलिस से निकासी समन्वय",
        ],
        "required_resources": ["Structural engineer", "Police", "Evacuation support"],
        "estimated_hours": 4,
        "prevention": "Annual building safety audits in old areas",
        "faq": [],
    },
    ("Public Safety", "Encroachment"): {
        "issue_en": "Illegal encroachment on public land",
        "issue_hi": "सार्वजनिक भूमि पर अवैध अतिक्रमण",
        "steps": [
            "Survey and document the encroachment",
            "Cross-check with land records",
            "Issue notice to encroacher",
            "Coordinate removal drive with enforcement team",
            "Install barriers to prevent re-encroachment",
        ],
        "steps_hi": [
            "अतिक्रमण का सर्वेक्षण और दस्तावेजीकरण",
            "भूमि रिकॉर्ड से क्रॉस-चेक करें",
            "अतिक्रमणकारी को नोटिस जारी करें",
            "प्रवर्तन दल के साथ हटाव अभियान",
            "पुनः अतिक्रमण रोकने हेतु बैरियर लगाएं",
        ],
        "required_resources": ["Survey team", "Enforcement squad", "Legal documentation"],
        "estimated_hours": 72,
        "prevention": "Regular patrolling; GIS-based encroachment monitoring",
        "faq": [],
    },
}


# ─────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────

def get_resolution(category: str, subcategory: str) -> Optional[dict]:
    """Look up the resolution steps for a (category, subcategory) pair."""
    return RESOLUTIONS.get((category, subcategory))


def get_resolution_steps(category: str, subcategory: str, lang: str = "english") -> list:
    """Return step list for a complaint type. Falls back to English."""
    res = get_resolution(category, subcategory)
    if res is None:
        return ["Investigate the reported issue", "Take corrective action", "Verify and close"]
    return res.get("steps_hi" if lang == "hindi" else "steps", res["steps"])


def get_faq_answer(category: str, subcategory: str, question: str) -> Optional[str]:
    """Fuzzy-match a citizen question against the FAQ list."""
    res = get_resolution(category, subcategory)
    if res is None or not res.get("faq"):
        return None
    q_lower = question.lower()
    for entry in res["faq"]:
        # simple keyword overlap check
        faq_words = set(entry["q"].lower().split())
        q_words = set(q_lower.split())
        overlap = len(faq_words & q_words)
        if overlap >= 2 or overlap / max(len(faq_words), 1) > 0.5:
            return entry["a"]
    return None


def get_estimated_hours(category: str, subcategory: str) -> int:
    """Return estimated resolution hours from the KB."""
    res = get_resolution(category, subcategory)
    return res["estimated_hours"] if res else 48


def get_required_resources(category: str, subcategory: str) -> list:
    """Return list of resources required to address the complaint."""
    res = get_resolution(category, subcategory)
    return res["required_resources"] if res else []


def get_all_resolutions() -> dict:
    """Return the full resolution database."""
    return RESOLUTIONS
