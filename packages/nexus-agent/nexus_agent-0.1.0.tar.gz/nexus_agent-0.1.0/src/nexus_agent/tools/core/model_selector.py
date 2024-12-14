"""Model selection tools based on OpenRouter rankings."""

from typing import Dict, Any, Optional, List
import requests
import aiohttp
import json

class ModelSelector:
    """A tool for selecting the optimal AI model based on OpenRouter rankings."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the model selector tool.
        
        Args:
            api_key (Optional[str]): OpenRouter API key
        """
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.rankings_cache = None
        self.rankings_cache_time = None
    
    async def _fetch_rankings(self) -> Dict[str, Any]:
        """
        Fetch current rankings from OpenRouter.
        
        Returns:
            Dict containing model rankings data
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "HTTP-Referer": "https://github.com/yourusername/Qwen-Bot"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/rankings", headers=headers) as response:
                response.raise_for_status()
                return await response.json()
    
    async def get_best_model(self, task: str) -> Dict[str, Any]:
        """
        Get the best model for a specific task based on OpenRouter rankings.
        
        Args:
            task (str): The task category (e.g., 'coding', 'math', 'writing')
            
        Returns:
            Dict containing model information and rankings
        """
        try:
            # Fetch current rankings
            rankings = await self._fetch_rankings()
            
            # Filter and sort models based on task
            task_models = []
            for model in rankings.get('models', []):
                task_score = model.get('scores', {}).get(task.lower(), 0)
                if task_score > 0:
                    task_models.append({
                        'model_id': model['id'],
                        'name': model['name'],
                        'score': task_score,
                        'context_length': model.get('context_length', 0),
                        'pricing': model.get('pricing', {})
                    })
            
            # Sort by score and get the best model
            if task_models:
                best_model = sorted(task_models, key=lambda x: x['score'], reverse=True)[0]
                return {
                    'success': True,
                    'model': best_model,
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'model': None,
                    'error': f'No models found for task: {task}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'model': None,
                'error': str(e)
            }
    
    async def list_supported_tasks(self) -> List[str]:
        """
        Get a list of tasks that have model rankings.
        
        Returns:
            List of supported task categories
        """
        try:
            rankings = await self._fetch_rankings()
            
            # Extract unique task categories from model scores
            tasks = set()
            for model in rankings.get('models', []):
                tasks.update(model.get('scores', {}).keys())
            
            return sorted(list(tasks))
            
        except Exception:
            return []
    
    async def get_model_details(self, model_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific model.
        
        Args:
            model_id (str): The ID of the model to get details for
            
        Returns:
            Dict containing model details
        """
        try:
            rankings = await self._fetch_rankings()
            
            for model in rankings.get('models', []):
                if model['id'] == model_id:
                    return {
                        'success': True,
                        'details': model,
                        'error': None
                    }
            
            return {
                'success': False,
                'details': None,
                'error': f'Model not found: {model_id}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'details': None,
                'error': str(e)
            }
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the model selector tools."""
        return {
            "get_best_model": {
                "description": "Get the best model for a specific task based on OpenRouter rankings",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The task category (e.g., 'coding', 'math', 'writing')"
                        }
                    },
                    "required": ["task"]
                }
            },
            "list_supported_tasks": {
                "description": "Get a list of tasks that have model rankings",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            "get_model_details": {
                "description": "Get detailed information about a specific model",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "model_id": {
                            "type": "string",
                            "description": "The ID of the model to get details for"
                        }
                    },
                    "required": ["model_id"]
                }
            }
        }
