"""Interface for the agent.

This module provides the chat interface implementation using Streamlit.
It handles the rendering of messages, model selection, and other UI components.
"""
#TODO: Done for 0.2.0

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache, wraps
from typing import Any, Dict, List, Optional, Union, TypeVar, Callable, Coroutine, cast

import extra_streamlit_components as stx
import streamlit as st
from pydantic import BaseModel, Field
from streamlit_custom_notification_box import custom_notification_box
from streamlit_option_menu import option_menu

from .agent import Agent, AgentConfig, OpenRouterError

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Type variable for generic return types
T = TypeVar('T')
AsyncFunc = Callable[..., Coroutine[Any, Any, T]]


def async_error_handler(func: AsyncFunc[T]) -> AsyncFunc[T]:
    """Decorator for handling errors in async methods.
    
    Args:
        func: Async function to wrap
        
    Returns:
        Wrapped async function with error handling
    """
    @wraps(func)
    async def wrapper(self: 'Interface', *args: Any, **kwargs: Any) -> T:
        try:
            return await func(self, *args, **kwargs)
        except OpenRouterError as e:
            logger.error("OpenRouter API error: %s", str(e))
            self._show_error("OpenRouter API error", str(e))
            raise
        except asyncio.TimeoutError:
            logger.error("Request timed out")
            self._show_error("Timeout", "Request took too long to complete")
            raise
        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            self._show_error("Error", str(e))
            raise
    return cast(AsyncFunc[T], wrapper)


class ToolExecutionResult(BaseModel):
    """Model for tool execution results in the chat history."""

    tool_name: str = Field(..., description="Name of the executed tool")
    category: str = Field(..., description="Tool category")
    success: bool = Field(..., description="Whether the tool execution succeeded")
    data: Optional[Any] = Field(default=None, description="Tool execution result data")
    error: Optional[str] = Field(default=None, description="Error message if execution failed")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional execution metadata")


class ChatMessage(BaseModel):
    """Model for chat messages with support for tool execution results."""

    role: str = Field(..., description="Message role (user/assistant/system/tool)")
    content: str = Field(..., description="Message content")
    tool_result: Optional[ToolExecutionResult] = Field(default=None, description="Tool execution result if applicable")


class ThemeManager:
    """Manages the application theme settings."""

    THEMES = {
        "dark": {
            "bg_color": "#0e1117",
            "text_color": "#fafafa",
            "button_bg": "#262730",
            "select_bg": "#262730",
        },
        "light": {
            "bg_color": "#ffffff",
            "text_color": "#1a1f36",
            "button_bg": "#f0f2f6",
            "select_bg": "#f0f2f6",
        },
    }

    @staticmethod
    def get_theme_cookie() -> str:
        """Get the theme preference from cookies."""
        cookie_manager = stx.CookieManager()
        return cookie_manager.get(cookie="theme") or "dark"

    @staticmethod
    def set_theme_cookie(theme: str) -> None:
        """Set the theme preference in cookies."""
        cookie_manager = stx.CookieManager()
        cookie_manager.set("theme", theme)

    @classmethod
    def apply_theme(cls, theme: str) -> None:
        """Apply the theme styling."""
        theme_config = cls.THEMES.get(theme, cls.THEMES["dark"])
        
        st.set_page_config(
            page_title="Nexus-Agent",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items=None,
        )

        st.markdown(
            f"""
            <style>
                .stApp {{
                    background-color: {theme_config['bg_color']};
                    color: {theme_config['text_color']};
                }}
                .stButton button {{
                    background-color: {theme_config['button_bg']};
                    color: {theme_config['text_color']};
                }}
                .stSelectbox div[data-baseweb="select"] {{
                    background-color: {theme_config['select_bg']};
                }}
                .stProgress > div > div > div > div {{
                    background-color: #0066cc;
                }}
                .stMarkdown a {{
                    color: #0066cc;
                }}
                .stChat {{
                    border-radius: 10px;
                    padding: 10px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )


class Interface:
    """Base interface class with core functionality."""

    def __init__(self, agent: Optional[Agent] = None):
        """Initialize the interface.
        
        Args:
            agent: Optional agent instance. If not provided, creates new one with default config.
        """
        self.agent = agent or Agent(AgentConfig())
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        self.available_models: List[Dict[str, Any]] = []
        self._executor = ThreadPoolExecutor()

    def _show_error(self, title: str, message: str) -> None:
        """Display error notification.
        
        Args:
            title: Error title
            message: Error message
        """
        custom_notification_box(
            icon="❌",
            textDisplay=f"{title}: {message}",
            externalLink="",
            url="",
            styles={"icon": {"color": "red"}, "text": {"color": "white"}},
        )

    @async_error_handler
    async def initialize(self) -> List[Dict[str, Any]]:
        """Initialize the interface and fetch available models."""
        self.available_models = await self.agent.get_available_models()
        return self.available_models

    @lru_cache(maxsize=1)
    def get_model_choices(self) -> List[Dict[str, Any]]:
        """Get available model choices for the dropdown."""
        choices = [
            {
                "id": "optimal",
                "name": "Optimal AI (Auto-select)",
                "description": "Automatically selects the best model for each task",
            }
        ]

        for model in self.available_models:
            description_parts = []
            if model.get("context_length"):
                desc = f"Context: {model['context_length']} tokens"
                description_parts.append(desc)

            pricing = model.get("pricing", {})
            if pricing.get("input") and pricing.get("output"):
                price_desc = f"${pricing['input']}/1K input, ${pricing['output']}/1K output"
                description_parts.append(price_desc)

            if "best_for" in model:
                best_desc = f"Best for: {', '.join(model['best_for'])}"
                description_parts.append(best_desc)

            choices.append({
                "id": model["id"],
                "name": model["name"],
                "description": " | ".join(description_parts),
            })

        return choices

    def select_model(self, model_id: str) -> None:
        """Select a model to use.
        
        Args:
            model_id: Model identifier
        """
        if model_id == "optimal":
            self.agent.use_optimal_selection()
        else:
            self.agent.set_model(model_id)

    @async_error_handler
    async def get_current_model(self) -> Dict[str, Any]:
        """Get information about the currently selected model."""
        return await self.agent.get_current_model()

    def format_tool_result(self, result: ToolExecutionResult) -> str:
        """Format tool execution result for display.
        
        Args:
            result: Tool execution result
            
        Returns:
            Formatted string for display
        """
        if not result.success:
            return f"❌ Error executing {result.tool_name}: {result.error}"

        category_icons = {
            "UTILITY": "🔧",
            "IO": "📁",
            "DEV": "💻",
            "AI": "🤖",
            "CORE": "⚙️",
        }

        icon = category_icons.get(result.category, "✅")
        return f"{icon} {result.data}"

    @async_error_handler
    async def send_message(
        self, message: str, task: Optional[str] = None
    ) -> Union[str, Dict[str, Any]]:
        """Send a message to the agent.
        
        Args:
            message: Message content
            task: Optional task category
            
        Returns:
            Response content or tool result
        """
        user_message = ChatMessage(role="user", content=message)
        msg_data = user_message.model_dump()
        sess = st.session_state
        sess.conversation_history.append(msg_data)

        messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in sess.conversation_history
            if "tool_result" not in msg
        ]

        response = await self.agent.chat(messages=messages, task=task, stream=False)

        if isinstance(response, dict) and "tool_result" in response:
            tool_result = ToolExecutionResult(**response["tool_result"])
            assistant_message = ChatMessage(
                role="assistant",
                content=self.format_tool_result(tool_result),
                tool_result=tool_result,
            )
        else:
            content = str(response) if response is not None else ""
            assistant_message = ChatMessage(role="assistant", content=content)

        sess.conversation_history.append(assistant_message.model_dump())
        return assistant_message.content

    def clear_history(self) -> None:
        """Clear the conversation history."""
        st.session_state.conversation_history = []

    @st.cache_data(ttl=3600)
    async def get_supported_tasks(self) -> List[str]:
        """Get a list of tasks that have model rankings."""
        return await self.agent.model_selector.list_supported_tasks()

    @st.cache_data(ttl=3600)
    async def get_task_best_model(self, task: str) -> Optional[Dict[str, Any]]:
        """Get information about the best model for a specific task.
        
        Args:
            task: Task category
            
        Returns:
            Best model information if available
        """
        result = await self.agent.model_selector.get_best_model(task)
        return result["model"] if result["success"] and result["model"] else None

    def run_async(self, coro: Any) -> Any:
        """Run async code in a way that's compatible with Streamlit.
        
        Args:
            coro: Coroutine to run
            
        Returns:
            Coroutine result
        """
        if asyncio.iscoroutine(coro):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()
        return coro


class ChatInterface(Interface):
    """Streamlit-based chat interface with enhanced UI components."""

    def __init__(self, agent: Agent):
        """Initialize chat interface.
        
        Args:
            agent: Agent instance
        """
        super().__init__(agent)
        self.theme_manager = ThemeManager()

    def render_message(self, msg: Dict[str, Any]) -> None:
        """Render a chat message with tool execution results.
        
        Args:
            msg: Message data
        """
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

            if tool_result := msg.get("tool_result"):
                with st.expander("Tool Execution Details", expanded=False):
                    st.json({
                        "tool": tool_result["tool_name"],
                        "category": tool_result["category"],
                        "success": tool_result["success"],
                        "metadata": tool_result.get("metadata", {}),
                    })

    def render_navigation(self) -> str:
        """Render the navigation menu.
        
        Returns:
            Selected page name
        """
        nav_styles = {
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#0066cc"},
        }

        return option_menu(
            menu_title=None,
            options=["Chat", "Settings", "About"],
            icons=["chat-dots-fill", "gear-fill", "info-circle-fill"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles=nav_styles,
        )

    def render_settings(self) -> None:
        """Render the settings panel."""
        st.markdown("### ⚙️ Settings")

        # Theme selection
        current_theme = self.theme_manager.get_theme_cookie()
        theme_options = {"dark": "🌙 Dark", "light": "☀️ Light"}

        selected_theme = st.selectbox(
            "Theme",
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=list(theme_options.keys()).index(current_theme),
        )

        if selected_theme != current_theme:
            self.theme_manager.set_theme_cookie(selected_theme)
            self.theme_manager.apply_theme(selected_theme)
            st.rerun()

        # Model selection
        model_choices = self.get_model_choices()
        model_ids = [choice["id"] for choice in model_choices]
        model_name_lookup = {c["id"]: c["name"] for c in model_choices}

        selected_model = st.selectbox(
            "🤖 Model",
            options=model_ids,
            format_func=lambda x: model_name_lookup[x],
            index=0,
            help="Select the AI model to use for chat",
        )

        if selected_model == "optimal":
            supported_tasks = self.run_async(self.get_supported_tasks())
            st.session_state.selected_task = st.selectbox(
                "📋 Task Category",
                options=supported_tasks,
                help="Select the type of task for optimal model selection",
            )
        else:
            st.session_state.selected_task = None

        self.select_model(selected_model)

        # Model information
        with st.expander("ℹ️ Model Information", expanded=False):
            model_info = self.run_async(self.get_current_model())
            st.json(model_info)

            if st.session_state.conversation_history:
                total_tokens = sum(
                    len(msg["content"].split()) * 1.3
                    for msg in st.session_state.conversation_history
                )
                st.markdown("### 📊 Token Usage")
                st.progress(min(total_tokens / 4000, 1.0))
                st.caption(f"{int(total_tokens):,} tokens used")

        if st.button("🗑️ Clear Chat History", type="secondary"):
            self.clear_history()
            custom_notification_box(
                icon="✅",
                textDisplay="Chat history cleared successfully",
                externalLink="",
                url="",
                styles={"icon": {"color": "green"}, "text": {"color": "white"}},
            )
            st.rerun()

    async def _handle_chat_input(self, prompt: str) -> None:
        """Handle chat input with improved error handling.
        
        Args:
            prompt: User input message
        """
        try:
            async with asyncio.timeout(30):
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Generating response..."):
                        response = await self.send_message(
                            prompt, st.session_state.get("selected_task")
                        )
                    st.markdown(response)
        except asyncio.TimeoutError:
            logger.error("Message sending timed out")
            custom_notification_box(
                icon="⚠️",
                textDisplay="Response generation timed out. Please try again.",
                externalLink="",
                url="",
                styles={"icon": {"color": "orange"}, "text": {"color": "white"}},
            )
        except Exception as e:
            logger.error("Chat input error: %s", str(e))
            if "context length" in str(e).lower():
                msg = (
                    "Context limit reached. Please clear history or use a "
                    "larger context model."
                )
            else:
                msg = f"An unexpected error occurred: {str(e)}"

            custom_notification_box(
                icon="❌",
                textDisplay=msg,
                externalLink="",
                url="",
                styles={"icon": {"color": "red"}, "text": {"color": "white"}},
            )

    async def launch(self) -> None:
        """Launch the Streamlit interface with enhanced UI."""
        await self.initialize()

        # Apply theme
        self.theme_manager.apply_theme(self.theme_manager.get_theme_cookie())

        # Navigation
        selected_page = self.render_navigation()

        if selected_page == "Chat":
            st.title("💬 Nexus-Agent")

            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.conversation_history:
                    self.render_message(msg)

            if prompt := st.chat_input("Message Nexus-Agent..."):
                self.render_message({"role": "user", "content": prompt})
                self.run_async(self._handle_chat_input(prompt))

        elif selected_page == "Settings":
            self.render_settings()

        else:  # About page
            st.title("ℹ️ About Nexus-Agent")
            about_text = """
            Nexus-Agent is an advanced AI chat interface that leverages 
            multiple AI models and tools to provide comprehensive 
            assistance across various tasks.

            ### Features
            - 🤖 Multiple AI model support
            - 🎯 Automatic model selection based on task
            - 🌙 Dark/Light theme support
            - 🔧 Various utility tools
            - 💻 Development tools
            - 📁 File operations
            - 🎨 AI image generation

            ### Version
            Current Version: 1.0.0

            ### Support
            For issues or feature requests, please visit our GitHub repository.
            """
            st.markdown(about_text)
