# Financial Calculator PRO

A polished, responsive, beginner-friendly Financial Calculator web app built
with Python Flask, HTML5, CSS3, JavaScript, and Chart.js — themed with a
dark emerald "Green Mist" glassmorphism UI.

## Features

- **💰 Savings Calculator** — projects time-to-goal, target comparison, and
  an animated savings timeline.
- **💳 EMI Calculator** — standard reducing-balance EMI math, amortization
  schedule, and remaining balance after N EMIs paid.
- **🧾 GST Calculator** — inclusive/exclusive GST math with preset chips
  (5%, 12%, 18%, 28%) or a custom rate.
- **📊 Percentage Calculator** — quick percentage-of-total calculations with
  a gauge visualization.
- **📚 Bilingual Learn section** — formulas, explanations, and worked
  examples in **English** and **Telugu**.
- **🤖 Ask Questions assistant** — chat-style Q&A backed by an offline
  knowledge base, with optional Google Gemini API integration.

## Tech stack

| Layer     | Tech                                            |
|-----------|--------------------------------------------------|
| Backend   | Python 3, Flask                                  |
| Frontend  | HTML5, CSS3 (Green Mist theme), vanilla JS       |
| Charts    | Chart.js (via CDN)                               |
| Testing   | `unittest`                                       |
| Hosting   | Vercel (Python serverless functions)             |

## Project structure

```text
Financial_Calculator_MiniProject/
├── app.py                      # Flask app & REST API routes
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel serverless routing config
├── .env.example                # Environment variable template
├── README.md
├── api/
│   └── index.py                 # Vercel serverless entrypoint
├── backend/
│   ├── __init__.py
│   ├── calculations.py          # Financial math engine
│   ├── learn_data.py            # English & Telugu Learn content
│   └── ai_helper.py             # Offline + Gemini-powered Q&A
├── templates/
│   └── index.html               # Single-page layout
├── static/
│   ├── css/style.css            # Green Mist theme & animations
│   └── js/
│       ├── script.js            # Navigation, forms, API calls
│       ├── charts.js            # Chart.js configurations
│       └── learn.js             # Learn modal + language switch
└── tests/
    └── test_calculations.py     # Unit test suite (9/9 passing)
```

## Running locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # optional: add GEMINI_API_KEY
python app.py
```

Visit `http://localhost:5000`.

## Running tests

```bash
python -m unittest tests.test_calculations -v
```

## Deploying to Vercel

1. Push this project to a GitHub repository.
2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import the
   GitHub repo.
3. Vercel will auto-detect `vercel.json` and build `api/index.py` as a
   Python serverless function that serves the whole Flask app.
4. (Optional) In **Project Settings → Environment Variables**, add
   `GEMINI_API_KEY` if you want the AI assistant to use Gemini instead of
   its offline knowledge base.
5. Deploy. Vercel gives you a live `https://your-project.vercel.app` URL.

No build step is required — Vercel installs `requirements.txt`
automatically for Python functions.

## REST API reference

| Method | Endpoint                    | Description                          |
|--------|------------------------------|---------------------------------------|
| GET    | `/`                          | Serves the single-page app            |
| POST   | `/api/calculate/savings`     | Savings projection                    |
| POST   | `/api/calculate/emi`         | EMI, amortization schedule            |
| POST   | `/api/calculate/gst`         | GST inclusive/exclusive breakdown     |
| POST   | `/api/calculate/percentage`  | Percentage-of-total calculation       |
| GET    | `/api/learn?lang=en\|te`     | Bilingual Learn section content       |
| POST   | `/api/ask-ai`                | Ask Questions assistant               |
| GET    | `/api/health`                | Health check                          |

## Notes

- The `GEMINI_API_KEY` is optional. Without it, `/api/ask-ai` automatically
  falls back to a small offline keyword-matched knowledge base, so the
  feature works out of the box with zero configuration.
- All financial formulas live in `backend/calculations.py` as pure,
  independently-testable functions with no Flask dependency.
