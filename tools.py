import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='duckduckgo_search')

def search_duckduckgo(query: str, max_results: int = 3) -> list:
    """Uses DuckDuckGo to search the web for free without API keys."""
    results = []
    try:
        results_generator = DDGS().text(query, max_results=max_results)
        # Convert to dictionary format our existing code expects
        for r in results_generator:
            results.append({
                "title": r.get("title", ""),
                "link": r.get("href", ""),
                "snippet": r.get("body", "")
            })
    except Exception as e:
        print(f"Error searching DuckDuckGo (v6): {e}")
    return results

def scrape_webpage(url: str) -> str:
    """Scrapes the readable text content from a given URL."""
    try:
        # User-Agent to prevent basic bot blocking
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
            
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        # Collapse whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit size to prevent blowing up the LLM context window
        return text[:10000] 
        
    except Exception as e:
        return f"Failed to scrape webpage: {str(e)}"
