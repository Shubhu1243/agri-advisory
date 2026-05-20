# disease_info.py
# Complete database of plant diseases with descriptions, symptoms, and top 5 pesticides

DISEASE_DATABASE = {
    "Apple___Apple_scab": {
        "common_name": "Apple Scab",
        "crop": "Apple",
        "description": "A fungal disease caused by Venturia inaequalis. It creates dark, scaly lesions on leaves and fruit.",
        "symptoms": [
            "Olive-green to brown velvety spots on leaves",
            "Dark, corky lesions on fruit",
            "Premature leaf drop",
            "Distorted or cracked fruit"
        ],
        "severity": "High",
        "pesticides": [
            {
                "name": "Captan 50 WP",
                "type": "Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 7-10 days during wet weather",
                "notes": "Apply before rain for best protection"
            },
            {
                "name": "Mancozeb 75 WP",
                "type": "Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 10-14 days",
                "notes": "Broad-spectrum protectant fungicide"
            },
            {
                "name": "Myclobutanil (Rally 40WSP)",
                "type": "Systemic Fungicide",
                "dosage": "0.4 g per liter of water",
                "frequency": "Every 14 days",
                "notes": "Also controls powdery mildew"
            },
            {
                "name": "Trifloxystrobin (Flint)",
                "type": "Strobilurin Fungicide",
                "dosage": "0.14 g per liter of water",
                "frequency": "Every 14 days",
                "notes": "Excellent curative and protective activity"
            },
            {
                "name": "Copper Hydroxide (Kocide)",
                "type": "Inorganic Fungicide",
                "dosage": "3 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Organic-approved option"
            }
        ],
        "prevention": "Prune trees for air circulation, collect fallen leaves, apply dormant sprays"
    },

    "Apple___Black_rot": {
        "common_name": "Apple Black Rot",
        "crop": "Apple",
        "description": "Caused by the fungus Botryosphaeria obtusa. Affects fruit, leaves, and bark.",
        "symptoms": [
            "Brown to black circular lesions on fruit",
            "Frogeye leaf spots (purple-bordered brown spots)",
            "Cankers on branches",
            "Mummified fruit remaining on tree"
        ],
        "severity": "High",
        "pesticides": [
            {
                "name": "Captan 50 WP",
                "type": "Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 10-14 days",
                "notes": "Start at pink stage, continue through harvest"
            },
            {
                "name": "Thiophanate-Methyl (Topsin-M)",
                "type": "Systemic Fungicide",
                "dosage": "1.5 g per liter of water",
                "frequency": "Every 10-14 days",
                "notes": "Effective against multiple fungal diseases"
            },
            {
                "name": "Ziram 76 DF",
                "type": "Protectant Fungicide",
                "dosage": "3 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Also repels deer and birds"
            },
            {
                "name": "Mancozeb 75 WP",
                "type": "Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 10-14 days",
                "notes": "Good resistance management partner"
            },
            {
                "name": "Sulfur (Microthiol Disperss)",
                "type": "Inorganic Fungicide",
                "dosage": "4 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Organic option, avoid in hot weather"
            }
        ],
        "prevention": "Remove mummified fruit and dead wood, improve air circulation, avoid wounding trees"
    },

    "Apple___Cedar_apple_rust": {
        "common_name": "Cedar Apple Rust",
        "crop": "Apple",
        "description": "Caused by Gymnosporangium juniperi-virginianae, requiring both cedar and apple hosts.",
        "symptoms": [
            "Bright orange-yellow spots on upper leaf surface",
            "Tube-like structures on lower leaf surface",
            "Deformed and spotted fruit",
            "Early defoliation"
        ],
        "severity": "Medium",
        "pesticides": [
            {
                "name": "Myclobutanil (Eagle 20EW)",
                "type": "Systemic Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 7-14 days during infection period",
                "notes": "Apply from pink stage through petal fall"
            },
            {
                "name": "Propiconazole (Banner Maxx)",
                "type": "Triazole Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 14 days",
                "notes": "Highly effective against rust diseases"
            },
            {
                "name": "Triadimefon (Bayleton)",
                "type": "Systemic Fungicide",
                "dosage": "0.5 g per liter of water",
                "frequency": "Every 10-14 days",
                "notes": "Good curative activity"
            },
            {
                "name": "Captan + Myclobutanil",
                "type": "Combination Fungicide",
                "dosage": "2.5 g + 0.4 g per liter",
                "frequency": "Every 10 days",
                "notes": "Broad-spectrum protection"
            },
            {
                "name": "Copper Sulfate (Bordeaux Mix)",
                "type": "Inorganic Fungicide",
                "dosage": "4 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Traditional organic option"
            }
        ],
        "prevention": "Remove nearby cedar/juniper trees, plant resistant apple varieties"
    },

    "Apple___healthy": {
        "common_name": "Healthy Apple Leaf",
        "crop": "Apple",
        "description": "The plant appears healthy with no signs of disease.",
        "symptoms": [],
        "severity": "None",
        "pesticides": [],
        "prevention": "Maintain regular monitoring, proper fertilization, and preventive spray schedule"
    },

    "Tomato___Early_blight": {
        "common_name": "Tomato Early Blight",
        "crop": "Tomato",
        "description": "Caused by Alternaria solani fungus. One of the most common tomato diseases worldwide.",
        "symptoms": [
            "Dark brown circular spots with concentric rings (target pattern)",
            "Yellow halo around lesions",
            "Lower leaves affected first",
            "Fruit rot at stem end"
        ],
        "severity": "High",
        "pesticides": [
            {
                "name": "Mancozeb 75 WP (Dithane M-45)",
                "type": "Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Most widely used, economical choice"
            },
            {
                "name": "Chlorothalonil (Kavach)",
                "type": "Contact Fungicide",
                "dosage": "2 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Excellent broad-spectrum protection"
            },
            {
                "name": "Azoxystrobin (Amistar)",
                "type": "Systemic Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 14 days",
                "notes": "Also promotes plant health"
            },
            {
                "name": "Propiconazole (Tilt 25 EC)",
                "type": "Triazole Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 10-14 days",
                "notes": "Strong curative activity"
            },
            {
                "name": "Copper Oxychloride (Blitox)",
                "type": "Inorganic Fungicide",
                "dosage": "3 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Affordable and widely available in India"
            }
        ],
        "prevention": "Crop rotation, remove infected plant debris, stake plants for air flow, mulch soil"
    },

    "Tomato___Late_blight": {
        "common_name": "Tomato Late Blight",
        "crop": "Tomato",
        "description": "Caused by Phytophthora infestans. The same pathogen responsible for Irish Potato Famine.",
        "symptoms": [
            "Water-soaked greenish-gray spots on leaves",
            "White fuzzy mold on undersides of leaves",
            "Dark brown firm lesions on fruit",
            "Rapid plant collapse in wet conditions"
        ],
        "severity": "Very High",
        "pesticides": [
            {
                "name": "Metalaxyl + Mancozeb (Ridomil Gold)",
                "type": "Systemic + Contact Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Gold standard for late blight control"
            },
            {
                "name": "Cymoxanil + Mancozeb (Curzate)",
                "type": "Combination Fungicide",
                "dosage": "3 g per liter of water",
                "frequency": "Every 7 days in disease pressure",
                "notes": "Good curative action (up to 3 days post-infection)"
            },
            {
                "name": "Dimethomorph (Acrobat)",
                "type": "Systemic Fungicide",
                "dosage": "1.5 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Always mix with contact fungicide"
            },
            {
                "name": "Chlorothalonil (Kavach 75 WP)",
                "type": "Protectant Fungicide",
                "dosage": "2 g per liter of water",
                "frequency": "Every 7 days",
                "notes": "Preventive use only, no curative activity"
            },
            {
                "name": "Ametoctradin + Dimethomorph (Zampro)",
                "type": "Dual-Mode Fungicide",
                "dosage": "2 ml per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Excellent resistance management"
            }
        ],
        "prevention": "Avoid overhead irrigation, destroy infected plants immediately, use certified disease-free seeds"
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "common_name": "Tomato Yellow Leaf Curl Virus",
        "crop": "Tomato",
        "description": "A viral disease transmitted by whitefly (Bemisia tabaci). Very destructive in warm climates.",
        "symptoms": [
            "Upward curling and yellowing of leaves",
            "Stunted plant growth",
            "Reduced fruit set",
            "Small, pale yellow leaves"
        ],
        "severity": "Very High",
        "pesticides": [
            {
                "name": "Imidacloprid (Confidor 200 SL)",
                "type": "Systemic Insecticide (Whitefly control)",
                "dosage": "0.5 ml per liter of water",
                "frequency": "Every 10-14 days",
                "notes": "Controls virus vector (whitefly), not the virus itself"
            },
            {
                "name": "Thiamethoxam (Actara 25 WG)",
                "type": "Neonicotinoid Insecticide",
                "dosage": "0.3 g per liter of water",
                "frequency": "Every 14 days",
                "notes": "Soil drench for longer protection"
            },
            {
                "name": "Spiromesifen (Oberon)",
                "type": "Acaricide/Insecticide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 10-14 days",
                "notes": "Specifically targets whitefly nymphs"
            },
            {
                "name": "Buprofezin (Applaud)",
                "type": "Insect Growth Regulator",
                "dosage": "1.5 ml per liter of water",
                "frequency": "Every 14-21 days",
                "notes": "Disrupts whitefly development"
            },
            {
                "name": "Neem Oil (Azadirachtin)",
                "type": "Botanical Insecticide",
                "dosage": "5 ml per liter of water",
                "frequency": "Every 7 days",
                "notes": "Organic option, repels and disrupts feeding"
            }
        ],
        "prevention": "Use reflective mulch, install sticky yellow traps, plant resistant varieties, use insect-proof nets"
    },

    "Tomato___healthy": {
        "common_name": "Healthy Tomato Leaf",
        "crop": "Tomato",
        "description": "The plant appears healthy with no signs of disease.",
        "symptoms": [],
        "severity": "None",
        "pesticides": [],
        "prevention": "Regular monitoring, balanced fertilization, proper irrigation management"
    },

    "Potato___Early_blight": {
        "common_name": "Potato Early Blight",
        "crop": "Potato",
        "description": "Caused by Alternaria solani. Typically affects older, stressed plants first.",
        "symptoms": [
            "Dark brown lesions with concentric rings on older leaves",
            "Yellowing around lesions",
            "Leaf drop starting from bottom of plant",
            "Small dark lesions on tubers"
        ],
        "severity": "Medium",
        "pesticides": [
            {
                "name": "Mancozeb 75 WP",
                "type": "Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Start spraying when disease first appears"
            },
            {
                "name": "Chlorothalonil (Bravo 720)",
                "type": "Contact Fungicide",
                "dosage": "2 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Very effective protectant fungicide"
            },
            {
                "name": "Azoxystrobin + Difenoconazole (Amistar Top)",
                "type": "Dual Systemic Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 14 days",
                "notes": "Excellent curative and preventive action"
            },
            {
                "name": "Fenamidone + Mancozeb (Equation Pro)",
                "type": "Combination Fungicide",
                "dosage": "3 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Good systemic and contact activity"
            },
            {
                "name": "Copper Hydroxide",
                "type": "Inorganic Fungicide",
                "dosage": "3 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Organic farming option"
            }
        ],
        "prevention": "Crop rotation (3 years), destroy crop debris, use certified seed potatoes"
    },

    "Potato___Late_blight": {
        "common_name": "Potato Late Blight",
        "crop": "Potato",
        "description": "Caused by Phytophthora infestans. The most devastating potato disease globally.",
        "symptoms": [
            "Water-soaked pale green spots turning brown-black",
            "White cottony growth on undersides in humid conditions",
            "Rapid browning and death of foliage",
            "Brown rot spreading through tuber flesh"
        ],
        "severity": "Very High",
        "pesticides": [
            {
                "name": "Metalaxyl-M + Mancozeb (Ridomil Gold MZ)",
                "type": "Systemic + Contact Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 7 days during risk periods",
                "notes": "Most effective product for late blight"
            },
            {
                "name": "Propamocarb + Fluopicolide (Infinito)",
                "type": "Dual Systemic Fungicide",
                "dosage": "1.5 ml per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Excellent tuber protection"
            },
            {
                "name": "Cymoxanil 8% + Mancozeb 64%",
                "type": "Combination Fungicide",
                "dosage": "3 g per liter of water",
                "frequency": "Every 7 days",
                "notes": "3-day curative window after infection"
            },
            {
                "name": "Mandipropamid (Revus)",
                "type": "CAA Fungicide",
                "dosage": "0.6 ml per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Excellent rainfastness (1 hour)"
            },
            {
                "name": "Copper Sulfate (Bordeaux Mixture 1%)",
                "type": "Inorganic Fungicide",
                "dosage": "10 g copper sulfate + 10 g lime per liter",
                "frequency": "Every 7-10 days",
                "notes": "Traditional and organic-approved"
            }
        ],
        "prevention": "Use certified blight-free seed, haulm destruction before harvest, proper storage ventilation"
    },

    "Potato___healthy": {
        "common_name": "Healthy Potato Leaf",
        "crop": "Potato",
        "description": "The plant appears healthy with no signs of disease.",
        "symptoms": [],
        "severity": "None",
        "pesticides": [],
        "prevention": "Regular scouting, balanced NPK fertilization, avoid waterlogging"
    },

    "Corn_(maize)___Common_rust_": {
        "common_name": "Corn Common Rust",
        "crop": "Corn/Maize",
        "description": "Caused by Puccinia sorghi fungus. Widely prevalent in cool, moist conditions.",
        "symptoms": [
            "Small cinnamon-brown to brick-red pustules on both leaf surfaces",
            "Pustules turn dark brown/black as they mature",
            "Yellowing of severely infected leaves",
            "Reduced grain fill in severe cases"
        ],
        "severity": "Medium",
        "pesticides": [
            {
                "name": "Propiconazole (Tilt 25 EC)",
                "type": "Triazole Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Apply at first sign, repeat in 14 days if needed",
                "notes": "Most cost-effective option for corn rust"
            },
            {
                "name": "Azoxystrobin (Amistar 25 SC)",
                "type": "Strobilurin Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 14-21 days",
                "notes": "Also improves overall plant health"
            },
            {
                "name": "Pyraclostrobin (Headline EC)",
                "type": "Strobilurin Fungicide",
                "dosage": "1.5 ml per liter of water",
                "frequency": "Every 14 days",
                "notes": "Good preventive and curative activity"
            },
            {
                "name": "Tebuconazole (Folicur 250 EW)",
                "type": "Triazole Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 14 days",
                "notes": "Broad-spectrum disease control"
            },
            {
                "name": "Mancozeb 75 WP",
                "type": "Contact Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Economical preventive option"
            }
        ],
        "prevention": "Plant resistant hybrids, early planting, balanced nitrogen fertilization"
    },

    "Corn_(maize)___healthy": {
        "common_name": "Healthy Corn Leaf",
        "crop": "Corn/Maize",
        "description": "The plant appears healthy with no signs of disease.",
        "symptoms": [],
        "severity": "None",
        "pesticides": [],
        "prevention": "Regular scouting, use certified disease-resistant hybrids"
    },

    "Grape___Black_rot": {
        "common_name": "Grape Black Rot",
        "crop": "Grape",
        "description": "Caused by Guignardia bidwellii. Can destroy entire grape crops in humid conditions.",
        "symptoms": [
            "Tan-brown circular lesions with dark border on leaves",
            "Small black pycnidia (dots) in lesion center",
            "Fruit shrivels into hard black 'mummies'",
            "Infected shoots and tendrils"
        ],
        "severity": "Very High",
        "pesticides": [
            {
                "name": "Mancozeb 75 WP",
                "type": "Contact Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 7-10 days from bud break",
                "notes": "Start at 1-inch shoot growth"
            },
            {
                "name": "Myclobutanil (Nova 40W)",
                "type": "Systemic Fungicide",
                "dosage": "0.4 g per liter of water",
                "frequency": "Every 14 days",
                "notes": "Excellent curative activity (3-4 days)"
            },
            {
                "name": "Captan 50 WP",
                "type": "Fungicide",
                "dosage": "2.5 g per liter of water",
                "frequency": "Every 7-10 days",
                "notes": "Especially important during bloom period"
            },
            {
                "name": "Azoxystrobin (Abound)",
                "type": "Strobilurin Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 14 days",
                "notes": "Do not use more than twice consecutively"
            },
            {
                "name": "Tebuconazole (Elite 45 DF)",
                "type": "Triazole Fungicide",
                "dosage": "0.4 g per liter of water",
                "frequency": "Every 14 days",
                "notes": "Strong curative and preventive activity"
            }
        ],
        "prevention": "Prune for air circulation, remove mummies, train vines properly"
    },

    "Grape___healthy": {
        "common_name": "Healthy Grape Leaf",
        "crop": "Grape",
        "description": "The plant appears healthy with no signs of disease.",
        "symptoms": [],
        "severity": "None",
        "pesticides": [],
        "prevention": "Proper canopy management, regular pruning, adequate spacing"
    },

    "Rice___Leaf_scald": {
        "common_name": "Rice Leaf Scald",
        "crop": "Rice",
        "description": "Caused by Microdochium oryzae. Common in tropical rice growing areas.",
        "symptoms": [
            "Zonate oblong lesions with brown margins",
            "Lesions start at leaf tips and margins",
            "Light brown center with dark brown border",
            "Infected leaves dry out rapidly"
        ],
        "severity": "Medium",
        "pesticides": [
            {
                "name": "Propiconazole (Tilt 25 EC)",
                "type": "Triazole Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "2-3 applications, 14 days apart",
                "notes": "Most recommended for rice leaf diseases"
            },
            {
                "name": "Tricyclazole (Beam 75 WP)",
                "type": "Specific Fungicide",
                "dosage": "0.6 g per liter of water",
                "frequency": "Every 14 days",
                "notes": "Highly effective against rice fungal diseases"
            },
            {
                "name": "Isoprothiolane (Fuji-one 40 EC)",
                "type": "Organophosphorus Fungicide",
                "dosage": "1.5 ml per liter of water",
                "frequency": "Every 14-21 days",
                "notes": "Systemic with good rainfastness"
            },
            {
                "name": "Copper Hydroxide",
                "type": "Inorganic Fungicide",
                "dosage": "3 g per liter of water",
                "frequency": "Every 10 days",
                "notes": "Preventive option"
            },
            {
                "name": "Hexaconazole (Contaf Plus)",
                "type": "Triazole Fungicide",
                "dosage": "1 ml per liter of water",
                "frequency": "Every 14 days",
                "notes": "Widely available in Indian markets"
            }
        ],
        "prevention": "Use balanced fertilization, avoid excessive nitrogen, proper water management"
    },

    "default": {
        "common_name": "Unknown Disease",
        "crop": "Unknown",
        "description": "Disease details not available in database. Please consult a local agricultural expert.",
        "symptoms": ["Consult a local agricultural expert for accurate diagnosis"],
        "severity": "Unknown",
        "pesticides": [
            {
                "name": "Consult Local Agronomist",
                "type": "Advisory",
                "dosage": "N/A",
                "frequency": "N/A",
                "notes": "Visit your nearest Krishi Vigyan Kendra (KVK) for guidance"
            }
        ],
        "prevention": "Regular monitoring and consult agricultural extension officers"
    }
}


def get_disease_info(disease_label: str) -> dict:
    """
    Retrieve disease information from the database.
    Falls back to 'default' if disease not found.
    """
    # Clean the label
    label = disease_label.strip()
    
    # Direct lookup
    if label in DISEASE_DATABASE:
        return DISEASE_DATABASE[label]
    
    # Partial match fallback
    for key in DISEASE_DATABASE:
        if key.lower() in label.lower() or label.lower() in key.lower():
            return DISEASE_DATABASE[key]
    
    # Return default with the disease name substituted
    default = DISEASE_DATABASE["default"].copy()
    parts = label.split("___")
    if len(parts) == 2:
        default["crop"] = parts[0].replace("_", " ")
        default["common_name"] = parts[1].replace("_", " ")
    return default


def get_severity_color(severity: str) -> str:
    """Return color code based on severity level."""
    colors = {
        "None": "#2ecc71",
        "Low": "#f1c40f",
        "Medium": "#e67e22",
        "High": "#e74c3c",
        "Very High": "#8e44ad"
    }
    return colors.get(severity, "#95a5a6")


def is_healthy(disease_label: str) -> bool:
    """Check if the plant is healthy."""
    return "healthy" in disease_label.lower()