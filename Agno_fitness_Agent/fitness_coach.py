import os
import streamlit as st
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.youtube import YouTubeTools

# Create tmp directory if it doesn't exist
os.makedirs("tmp", exist_ok=True)

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fffaf0;
        border: 1px solid #fbd38d;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #E0E2E6;
        border-radius: 5px;
        padding: 10px 16px;
        font-weight: 600;
        color: #000000;
        border: 1px solid #cccccc;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00008B !important;
        color: white !important;
        border: 1px solid #0000CD;
    }
    .youtube-resource {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #f9f9f9;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Initialize smart agent with all tools and a dedicated YouTube agent
@st.cache_resource
def initialize_agents(model_name):
    smart_agent = Agent(
        name="Smart Fitness Assistant",
        role="Comprehensive health and fitness expert",
        model=Ollama(id=model_name),
        tools=[
            DuckDuckGoTools(search=True, news=True),
            YouTubeTools(),
        ],
        instructions=[
            "You are a comprehensive health and fitness expert specializing in nutrition, exercise, and wellness optimization.",
            "Always provide evidence-based recommendations and include sources when possible.",
            "Intermittent fasting (12-16 hours) should be incorporated into dietary recommendations when appropriate.",
            "Use the DuckDuckGo search tool for any fitness or nutrition information you need to verify.",
            "Use the YouTube tool to find and recommend relevant fitness videos when appropriate.",
            "Present information in a clear, structured format with tables when helpful.",
            "Only respond to questions related to fitness, nutrition, and health. Politely decline other topics.",
            "Always consider the user's specific profile and goals in your recommendations.",
        ],
        show_tool_calls=True,
        markdown=True,
    )

    # Dedicated YouTube analysis agent
    youtube_agent = Agent(
        name="YouTube Fitness Analyst",
        role="Analyze YouTube videos and answer questions about them",
        model=Ollama(
            id="llama3.2:3b"
            if "llama" not in model_name and "qwen" not in model_name
            else model_name
        ),
        tools=[YouTubeTools()],
        instructions=[
            "You are specialized in analyzing fitness and workout YouTube videos.",
            "Using a video URL, get the video data and captions using the YouTube tools.",
            "Extract key information such as workout techniques, nutritional advice, and training tips.",
            "Provide timestamp references when discussing specific parts of videos.",
            "Focus on practical, actionable takeaways from fitness videos.",
            "If you cannot find the answer in the video, say so clearly.",
            "Keep your answers concise, informative, and engaging.",
        ],
        show_tool_calls=True,
        markdown=True,
    )

    return smart_agent, youtube_agent


def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 🎯 Why this plan works")
            st.info(
                plan_content.get("why_this_plan_works", "Information not available")
            )
            st.markdown("### 🍽️ Meal Plan")
            st.write(plan_content.get("meal_plan", "Plan not available"))

            # Intermittent Fasting Schedule
            st.markdown("### ⏱️ Intermittent Fasting Schedule")
            st.write(
                plan_content.get("fasting_schedule", "Fasting schedule not available")
            )

        with col2:
            st.markdown("### ⚠️ Important Considerations")
            considerations = plan_content.get("important_considerations", "").split(
                "\n"
            )
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)


def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 🎯 Goals")
            st.success(plan_content.get("goals", "Goals not specified"))
            st.markdown("### 🏋️‍♂️ Exercise Routine")
            st.write(plan_content.get("routine", "Routine not available"))

        with col2:
            st.markdown("### 💡 Pro Tips")
            tips = plan_content.get("tips", "").split("\n")
            for tip in tips:
                if tip.strip():
                    st.info(tip)

            # Recommended Videos
            if "video_resources" in plan_content and plan_content["video_resources"]:
                st.markdown("### 🎥 Recommended Videos")
                for video in plan_content["video_resources"]:
                    st.markdown(
                        f"""
                    <div style="margin-bottom: 15px; padding: 12px; border-radius: 8px; border: 1px solid #4169E1; background-color: #F0F8FF;">
                        <strong style="font-size: 16px; color: #00008B;">{video["title"]}</strong><br>
                        <a href="{video["url"]}" target="_blank" style="word-break: break-all;">{video["url"]}</a><br>
                        <div style="margin-top: 8px; font-size: 14px; color: #444;">
                            {video["description"][:150]}{"..." if len(video["description"]) > 150 else ""}
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )


def main():
    if "dietary_plan" not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False
        st.session_state.chat_history = []
        st.session_state.active_tab = "Plan Generator"
        st.session_state.video_analyses = []

    st.title("🏋️‍♂️ AI Health & Fitness Planner")
    st.markdown(
        """
        <div style='background-color: #00008B; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; color: white;'>
        Get personalized dietary and fitness plans tailored to your goals and preferences.
        Our AI-powered system considers your unique profile to create the perfect plan for you, including intermittent fasting options.
        </div>
    """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs(
        [
            "🎯 Plan Generator",
            "💬 Expert Chat",
            "🔍 Fitness Research",
            "🎥 Video Resources",
            "🎬 Video Analysis",
        ]
    )

    with st.sidebar:
        st.header("🤖 Model Configuration")

        # Define list of recommended models
        ollama_models = [
            "llama3.2:3b",
            "qwen2.5:7b",
            "deepseek-r1:7b",
            "phi4:latest",
            "gemma3:12b",
        ]

        # Custom model input option
        custom_model = st.checkbox("Use a custom Ollama model")

        if custom_model:
            selected_model = st.text_input(
                "Enter Ollama model name",
                help="Enter the name of any model you have pulled in Ollama",
            )
        else:
            selected_model = st.selectbox(
                "Select Ollama Model",
                options=ollama_models,
                help="Choose from recommended models or pull your preferred model with 'ollama pull model_name'",
            )

        # Information about models
        with st.expander("🔍 Model Information"):
            st.markdown("""
            **Recommended models:**
            * `llama3.2:3b` - Good for most basic use-cases
            * `qwen2.5:7b` - Performs well with tool use
            * `deepseek-r1:7b` - Strong reasoning capabilities
            * `phi4:latest` - Powerful while being small in size
            * `gemma3:12b` - Good balance of performance and efficiency
            
            Make sure you have pulled your chosen model with:
            ```bash
            ollama pull model_name
            ```
            """)

        if not selected_model:
            st.warning("⚠️ Please select or enter an Ollama model to proceed")
            return

        st.success(f"Using Ollama model: {selected_model}")

        # Intermittent fasting preferences
        st.header("⏱️ Fasting Preferences")
        fasting_enabled = st.checkbox("Include Intermittent Fasting", value=True)

        if fasting_enabled:
            fasting_hours = st.slider(
                "Fasting Window (hours)", min_value=12, max_value=20, value=16, step=1
            )
            fasting_start = st.selectbox(
                "Preferred Fasting Start Time",
                options=[
                    "After dinner (evening)",
                    "After early dinner (afternoon)",
                    "After breakfast (morning)",
                ],
                index=0,
            )
        else:
            fasting_hours = 0
            fasting_start = "None"

    # Initialize the smart agent
    if selected_model:
        try:
            smart_agent, youtube_agent = initialize_agents(selected_model)
        except Exception as e:
            st.error(f"❌ Error initializing Ollama model: {e}")
            st.info(
                "Make sure Ollama is running and the model is pulled. Run 'ollama serve' to start the service."
            )
            return

    # TAB 1: Plan Generator
    with tabs[0]:
        st.header("👤 Your Profile")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age", min_value=10, max_value=100, step=1, help="Enter your age"
            )
            height = st.number_input(
                "Height (cm)", min_value=100.0, max_value=250.0, step=0.1
            )
            activity_level = st.selectbox(
                "Activity Level",
                options=[
                    "Sedentary",
                    "Lightly Active",
                    "Moderately Active",
                    "Very Active",
                    "Extremely Active",
                ],
                help="Choose your typical activity level",
            )
            dietary_preferences = st.selectbox(
                "Dietary Preferences",
                options=[
                    "No Restrictions",
                    "Vegetarian",
                    "Vegan",
                    "Keto",
                    "Gluten Free",
                    "Low Carb",
                    "Dairy Free",
                ],
                help="Select your dietary preference",
            )

        with col2:
            weight = st.number_input(
                "Weight (kg)", min_value=20.0, max_value=300.0, step=0.1
            )
            sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
            fitness_goals = st.selectbox(
                "Fitness Goals",
                options=[
                    "Lose Weight",
                    "Gain Muscle",
                    "Endurance",
                    "Stay Fit",
                    "Strength Training",
                    "Athletic Performance",
                    "Body Recomposition",
                ],
                help="What do you want to achieve?",
            )
            health_conditions = st.multiselect(
                "Health Considerations",
                options=[
                    "None",
                    "Diabetes",
                    "Hypertension",
                    "Heart Disease",
                    "Joint Pain",
                    "Back Pain",
                    "Limited Mobility",
                    "Other",
                ],
                default=["None"],
                help="Select any health considerations",
            )

        if st.button("🎯 Generate My Personalized Plan", use_container_width=True):
            with st.spinner(
                f"Creating your perfect health and fitness routine using {selected_model}..."
            ):
                try:
                    # Construct user profile
                    user_profile = f"""
                    Age: {age}
                    Weight: {weight}kg
                    Height: {height}cm
                    Sex: {sex}
                    Activity Level: {activity_level}
                    Dietary Preferences: {dietary_preferences}
                    Fitness Goals: {fitness_goals}
                    Health Considerations: {", ".join(health_conditions)}
                    Intermittent Fasting: {"Yes" if fasting_enabled else "No"}
                    Fasting Hours: {fasting_hours if fasting_enabled else "N/A"}
                    Fasting Start: {fasting_start if fasting_enabled else "N/A"}
                    """

                    # Generate dietary plan using smart agent
                    dietary_prompt = f"""
                    Create a comprehensive personalized dietary plan based on this user profile:
                    {user_profile}
                    
                    Return a detailed meal plan that includes specific foods, portions, and timing.
                    Include breakfast, lunch, dinner, and snacks.
                    
                    {"Incorporate intermittent fasting with a " + str(fasting_hours) + "-hour fasting window starting " + fasting_start + "." if fasting_enabled else "Do not include intermittent fasting in the plan."}
                    
                    Explain why this plan works well for the user's specific goals and profile.
                    """

                    dietary_plan_response = smart_agent.run(dietary_prompt)

                    # Generate fitness plan using smart agent
                    fitness_prompt = f"""
                    Create a comprehensive personalized fitness plan based on this user profile:
                    {user_profile}
                    
                    Include:
                    1. A weekly exercise schedule with specific workouts
                    2. Detailed descriptions of key exercises
                    3. Progression plan for 4-8 weeks
                    4. Rest and recovery recommendations
                    
                    Suggest YouTube videos that would be helpful for demonstrating proper form or specific routines.
                    Use the YouTube tool to find 2-3 relevant videos related to the user's specific fitness goals.
                    """

                    fitness_plan_response = smart_agent.run(fitness_prompt)

                    # Format dietary plan
                    dietary_plan = {
                        "why_this_plan_works": "Personalized nutrition tailored to your goals, preferences, and lifestyle",
                        "meal_plan": dietary_plan_response.content,
                        "fasting_schedule": f"{fasting_hours}-hour fasting window starting {fasting_start}"
                        if fasting_enabled
                        else "No intermittent fasting included",
                        "important_considerations": """
                        - Hydration: Drink plenty of water throughout the day, especially during fasting periods
                        - Electrolytes: Monitor sodium, potassium, and magnesium levels
                        - Fiber: Ensure adequate intake through vegetables and fruits
                        - Listen to your body: Adjust portion sizes and fasting schedule as needed
                        - Consistency: Follow the plan regularly to see results
                        """,
                    }

                    # Get video resources using YouTube tool
                    try:
                        # Parse the response to extract video recommendations
                        # This is a more robust approach to extract real video links and data
                        try:
                            # First try to find videos directly related to the user's fitness goals
                            search_term = f"best {fitness_goals.lower()} workout for {age} year old {sex.lower()}"
                            video_tool_response = smart_agent.run(
                                f"Use the YouTube tool to find 3 high-quality instructional videos about: {search_term}. Return just the video data in a clear format with titles, URLs and brief descriptions."
                            )

                            # Backup search if the first one doesn't yield good results
                            if "youtube.com" not in video_tool_response.content:
                                backup_search = (
                                    f"fitness training {fitness_goals.lower()} tutorial"
                                )
                                video_tool_response = smart_agent.run(
                                    f"Use the YouTube tool to search for '{backup_search}' and return 3 video recommendations with their URLs and descriptions."
                                )

                            # Extract URLs from the response
                            import re

                            urls = re.findall(
                                r"https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+",
                                video_tool_response.content,
                            )
                            titles = re.findall(
                                r"\*\*(.*?)\*\*|Title: (.*?)[\n\r]",
                                video_tool_response.content,
                            )

                            # Create video resources
                            video_resources = []
                            for i, url in enumerate(urls[:3]):  # Limit to 3 videos
                                title = ""
                                if i < len(titles):
                                    # Extract title from either group 1 or group 2 of the regex match
                                    title_match = titles[i]
                                    title = (
                                        title_match[0]
                                        if title_match[0]
                                        else title_match[1]
                                        if len(title_match) > 1
                                        else f"Fitness Video {i + 1}"
                                    )

                                # Extract description near the URL
                                description_search = video_tool_response.content[
                                    max(
                                        0, video_tool_response.content.find(url) - 100
                                    ) : min(
                                        len(video_tool_response.content),
                                        video_tool_response.content.find(url) + 200,
                                    )
                                ]
                                description_match = re.search(
                                    r"Description: (.*?)[\n\r]|description: (.*?)[\n\r]",
                                    description_search,
                                )
                                description = (
                                    description_match.group(1)
                                    if description_match
                                    else f"Instructional video for your {fitness_goals.lower()} program"
                                )

                                video_resources.append(
                                    {
                                        "title": title,
                                        "url": url,
                                        "description": description,
                                    }
                                )

                            # If we couldn't extract enough videos, add some defaults
                            while len(video_resources) < 2:
                                video_resources.append(
                                    {
                                        "title": f"{fitness_goals} Training Guide",
                                        "url": f"https://www.youtube.com/results?search_query={fitness_goals.replace(' ', '+')}+training",
                                        "description": f"Search results for {fitness_goals} training programs",
                                    }
                                )

                        except Exception as video_err:
                            st.warning(
                                f"Could not fetch specific videos. Using general recommendations instead."
                            )
                            # Fallback video resources
                            video_resources = [
                                {
                                    "title": f"{fitness_goals} Fundamentals",
                                    "url": f"https://www.youtube.com/results?search_query={fitness_goals.replace(' ', '+')}+workout",
                                    "description": "Basic training principles and demonstrations",
                                },
                                {
                                    "title": "Form and Technique Guide",
                                    "url": f"https://www.youtube.com/results?search_query=proper+form+{fitness_goals.replace(' ', '+')}",
                                    "description": "Proper exercise form to prevent injury and maximize results",
                                },
                            ]
                    except:
                        video_resources = []

                    # Format fitness plan
                    fitness_plan = {
                        "goals": f"Achieve {fitness_goals} while considering your {activity_level} lifestyle",
                        "routine": fitness_plan_response.content,
                        "video_resources": video_resources,
                        "tips": """
                        - Track your progress regularly with measurements and photos
                        - Allow proper rest between workouts to optimize recovery
                        - Focus on proper form rather than lifting heavier weights
                        - Stay consistent with your routine - consistency beats perfection
                        - Adapt your workout intensity based on how you feel
                        """,
                    }

                    st.session_state.dietary_plan = dietary_plan
                    st.session_state.fitness_plan = fitness_plan
                    st.session_state.plans_generated = True
                    st.session_state.qa_pairs = []

                    display_dietary_plan(dietary_plan)
                    display_fitness_plan(fitness_plan)

                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
                    st.info(
                        "If the model is taking too long to respond, try a different model or check if Ollama is running properly."
                    )

        if st.session_state.plans_generated:
            st.header("❓ Questions about your plan?")
            question_input = st.text_input(
                "What would you like to know?", key="plan_question"
            )

            if st.button("Get Answer", key="plan_answer_btn"):
                if question_input:
                    with st.spinner("Finding the best answer for you..."):
                        dietary_plan = st.session_state.dietary_plan
                        fitness_plan = st.session_state.fitness_plan

                        context = f"Dietary Plan: {dietary_plan.get('meal_plan', '')}\n\nFitness Plan: {fitness_plan.get('routine', '')}"
                        full_context = f"{context}\nUser Question: {question_input}"

                        try:
                            run_response = smart_agent.run(full_context)

                            if hasattr(run_response, "content"):
                                answer = run_response.content
                            else:
                                answer = "Sorry, I couldn't generate a response at this time."

                            st.session_state.qa_pairs.append((question_input, answer))
                        except Exception as e:
                            st.error(
                                f"❌ An error occurred while getting the answer: {e}"
                            )

            if st.session_state.qa_pairs:
                st.header("💬 Q&A History")
                for question, answer in st.session_state.qa_pairs:
                    st.markdown(f"**Q:** {question}")
                    st.markdown(f"**A:** {answer}")

    # TAB 2: Expert Chat
    with tabs[1]:
        st.header("💬 Chat with Fitness Expert")
        st.markdown(
            "Ask any questions about health, fitness, nutrition, or workout routines."
        )

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        chat_input = st.chat_input(
            "Ask your fitness question here...", key="fitness_chat"
        )

        if chat_input:
            # Display user message
            with st.chat_message("user"):
                st.markdown(chat_input)

            # Add to history
            st.session_state.chat_history.append(
                {"role": "user", "content": chat_input}
            )

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = smart_agent.run(chat_input)

                        if hasattr(response, "content"):
                            response_content = response.content
                        else:
                            response_content = str(response)

                        st.markdown(response_content)

                        # Add to history
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": response_content}
                        )
                    except Exception as e:
                        st.error(f"Error: {e}")

    # TAB 3: Fitness Research
    with tabs[2]:
        st.header("🔍 Fitness Research Tool")
        st.markdown("Search for specific fitness and nutrition information")

        search_query = st.text_input(
            "What fitness or nutrition information would you like to find?",
            key="research_query",
        )

        if st.button("Search", key="search_btn"):
            if search_query:
                with st.spinner("Searching for information..."):
                    try:
                        search_prompt = f"Research the following fitness or nutrition topic and provide a detailed, evidence-based response with citations: {search_query}"
                        search_response = smart_agent.run(search_prompt)

                        if hasattr(search_response, "content"):
                            st.markdown(search_response.content)
                        else:
                            st.markdown(str(search_response))
                    except Exception as e:
                        st.error(f"Error during research: {e}")

    # TAB 4: Video Resources
    with tabs[3]:
        st.header("🎥 Fitness Video Resources")
        st.markdown("Find instructional fitness videos for your specific needs")

        col1, col2 = st.columns(2)

        with col1:
            video_topic = st.text_input(
                "What type of fitness videos are you looking for?", key="video_topic"
            )
            video_difficulty = st.select_slider(
                "Difficulty Level",
                options=["Beginner", "Intermediate", "Advanced"],
                value="Intermediate",
            )

        with col2:
            video_duration = st.select_slider(
                "Video Duration",
                options=["Short (<10 min)", "Medium (10-30 min)", "Long (>30 min)"],
                value="Medium (10-30 min)",
            )
            video_equipment = st.multiselect(
                "Available Equipment",
                options=[
                    "None/Bodyweight",
                    "Dumbbells",
                    "Resistance Bands",
                    "Kettlebells",
                    "Full Gym",
                ],
                default=["None/Bodyweight"],
            )

        if st.button("Find Videos", key="video_btn"):
            if video_topic:
                with st.spinner("Searching for fitness videos..."):
                    try:
                        # More specific prompt that ensures we get actual YouTube URLs
                        video_prompt = f"""
                        Use the YouTube tool to search for videos about {video_topic} fitness that are:
                        - Difficulty: {video_difficulty}
                        - Duration: {video_duration}
                        - Equipment required: {", ".join(video_equipment)}
                        
                        Please find and list 3-5 specific videos with the following information:
                        1. Exact video title with YouTube URL
                        2. Brief description of content (1-2 sentences)
                        3. Why this video is beneficial for the user
                        
                        Ensure you include the full YouTube URL for each video (format: https://www.youtube.com/watch?v=xyz). 
                        Use the YouTubeTools to get accurate video information.
                        """

                        video_response = smart_agent.run(video_prompt)

                        if hasattr(video_response, "content"):
                            content = video_response.content

                            # Check if we actually got videos
                            if "youtube.com/watch" not in content:
                                # Try a second attempt with a simplified query
                                retry_prompt = f"Use the YouTube tool to search for '{video_topic} {video_difficulty} fitness' and return 3 specific videos with their exact YouTube URLs and brief descriptions."
                                retry_response = smart_agent.run(retry_prompt)
                                if hasattr(retry_response, "content"):
                                    content = retry_response.content

                            # Display results in a more visual way
                            st.markdown("### Found Videos")

                            # Extract and display videos in cards
                            import re

                            urls = re.findall(
                                r"https?://(?:www\.)?youtube\.com/watch\?v=[a-zA-Z0-9_-]+",
                                content,
                            )

                            if urls:
                                for i, url in enumerate(urls):
                                    # Find nearby text (title and description)
                                    start_idx = max(0, content.find(url) - 200)
                                    end_idx = min(len(content), content.find(url) + 300)
                                    video_section = content[start_idx:end_idx]

                                    # Extract title (best effort)
                                    title_match = re.search(
                                        r"\*\*(.*?)\*\*|\[(.*?)\]|Title: (.*?)[\n\r]",
                                        video_section,
                                    )
                                    title = "Fitness Video"
                                    if title_match:
                                        for group in title_match.groups():
                                            if group:
                                                title = group
                                                break

                                    # Display video card
                                    st.markdown(
                                        f"""
                                    <div style="margin-bottom: 20px; padding: 15px; border-radius: 8px; border: 1px solid #ddd; background-color: #f9f9f9;">
                                        <h4>{i + 1}. {title}</h4>
                                        <a href="{url}" target="_blank">{url}</a>
                                        <p style="margin-top: 10px;">{video_section}</p>
                                    </div>
                                    """,
                                        unsafe_allow_html=True,
                                    )
                            else:
                                st.markdown(
                                    content
                                )  # Fallback to original content if no videos found
                        else:
                            st.markdown(str(video_response))
                    except Exception as e:
                        st.error(f"Error finding videos: {e}")
                        st.info("Trying alternative approach...")

                        # Fallback approach - direct YouTube search results
                        search_term = f"{video_topic} {video_difficulty} fitness"
                        search_url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"

                        st.markdown(
                            f"""
                        <div style="padding: 15px; border-radius: 8px; border: 1px solid #ffcc00; background-color: #fffaee;">
                            <h4>⚠️ Could not retrieve specific videos</h4>
                            <p>Please use this link to view search results on YouTube:</p>
                            <a href="{search_url}" target="_blank">{search_term} - YouTube Search</a>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

    # TAB 5: Video Analysis
    with tabs[4]:
        st.header("🎬 YouTube Video Analysis")
        st.markdown("""
        This section allows you to analyze fitness YouTube videos in depth. Enter a YouTube URL to get detailed insights, 
        summaries, and key points from the video content.
        """)

        # Video URL input
        video_url = st.text_input(
            "Enter a YouTube video URL",
            key="video_analysis_url",
            placeholder="https://www.youtube.com/watch?v=...",
        )

        # Analysis options
        analysis_options = st.multiselect(
            "What would you like to analyze?",
            options=[
                "Summary of key points",
                "Exercise technique breakdown",
                "Nutritional advice",
                "Training methodology",
                "Equipment requirements",
                "Progression suggestions",
            ],
            default=["Summary of key points"],
            key="analysis_options",
        )

        # Question about the video
        specific_question = st.text_input(
            "Ask a specific question about the video (optional)",
            key="video_question",
            placeholder="E.g., What does the instructor say about proper form for squats?",
        )

        # Analysis button
        if st.button("Analyze Video", key="analyze_video_btn"):
            if video_url and "youtube.com" in video_url:
                with st.spinner(
                    "Analyzing video content... This may take a few moments."
                ):
                    try:
                        # Format the analysis request
                        analysis_prompt = f"""
                        Analyze this YouTube video: {video_url}
                        
                        Focus on these aspects:
                        {", ".join(analysis_options)}
                        
                        {"Also answer this specific question: " + specific_question if specific_question else ""}
                        
                        First, get the video data and captions using the YouTube tools.
                        Then provide a structured analysis with timestamps when possible.
                        Include practical takeaways that someone could apply to their own fitness routine.
                        """

                        # Run the analysis
                        analysis_response = youtube_agent.run(analysis_prompt)

                        # Display results
                        if hasattr(analysis_response, "content"):
                            # Display the video preview
                            video_id = None
                            if "v=" in video_url:
                                video_id = video_url.split("v=")[1].split("&")[0]
                            elif "youtu.be/" in video_url:
                                video_id = video_url.split("youtu.be/")[1].split("?")[0]

                            if video_id:
                                st.markdown(
                                    f"""
                                <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                                    <iframe width="560" height="315" 
                                    src="https://www.youtube.com/embed/{video_id}" 
                                    frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
                                    encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
                                    </iframe>
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )

                            # Analysis results
                            st.markdown("## Analysis Results")
                            st.markdown(analysis_response.content)

                            # Provide downloadable summary
                            summary_text = f"""
                            # Video Analysis Summary
                            
                            **Video URL:** {video_url}
                            **Analysis Focus:** {", ".join(analysis_options)}
                            
                            {analysis_response.content}
                            
                            *Analysis generated by AI Health & Fitness Planner*
                            """

                            st.download_button(
                                label="Download Analysis",
                                data=summary_text,
                                file_name="video_analysis_summary.md",
                                mime="text/markdown",
                            )

                            # Add to analysis history
                            if "video_analyses" not in st.session_state:
                                st.session_state.video_analyses = []

                            st.session_state.video_analyses.append(
                                {
                                    "url": video_url,
                                    "content": analysis_response.content,
                                    "options": analysis_options,
                                }
                            )

                        else:
                            st.error(
                                "Could not generate analysis. Please try a different video or check the URL."
                            )
                    except Exception as e:
                        st.error(f"Error analyzing video: {e}")
                        st.info(
                            "Please make sure you've entered a valid YouTube URL and that you're using a model like llama3.2 or qwen that supports YouTube tools."
                        )
            else:
                st.error("Please enter a valid YouTube URL")

        # Tips and examples
        with st.expander("Tips for video analysis"):
            st.markdown("""
            ### How to get the most out of video analysis
            
            - **Use complete URLs:** Make sure to use the full YouTube URL including the `v=` parameter
            - **Be specific with questions:** Asking detailed questions will yield better results
            - **Choose appropriate options:** Select analysis options relevant to the video content
            - **Works best with:** Tutorial videos, workout demonstrations, and fitness lectures
            - **Save analyses:** Use the download button to save important analyses for reference
            
            ### Example videos to analyze
            
            - Workout techniques: https://www.youtube.com/watch?v=IODxDxX7oi4 (Push-up tutorial)
            - Nutrition advice: https://www.youtube.com/watch?v=wxzc_2c6GMg (Meal planning)
            - Training programs: https://www.youtube.com/watch?v=ixkQaZXVQjs (HIIT workout)
            """)

        # Previous analyses
        if "video_analyses" in st.session_state and st.session_state.video_analyses:
            st.markdown("### Previous Analyses")
            for i, analysis in enumerate(st.session_state.video_analyses):
                with st.expander(f"Analysis {i + 1}: {analysis['url'][:50]}..."):
                    st.markdown(analysis["content"])

                    # Option to remove this analysis
                    if st.button(
                        f"Remove Analysis {i + 1}", key=f"remove_analysis_{i}"
                    ):
                        st.session_state.video_analyses.pop(i)
                        st.rerun()


if __name__ == "__main__":
    main()
