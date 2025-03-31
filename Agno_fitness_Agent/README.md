
# AI Health & Fitness Planner

![Fitness Planner Banner](https://raw.githubusercontent.com/username/repo/main/assets/banner.png)

## 🚀 Overview

AI Health & Fitness Planner is a comprehensive tool that leverages local AI models through Ollama to create personalized fitness and nutrition plans. The application combines cutting-edge AI capabilities with practical fitness knowledge to help users achieve their health goals.

Key features include:
- 🏋️‍♂️ Personalized workout routines based on your fitness goals
- 🍎 Custom meal plans with optional intermittent fasting integration
- 🔍 Research tool for evidence-based fitness information
- 🎥 Video resource finder for workout tutorials
- 🎬 YouTube video analyzer for in-depth content insights
- 💬 AI chat assistant for fitness and nutrition questions

## 📋 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Compatible LLM models pulled to your local machine

## 🛠️ Installation

1. Clone this repository:
   ```bash
   https://github.com/Amityadav9/Agno_Tests.git
   cd Agno_fitness_Agent
   ```

2. Install required packages:
   ```bash
   pip install streamlit agno ollama duckduckgo-search youtube-transcript-api
   ```

3. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

4. Pull recommended models:
   ```bash
   ollama pull llama3.2:3b   # Best all-around model
   ollama pull qwen2.5:7b    # Great for tool use
   ollama pull deepseek-r1:7b # Strong reasoning model
   # Additional models as needed
   ```

5. Run the application:
   ```bash
   streamlit run fitness_planner.py
   ```

## 🖥️ Usage

### Plan Generator Tab

1. **Select your model** in the sidebar
2. **Configure intermittent fasting** preferences (if desired)
3. **Enter your profile details**:
   - Age, height, weight
   - Activity level
   - Dietary preferences
   - Fitness goals
   - Health considerations
4. **Generate your personalized plan**
5. Review your detailed fitness and nutrition recommendations

### Expert Chat Tab

Speak directly with the AI about any fitness or nutrition related questions.

### Fitness Research Tab

Research specific fitness topics using the DuckDuckGo search integration.

### Video Resources Tab

Find instructional fitness videos based on:
- Topic
- Difficulty level
- Duration
- Available equipment

### Video Analysis Tab

Get in-depth analysis of specific fitness YouTube videos:
1. Enter a YouTube URL
2. Select analysis options
3. Ask specific questions about the video content
4. View embedded video and detailed analysis results

## 🌟 Key Features

### Intelligent Tool Integration

The application uses specialized AI agents:

- **Smart Fitness Assistant:** Comprehensive health and fitness expert using both DuckDuckGo and YouTube tools
- **YouTube Fitness Analyst:** Specialized in analyzing fitness video content

### Intermittent Fasting Integration

- Customize fasting windows (12-20 hours)
- Set preferred fasting starting time
- Get meal plans tailored to your fasting schedule

### Comprehensive Fitness Planning

- Weekly workout schedules
- Exercise progression plans
- Rest and recovery recommendations
- Form guidance and technique tips

### Interactive Video Features

- Find relevant tutorial videos
- Analyze video content for technique insights
- Get timestamp references to specific parts of videos
- Download analysis summaries for future reference

## 📱 Screenshots

![Plan Generator](https://raw.githubusercontent.com/username/repo/main/assets/screenshot-plan.png)

![Video Analysis](https://raw.githubusercontent.com/username/repo/main/assets/screenshot-video.png)

## 📚 How It Works

The application leverages the Agno framework to create specialized AI agents that can use various tools. The agents are powered by your local Ollama models, ensuring privacy and performance.

Key components:
- **Streamlit:** Provides the frontend interface
- **Agno:** Framework for creating AI agents with tool use capabilities
- **Ollama:** Local LLM model runner
- **DuckDuckGo Tools:** Web search integration
- **YouTube Tools:** Video search and analysis capabilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👏 Acknowledgments

- [Agno](https://github.com/agno-ai/agno) for the agent framework
- [Ollama](https://github.com/ollama/ollama) for local model hosting
- [Streamlit](https://github.com/streamlit/streamlit) for the web interface
- All open-source LLM model creators
