"""
Gym Membership Management System.

This module handles the logic for calculating gym membership costs,
applying discounts, and interacting with the user via CLI.
"""

MEMBERSHIP_PLANS = {
    "Basic": 50,
    "Premium": 100,
    "Family": 150
}

# (Nombre, Costo, Es_Premium)
ADDITIONAL_FEATURES = {
    "1": {"name": "Personal Training", "cost": 30, "is_premium": False},
    "2": {"name": "Group Classes", "cost": 20, "is_premium": False},
    "3": {"name": "Sauna Access", "cost": 40, "is_premium": True},
    "4": {"name": "Nutritional Plan", "cost": 60, "is_premium": True}
}


def display_menu():
    """Display available membership plans."""
    print("\n--- GYM MEMBERSHIP PLANS ---")
    for plan, cost in MEMBERSHIP_PLANS.items():
        print(f"- {plan}: ${cost}")


def display_features():
    """Display available additional features."""
    print("\n--- ADDITIONAL FEATURES ---")
    for key, data in ADDITIONAL_FEATURES.items():
        type_str = "[PREMIUM]" if data['is_premium'] else ""
        print(f"{key}. {data['name']} (${data['cost']}) {type_str}")


def _get_features_details(selected_features_keys):
    """
    Calculate cost and gather names of selected features.
    Returns: (features_cost, selected_names, has_premium)
    """
    features_cost = 0
    selected_names = []
    has_premium = False

    for key in selected_features_keys:
        if key in ADDITIONAL_FEATURES:
            feat = ADDITIONAL_FEATURES[key]
            features_cost += feat["cost"]
            selected_names.append(feat["name"])
            if feat["is_premium"]:
                has_premium = True
        else:
            raise ValueError(f"Invalid feature key: {key}")
    return features_cost, selected_names, has_premium


def calculate_total_cost(plan_name, selected_features_keys, num_members):
    """
    Calculate the total cost applying surcharges and discounts.
    Returns: (final_cost_int, details_dict)
    """
    if plan_name not in MEMBERSHIP_PLANS:
        raise ValueError("Invalid membership plan.")

    base_cost = MEMBERSHIP_PLANS[plan_name]
    feat_cost, feat_names, has_premium = _get_features_details(selected_features_keys)

    # Subtotal per person
    total_gross = (base_cost + feat_cost) * num_members

    # 1. Premium Surcharge (15%)
    surcharge = total_gross * 0.15 if has_premium else 0.0
    total_after_surcharge = total_gross + surcharge

    # 2. Group Discount (10% if 2+ members)
    group_discount = total_after_surcharge * 0.10 if num_members >= 2 else 0.0
    total_after_group = total_after_surcharge - group_discount

    # 3. Special Offer Discount
    special_discount = 0.0
    if total_after_group > 400:
        special_discount = 50.0
    elif total_after_group > 200:
        special_discount = 20.0

    final_total = max(0, total_after_group - special_discount)

    details = {
        "base_total": total_gross,
        "surcharge": surcharge,
        "group_discount": group_discount,
        "special_discount": special_discount,
        "features_names": feat_names
    }

    return int(final_total), details


def get_user_input_plan():
    """Get and validate plan selection from user."""
    display_menu()
    plan = input("Enter the name of the plan you want (e.g., Basic): ").strip()
    if plan not in MEMBERSHIP_PLANS:
        print("Error: Plan not available.")
        return None
    return plan


def get_user_input_members():
    """Get and validate number of members."""
    try:
        num = int(input("How many members are signing up? "))
        if num < 1:
            print("Error: At least one member is required.")
            return None
        if num >= 2:
            print(">> NOTE: Group discount of 10% will be applied!")
        return num
    except ValueError:
        print("Error: Invalid number.")
        return None


def get_user_input_features():
    """Get and validate features selection."""
    display_features()
    print("Enter feature numbers separated by comma (e.g., 1,3) or leave empty.")
    f_input = input("Selection: ").strip()
    selected_keys = [k.strip() for k in f_input.split(',')] if f_input else []

    # Validate existence
    for key in selected_keys:
        if key not in ADDITIONAL_FEATURES:
            print(f"Error: Feature '{key}' is not available.")
            return None
    return selected_keys


def confirm_purchase(plan, num_members, cost, details):
    """Display summary and ask for confirmation."""
    print("\n--- CONFIRMATION ---")
    feat_str = ', '.join(details['features_names']) if details['features_names'] else 'None'
    print(f"Plan: {plan} (x{num_members} members)")
    print(f"Features: {feat_str}")
    print(f"Gross Total: ${details['base_total']:.2f}")

    if details['surcharge'] > 0:
        print(f"Premium Surcharge (+15%): +${details['surcharge']:.2f}")
    if details['group_discount'] > 0:
        print(f"Group Discount (-10%): -${details['group_discount']:.2f}")
    if details['special_discount'] > 0:
        print(f"Special Offer Discount: -${details['special_discount']:.2f}")

    print(f"\nFINAL TOTAL COST: ${cost}")

    confirm = input("\nDo you want to confirm this membership? (yes/no): ").lower()
    if confirm in ('yes', 'y'):
        print(f"Membership Confirmed! Total to pay: ${cost}")
        return True
    print("Membership Canceled.")
    return False


def run_gym_system():
    """
    Main execution flow of the Gym System.
    Returns total cost (int) or -1 on failure/cancel.
    """
    print("Welcome to the Gym Membership Management System")

    # Step 1: Plan
    plan_choice = get_user_input_plan()
    if not plan_choice:
        return -1

    # Step 2: Members
    num_members = get_user_input_members()
    if not num_members:
        return -1

    # Step 3: Features
    selected_keys = get_user_input_features()
    if selected_keys is None:
        return -1

    # Step 4: Calculation
    try:
        total_cost, details = calculate_total_cost(plan_choice, selected_keys, num_members)
    except ValueError as err:
        print(f"Calculation Error: {err}")
        return -1

    # Step 5: Confirmation
    if confirm_purchase(plan_choice, num_members, total_cost, details):
        return total_cost

    return -1


if __name__ == "__main__":
    FINAL_RESULT = run_gym_system()
    # Debug print as requested by logic requirements
    # print(f"System Exit Code: {FINAL_RESULT}")
