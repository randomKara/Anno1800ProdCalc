"""
Recipe class defines a transformation of goods with precise throughput rates.
"""

from typing import Dict


class Recipe:
    """
    Defines a transformation of goods with precise throughput rates in tons per minute.
    
    A Recipe represents how inputs are transformed into outputs at specific rates.
    """
    
    def __init__(self, inputs: Dict[str, float], outputs: Dict[str, float]) -> None:
        """
        Initialize a new Recipe.
        
        Args:
            inputs: Dictionary where keys are input good names and values are their consumption rate in tons/minute
            outputs: Dictionary where keys are output good names and values are their production rate in tons/minute
        """
        self.inputs: Dict[str, float] = inputs
        self.outputs: Dict[str, float] = outputs
    
    def __repr__(self) -> str:
        """Return a string representation of the Recipe."""
        inputs_str = ", ".join([f"{good}: {rate}t/min" for good, rate in self.inputs.items()])
        outputs_str = ", ".join([f"{good}: {rate}t/min" for good, rate in self.outputs.items()])
        return f"Recipe(inputs=[{inputs_str}], outputs=[{outputs_str}])"
    
    def get_input_rate(self, good_name: str) -> float:
        """
        Get the input rate for a specific good.
        
        Args:
            good_name: Name of the input good
            
        Returns:
            Input rate in tons/minute, or 0.0 if the good is not an input
        """
        return self.inputs.get(good_name, 0.0)
    
    def get_output_rate(self, good_name: str) -> float:
        """
        Get the output rate for a specific good.
        
        Args:
            good_name: Name of the output good
            
        Returns:
            Output rate in tons/minute, or 0.0 if the good is not an output
        """
        return self.outputs.get(good_name, 0.0) 