"""
Code interpretation and execution tools using Docker for secure isolation.

This implementation provides secure environments for executing code by:
1. Using Docker containers for complete isolation
2. Supporting multiple languages (Python, JavaScript, Shell)
3. Supporting visualization libraries (matplotlib, etc.)
4. Implementing proper timeout mechanisms
5. Managing package dependencies
6. Providing rich output handling for Streamlit

The Docker-based approach is significantly safer than exec() as it provides:
- Complete process isolation
- Resource limitations
- Network isolation
- Filesystem isolation
"""

import ast
import asyncio
import base64
import contextlib
import io
import json
import os
import platform
import tempfile
import uuid
from typing import Any, Dict, Optional, Tuple

import black
import docker
import mypy.api
from docker.errors import APIError, DockerException, ImageNotFound

# Default Docker images for different languages
PYTHON_IMAGE = "python:3.9-slim"
NODE_IMAGE = "node:16-slim"


def get_docker_install_instructions() -> str:
    """Get platform-specific Docker installation instructions."""
    system = platform.system().lower()

    if system == "darwin":
        return """
Docker is not installed or running. To install Docker on macOS:

1. Visit https://www.docker.com/products/docker-desktop
2. Download and install Docker Desktop for Mac
3. Launch Docker Desktop
4. Wait for Docker to start (whale icon in menu bar should stop animating)
5. Open Terminal and run 'docker --version' to verify installation

If Docker is installed but not running:
1. Launch Docker Desktop from Applications
2. Wait for Docker to start
3. Try running your code again
"""
    elif system == "linux":
        return """
Docker is not installed or running. To install Docker on Linux:

Ubuntu/Debian:
1. sudo apt-get update
2. sudo apt-get install docker.io
3. sudo systemctl start docker
4. sudo systemctl enable docker
5. sudo usermod -aG docker $USER
6. Log out and back in for group changes to take effect

Other distributions:
Visit https://docs.docker.com/engine/install/

To start Docker if installed:
sudo systemctl start docker

To verify installation:
docker --version
"""
    elif system == "windows":
        return """
Docker is not installed or running. To install Docker on Windows:

1. Visit https://www.docker.com/products/docker-desktop
2. Download and install Docker Desktop for Windows
3. Ensure WSL 2 is installed (Windows Subsystem for Linux)
4. Launch Docker Desktop
5. Wait for Docker to start
6. Open PowerShell and run 'docker --version' to verify installation

If Docker is installed but not running:
1. Launch Docker Desktop
2. Wait for Docker to start
3. Try running your code again
"""
    else:
        return "Please visit https://docs.docker.com/get-docker/ for Docker installation instructions."


class DockerError(Exception):
    """Custom exception for Docker-related errors with helpful messages."""

    def __init__(self, message: str, error_type: str, resolution: str):
        self.error_type = error_type
        self.resolution = resolution
        super().__init__(message)


class CodeInterpreter:
    """
    A secure code interpreter that uses Docker for isolation.

    This class provides secure environments for executing code by:
    - Running code in isolated Docker containers
    - Supporting multiple languages
    - Supporting visualization libraries
    - Implementing timeouts
    - Managing dependencies
    """

    def __init__(self):
        """Initialize the Docker-based code interpreter."""
        self.timeout = 30  # Default timeout in seconds
        self._init_docker()

    def _init_docker(self) -> None:
        """Initialize Docker client with enhanced error handling."""
        try:
            self.client = docker.from_env()
            # Test Docker connection
            self.client.ping()

            # Ensure required images are available
            self._ensure_images()

        except DockerException as e:
            if "Connection refused" in str(e):
                raise DockerError(
                    "Docker daemon is not running",
                    "DOCKER_NOT_RUNNING",
                    "Please start Docker and try again.\n" + get_docker_install_instructions(),
                ) from e
            elif "Permission denied" in str(e):
                raise DockerError(
                    "Insufficient permissions to access Docker",
                    "PERMISSION_DENIED",
                    "Please ensure your user has permissions to access Docker.\n"
                    "Try running: sudo usermod -aG docker $USER",
                ) from e
            else:
                raise DockerError(
                    "Docker is not available", "DOCKER_UNAVAILABLE", get_docker_install_instructions()
                ) from e

    def _ensure_images(self) -> None:
        """Ensure required Docker images are available."""
        try:
            for image in [PYTHON_IMAGE, NODE_IMAGE, "alpine:latest"]:
                try:
                    self.client.images.get(image)
                except ImageNotFound:
                    print(f"Pulling {image}...")
                    self.client.images.pull(image)
        except APIError as e:
            if "network timeout" in str(e).lower():
                raise DockerError(
                    "Network timeout while pulling Docker images",
                    "NETWORK_TIMEOUT",
                    "Please check your internet connection and try again.",
                ) from e
            raise DockerError(
                f"Failed to pull Docker images: {str(e)}",
                "PULL_ERROR",
                "Please ensure you have internet access and Docker has sufficient permissions.",
            ) from e

    async def execute_python(self, code: str, packages: Optional[list] = None) -> Dict[str, Any]:
        """Execute Python code in a Docker container."""
        container_name = f"python_interpreter_{uuid.uuid4().hex}"

        script = f"""
import sys
import io
import contextlib
import json
import traceback
from typing import Dict, Any

# Redirect stdout/stderr
output = io.StringIO()
error = io.StringIO()

# Setup matplotlib for non-interactive backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def execute_code():
    result = None
    plots = []

    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            exec({repr(code)}, globals(), locals())

            # Capture any matplotlib plots
            if plt.get_fignums():
                for fig in plt.get_fignums():
                    plt_data = io.BytesIO()
                    plt.figure(fig).savefig(plt_data, format='png')
                    plt_data.seek(0)
                    plots.append(base64.b64encode(plt_data.read()).decode())
                plt.close('all')

        return {{
            "success": True,
            "output": output.getvalue(),
            "error": error.getvalue(),
            "plots": plots,
            "result": result
        }}

    except Exception as e:
        return {{
            "success": False,
            "output": output.getvalue(),
            "error": f"{{str(e)}}\\n{{traceback.format_exc()}}",
            "plots": plots,
            "result": None
        }}

result = execute_code()
print(json.dumps(result))
"""

        return await self._run_in_container(container_name, PYTHON_IMAGE, script, "python", packages)

    async def execute_javascript(self, code: str) -> Dict[str, Any]:
        """Execute JavaScript code in a Docker container."""
        container_name = f"node_interpreter_{uuid.uuid4().hex}"

        script = f"""
const util = require('util');

try {{
    const result = eval({json.dumps(code)});
    console.log(JSON.stringify({{
        success: true,
        output: util.format(result),
        error: null
    }}));
}} catch (error) {{
    console.log(JSON.stringify({{
        success: false,
        output: '',
        error: error.toString()
    }}));
}}
"""

        return await self._run_in_container(container_name, NODE_IMAGE, script, "node")

    async def execute_shell(self, code: str) -> Dict[str, Any]:
        """Execute shell commands in a Docker container."""
        # For security, we'll use a minimal Alpine Linux container
        container_name = f"shell_interpreter_{uuid.uuid4().hex}"

        script = f"""
set -e
{code}
"""

        return await self._run_in_container(container_name, "alpine:latest", script, "sh")

    async def _run_in_container(
        self, container_name: str, image: str, script: str, interpreter: str, packages: Optional[list] = None
    ) -> Dict[str, Any]:
        """Run code in a Docker container with proper isolation."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                script_path = os.path.join(temp_dir, "script")
                with open(script_path, "w") as f:
                    f.write(script)

                volumes = {temp_dir: {"bind": "/workspace", "mode": "ro"}}

                # Create and start the container
                container = self.client.containers.run(
                    image,
                    name=container_name,
                    command=f"{interpreter} /workspace/script",
                    volumes=volumes,
                    working_dir="/workspace",
                    detach=True,
                    remove=True,
                    mem_limit="512m",
                    network_disabled=True,
                )

                try:
                    # Wait for execution with timeout
                    await asyncio.get_event_loop().run_in_executor(None, lambda: container.wait(timeout=self.timeout))

                    # Get the output
                    output = container.logs().decode()

                    try:
                        result = json.loads(output)
                        result["metadata"] = {
                            "container_name": container_name,
                            "image": image,
                            "interpreter": interpreter,
                            "timeout": self.timeout,
                        }
                        return result
                    except json.JSONDecodeError:
                        return {
                            "success": False,
                            "output": output,
                            "error": "Failed to parse execution result",
                            "metadata": {
                                "error_type": "JSON_DECODE_ERROR",
                                "container_name": container_name,
                                "image": image,
                            },
                        }

                except asyncio.TimeoutError:
                    return {
                        "success": False,
                        "output": "",
                        "error": f"Execution timed out after {self.timeout} seconds",
                        "metadata": {
                            "error_type": "TIMEOUT",
                            "container_name": container_name,
                            "image": image,
                            "timeout": self.timeout,
                        },
                    }

        except DockerError as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "metadata": {"error_type": e.error_type, "resolution": e.resolution},
            }
        except Exception as e:
            return {"success": False, "output": "", "error": str(e), "metadata": {"error_type": type(e).__name__}}

        finally:
            # Ensure the container is removed
            with contextlib.suppress(Exception):
                container = self.client.containers.get(container_name)
                container.remove(force=True)

    async def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze Python code for structure and potential issues."""
        try:
            tree = ast.parse(code)

            # Collect information about the code
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]

            # Calculate cyclomatic complexity
            complexity = self._calculate_complexity(tree)

            return {
                "success": True,
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "complexity": complexity,
                "error": None,
                "metadata": {"analysis_type": "static", "metrics": ["functions", "classes", "imports", "complexity"]},
            }

        except Exception as e:
            return {
                "success": False,
                "functions": [],
                "classes": [],
                "imports": [],
                "complexity": 0,
                "error": str(e),
                "metadata": {"error_type": type(e).__name__},
            }

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity of the code."""
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity

    def format_code(self, code: str) -> Dict[str, Any]:
        """Format Python code using black."""
        try:
            formatted_code = black.format_str(code, mode=black.FileMode())
            return {
                "success": True,
                "code": formatted_code,
                "error": None,
                "metadata": {"formatter": "black", "line_length": 88},
            }
        except Exception as e:
            return {"success": False, "code": code, "error": str(e), "metadata": {"error_type": type(e).__name__}}

    def check_types(self, code: str) -> Dict[str, Any]:
        """Check types using mypy."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as temp:
            temp.write(code)
            temp.flush()

            stdout, stderr, exit_code = mypy.api.run([temp.name])

            return {
                "success": exit_code == 0,
                "errors": stdout.split("\n") if stdout else [],
                "output": stderr or "",
                "metadata": {"checker": "mypy", "exit_code": exit_code, "has_errors": bool(stdout)},
            }

    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the code interpreter tools."""
        return {
            "execute_python": {
                "description": "Execute Python code in a secure Docker environment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Python code to execute"},
                        "packages": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Additional Python packages to install",
                        },
                    },
                    "required": ["code"],
                },
            },
            "execute_javascript": {
                "description": "Execute JavaScript code in a secure Docker environment",
                "parameters": {
                    "type": "object",
                    "properties": {"code": {"type": "string", "description": "JavaScript code to execute"}},
                    "required": ["code"],
                },
            },
            "execute_shell": {
                "description": "Execute shell commands in a secure Docker environment",
                "parameters": {
                    "type": "object",
                    "properties": {"code": {"type": "string", "description": "Shell commands to execute"}},
                    "required": ["code"],
                },
            },
            "analyze_code": {
                "description": "Analyze code structure and complexity",
                "parameters": {
                    "type": "object",
                    "properties": {"code": {"type": "string", "description": "Code to analyze"}},
                    "required": ["code"],
                },
            },
        }
