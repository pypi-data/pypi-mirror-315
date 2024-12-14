"""Web browser interaction tools."""

import requests
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
import json

class WebBrowser:
    """A tool for web browsing and interaction."""
    
    def __init__(self):
        """Initialize the web browser tool."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    async def visit_url(self, url: str) -> str:
        """
        Visit a URL and get its content.
        
        Args:
            url (str): The URL to visit
            
        Returns:
            str: Page content or error message
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract main content
            title = soup.title.string if soup.title else "No title"
            text = soup.get_text(separator='\n', strip=True)
            
            # Limit text length
            max_length = 1000
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return f"Title: {title}\n\nContent:\n{text}"
            
        except Exception as e:
            return f"Error visiting URL: {str(e)}"
    
    async def extract_links(self, url: str) -> str:
        """
        Extract links from a webpage.
        
        Args:
            url (str): The URL to extract links from
            
        Returns:
            str: List of links or error message
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            # Format links
            formatted_links = []
            for link in links[:10]:  # Limit to first 10 links
                text = link.get_text(strip=True) or "No text"
                href = link['href']
                formatted_links.append(f"{text}: {href}")
            
            return "\n".join(formatted_links)
            
        except Exception as e:
            return f"Error extracting links: {str(e)}"
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the schema for the web browser tools."""
        return {
            "visit_url": {
                "description": "Visit a URL and get its content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to visit"
                        }
                    },
                    "required": ["url"]
                }
            },
            "extract_links": {
                "description": "Extract links from a webpage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to extract links from"
                        }
                    },
                    "required": ["url"]
                }
            }
        }
