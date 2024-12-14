"""Shell command execution tools."""

import subprocess
import shlex
from typing import Dict, Any, List, Optional

class Shell:
    """A tool for executing shell commands safely."""
    
    def __init__(self):
        """Initialize the shell tool."""
        # List of allowed commands for security
        self.allowed_commands = {
            'ls', 'dir', 'pwd', 'echo', 'cat',
            'head', 'tail', 'grep', 'find', 'wc'
        }
    
    async def execute_command(self, command: str) -> str:
        """
        Execute a shell command safely.
        
        Args:
            command (str): The command to execute
            
        Returns:
            str: Command output or error message
        """
        try:
            # Parse command and check if it's allowed
            cmd_parts = shlex.split(command)
            if not cmd_parts:
                return "Error: Empty command"
            
            base_cmd = cmd_parts[0]
            if base_cmd not in self.allowed_commands:
                return f"Error: Command '{base_cmd}' is not allowed"
            
            # Execute command with timeout
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=10,
                check=True
            )
            
            return result.stdout or "(No output)"
            
        except subprocess.TimeoutExpired:
            return "Error: Command timed out"
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the shell tools."""
        return {
            "execute_command": {
                "description": "Execute a shell command safely",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": f"The command to execute. Allowed commands: {', '.join(sorted(self.allowed_commands))}"
                        }
                    },
                    "required": ["command"]
                }
            }
        }
