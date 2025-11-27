import unittest
from gym_system import calculate_total_cost

class TestGymMembershipSystem(unittest.TestCase):

    def test_basic_plan_no_features_single_member(self):
        # Cost: 50
        cost, _ = calculate_total_cost("Basic", [], 1)
        self.assertEqual(cost, 50)

    def test_premium_plan_with_standard_feature(self):
        # Plan: 100, Feature (Group): 20. Total: 120.
        # < 200, no special discount.
        cost, _ = calculate_total_cost("Premium", ["2"], 1)
        self.assertEqual(cost, 120)

    def test_group_discount(self):
        # Plan: Basic (50) x 2 people = 100.
        # Group Discount: 10% of 100 = 10.
        # Total: 90.
        cost, _ = calculate_total_cost("Basic", [], 2)
        self.assertEqual(cost, 90)

    def test_premium_surcharge(self):
        # Plan: Basic (50).
        # Feature: Sauna (Premium, 40).
        # Subtotal: 90.
        # Surcharge (15%): 90 * 0.15 = 13.5. Total: 103.5.
        # Integer cast: 103.
        cost, _ = calculate_total_cost("Basic", ["3"], 1)
        self.assertEqual(cost, 103)

    def test_special_offer_discount_20(self):
        # Plan: Family (150) x 2 people = 300.
        # Group discount (10%): 300 - 30 = 270.
        # Special discount (>200): 270 - 20 = 250.
        cost, _ = calculate_total_cost("Family", [], 2)
        self.assertEqual(cost, 250)

    def test_special_offer_discount_50(self):
        # Plan: Family (150).
        # Features: None.
        # Members: 4.
        # Gross: 600.
        # Group Discount (10%): 60. Subtotal: 540.
        # Special Discount (>400): 50. Final: 490.
        cost, _ = calculate_total_cost("Family", [], 4)
        self.assertEqual(cost, 490)

    def test_complex_scenario(self):
        # Plan: Premium (100).
        # Feature: Nutritional Plan (Premium, 60).
        # Members: 2.
        # Gross: (100 + 60) * 2 = 320.
        # Surcharge (15% because premium feature): 320 * 0.15 = 48. Total: 368.
        # Group Discount (10%): 368 * 0.10 = 36.8. Total: 331.2.
        # Special Discount (>200): 20. Total: 311.2.
        # Int: 311.
        cost, details = calculate_total_cost("Premium", ["4"], 2)
        self.assertEqual(cost, 311)

    def test_invalid_plan(self):
        with self.assertRaises(ValueError):
            calculate_total_cost("NonExistent", [], 1)

if __name__ == '__main__':
    unittest.main()