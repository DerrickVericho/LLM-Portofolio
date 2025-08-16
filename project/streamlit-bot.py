from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="💰 Finance AI Expert",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1f4e79, #2e8b57);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f4e79;
        background-color: #f8f9fa;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .assistant-message {
        background-color: #f1f8e9;
        border-left-color: #4caf50;
    }
    .sidebar-content {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [] # Store chat history

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(
        k=10,  # Remember last 10 exchanges
        return_messages=True
    )

# Main header
st.markdown("""
<div class="main-header">
    <h1>💰 Finance AI Expert</h1>
    <p>Your Personal Investment & Trading Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("🔧 Configuration")
    
    # Model selection
    model_options = {
        "GPT-4o Mini (Recommended)": "gpt-4o-mini",
        "GPT-4o": "gpt-4o",
        "GPT-3.5 Turbo": "gpt-3.5-turbo"
    }
    selected_model = st.selectbox(
        "Choose Model",
        options=list(model_options.keys()),
        index=0,
        help="GPT-4o Mini offers the best balance of cost and performance for financial analysis"
    )
    model_name = model_options[selected_model]
    
    # Temperature setting
    temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Lower values = more focused, Higher values = more creative"
    )
    
    # Expertise focus
    st.subheader("🎯Model Expertise")
    expertise_areas = st.multiselect(
        "Select areas of focus:",
        [
            "Stock Analysis", 
            "Crypto & Blockchain", 
            "Portfolio Management",
            "Risk Assessment",
            "Technical Analysis",
            "Fundamental Analysis",
            "Market Trends",
            "Investment Strategies"
        ],
        default=["Stock Analysis", "Crypto & Blockchain", "Portfolio Management"]
    )
    
    # Clear history action
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.memory.clear()
        st.success("Chat history cleared!")
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats
    st.markdown("---")
    st.subheader("📈 Session Stats")
    st.metric("Messages Exchanged", len(st.session_state.messages))
    st.metric("Model Used", selected_model.split(" (")[0])

# Enhanced system prompt based on user preferences
def create_system_prompt(expertise_areas):
    base_prompt = """You are an expert fund manager and financial analyst with deep expertise in investment strategies, market analysis, and financial instruments. You have years of experience in both traditional and modern financial markets."""
    
    if expertise_areas:
        expertise_text = ", ".join(expertise_areas).lower()
        base_prompt += f"\n\nYour current focus areas include: {expertise_text}. Provide detailed, actionable insights in these areas."
    
    base_prompt += """
    
    Guidelines for responses:
    - Provide data-driven insights when possible
    - Include risk considerations for investment advice
    - Use clear, professional language
    - Give practical, actionable recommendations
    - Consider both short-term and long-term perspectives
    - Always remind users that this is not personalized financial advice
    
    Format your responses clearly with bullet points or sections when appropriate."""
    
    return base_prompt

# Enhanced chat function with memory
@st.cache_data(show_spinner=False)
def get_ai_response(message, expertise_areas, model_name, temperature, conversation_history_str):
    try:
        llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=1500
        )
        
        messages = [SystemMessage(content=create_system_prompt(expertise_areas))]
        
        # Add conversation history (last 3 messages to manage token limit)
        for role, content in conversation_history_str[-3:]:
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(AIMessage(content=content))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        response = llm.invoke(messages)
        return response.content, None
        
    except Exception as e:
        return None, str(e)


# Display chat history
chat_container = st.container()

with chat_container:
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            with st.chat_message("user", avatar="🧑‍💼"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="💰"):
                st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about finance, investing, or trading..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="🧑‍💼"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant", avatar="💰"):
        with st.spinner("Analyzing your question..."):
            # Convert messages to LangChain format for memory
            conversation_history_str = []
            for msg in st.session_state.messages[:-1]:  # Exclude the current prompt
                conversation_history_str.append((msg["role"], msg["content"]))
            
            response, error = get_ai_response(
                prompt, 
                expertise_areas, 
                model_name, 
                temperature,
                conversation_history_str
            )
            
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Add to memory
                st.session_state.memory.save_context(
                    {"input": prompt},
                    {"output": response}
                )
            else:
                st.error(f"❌ Error generating response: {error}")
                st.info("💡 Tips: Check your API key in .env file and ensure you have sufficient OpenAI credits.")

# Sample questions section (UX improvement)
if len(st.session_state.messages) == 0:
    st.markdown("### 🤔 Not sure what to ask? Try those question: ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 Investment Analysis:**
        - "What are the key factors to consider when evaluating a tech stock?"
        - "How do I build a diversified crypto portfolio?"
        - "What's the difference between growth and value investing?"
        """)
        
    with col2:
        st.markdown("""
        **⚡ Market Insights:**
        - "What are the current trends in the cryptocurrency market?"
        - "How do interest rates affect different asset classes?"
        - "What should I know about ESG investing?"
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    💡 <strong>Disclaimer:</strong> This AI assistant provides educational information only. 
    Always consult with qualified financial advisors for personalized investment advice.
    <br><br>
</div>
""", unsafe_allow_html=True)