"""
ProductionBuilding class models a type of production building.
"""

from typing import List
from recipe import Recipe


class ProductionBuilding:
    """
    Models a type of production building.
    
    A ProductionBuilding represents a facility that can transform inputs into outputs
    according to a specific recipe, with configurable cycle times and modifier targeting.
    """
    
    def __init__(self, name: str, base_recipe: Recipe, cycle_time_seconds: int, 
                 tags: List[str], is_electrifiable: bool, workforce: int, workforce_type: str, locations: List[str]) -> None:
        """
        Initialize a new ProductionBuilding.
        
        Args:
            name: Name of the building (e.g., "Bakery")
            base_recipe: The default production recipe
            cycle_time_seconds: Production cycle time in seconds
            tags: Tags for modifier targeting (e.g., ['Production', 'Old World'])
            is_electrifiable: Whether the building can receive electricity bonus
            workforce: Number of workers required to operate the building
            workforce_type: Type of workforce required (e.g., "Workers", "Artisans", "Engineers")
            locations: List of locations where the building can be placed (e.g., ['Old World', 'New World'])
        """
        self.name: str = name
        self.base_recipe: Recipe = base_recipe
        self.cycle_time_seconds: int = cycle_time_seconds
        self.tags: List[str] = tags
        self.is_electrifiable: bool = is_electrifiable
        self.workforce: int = workforce
        self.workforce_type: str = workforce_type
        self.locations: List[str] = locations
    
    def __repr__(self) -> str:
        """Return a string representation of the ProductionBuilding."""
        return f"ProductionBuilding(name='{self.name}', cycle_time={self.cycle_time_seconds}s, workforce={self.workforce} {self.workforce_type}, locations={self.locations}, tags={self.tags})"
    
    def get_base_output_rate(self, good_name: str) -> float:
        """
        Get the base output rate for a specific good.
        
        Args:
            good_name: Name of the output good
            
        Returns:
            Base output rate in tons/minute
        """
        return self.base_recipe.get_output_rate(good_name)
    
    def get_base_input_rate(self, good_name: str) -> float:
        """
        Get the base input rate for a specific good.
        
        Args:
            good_name: Name of the input good
            
        Returns:
            Base input rate in tons/minute
        """
        return self.base_recipe.get_input_rate(good_name)
    
    def get_cycles_per_minute(self) -> float:
        """
        Calculate how many production cycles occur per minute.
        
        Returns:
            Number of cycles per minute
        """
        if self.cycle_time_seconds <= 0:
            return 0.0
        return 60.0 / self.cycle_time_seconds
    
    def get_base_workforce(self) -> int:
        """
        Get the base workforce requirement for this building.
        
        Returns:
            Number of workers required to operate the building
        """
        return self.workforce
    
    def get_locations(self) -> List[str]:
        """
        Get the locations where this building can be placed.
        
        Returns:
            List of location names where the building can be built
        """
        return self.locations
    
    def get_workforce_type(self) -> str:
        """
        Get the type of workforce required by this building.
        
        Returns:
            Type of workforce required (e.g., "Workers", "Artisans", "Engineers")
        """
        return self.workforce_type 