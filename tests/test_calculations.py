"""
tests/test_calculations.py
Unit tests for backend/calculations.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.calculations import (
    calculate_savings,
    calculate_emi,
    calculate_gst,
    calculate_percentage,
)


class TestSavingsCalculator(unittest.TestCase):
    def test_basic_savings_projection(self):
        result = calculate_savings(monthly_income=30000, monthly_expenses=22000, goal_price=80000)
        self.assertEqual(result["available_savings"], 8000)
        self.assertEqual(result["estimated_months"], 10.0)
        self.assertEqual(result["estimated_years"], 0)

    def test_target_comparison_sufficient(self):
        result = calculate_savings(
            monthly_income=30000, monthly_expenses=22000, goal_price=80000,
            target_value=12, target_unit="months",
        )
        self.assertIn("target", result)
        self.assertEqual(result["target"]["status"], "Sufficient")

    def test_no_surplus_returns_error(self):
        result = calculate_savings(monthly_income=20000, monthly_expenses=20000, goal_price=50000)
        self.assertIn("error", result)


class TestEmiCalculator(unittest.TestCase):
    def test_standard_emi(self):
        result = calculate_emi(principal=500000, annual_rate=10, tenure_value=5, tenure_unit="years")
        self.assertAlmostEqual(result["emi"], 10623.51, delta=1)
        self.assertEqual(result["total_months"], 60)

    def test_zero_interest_emi(self):
        result = calculate_emi(principal=120000, annual_rate=0, tenure_value=12, tenure_unit="months")
        self.assertEqual(result["emi"], 10000.0)
        self.assertEqual(result["total_interest"], 0.0)

    def test_remaining_balance(self):
        result = calculate_emi(principal=500000, annual_rate=10, tenure_value=5,
                                tenure_unit="years", emis_paid=12)
        self.assertIn("remaining_balance", result)
        self.assertLess(result["remaining_balance"], 500000)


class TestGstCalculator(unittest.TestCase):
    def test_exclusive_gst(self):
        result = calculate_gst(price=1000, gst_percent=18, mode="exclusive")
        self.assertEqual(result["gst_amount"], 180.0)
        self.assertEqual(result["final_price"], 1180.0)

    def test_inclusive_gst(self):
        result = calculate_gst(price=1180, gst_percent=18, mode="inclusive")
        self.assertAlmostEqual(result["base_price"], 1000.0, delta=0.5)


class TestPercentageCalculator(unittest.TestCase):
    def test_basic_percentage(self):
        result = calculate_percentage(total_amount=2000, percentage=15)
        self.assertEqual(result["value"], 300.0)
        self.assertEqual(result["remainder"], 1700.0)


if __name__ == "__main__":
    unittest.main()
