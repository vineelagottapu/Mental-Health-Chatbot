import streamlit as st
import time
import json
from datetime import datetime
from utils.content_filter import ContentFilter
from utils.recommendations import RecommendationEngine
from utils.ai_client import OllamaClient
from utils.auth import AuthManager, show_auth_page, is_logged_in, get_current_user

# Page configuration
st.set_page_config(
    page_title="MindfulChat - Your AI Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Check authentication first
if not is_logged_in():
    show_auth_page()
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "ai_client" not in st.session_state:
    st.session_state.ai_client = OllamaClient()

if "content_filter" not in st.session_state:
    st.session_state.content_filter = ContentFilter()

if "recommendation_engine" not in st.session_state:
    st.session_state.recommendation_engine = RecommendationEngine()

if "auth_manager" not in st.session_state:
    st.session_state.auth_manager = AuthManager()

def add_message(role, content):
    """Add a message to the chat history"""
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": timestamp
    })
    
    # Auto-save chat history
    current_user = get_current_user()
    if current_user:
        st.session_state.auth_manager.save_chat_history(current_user, st.session_state.messages)

def display_chat_history():
    """Display the chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            st.caption(f"⏰ {message['timestamp']}")

def get_supportive_response(user_message):
    """Generate a supportive AI response"""
    try:
        # Filter sensitive content
        filtered_message = st.session_state.content_filter.filter_content(user_message)
        
        # Generate AI response
        ai_response = st.session_state.ai_client.get_response(filtered_message)
        
        # Check if user is asking for recommendations and add them naturally
        recommendation = st.session_state.recommendation_engine.get_recommendation(filtered_message)
        if recommendation:
            # Add recommendations in a more conversational way
            full_response = f"{ai_response}\n\n{recommendation}"
        else:
            full_response = ai_response
            
        return full_response
        
    except Exception as e:
        return "I'm here for you! Tell me more about what's on your mind."

def main():
    # Header
    current_user = get_current_user()
    st.title("🧠 MindfulChat")
    st.markdown("### Your AI Mental Health Companion")
    st.markdown(f"*Welcome back, {current_user}! A safe space to share your feelings and get support*")
    
    # Crisis resources sidebar
    with st.sidebar:
        st.markdown(f"### 👤 Logged in as: {current_user}")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Save chat history before logout
            st.session_state.auth_manager.save_chat_history(current_user, st.session_state.messages)
            st.session_state.auth_manager.logout_user()
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("### 🆘 Crisis Resources")
        st.markdown("""
        **If you're in crisis, please reach out immediately:**
        - **Emergency**: 911
        - **Crisis Text Line**: Text HOME to 741741
        - **National Suicide Prevention Lifeline**: 988
        - **Crisis Chat**: suicidepreventionlifeline.org
        """)
        
        st.markdown("### ℹ️ About MindfulChat")
        st.markdown("""
        MindfulChat is an AI companion designed to provide emotional support 
        and helpful recommendations. While I'm here to listen and support you, 
        I'm not a replacement for professional mental health care.
        """)
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.auth_manager.save_chat_history(current_user, [])
            st.rerun()
    
    # Welcome message
    if not st.session_state.messages:
        welcome_msg = """
        Hello! I'm MindfulChat, your AI mental health companion. 😊
        
        I'm here to:
        - Listen to your thoughts and feelings 💭
        - Provide emotional support and encouragement 💪
        - Recommend movies, songs, books, and activities 🎬🎵📚
        - Help you process stress, happiness, sadness, or any emotion you're experiencing
        
        Feel free to share whatever is on your mind. This is a safe space! 🌟
        """
        add_message("assistant", welcome_msg)
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if prompt := st.chat_input("Share what's on your mind..."):
        # Add user message
        add_message("user", prompt)
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"⏰ {datetime.now().strftime('%H:%M')}")
        
        # Generate and display AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_supportive_response(prompt)
            st.markdown(response)
            st.caption(f"⏰ {datetime.now().strftime('%H:%M')}")
            
            # Add AI response to history
            add_message("assistant", response)

if __name__ == "__main__":
    main()
