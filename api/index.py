"""
api/index.py
Vercel serverless entrypoint. Vercel's Python runtime looks for a WSGI
callable named `app` in this file (per vercel.json rewrites) and calls it
for every incoming request.
"""

import os
import sys

# Make the project root importable (so "backend.*" and the root app.py resolve)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402  (Flask app instance, re-exported for Vercel)

# Vercel's Python builder detects the `app` WSGI callable automatically.
