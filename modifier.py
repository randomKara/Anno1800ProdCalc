"""
Modifier class represents anything that can alter building operation.
"""

from typing import List, Dict, Any, Union


class Modifier:
    """
    Represents anything that can alter building operation (items, electricity, tractors, policies).
    
    A Modifier can affect productivity, replace inputs, or add extra outputs based on
    building tags and specific effects.
    """
    
    def __init__(self, name: str, target_tags: List[str], effects: List[Dict[str, Any]]) -> None:
        """
        Initialize a new Modifier.
        
        Args:
            name: Name of the modifier (e.g., "Electricity", "Feras Alsarami")
            target_tags: List of building tags this modifier can apply to
            effects: List of effect dictionaries. Each effect can be:
                - {'type': 'PRODUCTIVITY', 'value': float}: Adds productivity value
                - {'type': 'REPLACE_INPUT', 'original_good': str, 'new_good': str}: Replaces input good
                - {'type': 'EXTRA_OUTPUT', 'good': str, 'amount_per_cycle': int}: Adds extra output every X cycles
                - {'type': 'WORKFORCE_REDUCTION', 'value': float}: Reduces workforce requirement (e.g., 0.5 for -50%)
        """
        self.name: str = name
        self.target_tags: List[str] = target_tags
        self.effects: List[Dict[str, Any]] = effects
    
    def __repr__(self) -> str:
        """Return a string representation of the Modifier."""
        effects_str = ", ".join([f"{effect['type']}" for effect in self.effects])
        return f"Modifier(name='{self.name}', target_tags={self.target_tags}, effects=[{effects_str}])"
    
    def can_apply_to(self, building_tags: List[str]) -> bool:
        """
        Check if this modifier can be applied to a building with given tags.
        
        Args:
            building_tags: List of tags of the target building
            
        Returns:
            True if the modifier can be applied, False otherwise
        """
        return any(tag in building_tags for tag in self.target_tags)
    
    def get_productivity_bonus(self) -> float:
        """
        Get the total productivity bonus from all PRODUCTIVITY effects.
        
        Returns:
            Total productivity bonus as a float (e.g., 0.5 for +50%)
        """
        total_bonus = 0.0
        for effect in self.effects:
            if effect.get('type') == 'PRODUCTIVITY':
                total_bonus += effect.get('value', 0.0)
        return total_bonus
    
    def get_input_replacements(self) -> Dict[str, str]:
        """
        Get all input replacements from REPLACE_INPUT effects.
        
        Returns:
            Dictionary mapping original good names to new good names
        """
        replacements = {}
        for effect in self.effects:
            if effect.get('type') == 'REPLACE_INPUT':
                original = effect.get('original_good', '')
                new = effect.get('new_good', '')
                if original and new:
                    replacements[original] = new
        return replacements
    
    def get_extra_outputs(self) -> Dict[str, int]:
        """
        Get all extra outputs from EXTRA_OUTPUT effects.
        
        Returns:
            Dictionary mapping good names to amount per cycle
        """
        extra_outputs = {}
        for effect in self.effects:
            if effect.get('type') == 'EXTRA_OUTPUT':
                good = effect.get('good', '')
                amount = effect.get('amount_per_cycle', 0)
                if good and amount > 0:
                    extra_outputs[good] = amount
        return extra_outputs
    
    def get_workforce_reduction(self) -> float:
        """
        Get the total workforce reduction from all WORKFORCE_REDUCTION effects.
        
        Returns:
            Total workforce reduction as a float (e.g., 0.5 for -50%)
        """
        total_reduction = 0.0
        for effect in self.effects:
            if effect.get('type') == 'WORKFORCE_REDUCTION':
                total_reduction += effect.get('value', 0.0)
        return total_reduction 