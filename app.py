"""
app.py
Financial Calculator PRO - Flask application entrypoint & REST API routes.
"""

import os
from flask import Flask, render_template, request, jsonify

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from backend.calculations import (
    calculate_savings,
    calculate_emi,
    calculate_gst,
    calculate_percentage,
)
from backend.learn_data import get_learn_content
from backend.ai_helper import get_ai_answer


def create_app():
    app = Flask(__name__)

    # -----------------------------------------------------------------
    # Page route
    # -----------------------------------------------------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    # -----------------------------------------------------------------
    # API: Savings
    # -----------------------------------------------------------------
    @app.route("/api/calculate/savings", methods=["POST"])
    def api_savings():
        data = request.get_json(force=True, silent=True) or {}
        try:
            result = calculate_savings(
                monthly_income=data.get("monthly_income", 0),
                monthly_expenses=data.get("monthly_expenses", 0),
                goal_price=data.get("goal_price", 0),
                target_value=data.get("target_value"),
                target_unit=data.get("target_unit"),
            )
            result["goal_name"] = data.get("goal_name", "Your Goal")
            return jsonify({"success": True, "data": result})
        except (ValueError, TypeError, ZeroDivisionError) as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # -----------------------------------------------------------------
    # API: EMI
    # -----------------------------------------------------------------
    @app.route("/api/calculate/emi", methods=["POST"])
    def api_emi():
        data = request.get_json(force=True, silent=True) or {}
        try:
            result = calculate_emi(
                principal=data.get("principal", 0),
                annual_rate=data.get("annual_rate", 0),
                tenure_value=data.get("tenure_value", 0),
                tenure_unit=data.get("tenure_unit", "years"),
                emis_paid=data.get("emis_paid", 0),
            )
            return jsonify({"success": True, "data": result})
        except (ValueError, TypeError, ZeroDivisionError) as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # -----------------------------------------------------------------
    # API: GST
    # -----------------------------------------------------------------
    @app.route("/api/calculate/gst", methods=["POST"])
    def api_gst():
        data = request.get_json(force=True, silent=True) or {}
        try:
            result = calculate_gst(
                price=data.get("price", 0),
                gst_percent=data.get("gst_percent", 0),
                mode=data.get("mode", "exclusive"),
            )
            result["product_name"] = data.get("product_name", "Product")
            return jsonify({"success": True, "data": result})
        except (ValueError, TypeError, ZeroDivisionError) as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # -----------------------------------------------------------------
    # API: Percentage
    # -----------------------------------------------------------------
    @app.route("/api/calculate/percentage", methods=["POST"])
    def api_percentage():
        data = request.get_json(force=True, silent=True) or {}
        try:
            result = calculate_percentage(
                total_amount=data.get("total_amount", 0),
                percentage=data.get("percentage", 0),
            )
            return jsonify({"success": True, "data": result})
        except (ValueError, TypeError, ZeroDivisionError) as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # -----------------------------------------------------------------
    # API: Learn content
    # -----------------------------------------------------------------
    @app.route("/api/learn", methods=["GET"])
    def api_learn():
        lang = request.args.get("lang", "en")
        return jsonify({"success": True, "data": get_learn_content(lang)})

    # -----------------------------------------------------------------
    # API: Ask AI assistant
    # -----------------------------------------------------------------
    @app.route("/api/ask-ai", methods=["POST"])
    def api_ask_ai():
        data = request.get_json(force=True, silent=True) or {}
        question = data.get("question", "")
        result = get_ai_answer(question)
        return jsonify({"success": True, "data": result})

    # -----------------------------------------------------------------
    # Health check (useful for Vercel / uptime checks)
    # -----------------------------------------------------------------
    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
