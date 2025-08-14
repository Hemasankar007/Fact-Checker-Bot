from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging
from config.settings import Settings

class WebSearchTool:
    def __init__(self):
        self.max_results = Settings.SEARCH_MAX_RESULTS
    
    def search(self, query: str) -> List[Dict]:
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=self.max_results)
            processed_results = []
            
            for result in results:
                processed_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
            
            return processed_results
            
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            return []
    
    def get_page_content(self, url: str) -> str:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit to first 5000 chars
            
        except Exception as e:
            logging.error(f"Error fetching page content: {str(e)}")
            return ""
