"""
SystemCalculator class orchestrates the global calculation for production chains.
"""

from typing import Dict, List, Tuple, Any, Optional
from good import Good
from recipe import Recipe
from production_building import ProductionBuilding
from modifier import Modifier


class SystemCalculator:
    """
    Orchestrates the global calculation. This is the main engine for production chain calculations.
    
    The SystemCalculator manages all goods, recipes, buildings, and modifiers,
    and provides methods to calculate production chains with or without optimization.
    """
    
    def __init__(self) -> None:
        """Initialize a new SystemCalculator with empty collections."""
        self.all_goods: Dict[str, Good] = {}
        self.all_recipes: Dict[str, Recipe] = {}
        self.all_buildings: Dict[str, ProductionBuilding] = {}
        self.all_modifiers: List[Modifier] = []
    
    def add_good(self, good: Good) -> None:
        """Add a good to the system."""
        self.all_goods[good.name] = good
    
    def add_recipe(self, name: str, recipe: Recipe) -> None:
        """Add a recipe to the system."""
        self.all_recipes[name] = recipe
    
    def add_building(self, building: ProductionBuilding) -> None:
        """Add a building to the system."""
        self.all_buildings[building.name] = building
    
    def add_modifier(self, modifier: Modifier) -> None:
        """Add a modifier to the system."""
        self.all_modifiers.append(modifier)
    
    def _find_best_modifiers_for(self, building: ProductionBuilding) -> List[Modifier]:
        """
        Find the best modifiers for a given building.
        
        This is a placeholder implementation that finds compatible modifiers
        and returns a predefined list (electricity if possible, and first productivity item found).
        The complex optimization logic will be added later.
        
        Args:
            building: The production building to find modifiers for
            
        Returns:
            List of best modifiers for the building
        """
        compatible_modifiers = []
        
        for modifier in self.all_modifiers:
            if modifier.can_apply_to(building.tags):
                compatible_modifiers.append(modifier)
        
        # Placeholder logic: prioritize specific modifiers for demonstration
        best_modifiers = []
        
        # For demonstration: prefer Master Baker for Old World buildings, electricity for others
        if "Old World" in building.tags:
            master_baker = next((m for m in compatible_modifiers if m.name == "Master Baker"), None)
            if master_baker:
                best_modifiers.append(master_baker)
        else:
            # Add electricity if building is electrifiable
            electricity_modifier = next((m for m in compatible_modifiers if m.name == "Electricity"), None)
            if building.is_electrifiable and electricity_modifier:
                best_modifiers.append(electricity_modifier)
        
        # Add automation if no other modifiers found
        if not best_modifiers:
            automation_modifier = next((m for m in compatible_modifiers if m.name == "Automation"), None)
            if automation_modifier:
                best_modifiers.append(automation_modifier)
        
        return best_modifiers
    
    def _apply_modifiers(self, building: ProductionBuilding, modifiers: List[Modifier]) -> Tuple[Recipe, float, int]:
        """
        Apply modifiers to a building and calculate the resulting recipe, productivity, and workforce.
        
        Args:
            building: The production building to apply modifiers to
            modifiers: List of modifiers to apply
            
        Returns:
            Tuple of (modified_recipe, total_productivity, modified_workforce)
        """
        # Start with base recipe, 100% productivity, and base workforce
        modified_inputs = dict(building.base_recipe.inputs)
        modified_outputs = dict(building.base_recipe.outputs)
        total_productivity = 1.0
        modified_workforce = building.get_base_workforce()
        
        for modifier in modifiers:
            # Apply productivity bonus
            productivity_bonus = modifier.get_productivity_bonus()
            total_productivity += productivity_bonus
            
            # Apply workforce reduction
            workforce_reduction = modifier.get_workforce_reduction()
            modified_workforce = int(modified_workforce * (1.0 - workforce_reduction))
            
            # Apply input replacements
            input_replacements = modifier.get_input_replacements()
            for original_good, new_good in input_replacements.items():
                if original_good in modified_inputs:
                    rate = modified_inputs.pop(original_good)
                    modified_inputs[new_good] = rate
            
            # Apply extra outputs
            extra_outputs = modifier.get_extra_outputs()
            cycles_per_minute = building.get_cycles_per_minute()
            for good, amount_per_cycle in extra_outputs.items():
                extra_rate = (amount_per_cycle * cycles_per_minute) / 60.0  # Convert to tons/minute
                modified_outputs[good] = modified_outputs.get(good, 0.0) + extra_rate
        
        # Apply productivity to both inputs and outputs (Anno 1800 mechanics)
        # In Anno 1800, productivity increases the speed at which the building operates
        # This means both inputs and outputs are increased proportionally, maintaining the same ratios
        productivity_modified_inputs = {good: rate * total_productivity for good, rate in modified_inputs.items()}
        productivity_modified_outputs = {good: rate * total_productivity for good, rate in modified_outputs.items()}
        
        modified_recipe = Recipe(productivity_modified_inputs, productivity_modified_outputs)
        return modified_recipe, total_productivity, modified_workforce
    
    def _find_building_for_good(self, good_name: str) -> Optional[ProductionBuilding]:
        """
        Find the building that produces a specific good.
        
        Args:
            good_name: Name of the good to find a producer for
            
        Returns:
            ProductionBuilding that produces the good, or None if not found
        """
        for building in self.all_buildings.values():
            if building.get_base_output_rate(good_name) > 0:
                return building
        return None
    
    def calculate_production_chain(self, target_good: str, target_rate: float, optimized: bool) -> Dict[str, Any]:
        """
        Calculate the production chain for a target good at a specific rate.
        
        This is the main recursive method that calculates either a base scenario
        (without optimizations) or an optimized scenario (with best modifiers).
        
        Args:
            target_good: Name of the good to produce
            target_rate: Target production rate in tons/minute
            optimized: Whether to use optimized calculations with modifiers
            
        Returns:
            Dictionary representing the complete production tree
        """
        # Check if good exists
        if target_good not in self.all_goods:
            return {"error": f"Good '{target_good}' not found in system"}
        
        good = self.all_goods[target_good]
        
        # If it's a raw good, no production chain needed
        if good.is_raw:
            return {
                "good_name": target_good,
                "target_rate": target_rate,
                "is_raw": True,
                "building_count": 0,
                "productivity": 1.0,
                "modifiers": [],
                "inputs": {},
                "sub_chains": {}
            }
        
        # Find building that produces this good
        building = self._find_building_for_good(target_good)
        if not building:
            return {"error": f"No building found to produce '{target_good}'"}
        
        # Calculate production parameters
        if optimized:
            # Optimized scenario: use best modifiers
            best_modifiers = self._find_best_modifiers_for(building)
            modified_recipe, productivity, modified_workforce = self._apply_modifiers(building, best_modifiers)
            recipe = modified_recipe
        else:
            # Base scenario: use base recipe with 100% productivity
            recipe = building.base_recipe
            productivity = 1.0
            modified_workforce = building.get_base_workforce()
            best_modifiers = []
        
        # Calculate required building count
        output_rate = recipe.get_output_rate(target_good)
        if output_rate <= 0:
            return {"error": f"Building '{building.name}' does not produce '{target_good}'"}
        
        # With the new logic, productivity is already applied to the recipe
        building_count = target_rate / output_rate
        
        # Calculate required input rates
        required_inputs = {}
        sub_chains = {}
        
        for input_good, input_rate in recipe.inputs.items():
            required_input_rate = input_rate * building_count
            required_inputs[input_good] = required_input_rate
            
            # Recursively calculate sub-chain for this input
            sub_chain = self.calculate_production_chain(input_good, required_input_rate, optimized)
            sub_chains[input_good] = sub_chain
        
        return {
            "good_name": target_good,
            "target_rate": target_rate,
            "building_name": building.name,
            "building_count": building_count,
            "productivity": productivity,
            "workforce_per_building": modified_workforce,
            "workforce_type": building.get_workforce_type(),
            "total_workforce": modified_workforce * building_count,
            "building_locations": building.get_locations(),
            "modifiers": [mod.name for mod in best_modifiers],
            "recipe": str(recipe),
            "inputs": required_inputs,
            "sub_chains": sub_chains
        } 