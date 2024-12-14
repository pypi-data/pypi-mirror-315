"""Code interpretation and execution tools."""

import ast
import sys
from io import StringIO
from typing import Any, Dict, Optional

class CodeInterpreter:
    """A tool for interpreting and executing Python code safely."""
    
    def __init__(self):
        self.locals: Dict[str, Any] = {}
        self.globals: Dict[str, Any] = {}
    
    async def execute_python(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in a controlled environment.
        
        Args:
            code (str): Python code to execute
            
        Returns:
            Dict containing execution results and any output
        """
        # Create string buffer to capture output
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output
        
        result = None
        error = None
        
        try:
            # Parse the code to check for syntax errors
            ast.parse(code)
            
            # Execute the code
            exec(code, self.globals, self.locals)
            
            # Get any printed output
            output = redirected_output.getvalue()
            
            return {
                "success": True,
                "output": output,
                "error": None,
                "result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": redirected_output.getvalue(),
                "error": str(e),
                "result": None
            }
            
        finally:
            sys.stdout = old_stdout
    
    async def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyze Python code for structure and potential issues.
        
        Args:
            code (str): Python code to analyze
            
        Returns:
            Dict containing analysis results
        """
        try:
            tree = ast.parse(code)
            
            # Collect information about the code
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
            
            return {
                "success": True,
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "functions": [],
                "classes": [],
                "imports": [],
                "error": str(e)
            }
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the code interpreter tools."""
        return {
            "execute_python": {
                "description": "Execute Python code in a controlled environment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python code to execute"
                        }
                    },
                    "required": ["code"]
                }
            },
            "analyze_code": {
                "description": "Analyze Python code for structure and potential issues",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python code to analyze"
                        }
                    },
                    "required": ["code"]
                }
            }
        }
