import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from agent_factory import agent1, agent2, agent3, agent4, AGENT1_PROMPT, AGENT2_PROMPT, AGENT3_PROMPT, AGENT4_PROMPT
from langgraph_chain import create_sequential_chain
import json
import time
from functools import wraps

# Load environment variables
load_dotenv()

# Check for Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API Key is missing. Please add it to your .env file or set it as an environment variable.")
    st.stop()

def retry_with_exponential_backoff(
    func,
    max_retries=3,
    initial_wait=1,
    exponential_base=2,
    errors=(Exception,),
):
    """Retry decorator with exponential backoff."""
    def decorator(*args, **kwargs):
        wait = initial_wait
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except errors as e:
                if attempt == max_retries - 1:
                    raise
                st.warning(f"Attempt {attempt + 1} failed. Retrying in {wait} seconds...")
                time.sleep(wait)
                wait *= exponential_base
    return decorator

# Initialize Gemini model
@retry_with_exponential_backoff
def initialize_gemini_model():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=GOOGLE_API_KEY, convert_system_message_to_human=True)

try:
    llm = initialize_gemini_model()
except Exception as e:
    st.error(f"Error initializing Gemini model after multiple attempts: {str(e)}")
    st.error("Please check your Google API Key and internet connection.")
    st.error("Try again later or contact support if the problem persists.")
    st.stop()

# Create chain
try:
    run_chain = create_sequential_chain([agent1, agent2, agent3, agent4])
except Exception as e:
    st.error(f"Error creating agent chain: {str(e)}")
    st.error("Please check the console for more details and report the issue.")
    st.stop()

# Streamlit UI
st.title("Chain-of-Thought Chat App")

# Sidebar for agent customization
st.sidebar.title("Agent Customization")

agents = [agent1, agent2, agent3, agent4]
default_prompts = [AGENT1_PROMPT, AGENT2_PROMPT, AGENT3_PROMPT, AGENT4_PROMPT]

for i, (agent, default_prompt) in enumerate(zip(agents, default_prompts), 1):
    agent.system_prompt = st.sidebar.text_area(f"Agent {i} System Prompt", agent.system_prompt, key=f"agent{i}_prompt")
    if st.sidebar.button(f"Set Agent {i}"):
        agent.update_system_prompt(agent.system_prompt)

if st.sidebar.button("Restore Defaults"):
    for agent, default_prompt in zip(agents, default_prompts):
        agent.update_system_prompt(default_prompt)

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_history = st.session_state.messages
            
            @retry_with_exponential_backoff
            def run_chain_with_retry(prompt, chat_history):
                return run_chain(prompt, chat_history)
            
            try:
                response = run_chain_with_retry(prompt, chat_history)
            except Exception as e:
                st.error("Failed to get a response after multiple attempts. Please try again later.")
                st.error(f"Error details: {str(e)}")
                st.stop()
            
            # Extract the final output from Agent 4
            final_output = response["agent_outcomes"]["Agent 4"]
            
            # If the final output is already a dictionary, extract the 'output' field
            if isinstance(final_output, dict) and 'output' in final_output:
                final_output = final_output['output']
            # If it's a string, use it as is (no JSON parsing needed)
            elif isinstance(final_output, str):
                final_output = final_output.strip()
            
            # Display the final output
            st.markdown(final_output)
            st.session_state.messages.append({"role": "assistant", "content": final_output})

            # Display the inference process
            with st.expander("See inference process"):
                for agent, outcome in response["agent_outcomes"].items():
                    st.subheader(agent)
                    st.markdown(outcome)
        except Exception as e:
            st.error(f"An error occurred while processing your request: {str(e)}")
            st.error("Please try again later or check your internet connection.")
            st.error("If the problem persists, please contact support.")