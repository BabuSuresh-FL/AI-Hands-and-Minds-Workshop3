import streamlit as st
import requests
import json

# Configure the page
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Hardcoded API Gateway URL - CHANGE THIS TO YOUR URL
# API_URL = "https://3ab2nker2e.execute-api.us-east-1.amazonaws.com/dev/chatbot"
API_URL = "<....Paste your URL here....>"

# Custom CSS for chat-like interface
st.markdown("""
<style>
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .user-message {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        color: black;
        margin: 1rem 0;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        color: black;
        margin: 1rem 0;
        border-left: 4px solid #4caf50;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 1rem;
    }
    .stButton > button {
        width: 100%;
        background: #4caf50;
        color: white;
        border: none;
        padding: 1rem;
        font-weight: bold;
        border-radius: 8px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Assistant")
st.markdown("Ask me anything!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...", placeholder="What would you like to know?")
    submitted = st.form_submit_button("💬 Send")

if submitted and user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show user message immediately
    st.markdown(f'<div class="user-message"><strong>You:</strong> {user_input}</div>', unsafe_allow_html=True)
    
    # Get response from API
    with st.spinner("Thinking..."):
        try:
            # Prepare the request payload
            payload = {
                "question": user_input,
                "message": user_input,
                "query": user_input
            }
            
            # Make API call
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                try:
                    # Try to get response text from various possible fields
                    response_data = response.json()
                    
                    # Common response field names
                    answer = (response_data.get("answer") or 
                             response_data.get("response") or 
                             response_data.get("message") or 
                             response_data.get("result") or 
                             str(response_data))
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # Show assistant response
                    st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong> {answer}</div>', unsafe_allow_html=True)
                    
                except json.JSONDecodeError:
                    error_msg = "I received a response but couldn't understand it."
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong> {error_msg}</div>', unsafe_allow_html=True)
            else:
                error_msg = f"Sorry, I'm having trouble right now. (Error {response.status_code})"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong> {error_msg}</div>', unsafe_allow_html=True)
                
        except requests.exceptions.RequestException:
            error_msg = "Sorry, I can't connect to my brain right now. Please try again later."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong> {error_msg}</div>', unsafe_allow_html=True)
    
    # Rerun to update the display
    st.rerun()

# Clear chat button (optional)
if st.session_state.messages:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
