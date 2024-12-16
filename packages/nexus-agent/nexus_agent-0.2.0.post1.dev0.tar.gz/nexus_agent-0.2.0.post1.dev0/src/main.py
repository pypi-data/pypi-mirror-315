"""Main entry point for the Nexus-Agent application.

This module initializes and launches the Nexus-Agent chat interface with all available tools
registered. It handles the setup of logging, tool registration, and the main async event loop.

Typical usage:
    python main.py

Environment Variables:
    OPENROUTER_API_KEY: API key for OpenRouter service
    LOG_LEVEL: Optional logging level (default: INFO)
"""

import asyncio
import logging
import logging.handlers
import os
import signal
import sys
from contextlib import asynccontextmanager, suppress
from typing import NoReturn

import streamlit as st
from dotenv import load_dotenv

# Try to use uvloop for better performance if available
with suppress(ImportError):
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from nexus_agent import Agent, ChatInterface
from nexus_agent.agent import ToolCategory, ToolMetadata
from nexus_agent.tools.ai.image_gen import ImageGenerator
from nexus_agent.tools.core.model_selector import ModelSelector
from nexus_agent.tools.dev.code_interpreter import CodeInterpreter
from nexus_agent.tools.dev.shell import Shell
from nexus_agent.tools.io.file_operation import FileOperations
from nexus_agent.tools.io.web_browser import WebBrowser
from nexus_agent.tools.utils.math_solver import MathSolver
from nexus_agent.tools.utils.search import Search
from nexus_agent.tools.utils.time_tools import TimeTools
from nexus_agent.tools.utils.weather import Weather

# Load environment variables
load_dotenv()

# Configure logging with environment variable support and rotation
log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
log_file = os.getenv("LOG_FILE", "nexus_agent.log")

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.handlers.RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5),  # 10MB
    ],
)
logger = logging.getLogger(__name__)


class ToolRegistry:
    """Manages tool registration and initialization."""

    def __init__(self, agent: Agent):
        """Initialize the tool registry.

        Args:
            agent: The Agent instance to register tools with
        """
        self.agent = agent
        self._tools = {}
        self._initialize_tools()

    def _initialize_tools(self) -> None:
        """Initialize tool instances with proper categorization."""
        self._tools = {
            "core": {"model_selector": ModelSelector()},
            "utility": {"weather": Weather(), "time": TimeTools(), "search": Search(), "math": MathSolver()},
            "io": {"file_ops": FileOperations(), "browser": WebBrowser()},
            "dev": {"code": CodeInterpreter(), "shell": Shell()},
            "ai": {"image_gen": ImageGenerator()},
        }

    def register_all(self) -> None:
        """Register all tools with the agent using enhanced metadata."""
        try:
            self._register_core_tools()
            self._register_utility_tools()
            self._register_io_tools()
            self._register_dev_tools()
            self._register_ai_tools()
            logger.info("Successfully registered all tools")
        except Exception as e:
            logger.error("Failed to register tools: %s", str(e))
            raise ValueError(f"Tool registration failed: {str(e)}") from e

    def _register_core_tools(self) -> None:
        """Register core system tools."""
        self.agent.register_function(
            func=self._tools["core"]["model_selector"].get_best_model,
            description="Select the best AI model for a given task",
            parameters={
                "type": "object",
                "properties": {"task": {"type": "string", "description": "The task category to select a model for"}},
                "required": ["task"],
            },
            metadata=ToolMetadata(
                name="get_best_model",
                description="Select optimal AI model for task execution",
                category=ToolCategory.CORE,
                version="1.0.0",
            ),
        )

    def _register_utility_tools(self) -> None:
        """Register utility tools."""
        # Weather tool
        self.agent.register_function(
            func=self._tools["utility"]["weather"].get_weather,
            description="Get current weather for a location",
            parameters={
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City or location name"}},
                "required": ["city"],
            },
            metadata=ToolMetadata(
                name="get_weather", description="Retrieve current weather information", category=ToolCategory.UTILITY
            ),
        )

        # Time tool
        self.agent.register_function(
            func=self._tools["utility"]["time"].get_current_time,
            description="Get the current time",
            parameters={"type": "object", "properties": {}},
            metadata=ToolMetadata(
                name="get_current_time", description="Get current system time", category=ToolCategory.UTILITY
            ),
        )

        # Search tool
        self.agent.register_function(
            func=self._tools["utility"]["search"].search_web,
            description="Search the web for information",
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "integer", "default": 5, "description": "Number of results to return"},
                },
                "required": ["query"],
            },
            metadata=ToolMetadata(
                name="search_web", description="Perform web search queries", category=ToolCategory.UTILITY
            ),
        )

        # Math tool
        self.agent.register_function(
            func=self._tools["utility"]["math"].calculate,
            description="Solve mathematical expressions",
            parameters={
                "type": "object",
                "properties": {"expression": {"type": "string", "description": "Mathematical expression to solve"}},
                "required": ["expression"],
            },
            metadata=ToolMetadata(
                name="calculate", description="Evaluate mathematical expressions", category=ToolCategory.UTILITY
            ),
        )

    def _register_io_tools(self) -> None:
        """Register I/O tools."""
        # File operations
        self.agent.register_function(
            func=self._tools["io"]["file_ops"].read_file,
            description="Read contents of a file",
            parameters={
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Path to the file"}},
                "required": ["path"],
            },
            metadata=ToolMetadata(name="read_file", description="Read file contents", category=ToolCategory.IO),
        )

        # Web browser
        self.agent.register_function(
            func=self._tools["io"]["browser"].visit_url,
            description="Navigate to a URL in the browser",
            parameters={
                "type": "object",
                "properties": {"url": {"type": "string", "description": "URL to navigate to"}},
                "required": ["url"],
            },
            metadata=ToolMetadata(
                name="visit_url", description="Control web browser navigation", category=ToolCategory.IO
            ),
        )

    def _register_dev_tools(self) -> None:
        """Register development tools."""
        # Code interpreter
        self.agent.register_function(
            func=self._tools["dev"]["code"].execute_python,
            description="Execute Python code",
            parameters={
                "type": "object",
                "properties": {"code": {"type": "string", "description": "Python code to execute"}},
                "required": ["code"],
            },
            metadata=ToolMetadata(
                name="execute_python",
                description="Run Python code interpreter",
                category=ToolCategory.DEV,
                is_streaming=True,
            ),
        )

        # Shell
        self.agent.register_function(
            func=self._tools["dev"]["shell"].execute_command,
            description="Execute shell commands",
            parameters={
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Shell command to execute"}},
                "required": ["command"],
            },
            metadata=ToolMetadata(
                name="execute_shell", description="Execute shell commands", category=ToolCategory.DEV, is_streaming=True
            ),
        )

    def _register_ai_tools(self) -> None:
        """Register AI-specific tools."""
        self.agent.register_function(
            func=self._tools["ai"]["image_gen"].generate_image,
            description="Generate an image from a text description",
            parameters={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Text description of the image"},
                    "size": {"type": "string", "default": "1024x1024", "description": "Image dimensions"},
                },
                "required": ["prompt"],
            },
            metadata=ToolMetadata(
                name="generate_image", description="AI image generation", category=ToolCategory.AI, requires_auth=True
            ),
        )


@asynccontextmanager
async def setup_signal_handlers(cleanup_cb):
    """Set up signal handlers for graceful shutdown.

    Args:
        cleanup_cb: Callback function for cleanup operations
    """
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(cleanup_cb(s)))
    try:
        yield
    finally:
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.remove_signal_handler(sig)


async def cleanup(signal=None):
    """Cleanup resources before shutdown.

    Args:
        signal: Optional signal that triggered cleanup
    """
    if signal:
        logger.info("Received exit signal %s", signal.name)

    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()

    logger.info("Cancelling %d outstanding tasks", len(tasks))
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("Cleanup completed")


def verify_environment():
    """Verify required environment variables are set.

    Raises:
        EnvironmentError: If required variables are missing
    """
    required_vars = ["OPENROUTER_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")


async def initialize_interface(agent: Agent) -> ChatInterface:
    """Initialize the chat interface with retry logic.

    Args:
        agent: The Agent instance to use

    Returns:
        ChatInterface: Initialized interface

    Raises:
        RuntimeError: If initialization fails after retries
    """
    try:
        interface = ChatInterface(agent)
        st.session_state.setdefault("interface", interface)

        if "initialized" not in st.session_state:
            st.session_state.initialized = True
            await interface.initialize()

        return interface

    except Exception as e:
        logger.error("Failed to initialize interface: %s", str(e))
        raise RuntimeError(f"Interface initialization failed: {str(e)}") from e


async def main() -> NoReturn:
    """Main entry point for the Nexus-Agent application.

    This function initializes the agent, registers tools, and launches the chat interface.
    It handles any errors that occur during startup and ensures proper cleanup.

    Raises:
        SystemExit: If a fatal error occurs during startup
    """
    try:
        # Verify environment
        verify_environment()

        # Initialize the agent
        agent = Agent()
        logger.info("Agent initialized successfully")

        # Register all tools
        registry = ToolRegistry(agent)
        registry.register_all()

        async with setup_signal_handlers(cleanup):
            # Initialize and launch the chat interface
            interface = await initialize_interface(agent)
            logger.info("Chat interface initialized successfully")

            await interface.launch()
            logger.info("Chat interface launched successfully")

    except EnvironmentError as e:
        logger.error("Environment configuration error: %s", str(e))
        st.error(f"Configuration error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error("Fatal error during startup: %s", str(e))
        st.error(f"Error starting application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        # Use uvloop if available
        if "uvloop" in sys.modules:
            uvloop.install()
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.critical("Unhandled exception: %s", str(e))
        sys.exit(1)
