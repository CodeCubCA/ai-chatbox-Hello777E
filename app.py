import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="centered"
)

# Initialize Groq client
@st.cache_resource
def init_groq_client():
    """Initialize the Groq API client"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Failed to initialize Groq client: {str(e)}")
        return None

client = init_groq_client()

# Check if client is initialized
if client is None:
    st.error("❌ Please set GROQ_API_KEY in your .env file or Streamlit secrets")
    st.info("💡 Get your API key from: https://console.groq.com/keys")
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a friendly and patient AI study buddy. Your job is to help students understand various subjects, answer questions, and provide learning advice. Explain concepts clearly and encourage students to think actively."
        }
    ]

# Page title
st.title("📚 the best best best studdy buddy")
st.markdown("Hi! I'm your AI learning companion. Ask me anything!")

# Sidebar - Settings and features
with st.sidebar:
    st.header("⚙️ Settings")

    # Clear chat history button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are a friendly and patient AI study buddy. Your job is to help students understand various subjects, answer questions, and provide learning advice. Explain concepts clearly and encourage students to think actively."
            }
        ]
        st.rerun()

    st.divider()

    # Usage tips
    st.header("💡 Tips")
    st.markdown("""
    - 📖 Ask me any study questions
    - 🤔 Need help with concepts or problems
    - 📝 Ask me to summarize topics
    - 💪 Get study method suggestions
    """)

# Display chat history (skip system messages)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Call Groq API with streaming
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=2048,
                stream=True
            )

            # Display response word by word
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            # Display complete response
            message_placeholder.markdown(full_response)

        except Exception as e:
            error_message = f"❌ Error occurred: {str(e)}"
            message_placeholder.error(error_message)
            full_response = error_message

    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
