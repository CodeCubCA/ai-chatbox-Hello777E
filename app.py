import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Translation dictionary for multilingual support
TRANSLATIONS = {
    "English": {
        "page_title": "Study Buddy",
        "app_title": "📚 the best best study buddy",
        "app_description": "Hi! I'm your AI learning companion. Ask me anything!",
        "settings_header": "⚙️ Settings",
        "language_label": "🌍 Language",
        "clear_chat_button": "🗑️ Clear Chat History",
        "download_chat_button": "📥 Download Chat",
        "tips_header": "💡 Tips",
        "tip_1": "📖 Ask me any study questions",
        "tip_2": "🤔 Need help with concepts or problems",
        "tip_3": "📝 Ask me to summarize topics",
        "tip_4": "💪 Get study method suggestions",
        "chat_input_placeholder": "Type your question...",
        "error_prefix": "❌ Error occurred:",
        "api_key_error": "❌ Please set GEMINI_API_KEY in your .env file or Streamlit secrets",
        "api_key_info": "💡 Get your API key from: https://aistudio.google.com/app/apikey",
        "chat_history_title": "Study Buddy - Chat History",
        "exported_on": "Exported on:",
        "user_label": "User:",
        "assistant_label": "Assistant:",
        "system_prompt": "You are a friendly and patient AI study buddy. Your job is to help students understand various subjects, answer questions, and provide learning advice. Explain concepts clearly and encourage students to think actively."
    },
    "中文": {
        "page_title": "学习伙伴",
        "app_title": "📚 最好最好的学习伙伴",
        "app_description": "你好！我是你的AI学习助手。有任何问题都可以问我！",
        "settings_header": "⚙️ 设置",
        "language_label": "🌍 语言",
        "clear_chat_button": "🗑️ 清空聊天记录",
        "download_chat_button": "📥 下载聊天记录",
        "tips_header": "💡 使用提示",
        "tip_1": "📖 向我提问任何学习问题",
        "tip_2": "🤔 需要帮助理解概念或解决问题",
        "tip_3": "📝 让我总结知识点",
        "tip_4": "💪 获取学习方法建议",
        "chat_input_placeholder": "输入你的问题...",
        "error_prefix": "❌ 发生错误：",
        "api_key_error": "❌ 请在.env文件或Streamlit密钥中设置GEMINI_API_KEY",
        "api_key_info": "💡 在此获取API密钥：https://aistudio.google.com/app/apikey",
        "chat_history_title": "学习伙伴 - 聊天记录",
        "exported_on": "导出时间：",
        "user_label": "用户：",
        "assistant_label": "助手：",
        "system_prompt": "你是一个友好且耐心的AI学习伙伴。你的工作是帮助学生理解各种科目，回答问题，并提供学习建议。请清晰地解释概念，鼓励学生积极思考。请用中文回答所有问题。"
    }
}

# Configure the page
st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="centered"
)

# Initialize language preference in session state
if "language" not in st.session_state:
    st.session_state.language = "English"

# Get current translations
def get_text(key):
    """Get translated text based on current language"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

# Initialize Google Gemini API
def init_gemini_api():
    """Initialize the Google Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize Gemini API: {str(e)}")
        return False

# Initialize API
api_initialized = init_gemini_api()

# Check if API is initialized
if not api_initialized:
    st.error(get_text("api_key_error"))
    st.info(get_text("api_key_info"))
    st.stop()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": get_text("system_prompt")
        }
    ]

# Function to update system prompt when language changes
def update_system_prompt():
    """Update the system prompt based on current language"""
    if st.session_state.messages and st.session_state.messages[0]["role"] == "system":
        st.session_state.messages[0]["content"] = get_text("system_prompt")

# Function to generate chat history text for download
def generate_chat_history():
    """Generate formatted chat history text"""
    chat_text = get_text("chat_history_title") + "\n"
    chat_text += "=" * 50 + "\n"
    chat_text += f"{get_text('exported_on')} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    chat_text += "=" * 50 + "\n\n"

    # Skip system messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            if message["role"] == "user":
                chat_text += f"{get_text('user_label')} {message['content']}\n\n"
            elif message["role"] == "assistant":
                chat_text += f"{get_text('assistant_label')} {message['content']}\n\n"

    return chat_text

# Page title
st.title(get_text("app_title"))
st.markdown(get_text("app_description"))

# Sidebar - Settings and features
with st.sidebar:
    st.header(get_text("settings_header"))

    # Language selector
    selected_language = st.selectbox(
        get_text("language_label"),
        options=list(TRANSLATIONS.keys()),
        index=list(TRANSLATIONS.keys()).index(st.session_state.language),
        key="language_selector"
    )

    # Update language if changed
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        update_system_prompt()
        st.rerun()

    st.divider()

    # Clear chat history button
    if st.button(get_text("clear_chat_button"), use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": get_text("system_prompt")
            }
        ]
        st.rerun()

    # Download chat history button
    # Check if there are any messages to export (excluding system message)
    has_chat_history = len([msg for msg in st.session_state.messages if msg["role"] != "system"]) > 0

    if has_chat_history:
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.txt"

        # Generate chat history content
        chat_content = generate_chat_history()

        # Download button
        st.download_button(
            label=get_text("download_chat_button"),
            data=chat_content,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.button(get_text("download_chat_button"), disabled=True, use_container_width=True)

    st.divider()

    # Usage tips
    st.header(get_text("tips_header"))
    st.markdown(f"""
    - {get_text('tip_1')}
    - {get_text('tip_2')}
    - {get_text('tip_3')}
    - {get_text('tip_4')}
    """)

# Display chat history (skip system messages)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
if prompt := st.chat_input(get_text("chat_input_placeholder")):
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
            # Prepare chat history for Gemini (convert from session state format)
            chat_history = []
            system_instruction = None

            for msg in st.session_state.messages:
                if msg["role"] == "system":
                    system_instruction = msg["content"]
                elif msg["role"] == "user":
                    chat_history.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "assistant":
                    chat_history.append({"role": "model", "parts": [msg["content"]]})

            # Create model - gemini-pro doesn't support system_instruction, so we'll prepend it to the first message
            model = genai.GenerativeModel('gemini-pro')

            # If this is the first message and we have a system instruction, prepend it to the prompt
            enhanced_prompt = prompt
            if system_instruction and len(chat_history) <= 1:
                enhanced_prompt = f"{system_instruction}\n\nUser question: {prompt}"

            # Start chat with history (excluding the last user message which we'll send separately)
            chat = model.start_chat(history=chat_history[:-1] if len(chat_history) > 1 else [])

            # Send the current prompt with streaming
            response = chat.send_message(
                enhanced_prompt,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                )
            )

            # Display response word by word
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")

            # Display complete response
            message_placeholder.markdown(full_response)

        except Exception as e:
            error_message = f"{get_text('error_prefix')} {str(e)}"
            message_placeholder.error(error_message)
            full_response = error_message

    # Add AI response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
