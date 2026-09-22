"""
backend/ai_helper.py
Powers the "Ask Questions" assistant.

Tries the Gemini API first (if GEMINI_API_KEY is set in the environment),
and falls back to a small offline keyword-matched knowledge base so the
feature still works with zero configuration / no API key / no network.
"""

import os
import re

try:
    import requests
except ImportError:  # pragma: no cover - requests should be installed, this is just a safety net
    requests = None


GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)

SYSTEM_CONTEXT = (
    "You are a friendly financial literacy assistant embedded inside a "
    "student's Financial Calculator web app. Answer questions about "
    "savings, EMI/loans, GST, and percentages simply and concisely, in "
    "2-4 sentences. If asked something unrelated to personal finance, "
    "gently redirect the user back to financial topics."
)

# ---------------------------------------------------------------------------
# Offline knowledge base fallback
# ---------------------------------------------------------------------------
_KNOWLEDGE_BASE = [
    {
        "keywords": ["emi", "loan", "installment", "instalment"],
        "answer": (
            "EMI stands for Equated Monthly Instalment. It's calculated using "
            "EMI = P × [r × (1+r)^n] ÷ [(1+r)^n − 1], where P is the loan "
            "amount, r is the monthly interest rate, and n is the number of "
            "months. A shorter tenure raises your EMI but lowers total interest."
        ),
    },
    {
        "keywords": ["gst", "tax", "goods and services"],
        "answer": (
            "GST (Goods and Services Tax) is an indirect tax added to goods "
            "and services in India, commonly at 5%, 12%, 18%, or 28%. "
            "'Exclusive' GST is added on top of the price; 'inclusive' GST "
            "means it's already baked into the quoted price."
        ),
    },
    {
        "keywords": ["saving", "savings", "goal", "budget"],
        "answer": (
            "Your available monthly savings is your income minus your "
            "expenses. To reach a savings goal, divide the goal amount by "
            "your available monthly savings to estimate how many months "
            "you'll need. Try to save at least 20% of your income."
        ),
    },
    {
        "keywords": ["percentage", "percent", "%"],
        "answer": (
            "To find a percentage of a number, multiply the number by the "
            "percentage and divide by 100. For example, 20% of ₹500 is "
            "(500 × 20) ÷ 100 = ₹100."
        ),
    },
    {
        "keywords": ["interest rate", "interest"],
        "answer": (
            "Interest is the cost of borrowing money (or the reward for "
            "saving it), usually expressed as an annual percentage. For "
            "loans, a lower interest rate means less total interest paid "
            "over the life of the loan."
        ),
    },
]

_DEFAULT_ANSWER = (
    "I can help with savings goals, EMI/loan calculations, GST, and "
    "percentages. Try asking something like 'How is EMI calculated?' or "
    "'What is GST inclusive vs exclusive?'"
)


def _offline_answer(question: str) -> str:
    q = question.lower()
    for entry in _KNOWLEDGE_BASE:
        if any(re.search(r"\b" + re.escape(kw) + r"\b", q) for kw in entry["keywords"]):
            return entry["answer"]
    return _DEFAULT_ANSWER


# ---------------------------------------------------------------------------
# Gemini API (optional)
# ---------------------------------------------------------------------------
def _gemini_answer(question: str, api_key: str):
    if requests is None:
        return None
    try:
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"{SYSTEM_CONTEXT}\n\nUser question: {question}"}]}
            ]
        }
        resp = requests.post(
            f"{GEMINI_ENDPOINT}?key={api_key}",
            json=payload,
            timeout=8,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return None
        parts = candidates[0].get("content", {}).get("parts", [])
        text = " ".join(p.get("text", "") for p in parts).strip()
        return text or None
    except Exception:
        # Any network/parse error -> fall back silently to offline mode
        return None


def get_ai_answer(question: str) -> dict:
    """
    Returns {"answer": str, "source": "gemini" | "offline"}
    """
    question = (question or "").strip()
    if not question:
        return {"answer": "Please type a question about savings, EMI, GST, or percentages.",
                "source": "offline"}

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if api_key:
        answer = _gemini_answer(question, api_key)
        if answer:
            return {"answer": answer, "source": "gemini"}

    return {"answer": _offline_answer(question), "source": "offline"}
