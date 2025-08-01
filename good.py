"""
Good class represents a commodity (raw resource or manufactured product) in the production system.
"""

from typing import Dict, Any


class Good:
    """
    Represents a commodity (raw resource or manufactured product).
    
    A Good can be either a raw resource that cannot be produced (like iron ore, clay)
    or a manufactured product that requires production chains.
    """
    
    def __init__(self, name: str, is_raw: bool) -> None:
        """
        Initialize a new Good.
        
        Args:
            name: The unique name of the good (e.g., "Grain", "Flour", "Bread")
            is_raw: True if this is a raw resource that cannot be produced, False otherwise
        """
        self.name: str = name
        self.is_raw: bool = is_raw
    
    def __repr__(self) -> str:
        """Return a string representation of the Good."""
        return f"Good(name='{self.name}', is_raw={self.is_raw})"
    
    def __hash__(self) -> int:
        """Return a hash value for the Good, allowing it to be used as dictionary key."""
        return hash(self.name)
    
    def __eq__(self, other: Any) -> bool:
        """Check if two Goods are equal based on their names."""
        if not isinstance(other, Good):
            return False
        return self.name == other.name 