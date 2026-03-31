# 🤖 Autonomous AI Web Researcher Agent

This is a 100% free, local Python application that uses **LangGraph** (agent orchestration) and **Ollama** (local LLMs) to search the internet and summarize findings.

## Tech Stack
* **Agentic Framework:** `langgraph`
* **Model Engine:** `Ollama` 
* **Search Tool:** `duckduckgo-search` (Free web search)
* **Scraper Tool:** `BeautifulSoup4` (HTML parsing)
* **Frontend:** `Streamlit`

## Setup Instructions

1. **Install Ollama**
   Ensure Ollama is installed on your machine. Open a terminal and run:
   ```bash
   ollama pull llama3.2:1b
   ```

2. **Setup Python Environment**
   Open a terminal in this `Autonomous Web Researcher Agent` folder.
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the App**
   ```powershell
   streamlit run app.py
   ```
