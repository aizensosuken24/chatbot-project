import streamlit as st
from openai import OpenAI

# Set the title of the Streamlit app
st.title("💬 AI Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Sidebar for API Key input
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.write("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

# Initialize the chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Loop through and display chat messages from history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Capture user input
if prompt := st.chat_input("Type your message here..."):
    # Stop the app if the user hasn't provided an API key
    if not openai_api_key:
        st.info("Please add your OpenAI API key in the sidebar to continue.")
        st.stop()

    # Initialize the OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Call the OpenAI API to get the assistant's response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    # Extract the response text
    msg = response.choices[0].message.content
    
    # Add assistant response to chat history and display it
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)