"""Mathematical computation tools."""

import math
import numpy as np
from typing import Any, Dict, Union, List

class MathSolver:
    """A tool for performing mathematical calculations and solving equations."""
    
    def __init__(self):
        # Define allowed mathematical functions
        self.math_globals = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'pow': pow,
            'sum': sum,
            'math': math,
            'np': np,
        }
    
    async def calculate(self, expression: str) -> str:
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression (str): The mathematical expression to evaluate
            
        Returns:
            str: Result of the calculation or error message
        """
        try:
            # Use eval in a very restricted way for basic math
            allowed_chars = set("0123456789+-*/(). ")
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters in expression")
            result = eval(expression, {"__builtins__": {}}, self.math_globals)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"
    
    async def solve_equation(self, equation: str) -> str:
        """
        Solve a simple algebraic equation.
        
        Args:
            equation (str): The equation to solve (e.g., "2x + 3 = 7")
            
        Returns:
            str: Solution to the equation or error message
        """
        try:
            # Simple equation solver for demonstration
            # In practice, you might want to use sympy for more complex equations
            if '=' not in equation:
                raise ValueError("Invalid equation format. Must contain '='")
            
            # Very basic linear equation solver
            left, right = equation.split('=')
            left = left.strip()
            right = right.strip()
            
            # Extract coefficient and constant
            if 'x' not in left:
                raise ValueError("Equation must contain variable 'x'")
            
            parts = left.split('x')
            if len(parts[0].strip()) == 0:
                coefficient = 1
            else:
                coefficient = float(parts[0].strip())
            
            constant = float(parts[1].strip() or 0) if len(parts) > 1 else 0
            right_val = float(right)
            
            # Solve for x
            x = (right_val - constant) / coefficient
            return f"x = {x}"
            
        except Exception as e:
            return f"Error solving equation: {str(e)}"
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the math solver tools."""
        return {
            "calculate": {
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            },
            "solve_equation": {
                "description": "Solve a simple algebraic equation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "equation": {
                            "type": "string",
                            "description": "The equation to solve (e.g., '2x + 3 = 7')"
                        }
                    },
                    "required": ["equation"]
                }
            }
        }
