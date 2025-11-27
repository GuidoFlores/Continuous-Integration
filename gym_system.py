import sys

# --- DATOS DE CONFIGURACIÓN ---
MEMBERSHIP_PLANS = {
    "Basic": 50,
    "Premium": 100,
    "Family": 150
}

# (Nombre, Costo, Es_Premium)
ADDITIONAL_FEATURES = {
    "1": {"name": "Personal Training", "cost": 30, "is_premium": False},
    "2": {"name": "Group Classes", "cost": 20, "is_premium": False},
    "3": {"name": "Sauna Access", "cost": 40, "is_premium": True},     # Feature Premium
    "4": {"name": "Nutritional Plan", "cost": 60, "is_premium": True}  # Feature Premium
}

def display_menu():
    """Muestra las opciones de membresía disponibles."""
    print("\n--- GYM MEMBERSHIP PLANS ---")
    for plan, cost in MEMBERSHIP_PLANS.items():
        print(f"- {plan}: ${cost}")

def display_features():
    """Muestra las características adicionales disponibles."""
    print("\n--- ADDITIONAL FEATURES ---")
    for key, data in ADDITIONAL_FEATURES.items():
        type_str = "[PREMIUM]" if data['is_premium'] else ""
        print(f"{key}. {data['name']} (${data['cost']}) {type_str}")

def calculate_total_cost(plan_name, selected_features_keys, num_members):
    """
    Calcula el costo total aplicando recargos y descuentos.
    Retorna: (costo_final_entero, detalles_diccionario)
    """
    
    # 1. Validación y Costo Base
    if plan_name not in MEMBERSHIP_PLANS:
        raise ValueError("Invalid membership plan.")
    
    base_cost = MEMBERSHIP_PLANS[plan_name]
    features_cost = 0
    has_premium_features = False
    
    selected_features_names = []

    # 2. Calcular costo de características
    for key in selected_features_keys:
        if key in ADDITIONAL_FEATURES:
            feat = ADDITIONAL_FEATURES[key]
            features_cost += feat["cost"]
            selected_features_names.append(feat["name"])
            if feat["is_premium"]:
                has_premium_features = True
        else:
            raise ValueError(f"Invalid feature key: {key}")

    # Subtotal por persona antes de multiplicar por miembros
    subtotal_per_person = base_cost + features_cost
    
    # Costo total bruto (por todos los miembros)
    total_gross = subtotal_per_person * num_members

    # 3. Aplicar Recargo Premium (15%)
    # Assumption: El recargo aplica al total acumulado si hay features premium
    surcharge = 0
    if has_premium_features:
        surcharge = total_gross * 0.15
    
    total_after_surcharge = total_gross + surcharge

    # 4. Aplicar Descuento Grupal (10% si son 2 o más)
    group_discount = 0
    if num_members >= 2:
        group_discount = total_after_surcharge * 0.10
    
    total_after_group = total_after_surcharge - group_discount

    # 5. Aplicar Descuento Especial (Special Offer)
    # > $400 -> -$50, > $200 -> -$20
    special_discount = 0
    if total_after_group > 400:
        special_discount = 50
    elif total_after_group > 200:
        special_discount = 20

    final_total = total_after_group - special_discount

    # Asegurar que no sea negativo (aunque es raro en este contexto)
    final_total = max(0, final_total)

    details = {
        "base_total": total_gross,
        "surcharge": surcharge,
        "group_discount": group_discount,
        "special_discount": special_discount,
        "features_names": selected_features_names
    }

    return int(final_total), details

def main():
    print("Welcome to the Gym Membership Management System")

    try:
        # --- PASO 1: Selección de Plan ---
        display_menu()
        plan_choice = input("Enter the name of the plan you want (e.g., Basic): ").strip()
        
        # Validación simple de existencia (case sensitive para simplificar)
        # Se podría mejorar con .title()
        if plan_choice not in MEMBERSHIP_PLANS:
            print("Error: Plan not available. Please restart.")
            return -1

        # --- PASO 2: Cantidad de Miembros ---
        try:
            num_members = int(input("How many members are signing up? "))
            if num_members < 1:
                print("Error: At least one member is required.")
                return -1
            if num_members >= 2:
                print(">> NOTE: Group discount of 10% will be applied!")
        except ValueError:
            print("Error: Invalid number.")
            return -1

        # --- PASO 3: Selección de Features ---
        display_features()
        print("Enter feature numbers separated by comma (e.g., 1,3) or leave empty for none.")
        features_input = input("Selection: ").strip()
        
        selected_keys = []
        if features_input:
            selected_keys = [k.strip() for k in features_input.split(',')]

        # Validar disponibilidad de features antes de calcular
        for k in selected_keys:
            if k not in ADDITIONAL_FEATURES:
                print(f"Error: Feature '{k}' is not available.")
                return -1

        # --- PASO 4: Cálculo ---
        try:
            total_cost, details = calculate_total_cost(plan_choice, selected_keys, num_members)
        except ValueError as e:
            print(f"Calculation Error: {e}")
            return -1

        # --- PASO 5: Confirmación ---
        print("\n--- CONFIRMATION ---")
        print(f"Plan: {plan_choice} (x{num_members} members)")
        print(f"Features: {', '.join(details['features_names']) if details['features_names'] else 'None'}")
        print(f"Gross Total: ${details['base_total']:.2f}")
        
        if details['surcharge'] > 0:
            print(f"Premium Surcharge (+15%): +${details['surcharge']:.2f}")
            
        if details['group_discount'] > 0:
            print(f"Group Discount (-10%): -${details['group_discount']:.2f}")
            
        if details['special_discount'] > 0:
            print(f"Special Offer Discount: -${details['special_discount']:.2f}")

        print(f"\nFINAL TOTAL COST: ${total_cost}")
        
        confirm = input("\nDo you want to confirm this membership? (yes/no): ").lower()
        
        if confirm == 'yes' or confirm == 'y':
            print(f"Membership Confirmed! Total to pay: ${total_cost}")
            return total_cost
        else:
            print("Membership Canceled.")
            return -1

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return -1

if __name__ == "__main__":
    result = main()
    # Para propósitos de demostración en terminal
    print(f"\n[System Exit Code]: {result}")