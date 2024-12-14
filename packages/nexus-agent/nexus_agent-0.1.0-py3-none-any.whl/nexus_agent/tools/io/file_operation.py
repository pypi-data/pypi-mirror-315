"""File operation tools."""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

class FileOperations:
    """A tool for handling file operations safely."""
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the file operations tool.
        
        Args:
            base_dir (Optional[str]): Base directory for file operations
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
    
    async def read_file(self, filepath: str) -> str:
        """
        Read contents of a file safely.
        
        Args:
            filepath (str): Path to the file
            
        Returns:
            str: File contents or error message
        """
        try:
            file_path = (self.base_dir / filepath).resolve()
            if not file_path.is_file():
                return f"Error: File '{filepath}' not found"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    async def write_file(self, filepath: str, content: str) -> str:
        """
        Write content to a file safely.
        
        Args:
            filepath (str): Path to the file
            content (str): Content to write
            
        Returns:
            str: Success message or error
        """
        try:
            file_path = (self.base_dir / filepath).resolve()
            
            # Create directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully wrote to {filepath}"
            
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    async def list_directory(self, directory: str = ".") -> str:
        """
        List contents of a directory.
        
        Args:
            directory (str): Directory path
            
        Returns:
            str: Directory contents or error message
        """
        try:
            dir_path = (self.base_dir / directory).resolve()
            if not dir_path.is_dir():
                return f"Error: Directory '{directory}' not found"
            
            contents = list(dir_path.iterdir())
            return "\n".join(str(p.relative_to(self.base_dir)) for p in contents)
            
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the file operation tools."""
        return {
            "read_file": {
                "description": "Read contents of a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Path to the file to read"
                        }
                    },
                    "required": ["filepath"]
                }
            },
            "write_file": {
                "description": "Write content to a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Path to the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["filepath", "content"]
                }
            },
            "list_directory": {
                "description": "List contents of a directory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "Directory path to list",
                            "default": "."
                        }
                    }
                }
            }
        }
