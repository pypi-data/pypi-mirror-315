"""Interface for the Qwen-Bot agent."""

from typing import Dict, Any, Optional, List
import asyncio
import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from .agent import Agent, AgentConfig
from pydantic import BaseModel

class ToolExecutionResult(BaseModel):
    """Model for tool execution results in the chat history."""
    tool_name: str
    category: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatMessage(BaseModel):
    """Model for chat messages with support for tool execution results."""
    role: str
    content: str
    tool_result: Optional[ToolExecutionResult] = None

class Interface:
    def __init__(self):
        self.agent = Agent(AgentConfig())
        if "conversation_history" not in st.session_state:
            st.session_state.conversation_history = []
        self.available_models: List[Dict[str, Any]] = []
        self._executor = ThreadPoolExecutor()
    
    async def initialize(self):
        """Initialize the interface and fetch available models."""
        self.available_models = await self.agent.get_available_models()
    
    def get_model_choices(self) -> List[Dict[str, Any]]:
        """Get available model choices for the dropdown."""
        choices = [{"id": "optimal", "name": "Optimal AI (Auto-select)", "description": "Automatically selects the best model for each task"}]
        
        for model in self.available_models:
            description_parts = []
            if model.get("context_length"):
                description_parts.append(f"Context: {model['context_length']} tokens")
            
            pricing = model.get("pricing", {})
            if pricing.get("input") is not None and pricing.get("output") is not None:
                description_parts.append(
                    f"${pricing['input']}/1K input, ${pricing['output']}/1K output"
                )
            
            if "best_for" in model:
                description_parts.append(f"Best for: {', '.join(model['best_for'])}")
            
            choices.append({
                "id": model["id"],
                "name": model["name"],
                "description": " | ".join(description_parts)
            })
        
        return choices
    
    def select_model(self, model_id: str):
        """Select a model to use."""
        if model_id == "optimal":
            self.agent.use_optimal_selection()
        else:
            self.agent.set_model(model_id)
    
    async def get_current_model(self) -> Dict[str, Any]:
        """Get information about the currently selected model."""
        return await self.agent.get_current_model()
    
    def format_tool_result(self, result: ToolExecutionResult) -> str:
        """Format tool execution result for display."""
        if not result.success:
            return f"❌ Error executing {result.tool_name}: {result.error}"
        
        # Format successful result based on category
        if result.category == "UTILITY":
            return f"🔧 {result.data}"
        elif result.category == "IO":
            return f"📁 {result.data}"
        elif result.category == "DEV":
            return f"💻 {result.data}"
        elif result.category == "AI":
            return f"🤖 {result.data}"
        else:
            return f"✅ {result.data}"
    
    async def send_message(self, message: str, task: Optional[str] = None) -> str:
        """Send a message to the agent."""
        # Add user message to history
        user_message = ChatMessage(role="user", content=message)
        st.session_state.conversation_history.append(user_message.model_dump())
        
        try:
            response = await self.agent.chat(
                messages=[msg for msg in st.session_state.conversation_history if "tool_result" not in msg],
                task=task,
                stream=False
            )
            
            # Handle tool execution results
            if isinstance(response, dict) and "tool_result" in response:
                tool_result = ToolExecutionResult(**response["tool_result"])
                assistant_message = ChatMessage(
                    role="assistant",
                    content=self.format_tool_result(tool_result),
                    tool_result=tool_result
                )
            else:
                assistant_message = ChatMessage(
                    role="assistant",
                    content=response
                )
            
            st.session_state.conversation_history.append(assistant_message.model_dump())
            return assistant_message.content
            
        except ValueError as e:
            if "context length" in str(e).lower():
                return "Error: Message too long for model's context window. Try clearing the conversation history or using a model with a larger context window."
            raise
    
    def clear_history(self):
        """Clear the conversation history."""
        st.session_state.conversation_history = []
    
    async def get_supported_tasks(self) -> List[str]:
        """Get a list of tasks that have model rankings."""
        return await self.agent.model_selector.list_supported_tasks()
    
    async def get_task_best_model(self, task: str) -> Optional[Dict[str, Any]]:
        """Get information about the best model for a specific task."""
        result = await self.agent.model_selector.get_best_model(task)
        return result['model'] if result['success'] and result['model'] else None

    def run_async(self, coro):
        """Run async code in a way that's compatible with Streamlit."""
        if asyncio.iscoroutine(coro):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()
        return coro

class ChatInterface(Interface):
    """Streamlit-based chat interface for the Qwen-Bot."""
    
    def __init__(self, agent: Agent):
        super().__init__()
        self.agent = agent
    
    def render_message(self, msg: Dict[str, Any]):
        """Render a chat message with tool execution results if present."""
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])
            
            if tool_result := msg.get("tool_result"):
                with st.expander("Tool Execution Details", expanded=False):
                    st.json({
                        "tool": tool_result["tool_name"],
                        "category": tool_result["category"],
                        "success": tool_result["success"],
                        "metadata": tool_result.get("metadata", {})
                    })
    
    async def launch(self) -> None:
        """Launch the Streamlit interface."""
        await self.initialize()
        
        # Configure the page
        st.set_page_config(
            page_title="Qwen-Bot",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Apply custom CSS for a modern, clean look
        st.markdown("""
            <style>
                /* Global styles */
                .stApp {
                    background-color: #f0f2f6;
                }
                
                /* Sidebar styling */
                .stSidebar {
                    background-color: #ffffff;
                    border-right: 1px solid #e1e4e8;
                    padding: 2rem 1rem;
                }
                
                /* Button styling */
                .stButton button {
                    border-radius: 8px;
                    background-color: #0066cc;
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    transition: background-color 0.3s;
                }
                .stButton button:hover {
                    background-color: #0052a3;
                }
                
                /* Chat message styling */
                .stChatMessage {
                    background-color: white;
                    border-radius: 12px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }
                
                /* Input field styling */
                .stTextInput input {
                    border-radius: 8px;
                    border: 2px solid #e1e4e8;
                    padding: 0.75rem;
                    transition: border-color 0.3s;
                }
                .stTextInput input:focus {
                    border-color: #0066cc;
                    box-shadow: 0 0 0 2px rgba(0,102,204,0.2);
                }
                
                /* Expander styling */
                .streamlit-expanderHeader {
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border: none;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                }
                
                /* Progress bar styling */
                .stProgress > div > div {
                    background-color: #0066cc;
                }
                
                /* Remove default Streamlit elements */
                div[data-testid="stToolbar"] {
                    display: none;
                }
                div[data-testid="stDecoration"] {
                    display: none;
                }
                footer {
                    display: none;
                }
                
                /* Typography */
                .stMarkdown {
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                }
                h1, h2, h3 {
                    color: #1a1f36;
                    font-weight: 600;
                }
                
                /* Tool result styling */
                .tool-result {
                    margin-top: 0.75rem;
                    padding: 1rem;
                    border-radius: 8px;
                    background-color: #f8f9fa;
                    border: 1px solid #e1e4e8;
                }
                
                /* JSON viewer styling */
                pre {
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    padding: 1rem;
                    border: 1px solid #e1e4e8;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Create two columns for better space utilization
        self._render_chat_interface()

    async def _handle_chat_input(self, prompt: str):
        """Handle chat input asynchronously."""
        try:
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner(""):
                    response = await self.send_message(prompt, st.session_state.get("selected_task"))
                st.markdown(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            if "context length" in str(e).lower():
                st.warning("Try clearing the conversation history or using a model with a larger context window.")

    def _render_chat_interface(self):
        """Render the chat interface synchronously."""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.title("💬 Qwen-Bot")
            
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.conversation_history:
                    self.render_message(msg)
            
            if prompt := st.chat_input("Message Qwen-Bot..."):
                self.render_message({"role": "user", "content": prompt})
                self.run_async(self._handle_chat_input(prompt))

        with col2:
            with st.sidebar:
                st.markdown("### ⚙️ Settings")
                
                # Model selection with improved UI
                model_choices = self.get_model_choices()
                selected_model = st.selectbox(
                    "🤖 Model",
                    options=[choice["id"] for choice in model_choices],
                    format_func=lambda x: next(choice["name"] for choice in model_choices if choice["id"] == x),
                    index=0,
                    help="Select the AI model to use for chat"
                )
                
                # Task selection for optimal mode
                if selected_model == "optimal":
                    supported_tasks = self.run_async(self.get_supported_tasks())
                    st.session_state.selected_task = st.selectbox(
                        "📋 Task Category",
                        options=supported_tasks,
                        help="Select the type of task for optimal model selection"
                    )
                else:
                    st.session_state.selected_task = None
                
                self.select_model(selected_model)
                
                # Collapsible model info
                with st.expander("ℹ️ Model Information", expanded=False):
                    model_info = self.run_async(self.get_current_model())
                    st.json(model_info)
                
                # Token counter with progress bar
                if st.session_state.conversation_history:
                    total_tokens = sum(len(msg["content"].split()) for msg in st.session_state.conversation_history) * 1.3
                    st.markdown("### 📊 Token Usage")
                    st.progress(min(total_tokens / 4000, 1.0))  # Assuming 4000 token limit
                    st.caption(f"{int(total_tokens):,} tokens used")
                
                # Clear history button with confirmation
                if st.button("🗑️ Clear Chat History", type="secondary"):
                    if st.session_state.conversation_history:  # Only show confirmation if there's history
                        if st.button("✓ Confirm Clear"):
                            self.clear_history()
                            st.experimental_rerun()
                    else:
                        self.clear_history()
                        st.experimental_rerun()
