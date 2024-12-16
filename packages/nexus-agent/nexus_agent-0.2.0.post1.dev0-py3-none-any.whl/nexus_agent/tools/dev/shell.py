"""Shell command execution tools."""

import asyncio
import platform
import shlex
import subprocess
from typing import Any, Dict, List, Optional


class ShellError(Exception):
    """Custom exception for shell-related errors."""

    def __init__(self, message: str, error_type: str, command: Optional[str] = None):
        self.error_type = error_type
        self.command = command
        super().__init__(message)


class Shell:
    """A tool for executing shell commands safely."""

    def __init__(self):
        """Initialize the shell tool."""
        # List of allowed commands for security
        self.allowed_commands = {"ls", "dir", "pwd", "echo", "cat", "head", "tail", "grep", "find", "wc"}
        self.timeout = 10  # Default timeout in seconds

    async def execute_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a shell command safely with enhanced error handling and metadata.

        Args:
            command (str): The command to execute

        Returns:
            Dict[str, Any]: Standardized response with success status, output/error, and metadata
        """
        try:
            # Parse command and check if it's allowed
            cmd_parts = shlex.split(command)
            if not cmd_parts:
                raise ShellError("Empty command", "EMPTY_COMMAND")

            base_cmd = cmd_parts[0]
            if base_cmd not in self.allowed_commands:
                raise ShellError(f"Command '{base_cmd}' is not allowed", "UNAUTHORIZED_COMMAND", command)

            # Execute command with timeout
            process = await asyncio.create_subprocess_exec(
                *cmd_parts, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout)
            except asyncio.TimeoutError:
                if process.returncode is None:
                    process.kill()
                raise ShellError(f"Command timed out after {self.timeout} seconds", "TIMEOUT", command)

            if process.returncode != 0:
                raise ShellError(stderr.decode() or "Command failed", "EXECUTION_ERROR", command)

            return {
                "success": True,
                "data": stdout.decode() or "(No output)",
                "error": None,
                "metadata": {
                    "command": command,
                    "platform": platform.system(),
                    "return_code": process.returncode,
                    "timeout": self.timeout,
                },
            }

        except ShellError as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "metadata": {
                    "error_type": e.error_type,
                    "command": e.command,
                    "platform": platform.system(),
                    "timeout": self.timeout,
                },
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "metadata": {"error_type": type(e).__name__, "command": command, "platform": platform.system()},
            }

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
                            "description": f"The command to execute. Allowed commands: {', '.join(sorted(self.allowed_commands))}",
                        }
                    },
                    "required": ["command"],
                },
                "returns": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "description": "Whether the command executed successfully"},
                        "data": {"type": ["string", "null"], "description": "Command output if successful"},
                        "error": {"type": ["string", "null"], "description": "Error message if command failed"},
                        "metadata": {"type": "object", "description": "Additional execution metadata"},
                    },
                },
            }
        }
