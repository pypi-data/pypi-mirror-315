"""Agent implementation for the Qwen-Bot."""

from typing import List, Dict, Any, Optional, Literal, Union
from pydantic import BaseModel
import openai
import os
import json
from dotenv import load_dotenv
from enum import Enum
from .tools.core.model_selector import ModelSelector

class ToolCategory(str, Enum):
    """Categories for organizing tools."""
    CORE = "core"
    UTILITY = "utility"
    IO = "io"
    DEV = "development"
    AI = "ai"

class ToolMetadata(BaseModel):
    """Metadata for tool registration."""
    name: str
    description: str
    category: ToolCategory
    version: str = "1.0.0"
    author: str = "Qwen-Bot"
    requires_auth: bool = False
    is_streaming: bool = False

class Function(BaseModel):
    """Enhanced function specification with metadata."""
    name: str
    description: str
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]

class ToolResponse(BaseModel):
    """Standardized response format for tools."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class AgentConfig(BaseModel):
    """Configuration for the agent."""
    selection_mode: Literal["optimal", "manual"] = "manual"  # How to select models
    model: Optional[str] = None  # Manual model selection, if selection_mode is "manual"
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = True
    default_task: str = "general"  # Default task category when using optimal selection
    x_title: Optional[str] = None  # For OpenRouter leaderboard display
    context_length: Optional[int] = None  # For models with different context windows

class Agent:
    def __init__(self, config: Optional[AgentConfig] = None):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        
        self.config = config or AgentConfig()
        self.available_functions: Dict[str, Dict[str, Any]] = {}
        self.function_specs: List[Function] = []
        
        # Initialize model selector for optimal selection mode
        self.model_selector = ModelSelector(api_key=self.api_key)
        
        # Configure OpenAI client for OpenRouter
        default_headers = {
            "HTTP-Referer": "https://github.com/yourusername/Qwen-Bot",
            "X-Title": self.config.x_title or "Qwen-Bot"
        }
            
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers=default_headers
        )

    def register_function(
        self,
        func: callable,
        description: str,
        parameters: Dict[str, Any],
        metadata: ToolMetadata,
        task: Optional[str] = None
    ):
        """
        Register a new function that can be called by the agent.
        
        Args:
            func: The function to register
            description: Description of what the function does
            parameters: JSON schema of function parameters
            metadata: Tool metadata including category and other information
            task: Optional task category this function is associated with
        """
        # Convert ToolMetadata to dictionary
        metadata_dict = metadata.model_dump()
        
        function_spec = Function(
            name=func.__name__,
            description=description,
            parameters=parameters,
            metadata=metadata_dict
        )
        self.function_specs.append(function_spec)
        self.available_functions[func.__name__] = {
            'func': func,
            'task': task or self.config.default_task,
            'metadata': metadata_dict
        }

    async def _get_model_for_task(self, task: str) -> str:
        """Get the model based on selection mode and configuration."""
        if self.config.selection_mode == "manual":
            if not self.config.model:
                raise ValueError("Model must be specified when using manual selection mode")
            return self.config.model
            
        # Optimal selection mode
        result = await self.model_selector.get_best_model(task)
        if result['success'] and result['model']:
            return result['model']['model_id']
        return "anthropic/claude-2"  # Fallback to default model

    async def _validate_context_length(self, messages: List[Dict[str, str]], model_info: Dict[str, Any]) -> bool:
        """
        Validate if the messages fit within the model's context window.
        
        Args:
            messages: List of chat messages
            model_info: Model information including context length
            
        Returns:
            bool: True if messages fit, False otherwise
        """
        if not self.config.context_length:
            return True
            
        # Simple token estimation (can be improved with proper tokenizer)
        estimated_tokens = sum(len(msg["content"].split()) * 1.3 for msg in messages)
        return estimated_tokens <= self.config.context_length

    async def _execute_function(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered function with standardized error handling and response format.
        
        Args:
            name: Name of the function to execute
            arguments: Arguments to pass to the function
            
        Returns:
            Standardized tool response including success status and result/error
        """
        if not (function_info := self.available_functions.get(name)):
            return {
                "tool_result": ToolResponse(
                    success=False,
                    error=f"Function {name} not found",
                    metadata={"error_type": "NOT_FOUND"}
                ).model_dump()
            }
        
        try:
            result = await function_info['func'](**arguments)
            metadata = function_info['metadata']
            
            return {
                "tool_result": ToolResponse(
                    success=True,
                    data=result,
                    metadata={
                        "category": metadata["category"],
                        "version": metadata["version"],
                        "is_streaming": metadata["is_streaming"]
                    }
                ).model_dump()
            }
            
        except Exception as e:
            return {
                "tool_result": ToolResponse(
                    success=False,
                    error=str(e),
                    metadata={
                        "error_type": type(e).__name__,
                        "category": function_info['metadata']["category"]
                    }
                ).model_dump()
            }

    def set_model(self, model: str):
        """
        Manually set the model to use. This automatically switches to manual selection mode.
        
        Args:
            model: The model identifier to use
        """
        self.config.selection_mode = "manual"
        self.config.model = model

    def use_optimal_selection(self):
        """Switch to optimal (automatic) model selection mode."""
        self.config.selection_mode = "optimal"
        self.config.model = None

    async def chat(
        self,
        messages: List[Dict[str, str]],
        task: Optional[str] = None,
        stream: bool = True
    ) -> Union[Any, Dict[str, Any]]:
        """
        Send a chat request to the model with function calling capabilities.
        
        Args:
            messages: List of chat messages
            task: Optional task category (used only in optimal selection mode)
            stream: Whether to stream the response
            
        Returns:
            Either a streaming response, function execution result, or text response
        """
        try:
            # Determine which model to use based on selection mode
            model = await self._get_model_for_task(task or self.config.default_task)

            # Get model information for context length validation
            models = await self.get_available_models()
            model_info = next((m for m in models if m["id"] == model), None)

            if model_info and not await self._validate_context_length(messages, model_info):
                raise ValueError("Input exceeds model's context length limit")

            functions = [
                {
                    "name": spec.name,
                    "description": spec.description,
                    "parameters": spec.parameters
                }
                for spec in self.function_specs
            ] if self.function_specs else None

            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                functions=functions,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=stream
            )

            if stream:
                return response

            if function_call := response.choices[0].message.function_call:
                try:
                    arguments = json.loads(function_call.arguments)
                    return await self._execute_function(function_call.name, arguments)
                except json.JSONDecodeError:
                    return {
                        "tool_result": ToolResponse(
                            success=False,
                            error="Invalid function arguments format",
                            metadata={"error_type": "JSON_DECODE_ERROR"}
                        ).model_dump()
                    }

            return response.choices[0].message.content

        except Exception as e:
            if "context length" in str(e).lower():
                raise ValueError("Input exceeds model's context length limit") from e
            raise Exception(f"Error in chat completion: {str(e)}") from e

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Fetch available models and their capabilities from OpenRouter.
        
        Returns:
            List of dictionaries containing model information including:
            - id: Model identifier
            - name: Display name
            - context_length: Maximum context length
            - pricing: Input/output token pricing
            - best_for: List of tasks this model excels at (if in optimal mode)
            - score: Model's score for its best tasks (if in optimal mode)
        """
        try:
            # Get all available models first
            response = self.client.models.list()  # Removed await since it's synchronous
            all_models = []

            for model in response.data:
                model_info = {
                    "id": model.id,
                    "name": model.id,
                    "context_length": getattr(model, "context_length", None),
                    "pricing": {
                        "input": getattr(model, "input_price_per_token", None),
                        "output": getattr(model, "output_price_per_token", None)
                    }
                }
                all_models.append(model_info)

            # If in optimal mode, also get task-specific rankings
            if self.config.selection_mode == "optimal":
                tasks = await self.model_selector.list_supported_tasks()
                for task in tasks:
                    result = await self.model_selector.get_best_model(task)
                    if result['success'] and result['model']:
                        # Mark the best model for each task
                        for model in all_models:
                            if model['id'] == result['model']['model_id']:
                                model.setdefault('best_for', []).append(task)
                                model['score'] = result['model']['score']

            return all_models

        except Exception as e:
# sourcery skip: raise-specific-error
            raise Exception(f"Error fetching models: {str(e)}") from e

    async def get_current_model(self) -> Dict[str, Any]:
        """
        Get information about the currently selected model.
        
        Returns:
            Dict containing current model information including:
            - mode: "manual" or "optimal"
            - model: Current model ID if in manual mode
            - default_task: Default task category if in optimal mode
            - current_model: Current model ID if in optimal mode
            - context_length: Maximum context length of current model
            - pricing: Current model's pricing information
        """
        current_info = {
            "mode": self.config.selection_mode,
        }

        if self.config.selection_mode == "manual":
            current_info["model"] = self.config.model
        else:
            current_info |= {
                "default_task": self.config.default_task,
                "current_model": await self._get_model_for_task(
                    self.config.default_task
                ),
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
