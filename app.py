import streamlit as st
from agent import app as agent_app  # Import our compiled LangGraph!

st.set_page_config(page_title="AI Researcher Agent", page_icon="🌐", layout="wide")

# ================================
# 🎨 PREMIUM CSS STYLING
# ================================
custom_css = """
<style>
    /* Change background colors */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Clean up default Streamlit elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Elegant Sidebar */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Glowing Title */
    .title-text {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3.5rem;
        background: -webkit-linear-gradient(45deg, #58a6ff, #a371f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .subtitle-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #8b949e;
        margin-bottom: 30px;
    }
    
    /* Input box styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #30363d;
        background-color: #161b22;
        color: white;
        padding: 15px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.3);
    }
    
    /* Start Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #238636, #2ea043);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 12px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(46, 160, 67, 0.4);
        color: white;
    }
    
    /* Report Container */
    .report-card {
        background-color: #161b22;
        padding: 40px;
        border-radius: 15px;
        border: 1px solid #30363d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-top: 30px;
        line-height: 1.6;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ================================
# 🖥️ APPLICATION LAYOUT
# ================================

# Header Row
st.markdown('<p class="title-text">🌐 Autonomous AI Agent</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">A local LangGraph agent that independently scrapes the web and compiles technical research reports.</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.shields.io/badge/Status-Online-success?style=for-the-badge", width=150)
    st.header("⚙️ Agent Settings")
    
    st.info("""
    **Core Technologies:**
    * 🧠 **Orchestration:** LangGraph
    * 🔎 **Tools:** DuckDuckGo & BS4
    * 💬 **Brain:** Local Ollama
    """)
    
    st.divider()
    ollama_model = st.selectbox(
        "Select LLM Brain (Ensure running locally)", 
        ["llama3", "mistral", "llama3.2:1b", "phi3", "qwen2"], 
        index=2
    )

# Main Input Section
col1, col2 = st.columns([4, 1])

with col1:
    topic = st.text_input("📝 What should I research today?", placeholder="e.g. 'What are the newest features in React 19?'", label_visibility="collapsed")

with col2:
    start_button = st.button("🚀 Initialize Agent")

# ================================
# ⚙️ AGENT EXECUTION LOOP
# ================================
if start_button:
    if not topic:
        st.warning("Please enter a research topic first.")
    else:
        inputs = {
            "topic": topic,
            "model_name": ollama_model,
        }
        
        # Elegant streaming status box
        with st.status("🧠 **Agent Thought Process Activated...**", expanded=True) as status_box:
            try:
                # Stream the state through the graph
                for event in agent_app.stream(inputs):
                    for node_name, node_output in event.items():
                        
                        # Dynamic micro-animations for thoughts
                        node_label = node_name.replace('_', ' ').upper()
                        if node_name == "search":
                            st.write(f"🔎 Used DuckDuckGo to search for `{topic}`")
                        elif node_name == "scrape":
                            url = node_output.get("selected_url", "a webpage")
                            st.write(f"📄 Scraping content from `{url}`")
                        elif node_name == "write":
                            st.write(f"✍️ Synthesizing data using `{ollama_model}`...")
                        else:
                            st.write(f"✅ Completed: **{node_label}**")
                            
                # Close the status box neatly
                status_box.update(label="🤖 Research Complete!", state="complete", expanded=False)
                
                # Fetch final report
                final_report = node_output.get("final_report", "Report generation failed.")
                
                # Display in a beautiful container
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.markdown(final_report)
                st.markdown('</div>', unsafe_allow_html=True)
                st.balloons() # Treat the user to a celebration!

            except Exception as e:
                status_box.update(label="🚨 Agent completely failed.", state="error", expanded=True)
                st.error(f"Error: {str(e)}")
                st.info("Check: Is Ollama running in your background terminal?")
