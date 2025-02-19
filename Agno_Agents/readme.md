# Agno Agents Streamlit App

A Streamlit interface for interacting with specialized AI agents powered by Ollama and Agno.

## Overview

This application provides a chat interface to communicate with three specialized AI agents:
1. **Web Agent** - Searches the web for information
2. **Finance Agent** - Retrieves financial data and stock information
3. **YouTube Agent** - Analyzes YouTube videos and answers questions about them

## Features

- Clean chat interface with message history
- Agent switching with preserved context per agent
- Web search capabilities
- Financial data analysis
- YouTube video content analysis

## Prerequisites

- Python 3.8+
- Ollama installed locally (https://ollama.ai)
- Required Ollama models:
  - llama3.2 (for Web Agent)
  - llama3.2:3b (for Finance Agent)
  - llama3.2:latest (for YouTube Agent)

## Installation

1. Clone this repository or download the source files

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install ollama duckduckgo-search yfinance pypdf sqlalchemy streamlit youtube-transcript-api agno
```

4. Make sure Ollama is running with the required models:
```bash
ollama pull llama3.2
ollama pull llama3.2:3b
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run streamlit_agent.py
```

2. The application will open in your web browser

3. Select an agent from the dropdown in the sidebar

4. Type your question in the chat input field and press Enter

5. View the agent's response and continue the conversation

## Agent Capabilities

### Web Agent
- Search the web for current information
- Provide detailed answers with sources
- Useful for general knowledge questions

### Finance Agent
- Retrieve stock prices
- Get analyst recommendations
- Access company information
- Fetch company news
- Display data in table format

### YouTube Agent
- Extract information from YouTube videos
- Analyze video content
- Answer questions about video topics
- Provides timestamps for relevant information

## File Structure

```
.
├── README.md
├── streamlit_agent.py  # Main application file
└── tmp/                # Storage directory for agent databases
    └── local_agents.db # SQLite database for agent storage
```

## Troubleshooting

- **Ollama Connection Issues**: Ensure Ollama is running locally with the required models
- **Missing Dependencies**: Verify all required packages are installed
- **Storage Errors**: Check that the `tmp` directory exists and is writable

## License

[MIT License](LICENSE)

## Acknowledgments

- Built with [Agno](https://github.com/agno-ai/agno) framework
- Uses [Ollama](https://ollama.ai) for local AI model inference
- Powered by [Streamlit](https://streamlit.io) for the web interface
