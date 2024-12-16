"""Agent implementation for the Bot.

This module implements the core agent functionality for interacting with the OpenRouter API.
It provides a flexible interface for:
- Chat completions with streaming support
- Function/tool calling capabilities 
- Multimodal message handling (text + images)
- Automatic model selection based on tasks
- Resource management and error handling
"""

# TODO: Done for 0.2.0

import asyncio
import json
import os
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional, Protocol, Union

import aiohttp
import tiktoken
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from .tools.core.model_selector import ModelSelector

MessageRole = Literal["system", "user", "assistant", "tool"]


class AsyncCallable(Protocol):
    """Protocol for async callable objects."""

    __name__: str

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Async callable interface."""


class ToolCategory(str, Enum):
    """Categories for organizing tools."""

    CORE = "core"
    UTILITY = "utility"
    IO = "io"
    DEV = "development"
    AI = "ai"


class ToolMetadata(BaseModel):
    """Metadata for tool registration.

    Attributes:
        name: Tool name for identification
        description: Detailed description of tool functionality
        category: Tool category for organization
        version: Tool version number
        author: Tool author/maintainer
        requires_auth: Whether tool needs authentication
        is_streaming: Whether tool supports streaming responses
    """

    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    category: ToolCategory = Field(..., description="Tool category")
    version: str = Field(default="1.0.0", description="Tool version")
    author: str = Field(default="Nexus-Agent", description="Tool author")
    requires_auth: bool = Field(default=False, description="Whether tool requires authentication")
    is_streaming: bool = Field(default=False, description="Whether tool supports streaming")


class Function(BaseModel):
    """Enhanced function specification with metadata.

    Attributes:
        name: Function name
        description: Function description
        parameters: JSON schema defining function parameters
        metadata: Additional function metadata
    """

    name: str = Field(..., description="Function name")
    description: str = Field(..., description="Function description")
    parameters: Dict[str, Any] = Field(..., description="Function parameters schema")
    metadata: Dict[str, Any] = Field(..., description="Function metadata")


class ToolResponse(BaseModel):
    """Standardized response format for tools.

    Attributes:
        success: Whether the tool execution succeeded
        data: Tool execution result data if successful
        error: Error message if execution failed
        metadata: Additional response metadata
    """

    success: bool = Field(..., description="Whether the tool execution succeeded")
    data: Optional[Any] = Field(default=None, description="Tool execution result data")
    error: Optional[str] = Field(default=None, description="Error message if execution failed")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class AgentConfig(BaseModel):
    """Configuration for the agent.

    Attributes:
        selection_mode: How to select models ('optimal' or 'manual')
        model: Manual model selection if selection_mode is 'manual'
        temperature: Model temperature parameter (0.0-2.0)
        max_tokens: Maximum tokens to generate
        stream: Whether to stream responses
        default_task: Default task category for optimal selection
        x_title: For OpenRouter leaderboard display
        context_length: For models with different context windows
        retry_attempts: Number of retry attempts for API calls
        log_level: Logging level
        response_format: Optional response format specification
        stop: Optional stop sequences
        prediction: Optional predicted output for latency optimization
    """

    selection_mode: Literal["optimal", "manual"] = Field(default="manual", description="How to select models")
    model: Optional[str] = Field(default=None, description="Manual model selection, if selection_mode is 'manual'")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Model temperature parameter")
    max_tokens: int = Field(default=1000, gt=0, description="Maximum tokens to generate")
    stream: bool = Field(default=True, description="Whether to stream responses")
    default_task: str = Field(default="general", description="Default task category when using optimal selection")
    x_title: Optional[str] = Field(default=None, description="For OpenRouter leaderboard display")
    context_length: Optional[int] = Field(default=None, description="For models with different context windows")
    retry_attempts: int = Field(default=3, ge=1, description="Number of retry attempts for API calls")
    log_level: str = Field(default="INFO", description="Logging level")
    response_format: Optional[Dict[str, str]] = Field(
        default=None, description="Optional response format specification"
    )
    stop: Optional[Union[str, List[str]]] = Field(default=None, description="Optional stop sequences")
    prediction: Optional[Dict[str, str]] = Field(
        default=None, description="Optional predicted output for latency optimization"
    )


class OpenRouterClient:
    """Client for making requests to the OpenRouter API.

    Handles authentication, request formatting, and response processing
    for interactions with the OpenRouter API endpoints.
    """

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str, default_headers: Dict[str, str]):
        """Initialize the OpenRouter client.

        Args:
            api_key: OpenRouter API key
            default_headers: Default headers to include in requests

        Raises:
            ValueError: If API key is not provided
        """
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.default_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            **default_headers,
        }
        self.session = None

    async def __aenter__(self):
        """Create aiohttp session on context enter."""
        self.session = aiohttp.ClientSession(headers=self.default_headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close aiohttp session on context exit."""
        if self.session:
            await self.session.close()

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Make a request to the OpenRouter API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request arguments

        Returns:
            API response data

        Raises:
            OpenRouterError: If the API request fails
            RuntimeError: If client session is not initialized
        """
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with context.")

        url = f"{self.BASE_URL}/{endpoint}"
        async with self.session.request(method, url, **kwargs) as response:
            if response.status >= 400:
                error_data = await response.json()
                raise OpenRouterError(error_data.get("error", {}).get("message", str(error_data)))

            return response if kwargs.get("stream", False) else await response.json()

    async def chat_completion(self, payload: Dict[str, Any], stream: bool = False) -> Any:
        """Send a chat completion request.

        Args:
            payload: Request payload
            stream: Whether to stream the response

        Returns:
            Chat completion response
        """
        return await self._make_request("POST", "chat/completions", json=payload, stream=stream)

    async def list_models(self) -> Dict[str, Any]:
        """Get available models.

        Returns:
            Dictionary containing available model information
        """
        return await self._make_request("GET", "models")


class OpenRouterError(Exception):
    """Custom exception for OpenRouter API errors."""


class Agent:
    """Core agent implementation with enhanced error handling and resource management.

    Provides high-level interface for:
    - Chat completions with streaming
    - Function/tool calling
    - Model selection and management
    - Resource cleanup and error handling
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the agent with configuration.

        Args:
            config: Optional agent configuration

        Raises:
            ValueError: If OPENROUTER_API_KEY environment variable is missing
        """
        load_dotenv()
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")

        self.api_key = api_key  # Now we know this is a str, not Optional[str]
        self.config = config or AgentConfig()
        self.available_functions: Dict[str, Dict[str, Any]] = {}
        self.function_specs: List[Function] = []
        self._message_history: List[Dict[str, MessageRole | str]] = []

        # Initialize model selector for optimal selection mode
        self.model_selector = ModelSelector(api_key=self.api_key)  # Now passing a str

        # Configure default headers for OpenRouter
        self.default_headers = {
            "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "https://github.com/yourusername/Nexus-Agent"),
            "X-Title": self.config.x_title or "Nexus-Agent",
            "X-Organization-ID": os.getenv("OPENROUTER_ORG_ID", ""),  # Optional organization tracking
        }

    def register_function(
        self,
        func: AsyncCallable,
        description: str,
        parameters: Dict[str, Any],
        metadata: ToolMetadata,
        task: Optional[str] = None,
    ) -> None:
        """Register a new function that can be called by the agent.

        Args:
            func: The function to register
            description: Description of what the function does
            parameters: JSON schema of function parameters
            metadata: Tool metadata including category and other information
            task: Optional task category this function is associated with

        Raises:
            ValueError: If function parameters are invalid
        """
        if not isinstance(func, Callable):
            raise ValueError("func must be callable")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("description must be a non-empty string")
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a dictionary")
        if not isinstance(metadata, ToolMetadata):
            raise ValueError("metadata must be a ToolMetadata instance")

        # Get function name safely
        func_name = getattr(func, "__name__", "unnamed_function")

        # Convert ToolMetadata to dictionary using new method
        metadata_dict = metadata.model_dump()

        function_spec = Function(name=func_name, description=description, parameters=parameters, metadata=metadata_dict)

        self.function_specs.append(function_spec)
        self.available_functions[func_name] = {
            "func": func,
            "task": task or self.config.default_task,
            "metadata": metadata_dict,
        }

    async def _get_model_for_task(self, task: str) -> str:
        """Get the model based on selection mode and configuration.

        Args:
            task: Task category for model selection

        Returns:
            Selected model identifier

        Raises:
            ValueError: If model is not specified in manual mode
        """
        if self.config.selection_mode == "manual":
            if not self.config.model:
                raise ValueError("Model must be specified when using manual selection mode")
            return self.config.model

        # Optimal selection mode
        result = await self.model_selector.get_best_model(task)
        if result["success"] and result["model"]:
            return result["model"]["model_id"]

        # Updated fallback models based on OpenRouter's offerings
        fallback_models = {
            "general": ["anthropic/claude-2", "openai/gpt-3.5-turbo"],
            "coding": ["anthropic/claude-2-100k", "google/palm-2-codechat-bison"],
            "research": ["anthropic/claude-2", "google/palm-2"],
            "creative": ["anthropic/claude-2", "openai/gpt-4"],
            "analysis": ["anthropic/claude-2", "openai/gpt-4"],
        }

        task_models = fallback_models.get(task, fallback_models["general"])
        available_models = await self.get_available_models()
        available_ids = [m["id"] for m in available_models]

        return next(
            (model for model in task_models if model in available_ids),
            "anthropic/claude-2",
        )

    async def _validate_context_length(self, messages: List[Dict[str, MessageRole | str]]) -> bool:
        """Validate if the messages fit within the model's context window using tiktoken.

        Args:
            messages: List of chat messages

        Returns:
            bool: True if messages fit, False otherwise
        """
        if not self.config.context_length:
            return True

        try:
            # Use cl100k_base encoding which is used by most recent models
            encoding = tiktoken.get_encoding("cl100k_base")
            total_tokens = 0

            for message in messages:
                # Count tokens in the message content
                content = str(message.get("content", ""))
                total_tokens += len(encoding.encode(content))

                # Add tokens for message format (role, etc.)
                total_tokens += 4  # Add tokens for message format overhead

            # Add tokens for base conversation format
            total_tokens += 2  # Add tokens for conversation format

            return total_tokens <= self.config.context_length

        except Exception:
            # Fallback to a conservative estimate if tiktoken fails
            approx_tokens = sum(len(str(msg.get("content", "")).split()) * 1.3 for msg in messages)
            return approx_tokens <= self.config.context_length

    async def _execute_function(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a registered function with standardized error handling and response format.

        Args:
            name: Name of the function to execute
            arguments: Arguments to pass to the function

        Returns:
            Standardized tool response including success status and result/error
        """
        if not (function_info := self.available_functions.get(name)):
            return {
                "tool_result": ToolResponse(
                    success=False, error=f"Function {name} not found", metadata={"error_type": "NOT_FOUND"}
                ).model_dump()
            }

        try:
            result = await function_info["func"](**arguments)
            metadata = function_info["metadata"]

            return {
                "tool_result": ToolResponse(
                    success=True,
                    data=result,
                    metadata={
                        "category": metadata["category"],
                        "version": metadata["version"],
                        "is_streaming": metadata["is_streaming"],
                    },
                ).model_dump()
            }

        except Exception as e:
            return {
                "tool_result": ToolResponse(
                    success=False,
                    error=str(e),
                    metadata={"error_type": type(e).__name__, "category": function_info["metadata"]["category"]},
                ).model_dump()
            }

    def set_model(self, model: str) -> None:
        """Manually set the model to use. This automatically switches to manual selection mode.

        Args:
            model: The model identifier to use
        """
        self.config.selection_mode = "manual"
        self.config.model = model

    def use_optimal_selection(self) -> None:
        """Switch to optimal (automatic) model selection mode."""
        self.config.selection_mode = "optimal"
        self.config.model = None

    def _manage_message_history(self, messages: List[Dict[str, MessageRole | str]]) -> None:
        """Manage message history to prevent memory leaks.

        Args:
            messages: New messages to add to history
        """
        # Keep only the last 100 messages
        max_history = 100
        self._message_history.extend(messages)
        if len(self._message_history) > max_history:
            self._message_history = self._message_history[-max_history:]

    async def _process_stream_response(self, response: aiohttp.ClientResponse) -> Any:
        """Process streaming response from OpenRouter.

        Args:
            response: Streaming response from OpenRouter API

        Yields:
            Parsed response chunks
        """
        async for line in response.content:
            if line:
                line = line.decode("utf-8").strip()
                if line.startswith("data: "):
                    line = line[6:]  # Remove 'data: ' prefix
                    if line == "[DONE]":
                        break
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue

    async def chat(
        self, messages: List[Dict[str, MessageRole | str]], task: Optional[str] = None, stream: bool = True
    ) -> Union[Any, Dict[str, Any]]:
        """Send a chat request to the model with function calling capabilities.

        Args:
            messages: List of chat messages
            task: Optional task category (used only in optimal selection mode)
            stream: Whether to stream the response

        Returns:
            Either a streaming response, function execution result, or text response

        Raises:
            ValueError: For various validation errors
            RuntimeError: For other errors during chat completion
        """
        try:
            # Manage message history
            self._manage_message_history(messages)

            # Determine which model to use based on selection mode
            model = await self._get_model_for_task(task or self.config.default_task)

            # Get model information for context length validation
            models = await self.get_available_models()
            model_info = next((m for m in models if m["id"] == model), None)

            if model_info and not await self._validate_context_length(messages):
                raise ValueError("Input exceeds model's context length limit")

            # Prepare the request payload
            payload = {
                "model": model,
                "messages": messages,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "stream": stream,
            }

            # Add optional parameters from config
            if self.config.response_format:
                payload["response_format"] = self.config.response_format
            if self.config.stop:
                payload["stop"] = self.config.stop
            if self.config.prediction:
                payload["prediction"] = self.config.prediction

            # Add functions if available
            if self.function_specs:
                payload["tools"] = [
                    {
                        "type": "function",
                        "function": {
                            "name": spec.name,
                            "description": spec.description,
                            "parameters": spec.parameters,
                        },
                    }
                    for spec in self.function_specs
                ]

            # Make the API request using the OpenRouter client
            async with OpenRouterClient(self.api_key, self.default_headers) as client:
                response = await client.chat_completion(payload, stream=stream)

                if stream:
                    return self._process_stream_response(response)

                # Handle function calls in the response
                if "choices" in response and response["choices"]:
                    choice = response["choices"][0]
                    message = choice.get("message", {})

                    # Handle tool calls (new format)
                    if tool_calls := message.get("tool_calls"):
                        for tool_call in tool_calls:
                            if tool_call["type"] == "function":
                                try:
                                    arguments = json.loads(tool_call["function"]["arguments"])
                                    return await self._execute_function(tool_call["function"]["name"], arguments)
                                except json.JSONDecodeError:
                                    return {
                                        "tool_result": ToolResponse(
                                            success=False,
                                            error="Invalid function arguments format",
                                            metadata={"error_type": "JSON_DECODE_ERROR"},
                                        ).model_dump()
                                    }

                    # Handle legacy function calls
                    elif function_call := message.get("function_call"):
                        try:
                            arguments = json.loads(function_call["arguments"])
                            return await self._execute_function(function_call["name"], arguments)
                        except json.JSONDecodeError:
                            return {
                                "tool_result": ToolResponse(
                                    success=False,
                                    error="Invalid function arguments format",
                                    metadata={"error_type": "JSON_DECODE_ERROR"},
                                ).model_dump()
                            }

                    return message.get("content")

                return response

        except OpenRouterError as e:
            if "rate limit" in str(e).lower():
                raise ValueError("OpenRouter rate limit exceeded. Please wait a moment before trying again.") from e
            elif "insufficient_quota" in str(e):
                raise ValueError("OpenRouter quota exceeded. Please check your usage limits.") from e
            elif "invalid_request" in str(e):
                raise ValueError("Invalid request to OpenRouter API. Please check your inputs.") from e
            else:
                raise ValueError(f"OpenRouter API error: {str(e)}") from e
        except asyncio.TimeoutError as e:
            raise ValueError("OpenRouter request timed out. Please try again.") from e
        except Exception as e:
            if "context length" in str(e).lower():
                raise ValueError("Input exceeds model's context length limit") from e
            elif "api key" in str(e).lower():
                raise ValueError("Invalid OpenRouter API key. Please check your configuration.") from e
            else:
                raise RuntimeError(f"Error in chat completion: {str(e)}") from e

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Fetch available models and their capabilities from OpenRouter.

        Returns:
            List of dictionaries containing model information including:
            - id: Model identifier
            - name: Display name
            - context_length: Maximum context length
            - pricing: Input/output token pricing
            - best_for: List of tasks this model excels at (if in optimal mode)
            - score: Model's score for its best tasks (if in optimal mode)

        Raises:
            RuntimeError: If fetching models fails
        """
        try:
            async with OpenRouterClient(self.api_key, self.default_headers) as client:
                response = await client.list_models()

                all_models = []
                for model in response.get("data", []):
                    model_info = {
                        "id": model["id"],
                        "name": model.get("name", model["id"]),
                        "context_length": model.get("context_length"),
                        "pricing": {
                            "input": model.get("pricing", {}).get("prompt"),
                            "output": model.get("pricing", {}).get("completion"),
                        },
                    }
                    all_models.append(model_info)

                # If in optimal mode, also get task-specific rankings
                if self.config.selection_mode == "optimal":
                    tasks = await self.model_selector.list_supported_tasks()
                    for task in tasks:
                        result = await self.model_selector.get_best_model(task)
                        if result["success"] and result["model"]:
                            # Mark the best model for each task
                            for model in all_models:
                                if model["id"] == result["model"]["model_id"]:
                                    model.setdefault("best_for", []).append(task)
                                    model["score"] = result["model"]["score"]

                return all_models

        except Exception as e:
            raise RuntimeError(f"Error fetching OpenRouter models: {str(e)}") from e

    async def get_current_model(self) -> Dict[str, Any]:
        """Get information about the currently selected model.

        Returns:
            Dict containing current model information including:
            - mode: "manual" or "optimal"
            - model: Current model ID if in manual mode
            - default_task: Default task category if in optimal mode
            - current_model: Current model ID if in optimal mode
            - context_length: Maximum context length of current model
            - pricing: Current model's pricing information
        """
        current_info: Dict[str, Any] = {
            "mode": self.config.selection_mode,
        }

        if self.config.selection_mode == "manual":
            if self.config.model:
                current_info["model"] = self.config.model
        else:
            current_info |= {
                "default_task": self.config.default_task,
                "current_model": await self._get_model_for_task(self.config.default_task),
            }

        # Add model capabilities if available
        models = await self.get_available_models()
        if model_id := current_info.get("model") or current_info.get("current_model"):
            if model_info := next((m for m in models if m["id"] == model_id), None):
                current_info |= {
                    "context_length": model_info.get("context_length"),
                    "pricing": model_info.get("pricing"),
                }

        return current_info
