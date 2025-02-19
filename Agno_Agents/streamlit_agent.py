"""Streamlit interface for Agno agents
Run `pip install ollama duckduckgo-search yfinance pypdf sqlalchemy streamlit youtube-transcript-api agno` to install dependencies.
"""

import os
import streamlit as st
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.youtube import YouTubeTools

# Configuration
local_agent_storage_file: str = "tmp/local_agents.db"
common_instructions = [
    "If the user asks about you or your skills, tell them your name and role.",
]

# Create tmp directory if it doesn't exist
os.makedirs("tmp", exist_ok=True)


# Initialize agents
@st.cache_resource
def initialize_agents():
    web_agent = Agent(
        name="Web Agent",
        role="Search the web for information",
        agent_id="web-agent",
        model=Ollama(id="llama3.2"),
        tools=[DuckDuckGoTools()],
        instructions=["Always include sources."] + common_instructions,
        storage=SqliteAgentStorage(
            table_name="web_agent", db_file=local_agent_storage_file
        ),
        show_tool_calls=True,
        add_history_to_messages=True,
        num_history_responses=2,
        add_name_to_instructions=True,
        add_datetime_to_instructions=True,
        markdown=True,
    )

    finance_agent = Agent(
        name="Finance Agent",
        role="Get financial data",
        agent_id="finance-agent",
        model=Ollama(id="llama3.2:3b"),
        tools=[
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True,
            )
        ],
        description="You are an investment analyst that researches stocks and helps users make informed decisions.",
        instructions=["Always use tables to display data"] + common_instructions,
        storage=SqliteAgentStorage(
            table_name="finance_agent", db_file=local_agent_storage_file
        ),
        add_history_to_messages=True,
        num_history_responses=5,
        add_name_to_instructions=True,
        add_datetime_to_instructions=True,
        markdown=True,
    )

    youtube_agent = Agent(
        name="YouTube Agent",
        role="Understand YouTube videos and answer questions",
        agent_id="youtube-agent",
        model=Ollama(id="llama3.2:latest"),
        tools=[YouTubeTools()],
        description="You are a YouTube agent that has the special skill of understanding YouTube videos and answering questions about them.",
        instructions=[
            "Using a video URL, get the video data using the `get_youtube_video_data` tool and captions using the `get_youtube_video_data` tool.",
            "Using the data and captions, answer the user's question in an engaging and thoughtful manner. Focus on the most important details.",
            "If you cannot find the answer in the video, say so and ask the user to provide more details.",
            "Keep your answers concise and engaging.",
        ]
        + common_instructions,
        add_history_to_messages=True,
        num_history_responses=5,
        show_tool_calls=True,
        add_name_to_instructions=True,
        add_datetime_to_instructions=True,
        storage=SqliteAgentStorage(
            table_name="youtube_agent", db_file=local_agent_storage_file
        ),
        markdown=True,
    )

    return {
        "Web Agent": web_agent,
        "Finance Agent": finance_agent,
        "YouTube Agent": youtube_agent,
    }


# App title
st.title("AI Agent Assistant")
st.write("Ask questions to specialized AI agents")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Web Agent"

# Initialize agents
agents = initialize_agents()

# Agent selection
selected_agent = st.sidebar.selectbox(
    "Select an agent:",
    options=list(agents.keys()),
    index=list(agents.keys()).index(st.session_state.selected_agent),
)

if selected_agent != st.session_state.selected_agent:
    st.session_state.messages = []
    st.session_state.selected_agent = selected_agent
    st.rerun()

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from selected agent
    with st.chat_message("assistant"):
        with st.spinner(f"{selected_agent} is thinking..."):
            current_agent = agents[selected_agent]

            # Use run method instead of chat
            response = current_agent.run(prompt)

            # Extract content based on response type
            if hasattr(response, "content"):
                response_content = response.content
            else:
                # If response is a string
                response_content = str(response)

            # Display response
            st.markdown(response_content)

            # Add assistant response to history
            st.session_state.messages.append(
                {"role": "assistant", "content": response_content}
            )

# Add information about the agents
st.sidebar.markdown("### Agent Information")
st.sidebar.markdown("**Web Agent:** Searches the web for information")
st.sidebar.markdown("**Finance Agent:** Provides financial data and stock information")
st.sidebar.markdown(
    "**YouTube Agent:** Analyzes YouTube videos and answers questions about them"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### How to use")
st.sidebar.markdown("1. Select an agent from the dropdown")
st.sidebar.markdown("2. Type your question in the chat box")
st.sidebar.markdown("3. Wait for the agent to respond")
st.sidebar.markdown("4. Continue the conversation or switch agents")
