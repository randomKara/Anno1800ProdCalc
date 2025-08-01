"""
Main module demonstrating the Anno 1800 Production Calculator.

This module shows how to use the SystemCalculator to calculate production chains
for both base and optimized scenarios.
"""

from good import Good
from recipe import Recipe
from production_building import ProductionBuilding
from modifier import Modifier
from system_calculator import SystemCalculator
import json


def print_production_chain(chain: dict, indent: int = 0) -> None:
    """
    Print a production chain in a readable format.
    
    Args:
        chain: The production chain dictionary
        indent: Current indentation level
    """
    if "error" in chain:
        print(" " * indent + f"ERROR: {chain['error']}")
        return
    
    indent_str = " " * indent
    
    if chain.get("is_raw", False):
        print(f"{indent_str}📦 {chain['good_name']} (Raw Resource)")
        print(f"{indent_str}   Required: {chain['target_rate']:.2f} t/min")
        return
    
    print(f"{indent_str}🏭 {chain['good_name']}")
    print(f"{indent_str}   Building: {chain['building_name']}")
    print(f"{indent_str}   Locations: {', '.join(chain.get('building_locations', []))}")
    print(f"{indent_str}   Count: {chain['building_count']:.2f}")
    print(f"{indent_str}   Productivity: {chain['productivity']:.1%}")
    print(f"{indent_str}   Workforce per building: {chain.get('workforce_per_building', 0)} {chain.get('workforce_type', '')}")
    print(f"{indent_str}   Total workforce: {chain.get('total_workforce', 0):.0f} {chain.get('workforce_type', '')}")
    
    if chain['modifiers']:
        print(f"{indent_str}   Modifiers: {', '.join(chain['modifiers'])}")
    
    print(f"{indent_str}   Recipe: {chain['recipe']}")
    print(f"{indent_str}   Target Rate: {chain['target_rate']:.2f} t/min")
    
    if chain['inputs']:
        print(f"{indent_str}   Inputs:")
        for good, rate in chain['inputs'].items():
            print(f"{indent_str}     {good}: {rate:.2f} t/min")
    
    if chain['sub_chains']:
        print(f"{indent_str}   Sub-chains:")
        for input_good, sub_chain in chain['sub_chains'].items():
            print(f"{indent_str}     ↓ {input_good}:")
            print_production_chain(sub_chain, indent + 6)


def create_test_data() -> SystemCalculator:
    """
    Create test data for the production calculator.
    
    Returns:
        SystemCalculator with sample data for Bread and Chocolate production
    """
    calculator = SystemCalculator()
    
    # Create goods
    grain = Good("Grain", is_raw=True)
    flour = Good("Flour", is_raw=False)
    bread = Good("Bread", is_raw=False)
    cocoa = Good("Cocoa", is_raw=True)
    sugar = Good("Sugar", is_raw=True)
    chocolate = Good("Chocolate", is_raw=False)
    
    # Add goods to calculator
    for good in [grain, flour, bread, cocoa, sugar, chocolate]:
        calculator.add_good(good)
    
    # Create recipes
    flour_recipe = Recipe(
        inputs={"Grain": 2.0},  # 2 tons of grain per minute
        outputs={"Flour": 1.5}  # 1.5 tons of flour per minute
    )
    
    bread_recipe = Recipe(
        inputs={"Flour": 1.0},  # 1 ton of flour per minute
        outputs={"Bread": 0.8}  # 0.8 tons of bread per minute
    )
    
    chocolate_recipe = Recipe(
        inputs={"Cocoa": 1.5, "Sugar": 0.5},  # 1.5 tons cocoa + 0.5 tons sugar per minute
        outputs={"Chocolate": 1.0}  # 1 ton of chocolate per minute
    )
    
    # Create buildings
    mill = ProductionBuilding(
        name="Mill",
        base_recipe=flour_recipe,
        cycle_time_seconds=30,
        tags=["Production", "Old World"],
        is_electrifiable=True,
        workforce=10,
        workforce_type="Workers",
        locations=["Old World"]
    )
    
    bakery = ProductionBuilding(
        name="Bakery",
        base_recipe=bread_recipe,
        cycle_time_seconds=45,
        tags=["Production", "Old World"],
        is_electrifiable=True,
        workforce=15,
        workforce_type="Artisans",
        locations=["Old World"]
    )
    
    chocolate_factory = ProductionBuilding(
        name="Chocolate Factory",
        base_recipe=chocolate_recipe,
        cycle_time_seconds=60,
        tags=["Production", "New World"],
        is_electrifiable=True,
        workforce=20,
        workforce_type="Engineers",
        locations=["New World", "Old World"]  # Can be built in both worlds
    )
    
    # Add buildings to calculator
    for building in [mill, bakery, chocolate_factory]:
        calculator.add_building(building)
    
    # Create modifiers
    electricity = Modifier(
        name="Electricity",
        target_tags=["Production"],
        effects=[{"type": "PRODUCTIVITY", "value": 0.5}]  # +50% productivity
    )
    
    master_baker = Modifier(
        name="Master Baker",
        target_tags=["Old World"],
        effects=[
            {"type": "PRODUCTIVITY", "value": 0.25},  # +25% productivity
            {"type": "EXTRA_OUTPUT", "good": "Bread", "amount_per_cycle": 1},  # Extra bread every cycle
            {"type": "WORKFORCE_REDUCTION", "value": 0.3}  # -30% workforce requirement
        ]
    )
    
    automation = Modifier(
        name="Automation",
        target_tags=["Production"],
        effects=[
            {"type": "WORKFORCE_REDUCTION", "value": 0.5}  # -50% workforce requirement
        ]
    )
    
    # Add modifiers to calculator
    for modifier in [electricity, master_baker, automation]:
        calculator.add_modifier(modifier)
    
    return calculator


def main() -> None:
    """Main function demonstrating the production calculator."""
    print("🍞 Anno 1800 Production Calculator Demo")
    print("=" * 50)
    
    # Initialize calculator with test data
    calculator = create_test_data()
    
    # Define production target
    TARGET_GOOD = "Chocolate"
    TARGET_RATE = 8.0  # 8 tons per minute
    
    print(f"\n🎯 Target: Produce {TARGET_RATE} t/min of {TARGET_GOOD}")
    print("\n" + "=" * 50)
    
    # Calculate base scenario (no optimizations)
    print("📊 BASE SCENARIO (No Optimizations)")
    print("-" * 30)
    base_result = calculator.calculate_production_chain(TARGET_GOOD, TARGET_RATE, optimized=False)
    print_production_chain(base_result)
    
    print("\n" + "=" * 50)
    
    # Calculate optimized scenario (with best modifiers)
    print("⚡ OPTIMIZED SCENARIO (With Best Modifiers)")
    print("-" * 40)
    optimized_result = calculator.calculate_production_chain(TARGET_GOOD, TARGET_RATE, optimized=True)
    print_production_chain(optimized_result)
    
    print("\n" + "=" * 50)
    
    # Show comparison summary
    print("📈 COMPARISON SUMMARY")
    print("-" * 20)
    
    def count_total_buildings(chain: dict) -> float:
        """Recursively count total buildings in a production chain."""
        if "error" in chain or chain.get("is_raw", False):
            return 0.0
        
        total = chain.get("building_count", 0.0)
        for sub_chain in chain.get("sub_chains", {}).values():
            total += count_total_buildings(sub_chain)
        return total
    
    def count_total_workforce(chain: dict) -> float:
        """Recursively count total workforce in a production chain."""
        if "error" in chain or chain.get("is_raw", False):
            return 0.0
        
        total = chain.get("total_workforce", 0.0)
        for sub_chain in chain.get("sub_chains", {}).values():
            total += count_total_workforce(sub_chain)
        return total
    
    def count_workforce_by_type(chain: dict) -> dict:
        """Recursively count workforce by type in a production chain."""
        if "error" in chain or chain.get("is_raw", False):
            return {}
        
        workforce_by_type = {}
        workforce_type = chain.get("workforce_type", "")
        total_workforce = chain.get("total_workforce", 0.0)
        
        if workforce_type and total_workforce > 0:
            workforce_by_type[workforce_type] = workforce_by_type.get(workforce_type, 0.0) + total_workforce
        
        for sub_chain in chain.get("sub_chains", {}).values():
            sub_workforce = count_workforce_by_type(sub_chain)
            for wf_type, count in sub_workforce.items():
                workforce_by_type[wf_type] = workforce_by_type.get(wf_type, 0.0) + count
        
        return workforce_by_type
    
    base_buildings = count_total_buildings(base_result)
    optimized_buildings = count_total_buildings(optimized_result)
    base_workforce = count_total_workforce(base_result)
    optimized_workforce = count_total_workforce(optimized_result)
    base_workforce_by_type = count_workforce_by_type(base_result)
    optimized_workforce_by_type = count_workforce_by_type(optimized_result)
    
    print(f"Base scenario total buildings: {base_buildings:.1f}")
    print(f"Optimized scenario total buildings: {optimized_buildings:.1f}")
    print(f"Buildings saved: {base_buildings - optimized_buildings:.1f}")
    print(f"Efficiency improvement: {((base_buildings - optimized_buildings) / base_buildings * 100):.1f}%")
    print()
    print(f"Base scenario total workforce: {base_workforce:.0f}")
    print(f"Optimized scenario total workforce: {optimized_workforce:.0f}")
    print(f"Workforce saved: {base_workforce - optimized_workforce:.0f}")
    print(f"Workforce reduction: {((base_workforce - optimized_workforce) / base_workforce * 100):.1f}%")
    print()
    print("Workforce breakdown by type:")
    for wf_type in sorted(set(base_workforce_by_type.keys()) | set(optimized_workforce_by_type.keys())):
        base_count = base_workforce_by_type.get(wf_type, 0.0)
        opt_count = optimized_workforce_by_type.get(wf_type, 0.0)
        if base_count > 0 or opt_count > 0:
            saved = base_count - opt_count
            reduction = ((base_count - opt_count) / base_count * 100) if base_count > 0 else 0
            print(f"  {wf_type}: {base_count:.0f} → {opt_count:.0f} ({saved:+.0f}, {reduction:+.1f}%)")


if __name__ == "__main__":
    main()
