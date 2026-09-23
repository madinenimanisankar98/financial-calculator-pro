"""
backend/calculations.py
Core financial math engine for the Financial Calculator PRO app.
Pure functions only (no Flask imports) so they are easy to unit test.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Module 1: Savings Calculator
# ---------------------------------------------------------------------------
def calculate_savings(monthly_income, monthly_expenses, goal_price,
                       target_value=None, target_unit=None):
    """
    Calculate savings projection towards a goal.

    target_unit: "months" or "years" (optional)
    """
    monthly_income = float(monthly_income)
    monthly_expenses = float(monthly_expenses)
    goal_price = float(goal_price)

    available_savings = monthly_income - monthly_expenses

    result = {
        "available_savings": round(available_savings, 2),
        "goal_price": round(goal_price, 2),
        "monthly_income": round(monthly_income, 2),
        "monthly_expenses": round(monthly_expenses, 2),
    }

    if available_savings <= 0:
        result.update({
            "estimated_months": None,
            "estimated_years": None,
            "estimated_remaining_months": None,
            "estimated_total_days": None,
            "error": "Your expenses are equal to or greater than your income, "
                     "so you currently have no monthly surplus to save.",
            "timeline": [],
        })
        return result

    estimated_months = goal_price / available_savings
    est_years = int(estimated_months // 12)
    est_remaining_months = round(estimated_months - (est_years * 12), 2)
    est_total_days = round(estimated_months * 30, 1)

    result.update({
        "estimated_months": round(estimated_months, 2),
        "estimated_years": est_years,
        "estimated_remaining_months": est_remaining_months,
        "estimated_total_days": est_total_days,
    })

    # Savings accumulation timeline (for the line graph) - cap at 60 points
    months_to_plot = min(int(estimated_months) + 1, 60) or 1
    timeline = []
    for m in range(0, months_to_plot + 1):
        saved = round(min(available_savings * m, goal_price), 2)
        timeline.append({"month": m, "saved": saved})
    result["timeline"] = timeline

    # Goal progress fill (0 unless user has already saved something - here
    # we report the theoretical progress at month 1 as a starting indicator)
    result["progress_percent"] = 0

    # Target comparison
    if target_value is not None and target_unit is not None and float(target_value) > 0:
        target_value = float(target_value)
        target_months = target_value * 12 if target_unit == "years" else target_value

        required_monthly_savings = goal_price / target_months if target_months > 0 else None

        if required_monthly_savings is not None:
            if available_savings >= required_monthly_savings:
                status = "Sufficient"
            elif available_savings >= required_monthly_savings * 0.9:
                status = "Close"
            else:
                status = "Insufficient"

            result["target"] = {
                "target_months": round(target_months, 2),
                "required_monthly_savings": round(required_monthly_savings, 2),
                "status": status,
            }

    return result


# ---------------------------------------------------------------------------
# Module 2: EMI Calculator
# ---------------------------------------------------------------------------
def calculate_emi(principal, annual_rate, tenure_value, tenure_unit="years",
                   emis_paid=0):
    """
    Standard reducing-balance EMI calculation.
    tenure_unit: "years" or "months"
    """

     principal = float(principal)
    annual_rate = float(annual_rate)
    tenure_value = float(tenure_value)
    emis_paid = int(emis_paid or 0)

    total_months = int(tenure_value * 12) if tenure_unit == "years" else int(tenure_value)
    if total_months <= 0:
        raise ValueError("Loan tenure must be greater than zero.")

    monthly_rate = (annual_rate / 12) / 100

    if monthly_rate == 0:
        # 0% interest loan - simple division
        emi = principal / total_months
        total_payable = principal
        total_interest = 0.0
    else:
        r = monthly_rate
        n = total_months
        factor = (1 + r) ** n
        emi = principal * (r * factor) / (factor - 1)
        total_payable = emi * total_months
        total_interest = total_payable - principal

    result = {
        "emi": round(emi, 2),
        "total_payable": round(total_payable, 2),
        "total_interest": round(total_interest, 2),
        "principal": round(principal, 2),
        "total_months": total_months,
    }

    # Remaining balance after k EMIs paid
    if emis_paid > 0:
        k = min(emis_paid, total_months)
        if monthly_rate == 0:
            remaining_balance = max(principal - (emi * k), 0)
        else:
            r = monthly_rate
            n = total_months
            factor_n = (1 + r) ** n
            factor_k = (1 + r) ** k
            remaining_balance = principal * (factor_n - factor_k) / (factor_n - 1)
        result["emis_paid"] = k
        result["remaining_balance"] = round(max(remaining_balance, 0), 2)

    # Amortization schedule for the line graph (cap at 120 points for perf)
    schedule = []
    step = max(1, total_months // 120)
    if monthly_rate == 0:
        for m in range(0, total_months + 1, step):
            bal = max(principal - (emi * m), 0)
            schedule.append({"month": m, "balance": round(bal, 2)})
    else:
        r = monthly_rate
        n = total_months
        factor_n = (1 + r) ** n
        for m in range(0, total_months + 1, step):
            factor_m = (1 + r) ** m
            bal = principal * (factor_n - factor_m) / (factor_n - 1)
            schedule.append({"month": m, "balance": round(max(bal, 0), 2)})
    if schedule[-1]["month"] != total_months:
        schedule.append({"month": total_months, "balance": 0.0})
    result["amortization"] = schedule

    return result


# ---------------------------------------------------------------------------
# Module 3: GST Calculator
# ---------------------------------------------------------------------------
def calculate_gst(price, gst_percent, mode="exclusive"):
    """
    mode: "exclusive" -> price is before tax, add GST on top
          "inclusive" -> price already includes GST, extract the tax portion
    """
    price = float(price)
    gst_percent = float(gst_percent)

    if mode == "inclusive":
        base_price = price / (1 + (gst_percent / 100))
        gst_amount = price - base_price
        final_price = price
    else:  # exclusive
        base_price = price
        gst_amount = price * (gst_percent / 100)
        final_price = base_price + gst_amount

    return {
        "mode": mode,
        "gst_percent": gst_percent,
        "base_price": round(base_price, 2),
        "gst_amount": round(gst_amount, 2),
        "final_price": round(final_price, 2),
    }


# ---------------------------------------------------------------------------
# Module 4: Percentage Calculator
# ---------------------------------------------------------------------------
def calculate_percentage(total_amount, percentage):
    total_amount = float(total_amount)
    percentage = float(percentage)

    value = (total_amount * percentage) / 100
    remainder = total_amount - value

    return {
        "total_amount": round(total_amount, 2),
        "percentage": percentage,
        "value": round(value, 2),
        "remainder": round(remainder, 2),
    }
