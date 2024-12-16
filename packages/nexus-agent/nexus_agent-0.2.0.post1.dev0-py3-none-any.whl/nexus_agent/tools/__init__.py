"""Nexus-Agent tools package.

This package provides various tools organized by category:
- core: Core functionality tools like model selection
- io: Input/Output tools for file and web operations
- utils: Utility tools for common operations
- dev: Development tools for code and shell operations
- ai: AI-specific tools (Note: Image generation is now handled directly by agent.py)
"""

from .ai import *
from .core import *
from .dev import *
from .io import *
from .utils import *

__all__ = [
    # Core tools
    "ModelSelector",
    # IO tools
    "FileOperations",
    "WebBrowser",
    # Utility tools
    "MathSolver",
    "TimeTools",
    "Weather",
    "Search",
    # Development tools
    "CodeInterpreter",
    "Shell",
]
