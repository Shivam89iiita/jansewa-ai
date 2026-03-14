"""
Complaint Category Knowledge Base
===================================
Complete taxonomy of governance complaints with:
- Hindi/English category names
- Subcategories and keywords
- Default severity, SLA, and department mappings
- Synonyms and regional language terms
"""

# ─────────────────────────────────────────────────────────
# MASTER CATEGORY TAXONOMY
# ─────────────────────────────────────────────────────────

CATEGORIES = {
    "water_supply": {
        "id": 1,
        "name_en": "Water Supply",
        "name_hi": "जल आपूर्ति",
        "department": "Water Supply Department",
        "department_hi": "जल आपूर्ति विभाग",
        "default_severity": "HIGH",
        "base_urgency": 85,
        "sla_hours": 24,
        "subcategories": {
            "no_water": {
                "name_en": "No Water Supply",
                "name_hi": "पानी नहीं आ रहा",
                "severity": "CRITICAL",
                "urgency": 95,
                "sla_hours": 12,
                "keywords_en": [
                    "no water", "water not coming", "water supply stopped",
                    "water cut", "water shortage", "dry tap", "taps dry",
                    "no running water", "water not available", "water problem",
                ],
                "keywords_hi": [
                    "पानी नहीं", "पानी बंद", "पानी नहीं आ रहा", "नल सूखा",
                    "जल आपूर्ति बंद", "पानी की किल्लत", "पाइप में पानी नहीं",
                    "paani nahi", "paani band", "nal se paani nahi aa raha",
                ],
            },
            "dirty_water": {
                "name_en": "Contaminated/Dirty Water",
                "name_hi": "गंदा पानी",
                "severity": "CRITICAL",
                "urgency": 95,
                "sla_hours": 6,
                "keywords_en": [
                    "dirty water", "contaminated water", "brown water",
                    "yellow water", "smelly water", "unclean water",
                    "water pollution", "unsafe water", "muddy water",
                ],
                "keywords_hi": [
                    "गंदा पानी", "दूषित पानी", "पीला पानी", "बदबूदार पानी",
                    "ganda paani", "paani mein keede", "safed paani",
                ],
            },
            "low_pressure": {
                "name_en": "Low Water Pressure",
                "name_hi": "पानी का कम दबाव",
                "severity": "MEDIUM",
                "urgency": 60,
                "sla_hours": 48,
                "keywords_en": [
                    "low pressure", "weak flow", "trickle", "barely any water",
                    "low water pressure", "water pressure low",
                ],
                "keywords_hi": [
                    "कम प्रेशर", "पानी धीरे आ रहा", "बहुत कम पानी",
                    "kam pressure", "paani bahut kam aa raha",
                ],
            },
            "pipeline_leak": {
                "name_en": "Pipeline Leakage/Burst",
                "name_hi": "पाइपलाइन रिसाव/टूटी",
                "severity": "HIGH",
                "urgency": 85,
                "sla_hours": 12,
                "keywords_en": [
                    "pipe leak", "pipe burst", "broken pipe", "leaking pipe",
                    "pipeline burst", "water pipe broken", "water leaking",
                    "pipeline damage", "water wastage", "pipe damage",
                ],
                "keywords_hi": [
                    "पाइप टूटा", "पाइप लीक", "पानी बह रहा", "पाइपलाइन फटी",
                    "pipe toota", "pipe se paani beh raha",
                ],
            },
            "billing": {
                "name_en": "Water Bill Issues",
                "name_hi": "पानी बिल की समस्या",
                "severity": "LOW",
                "urgency": 30,
                "sla_hours": 72,
                "keywords_en": [
                    "water bill", "excess bill", "wrong bill", "bill dispute",
                    "overcharged", "meter faulty", "water meter",
                ],
                "keywords_hi": [
                    "पानी का बिल", "बिल ज्यादा", "गलत बिल", "मीटर खराब",
                    "paani ka bill", "bill zyada aaya",
                ],
            },
        },
    },

    "road_pothole": {
        "id": 2,
        "name_en": "Road / Pothole",
        "name_hi": "सड़क / गड्ढा",
        "department": "Roads & Infrastructure Department",
        "department_hi": "सड़क एवं अवसंरचना विभाग",
        "default_severity": "MEDIUM",
        "base_urgency": 60,
        "sla_hours": 72,
        "subcategories": {
            "pothole": {
                "name_en": "Pothole on Road",
                "name_hi": "सड़क पर गड्ढा",
                "severity": "HIGH",
                "urgency": 75,
                "sla_hours": 48,
                "keywords_en": [
                    "pothole", "road hole", "big hole", "dangerous hole",
                    "pit on road", "crater", "road damage", "dip in road",
                ],
                "keywords_hi": [
                    "गड्ढा", "सड़क में गड्ढा", "रोड पर गड्ढा", "बड़ा गड्ढा",
                    "gadda", "sadak mein gadda", "road pe hole",
                ],
            },
            "road_damage": {
                "name_en": "Road Surface Damage",
                "name_hi": "सड़क की सतह खराब",
                "severity": "MEDIUM",
                "urgency": 55,
                "sla_hours": 96,
                "keywords_en": [
                    "road broken", "road damaged", "cracks in road",
                    "road surface", "bad road", "road condition",
                    "uneven road", "road deteriorated",
                ],
                "keywords_hi": [
                    "सड़क टूटी", "सड़क खराब", "रास्ता खराब", "सड़क में दरार",
                    "sadak tooti", "sadak kharab", "road toor gayi",
                ],
            },
            "waterlogging": {
                "name_en": "Waterlogging on Road",
                "name_hi": "सड़क पर जलभराव",
                "severity": "HIGH",
                "urgency": 80,
                "sla_hours": 24,
                "keywords_en": [
                    "waterlogging", "water on road", "flooding", "road flooded",
                    "stagnant water", "water accumulation", "road submerged",
                ],
                "keywords_hi": [
                    "जलभराव", "सड़क पर पानी", "पानी भरा", "बाढ़ जैसी स्थिति",
                    "paani bhara", "sadak pe paani", "jal bharav",
                ],
            },
            "footpath": {
                "name_en": "Footpath / Sidewalk Issues",
                "name_hi": "फुटपाथ की समस्या",
                "severity": "LOW",
                "urgency": 35,
                "sla_hours": 120,
                "keywords_en": [
                    "footpath", "sidewalk", "pavement broken", "footpath blocked",
                    "pedestrian", "walking path", "footpath encroachment",
                ],
                "keywords_hi": [
                    "फुटपाथ", "पैदल मार्ग", "फुटपाथ टूटा", "पगडंडी",
                    "footpath toota", "pedestrian path",
                ],
            },
            "speed_breaker": {
                "name_en": "Speed Breaker Required/Damaged",
                "name_hi": "स्पीड ब्रेकर",
                "severity": "MEDIUM",
                "urgency": 50,
                "sla_hours": 96,
                "keywords_en": [
                    "speed breaker", "speed bump", "no speed breaker",
                    "speed breaker broken", "need speed breaker",
                ],
                "keywords_hi": [
                    "स्पीड ब्रेकर", "speed breaker chahiye", "speed breaker toota",
                ],
            },
        },
    },

    "electricity": {
        "id": 3,
        "name_en": "Electricity",
        "name_hi": "बिजली",
        "department": "Electricity Department",
        "department_hi": "विद्युत विभाग",
        "default_severity": "HIGH",
        "base_urgency": 75,
        "sla_hours": 24,
        "subcategories": {
            "power_cut": {
                "name_en": "Power Cut / Outage",
                "name_hi": "बिजली कटौती",
                "severity": "HIGH",
                "urgency": 80,
                "sla_hours": 12,
                "keywords_en": [
                    "no electricity", "power cut", "blackout", "no power",
                    "electricity gone", "power outage", "no light", "load shedding",
                ],
                "keywords_hi": [
                    "बिजली नहीं", "बिजली कटौती", "बिजली गुल", "अंधेरा",
                    "bijli nahi", "bijli gayi", "bijli nahi aa rahi",
                    "light nahi", "bijli kat gayi",
                ],
            },
            "street_light": {
                "name_en": "Street Light Not Working",
                "name_hi": "सड़क की बत्ती बंद",
                "severity": "MEDIUM",
                "urgency": 55,
                "sla_hours": 48,
                "keywords_en": [
                    "street light", "lamp post", "no light outside",
                    "dark street", "broken street light", "light pole",
                    "bulb fused", "led light not working",
                ],
                "keywords_hi": [
                    "सड़क की बत्ती", "स्ट्रीट लाइट", "बत्ती बंद", "खंभे की लाइट",
                    "street light band", "raat ko andhera",
                ],
            },
            "transformer": {
                "name_en": "Transformer Issue",
                "name_hi": "ट्रांसफार्मर की समस्या",
                "severity": "CRITICAL",
                "urgency": 90,
                "sla_hours": 8,
                "keywords_en": [
                    "transformer", "transformer blast", "transformer fire",
                    "transformer damaged", "transformer overload",
                ],
                "keywords_hi": [
                    "ट्रांसफार्मर", "ट्रांसफार्मर फटा", "ट्रांसफार्मर में आग",
                    "transformer blast", "transformer kharab",
                ],
            },
            "wire_danger": {
                "name_en": "Loose / Dangerous Wires",
                "name_hi": "खुले / खतरनाक तार",
                "severity": "CRITICAL",
                "urgency": 95,
                "sla_hours": 4,
                "keywords_en": [
                    "loose wire", "open wire", "dangling wire", "exposed wire",
                    "electric shock", "wire hanging", "dangerous wire",
                    "live wire", "wire sparking",
                ],
                "keywords_hi": [
                    "खुला तार", "तार लटक रहा", "बिजली का तार", "करंट",
                    "tar latka hai", "bijli ka tar", "shock laga",
                ],
            },
        },
    },

    "drainage": {
        "id": 4,
        "name_en": "Drainage / Sewage",
        "name_hi": "नाली / सीवर",
        "department": "Drainage & Sanitation Department",
        "department_hi": "जल निकासी एवं स्वच्छता विभाग",
        "default_severity": "HIGH",
        "base_urgency": 80,
        "sla_hours": 24,
        "subcategories": {
            "drain_overflow": {
                "name_en": "Drain Overflow",
                "name_hi": "नाली उभर रही है",
                "severity": "CRITICAL",
                "urgency": 90,
                "sla_hours": 8,
                "keywords_en": [
                    "drain overflow", "sewage overflow", "drain blocked",
                    "sewage on road", "drain overflowing", "sewer backup",
                ],
                "keywords_hi": [
                    "नाली उभर रही", "सीवर ओवरफ्लो", "नाली बंद", "गंदा पानी सड़क पर",
                    "naali ubhar rahi", "nali band", "sewer overflow",
                ],
            },
            "drain_blocked": {
                "name_en": "Drain Blockage",
                "name_hi": "नाली बंद/जाम",
                "severity": "HIGH",
                "urgency": 75,
                "sla_hours": 24,
                "keywords_en": [
                    "drain blocked", "clogged drain", "drain jammed",
                    "blocked sewer", "drain not flowing",
                ],
                "keywords_hi": [
                    "नाली जाम", "नाली बंद", "नाली का पानी रुका",
                    "nali jam", "nali band ho gayi",
                ],
            },
            "open_drain": {
                "name_en": "Open Drain / No Cover",
                "name_hi": "खुली नाली",
                "severity": "HIGH",
                "urgency": 80,
                "sla_hours": 48,
                "keywords_en": [
                    "open drain", "drain cover missing", "no drain cover",
                    "uncovered drain", "dangerous drain",
                ],
                "keywords_hi": [
                    "खुली नाली", "नाली का ढक्कन नहीं", "बिना ढक्कन",
                    "khuli naali", "nali ka dhakkan nahi",
                ],
            },
            "drain_smell": {
                "name_en": "Bad Smell from Drain",
                "name_hi": "नाली से बदबू",
                "severity": "MEDIUM",
                "urgency": 55,
                "sla_hours": 48,
                "keywords_en": [
                    "bad smell", "stench", "foul smell", "drain smell",
                    "sewage smell", "horrible stink",
                ],
                "keywords_hi": [
                    "बदबू", "नाली से बदबू", "गंदी बास", "सीवर की बदबू",
                    "badboo", "smell aa rahi hai", "nali se badboo",
                ],
            },
        },
    },

    "garbage": {
        "id": 5,
        "name_en": "Garbage / Sanitation",
        "name_hi": "कूड़ा / स्वच्छता",
        "department": "Sanitation Department",
        "department_hi": "स्वच्छता विभाग",
        "default_severity": "MEDIUM",
        "base_urgency": 65,
        "sla_hours": 24,
        "subcategories": {
            "not_collected": {
                "name_en": "Garbage Not Collected",
                "name_hi": "कूड़ा नहीं उठाया गया",
                "severity": "HIGH",
                "urgency": 75,
                "sla_hours": 12,
                "keywords_en": [
                    "garbage not collected", "no garbage pickup",
                    "dustbin not cleared", "trash not picked",
                    "waste not collected", "garbage lying",
                ],
                "keywords_hi": [
                    "कूड़ा नहीं उठाया", "सफाई नहीं हुई", "कचरा पड़ा है",
                    "kachra nahi uthaya", "safai nahi hui", "dustbin nahi saaf hua",
                ],
            },
            "dumping": {
                "name_en": "Illegal Dumping",
                "name_hi": "अवैध कूड़ा फेंकना",
                "severity": "MEDIUM",
                "urgency": 60,
                "sla_hours": 48,
                "keywords_en": [
                    "illegal dumping", "garbage dump", "waste dump",
                    "dumping ground", "throwing garbage", "open dumping",
                ],
                "keywords_hi": [
                    "कूड़ा फेंकना", "कचरा डंप", "खुले में कूड़ा",
                    "kooda phenk rahe", "garbage dump ban gaya",
                ],
            },
            "dustbin_missing": {
                "name_en": "Dustbin Missing / Full",
                "name_hi": "डस्टबिन नहीं / भरा हुआ",
                "severity": "LOW",
                "urgency": 40,
                "sla_hours": 72,
                "keywords_en": [
                    "no dustbin", "dustbin missing", "dustbin full",
                    "overflowing dustbin", "need dustbin",
                ],
                "keywords_hi": [
                    "डस्टबिन नहीं है", "डस्टबिन भरा", "कूड़ेदान नहीं",
                    "dustbin nahi hai", "dustbin full ho gaya",
                ],
            },
        },
    },

    "health": {
        "id": 6,
        "name_en": "Health / Medical",
        "name_hi": "स्वास्थ्य / चिकित्सा",
        "department": "Health Department",
        "department_hi": "स्वास्थ्य विभाग",
        "default_severity": "HIGH",
        "base_urgency": 90,
        "sla_hours": 12,
        "subcategories": {
            "disease_outbreak": {
                "name_en": "Disease Outbreak",
                "name_hi": "बीमारी का प्रकोप",
                "severity": "CRITICAL",
                "urgency": 98,
                "sla_hours": 4,
                "keywords_en": [
                    "dengue", "malaria", "cholera", "epidemic", "outbreak",
                    "fever spreading", "diarrhea", "typhoid", "chikungunya",
                    "disease", "infection spreading",
                ],
                "keywords_hi": [
                    "डेंगू", "मलेरिया", "हैजा", "महामारी", "बुखार फैल रहा",
                    "दस्त", "टाइफाइड", "चिकनगुनिया", "बीमारी फैल रही",
                    "dengue ho raha", "bukhar aa raha sabko",
                ],
            },
            "mosquito": {
                "name_en": "Mosquito Breeding",
                "name_hi": "मच्छर पनप रहे",
                "severity": "HIGH",
                "urgency": 80,
                "sla_hours": 24,
                "keywords_en": [
                    "mosquito", "mosquitoes", "breeding", "mosquito breeding",
                    "fogging needed", "stagnant water mosquito",
                ],
                "keywords_hi": [
                    "मच्छर", "मच्छर बहुत", "मच्छर पैदा हो रहे", "फॉगिंग चाहिए",
                    "machchar bahut hai", "fogging nahi hui",
                ],
            },
            "hospital": {
                "name_en": "Hospital / Clinic Issues",
                "name_hi": "अस्पताल/क्लिनिक की समस्या",
                "severity": "HIGH",
                "urgency": 85,
                "sla_hours": 24,
                "keywords_en": [
                    "hospital", "clinic", "doctor not available", "no medicine",
                    "primary health center", "PHC closed",
                ],
                "keywords_hi": [
                    "अस्पताल", "क्लिनिक", "डॉक्टर नहीं", "दवाई नहीं",
                    "hospital band", "doctor nahi aata",
                ],
            },
            "stray_animals": {
                "name_en": "Stray Animals / Dog Bite",
                "name_hi": "आवारा जानवर / कुत्ते का काटना",
                "severity": "HIGH",
                "urgency": 80,
                "sla_hours": 12,
                "keywords_en": [
                    "stray dog", "dog bite", "stray animals", "monkey menace",
                    "cattle on road", "animal attack", "rabid dog",
                ],
                "keywords_hi": [
                    "आवारा कुत्ता", "कुत्ते ने काटा", "आवारा जानवर", "बंदर",
                    "kutte ne kaata", "aawara janwar", "kutte bahut hain",
                ],
            },
        },
    },

    "public_safety": {
        "id": 7,
        "name_en": "Public Safety",
        "name_hi": "सार्वजनिक सुरक्षा",
        "department": "Public Safety & Enforcement",
        "department_hi": "सार्वजनिक सुरक्षा एवं प्रवर्तन विभाग",
        "default_severity": "HIGH",
        "base_urgency": 95,
        "sla_hours": 8,
        "subcategories": {
            "encroachment": {
                "name_en": "Illegal Encroachment",
                "name_hi": "अवैध अतिक्रमण",
                "severity": "MEDIUM",
                "urgency": 55,
                "sla_hours": 72,
                "keywords_en": [
                    "encroachment", "illegal construction", "unauthorized building",
                    "blocking road", "footpath encroachment",
                ],
                "keywords_hi": [
                    "अतिक्रमण", "अवैध निर्माण", "सड़क पर कब्जा", "अवैध दुकान",
                    "atikraman", "illegal construction",
                ],
            },
            "unsafe_building": {
                "name_en": "Unsafe / Collapsing Structure",
                "name_hi": "असुरक्षित / गिरने वाली इमारत",
                "severity": "CRITICAL",
                "urgency": 98,
                "sla_hours": 4,
                "keywords_en": [
                    "building collapse", "wall falling", "unsafe structure",
                    "cracks in building", "tilting building", "dangerous building",
                ],
                "keywords_hi": [
                    "इमारत गिर रही", "दीवार गिर रही", "खतरनाक इमारत",
                    "building gir rahi", "deewar gir sakti hai",
                ],
            },
            "tree_fallen": {
                "name_en": "Fallen Tree / Dangerous Tree",
                "name_hi": "पेड़ गिरा / खतरनाक पेड़",
                "severity": "HIGH",
                "urgency": 85,
                "sla_hours": 12,
                "keywords_en": [
                    "tree fallen", "tree blocking", "dangerous tree",
                    "tree about to fall", "broken branch", "uprooted tree",
                ],
                "keywords_hi": [
                    "पेड़ गिरा", "पेड़ गिर सकता है", "डाल टूटी",
                    "ped gira", "ped gir sakta hai", "branch tooti",
                ],
            },
            "crime_safety": {
                "name_en": "Crime / Safety Concern",
                "name_hi": "अपराध / सुरक्षा चिंता",
                "severity": "CRITICAL",
                "urgency": 95,
                "sla_hours": 4,
                "keywords_en": [
                    "crime", "theft", "robbery", "chain snatching",
                    "eve teasing", "harassment", "drunk and disorderly",
                    "gambling", "drug dealing", "not safe",
                ],
                "keywords_hi": [
                    "चोरी", "लूट", "छेड़खानी", "शराबी", "जुआ", "नशा",
                    "असुरक्षित", "chori ho gayi", "loot", "safe nahi hai",
                ],
            },
        },
    },

    "other": {
        "id": 8,
        "name_en": "Other / General",
        "name_hi": "अन्य / सामान्य",
        "department": "General Administration",
        "department_hi": "सामान्य प्रशासन विभाग",
        "default_severity": "LOW",
        "base_urgency": 40,
        "sla_hours": 96,
        "subcategories": {
            "park_maintenance": {
                "name_en": "Park / Garden Maintenance",
                "name_hi": "पार्क / बगीचे की देखभाल",
                "severity": "LOW",
                "urgency": 25,
                "sla_hours": 120,
                "keywords_en": [
                    "park", "garden", "playground", "park maintenance",
                    "grass not cut", "park dirty", "broken bench",
                ],
                "keywords_hi": [
                    "पार्क", "बगीचा", "खेल मैदान", "पार्क की सफाई",
                    "park ganda hai", "ghaas nahi kati",
                ],
            },
            "noise_pollution": {
                "name_en": "Noise Pollution",
                "name_hi": "ध्वनि प्रदूषण",
                "severity": "LOW",
                "urgency": 30,
                "sla_hours": 72,
                "keywords_en": [
                    "noise", "loud music", "noise pollution",
                    "loudspeaker", "factory noise", "construction noise",
                ],
                "keywords_hi": [
                    "शोर", "तेज आवाज", "लाउडस्पीकर", "ध्वनि प्रदूषण",
                    "shor bahut hai", "loud music", "awaaz bahut hai",
                ],
            },
            "corruption": {
                "name_en": "Corruption / Bribery Report",
                "name_hi": "भ्रष्टाचार / रिश्वत",
                "severity": "HIGH",
                "urgency": 85,
                "sla_hours": 24,
                "keywords_en": [
                    "corruption", "bribery", "bribe", "scam", "fraud",
                    "money demanded", "extortion", "official demanding",
                ],
                "keywords_hi": [
                    "भ्रष्टाचार", "रिश्वत", "घोटाला", "पैसे मांग रहे",
                    "rishwat", "bhrashtachar", "paisa maang rahe",
                    "ghapla", "corrupt", "chor",
                ],
            },
            "certificate": {
                "name_en": "Certificate / Document Issues",
                "name_hi": "प्रमाणपत्र / दस्तावेज़",
                "severity": "LOW",
                "urgency": 25,
                "sla_hours": 120,
                "keywords_en": [
                    "birth certificate", "death certificate", "property",
                    "license", "permit", "document", "NOC",
                ],
                "keywords_hi": [
                    "जन्म प्रमाणपत्र", "मृत्यु प्रमाणपत्र", "प्रॉपर्टी",
                    "लाइसेंस", "दस्तावेज़", "NOC", "certificate nahi mil raha",
                ],
            },
        },
    },
}


# ─────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────

def get_all_categories() -> list[dict]:
    """Return flat list of categories."""
    return [
        {
            "id": cat["id"],
            "name_en": cat["name_en"],
            "name_hi": cat["name_hi"],
            "department": cat["department"],
        }
        for cat in CATEGORIES.values()
    ]


def get_category_by_name(name: str) -> dict | None:
    """Look up category by English name (case-insensitive)."""
    name_lower = name.lower().strip()
    for key, cat in CATEGORIES.items():
        if cat["name_en"].lower() == name_lower or key == name_lower:
            return cat
    return None


def get_all_keywords() -> dict[str, list[str]]:
    """Return {category_key: [all_keywords]} dict for classifier."""
    result = {}
    for cat_key, cat in CATEGORIES.items():
        keywords = []
        for sub in cat["subcategories"].values():
            keywords.extend(sub.get("keywords_en", []))
            keywords.extend(sub.get("keywords_hi", []))
        result[cat_key] = keywords
    return result


def get_subcategory_match(text: str) -> dict | None:
    """Find the best-matching subcategory for a text input."""
    text_lower = text.lower()
    best_match = None
    best_score = 0

    for cat_key, cat in CATEGORIES.items():
        for sub_key, sub in cat["subcategories"].items():
            score = 0
            for kw in sub.get("keywords_en", []) + sub.get("keywords_hi", []):
                if kw.lower() in text_lower:
                    score += len(kw)  # longer keyword matches = higher confidence
            if score > best_score:
                best_score = score
                best_match = {
                    "category_key": cat_key,
                    "category_name": cat["name_en"],
                    "category_name_hi": cat["name_hi"],
                    "subcategory_key": sub_key,
                    "subcategory_name": sub["name_en"],
                    "subcategory_name_hi": sub["name_hi"],
                    "severity": sub["severity"],
                    "urgency": sub["urgency"],
                    "sla_hours": sub["sla_hours"],
                    "department": cat["department"],
                    "department_hi": cat["department_hi"],
                    "match_score": score,
                }

    return best_match
