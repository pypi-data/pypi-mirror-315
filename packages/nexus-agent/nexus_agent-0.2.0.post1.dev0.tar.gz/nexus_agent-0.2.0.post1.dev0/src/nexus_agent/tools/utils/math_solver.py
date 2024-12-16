"""Mathematical computation tools."""

import ast
import math
import operator
from datetime import datetime
from typing import Any, Callable, Dict, List, Type, TypeVar, Union

import numpy as np

# Type aliases for better type checking
Number = Union[int, float]
NodeType = TypeVar("NodeType", bound=ast.AST)
OperatorFunc = Callable[[Number, Number], Number]
UnaryOperatorFunc = Callable[[Number], Number]


class MathError(Exception):
    """Custom exception for mathematical errors."""

    def __init__(self, message: str, error_type: str):
        self.error_type = error_type
        super().__init__(message)


class MathSolver:
    """A tool for performing mathematical calculations and solving equations."""

    def __init__(self):
        # Define allowed mathematical operators with proper typing
        self.operators: Dict[Type[ast.operator], OperatorFunc] = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
        }

        # Define allowed unary operators
        self.unary_operators: Dict[Type[ast.unaryop], UnaryOperatorFunc] = {
            ast.USub: operator.neg,
        }

        # Define allowed mathematical functions
        self.math_globals: Dict[str, Callable] = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "sum": sum,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
        }

    def _eval_node(self, node: ast.AST) -> Number:
        """
        Safely evaluate an AST node.

        Args:
            node: The AST node to evaluate

        Returns:
            Number: Result of the evaluation

        Raises:
            MathError: If the expression contains unsupported operations
        """
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise MathError(f"Unsupported constant type: {type(node.value).__name__}", "UNSUPPORTED_TYPE")
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self.operators:
                raise MathError(f"Unsupported operator: {op_type.__name__}", "UNSUPPORTED_OPERATOR")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            try:
                return self.operators[op_type](left, right)
            except ZeroDivisionError:
                raise MathError("Division by zero", "DIVISION_BY_ZERO")
            except OverflowError:
                raise MathError("Result too large to compute", "OVERFLOW")
            except ValueError as e:
                raise MathError(str(e), "VALUE_ERROR")
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self.unary_operators:
                raise MathError(f"Unsupported unary operator: {op_type.__name__}", "UNSUPPORTED_OPERATOR")
            operand = self._eval_node(node.operand)
            return self.unary_operators[op_type](operand)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise MathError("Invalid function call", "INVALID_FUNCTION")
            if node.func.id not in self.math_globals:
                raise MathError(f"Function not allowed: {node.func.id}", "UNAUTHORIZED_FUNCTION")
            args = [self._eval_node(arg) for arg in node.args]
            try:
                return self.math_globals[node.func.id](*args)
            except Exception as e:
                raise MathError(f"Function evaluation error: {str(e)}", "FUNCTION_ERROR")
        else:
            raise MathError(f"Unsupported expression type: {type(node).__name__}", "UNSUPPORTED_EXPRESSION")

    async def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Safely evaluate a mathematical expression.

        Args:
            expression (str): The mathematical expression to evaluate

        Returns:
            Dict[str, Any]: Result with success status and metadata
        """
        try:
            # Basic input validation
            if not expression or not expression.strip():
                raise MathError("Expression cannot be empty", "EMPTY_EXPRESSION")

            # Parse the expression into an AST
            try:
                tree = ast.parse(expression, mode="eval")
            except SyntaxError:
                raise MathError("Invalid expression syntax", "SYNTAX_ERROR")

            if not isinstance(tree.body, (ast.BinOp, ast.UnaryOp, ast.Constant, ast.Call)):
                raise MathError("Invalid expression type", "INVALID_EXPRESSION")

            # Evaluate the AST
            result = self._eval_node(tree.body)

            return {
                "success": True,
                "data": {"expression": expression, "result": result, "formatted": f"{expression} = {result}"},
                "error": None,
                "metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "expression_type": type(tree.body).__name__,
                    "precision": "double",
                    "result_type": type(result).__name__,
                },
            }

        except MathError as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "metadata": {"error_type": e.error_type, "timestamp": datetime.utcnow().isoformat()},
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "metadata": {"error_type": type(e).__name__, "timestamp": datetime.utcnow().isoformat()},
            }

    async def solve_equation(self, equation: str) -> Dict[str, Any]:
        """
        Solve a simple algebraic equation.

        Args:
            equation (str): The equation to solve (e.g., "2x + 3 = 7")

        Returns:
            Dict[str, Any]: Solution with success status and metadata
        """
        try:
            # Input validation
            if not equation or "=" not in equation:
                raise MathError("Invalid equation format. Must contain '='", "INVALID_FORMAT")

            # Split and clean equation parts
            left, right = equation.split("=")
            left = left.strip()
            right = right.strip()

            if "x" not in left:
                raise MathError("Equation must contain variable 'x'", "MISSING_VARIABLE")

            # Parse coefficient and constant
            parts = left.split("x")
            coefficient: float = 1.0
            if parts[0].strip():
                try:
                    coefficient = float(ast.literal_eval(parts[0].strip()))
                except:
                    raise MathError("Invalid coefficient", "INVALID_COEFFICIENT")

            constant: float = 0.0
            if len(parts) > 1 and parts[1].strip():
                try:
                    constant = float(ast.literal_eval(parts[1].strip()))
                except:
                    raise MathError("Invalid constant term", "INVALID_CONSTANT")

            # Parse right side
            try:
                right_val = float(ast.literal_eval(right))
            except:
                raise MathError("Invalid right-hand side", "INVALID_RHS")

            # Check for division by zero
            if coefficient == 0:
                raise MathError("Cannot solve equation: coefficient of x is zero", "ZERO_COEFFICIENT")

            # Solve for x
            x = (right_val - constant) / coefficient

            return {
                "success": True,
                "data": {
                    "equation": equation,
                    "solution": x,
                    "formatted": f"x = {x}",
                    "components": {"coefficient": coefficient, "constant": constant, "rhs": right_val},
                },
                "error": None,
                "metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "equation_type": "linear",
                    "precision": "double",
                },
            }

        except MathError as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "metadata": {"error_type": e.error_type, "timestamp": datetime.utcnow().isoformat()},
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "metadata": {"error_type": type(e).__name__, "timestamp": datetime.utcnow().isoformat()},
            }

    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the math solver tools."""
        return {
            "calculate": {
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "The mathematical expression to evaluate"}
                    },
                    "required": ["expression"],
                },
                "returns": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "description": "Whether the calculation succeeded"},
                        "data": {"type": ["object", "null"], "description": "Calculation result if successful"},
                        "error": {"type": ["string", "null"], "description": "Error message if calculation failed"},
                        "metadata": {"type": "object", "description": "Additional metadata about the calculation"},
                    },
                },
            },
            "solve_equation": {
                "description": "Solve a simple algebraic equation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "equation": {"type": "string", "description": "The equation to solve (e.g., '2x + 3 = 7')"}
                    },
                    "required": ["equation"],
                },
                "returns": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "description": "Whether the equation was solved successfully"},
                        "data": {"type": ["object", "null"], "description": "Solution data if successful"},
                        "error": {"type": ["string", "null"], "description": "Error message if solving failed"},
                        "metadata": {"type": "object", "description": "Additional metadata about the solution"},
                    },
                },
            },
        }
