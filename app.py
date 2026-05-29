import streamlit as st
import google.generativeai as genai

# Set the title of the Streamlit app
st.title("💬 Free AI Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Google Gemini (Free Tier)")

# Sidebar for API Key input
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    st.write("[Get a FREE Gemini API key](https://aistudio.google.com/)")

# Initialize the chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I am powered by Gemini. How can I help you today?"}]

# Loop through and display chat messages from history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Capture user input
if prompt := st.chat_input("Type your message here..."):
    # Stop the app if the user hasn't provided an API key
    if not gemini_api_key:
        st.info("Please add your Gemini API key in the sidebar to continue.")
        st.stop()

    # Configure Gemini API with the user's key
    genai.configure(api_key=gemini_api_key)
    
    # Use the fast and free gemini-1.5-flash model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Convert Streamlit history format to Gemini's expected format
    gemini_history = []
    for msg in st.session_state.messages[:-1]: # exclude the latest prompt
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})
    
    # Start chat session with history and send the new message
    try:
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(prompt)
        msg = response.text
    except Exception as e:
        msg = f"Error: {str(e)}"
    
    # Add assistant response to chat history and display it
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
