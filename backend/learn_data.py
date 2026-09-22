"""
backend/learn_data.py
Bilingual (English / Telugu) educational content for the Learn section.
"""

LEARN_CONTENT = {
    "en": {
        "savings": {
            "title": "Savings Calculator",
            "formula": "Available Savings = Monthly Income − Monthly Expenses",
            "explanation": (
                "Your available savings is simply what is left over after your "
                "monthly expenses are subtracted from your income. To estimate "
                "how long it will take to reach a goal, divide the goal price "
                "by your available monthly savings."
            ),
            "example": (
                "Example: If you earn ₹30,000 a month and spend ₹22,000, your "
                "available savings is ₹8,000. To buy a ₹80,000 laptop, you would "
                "need about 10 months (80,000 ÷ 8,000 = 10)."
            ),
            "tip": "Try to save at least 20% of your income every month before spending on wants.",
        },
        "emi": {
            "title": "EMI Calculator",
            "formula": "EMI = P × [r × (1+r)^n] ÷ [(1+r)^n − 1]",
            "explanation": (
                "P is the loan principal, r is the monthly interest rate "
                "(annual rate ÷ 12 ÷ 100), and n is the total number of monthly "
                "instalments. This formula spreads the loan and its interest "
                "evenly across every month of the tenure."
            ),
            "example": (
                "Example: A ₹5,00,000 loan at 10% annual interest for 5 years "
                "results in a monthly EMI of roughly ₹10,624, with total interest "
                "of about ₹1,37,000 over the loan's life."
            ),
            "tip": "A shorter tenure means a higher EMI but much lower total interest paid.",
        },
        "gst": {
            "title": "GST Calculator",
            "formula": "Exclusive: GST = Price × (Rate ÷ 100)  |  Inclusive: Base = Price ÷ (1 + Rate/100)",
            "explanation": (
                "GST (Goods and Services Tax) can be added on top of a price "
                "(exclusive) or already be part of the price you were quoted "
                "(inclusive). Choosing the right mode is important to know the "
                "true tax amount."
            ),
            "example": (
                "Example: A ₹1,000 item with 18% exclusive GST costs ₹1,180 "
                "after tax. A ₹1,180 item with 18% inclusive GST has a base "
                "price of about ₹1,000 and ₹180 tax already built in."
            ),
            "tip": "Common GST slabs in India are 5%, 12%, 18%, and 28% depending on the item category.",
        },
        "percentage": {
            "title": "Percentage Calculator",
            "formula": "Value = (Total × Percentage) ÷ 100",
            "explanation": (
                "To find what a percentage of an amount is, multiply the total "
                "by the percentage and divide by 100."
            ),
            "example": "Example: 15% of ₹2,000 is (2000 × 15) ÷ 100 = ₹300.",
            "tip": "Percentages are useful for discounts, tips, interest, and growth calculations.",
        },
    },
    "te": {
        "savings": {
            "title": "పొదుపు కాలిక్యులేటర్",
            "formula": "అందుబాటులో ఉన్న పొదుపు = నెలవారీ ఆదాయం − నెలవారీ ఖర్చులు",
            "explanation": (
                "మీ ఆదాయం నుండి నెలవారీ ఖర్చులు తీసివేస్తే మిగిలేదే మీ అందుబాటులో "
                "ఉన్న పొదుపు. ఒక లక్ష్యాన్ని చేరుకోవడానికి ఎన్ని నెలలు పడుతుందో "
                "తెలుసుకోవాలంటే, లక్ష్య ధరను మీ నెలవారీ పొదుపుతో భాగించండి."
            ),
            "example": (
                "ఉదాహరణ: మీరు నెలకు ₹30,000 సంపాదించి ₹22,000 ఖర్చు చేస్తే, "
                "మీ పొదుపు ₹8,000. ₹80,000 ల్యాప్‌టాప్ కొనడానికి సుమారు 10 నెలలు "
                "పడుతుంది (80,000 ÷ 8,000 = 10)."
            ),
            "tip": "ఖర్చు చేయడానికి ముందు మీ ఆదాయంలో కనీసం 20% ప్రతి నెలా పొదుపు చేయడానికి ప్రయత్నించండి.",
        },
        "emi": {
            "title": "EMI కాలిక్యులేటర్",
            "formula": "EMI = P × [r × (1+r)^n] ÷ [(1+r)^n − 1]",
            "explanation": (
                "P అంటే రుణ మొత్తం, r అంటే నెలవారీ వడ్డీ రేటు (వార్షిక రేటు ÷ 12 ÷ 100), "
                "n అంటే మొత్తం నెలవారీ వాయిదాల సంఖ్య. ఈ సూత్రం రుణాన్ని మరియు దాని "
                "వడ్డీని కాలవ్యవధి అంతటా సమానంగా విభజిస్తుంది."
            ),
            "example": (
                "ఉదాహరణ: ₹5,00,000 రుణం 10% వార్షిక వడ్డీతో 5 సంవత్సరాలకు తీసుకుంటే, "
                "నెలవారీ EMI సుమారు ₹10,624 ఉంటుంది, మొత్తం వడ్డీ దాదాపు ₹1,37,000."
            ),
            "tip": "తక్కువ కాలవ్యవధి అంటే ఎక్కువ EMI కానీ మొత్తం వడ్డీ చాలా తక్కువగా ఉంటుంది.",
        },
        "gst": {
            "title": "GST కాలిక్యులేటర్",
            "formula": "Exclusive: GST = ధర × (రేటు ÷ 100)  |  Inclusive: మూల ధర = ధర ÷ (1 + రేటు/100)",
            "explanation": (
                "GST (వస్తు, సేవల పన్ను) ధరపై అదనంగా చేర్చవచ్చు (exclusive) లేదా "
                "మీకు చెప్పిన ధరలో ఇప్పటికే భాగంగా ఉండవచ్చు (inclusive). నిజమైన "
                "పన్ను మొత్తాన్ని తెలుసుకోవడానికి సరైన మోడ్‌ను ఎంచుకోవడం ముఖ్యం."
            ),
            "example": (
                "ఉదాహరణ: ₹1,000 వస్తువుకు 18% exclusive GST వేస్తే పన్ను తర్వాత "
                "ధర ₹1,180 అవుతుంది. ₹1,180 ధరలో 18% inclusive GST ఉంటే మూల ధర "
                "సుమారు ₹1,000 మరియు పన్ను ₹180 ఇప్పటికే కలిసి ఉంటుంది."
            ),
            "tip": "భారతదేశంలో సాధారణ GST స్లాబ్‌లు వస్తువు రకాన్ని బట్టి 5%, 12%, 18%, 28%.",
        },
        "percentage": {
            "title": "శాతం కాలిక్యులేటర్",
            "formula": "విలువ = (మొత్తం × శాతం) ÷ 100",
            "explanation": (
                "ఒక మొత్తంలో శాతం విలువను కనుగొనడానికి, మొత్తాన్ని శాతంతో గుణించి "
                "100తో భాగించండి."
            ),
            "example": "ఉదాహరణ: ₹2,000లో 15% అంటే (2000 × 15) ÷ 100 = ₹300.",
            "tip": "శాతాలు తగ్గింపులు, టిప్‌లు, వడ్డీ మరియు వృద్ధి లెక్కలకు ఉపయోగపడతాయి.",
        },
    },
}


def get_learn_content(lang="en"):
    """Return the learn content dict for the requested language (defaults to English)."""
    return LEARN_CONTENT.get(lang, LEARN_CONTENT["en"])
