from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Import our custom free tools
from tools import search_duckduckgo, scrape_webpage

# 1. Define the Agent's Memory/State Framework
class AgentState(TypedDict):
    topic: str
    search_results: List[dict]
    selected_url: str
    scraped_content: str
    final_report: str
    model_name: str

# 2. Define the Agent's Actions (Nodes)

def search_node(state: AgentState):
    """Searches the web for the user's topic."""
    print(f"-> Searching DuckDuckGo for: {state['topic']}")
    
    # We alter the search slightly to get recent articles
    query = f"{state['topic']} latest news or guide"
    results = search_duckduckgo(query, max_results=3)
    
    return {"search_results": results}

def scrape_node(state: AgentState):
    """Picks the first result and reads its contents."""
    results = state.get("search_results", [])
    
    if not results:
        return {"scraped_content": "No results found to scrape.", "selected_url": "None"}
        
    # We'll just grab the very first link for simplicity
    best_link = results[0]["link"]
    print(f"-> Scraping Website: {best_link}")
    
    content = scrape_webpage(best_link)
    
    return {"selected_url": best_link, "scraped_content": content}

def write_report_node(state: AgentState):
    """Uses the local LLM to digest the scraped content and write a report."""
    print(f"-> Writing Final Report using {state.get('model_name', 'llama3.2:1b')}...")
    
    # Initialize local Ollama
    llm = Ollama(model=state.get("model_name", "llama3.2:1b"))
    
    prompt = PromptTemplate(
        input_variables=["topic", "content", "url"],
        template="""You are an expert AI Researcher. Write a clear, comprehensive, and engaging report on the topic: "{topic}".
        
Base your report entirely on the following recently scraped web content from "{url}". 
Do not hallucinate facts outside of this content.
If the content seems totally unrelated to the topic, state that frankly.

Structure the report well using Markdown (Headers, bullet points).

--- Scraped Content ---
{content}

--- End Content ---

Expert Report:"""
    )
    
    chain = prompt | llm
    
    response = chain.invoke({
        "topic": state["topic"],
        "content": state.get("scraped_content", "No content available."),
        "url": state.get("selected_url", "Unknown")
    })
    
    return {"final_report": response}


# 3. Construct the WorkFlow Graph

# Initialize the graph Builder
workflow = StateGraph(AgentState)

# Add our thinking nodes
workflow.add_node("search", search_node)
workflow.add_node("scrape", scrape_node)
workflow.add_node("write", write_report_node)

# Define the flow/edges
workflow.set_entry_point("search")
workflow.add_edge("search", "scrape")
workflow.add_edge("scrape", "write")
workflow.add_edge("write", END)

# Compile into an executable application
app = workflow.compile()
