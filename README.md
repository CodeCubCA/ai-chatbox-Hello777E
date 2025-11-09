# Study Buddy - AI-Powered Learning Companion

An interactive AI chatbot application designed to help students learn and understand various subjects through conversational tutoring.

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/a2pucUEo)

## Features

- **Interactive Chat Interface** - Real-time conversation with an AI tutor
- **Streaming Responses** - See answers appear word-by-word as they're generated
- **Persistent Chat History** - Conversations are maintained during your session
- **Clear History** - Start fresh conversations anytime
- **Helpful Tips** - Usage guidance in the sidebar
- **Error Handling** - Graceful error messages and validation

## Technology Stack

- **Python** - Core programming language
- **Streamlit** - Web application framework
- **Google Gemini API** - AI language model provider (Gemini 2.5 Flash)

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/CodeCubCA/ai-chatbox-Hello777E.git
cd ai-chatbox
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Google Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the application:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## How to Use

1. Type your question or topic in the chat input at the bottom
2. Press Enter or click Send
3. Watch as Study Buddy responds in real-time
4. Continue the conversation - the AI remembers context from earlier in the session
5. Use the "Clear Chat History" button in the sidebar to start a new conversation

## Example Questions

- "Can you explain photosynthesis?"
- "Help me understand quadratic equations"
- "What's the difference between mitosis and meiosis?"
- "How do I write a good essay introduction?"

## Project Structure

```
ai-chatbox/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variable template
└── README.md          # This file
```

## Dependencies

- `streamlit>=1.31.0` - Web UI framework
- `google-generativeai>=0.3.0` - Google Gemini API client
- `python-dotenv>=1.0.0` - Environment variable management

## Configuration

The AI is configured with:
- **Model**: Google Gemini 2.5 Flash
- **Temperature**: 0.7 (balanced creativity and accuracy)
- **Max Tokens**: 2048 per response
- **Streaming**: Enabled for real-time responses

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is part of an educational assignment.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini](https://ai.google.dev/)
- Uses Google's Gemini 2.5 Flash model
