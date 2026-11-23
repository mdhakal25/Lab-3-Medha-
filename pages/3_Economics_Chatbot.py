# Lab 3: Chatbot page
# TODO: Rename this file to fit your page. Keep the number at the front.
#
# A chatbot built with Pydantic AI (see the Pydantic AI pages on Canvas).
# It should:
#   - use a Pydantic AI Agent with instructions that fit your project's theme (no tools yet)
#   - use Streamlit's chat elements: st.chat_message and st.chat_input
#   - remember the conversation (message_history, saved in st.session_state)
#   - use try/except so an error shows a message instead of crashing the page
#   - stay on theme, without using any API or external data
#
# Your Gemini API key goes in .streamlit/secrets.toml as GOOGLE_API_KEY.

import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

# Page title and introduction
st.title("Economics Chatbot")

st.write("""
Welcome to the Global Growth Tracker Economics Chatbot!
Ask questions about economic concepts, global markets, and
how different factors can influence economic growth.
""")

# Connect to Google Gemini
provider = GoogleProvider(api_key=st.secrets["GOOGLE_API_KEY"])
model = GoogleModel("gemini-3.5-flash-lite", provider=provider)

# Create the economics chatbot
economics_agent = Agent(
    model,
    instructions="""
    You are a friendly economics assistant for Global Growth Tracker.

    Help users understand economic concepts, global markets,
    and factors that influence economic growth.

    Explain topics clearly and naturally so that college students
    and people without an economics background can understand.

    Keep answers informative, conversational, and easy to follow.

    Stay focused on economics and related topics.

    You do not have access to live economic data or the World Bank API.
    If someone asks for exact statistics, explain that you cannot
    look them up yet and suggest using the Economic Data Explorer.
    """
)

# Store the chat messages
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Store Pydantic AI conversation history
if "message_history" not in st.session_state:
    st.session_state.message_history = []

# Display previous messages
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Let users ask questions
user_prompt = st.chat_input("Ask a question about economics...")

if user_prompt:
    # Save and display the user's message
    st.session_state.chat_messages.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.write(user_prompt)

    # Generate and display the chatbot's response
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                result = economics_agent.run_sync(
                    user_prompt,
                    message_history=st.session_state.message_history
                )

            assistant_response = result.output
            st.write(assistant_response)

            # Save the assistant response
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": assistant_response
            })

            # Update Pydantic AI conversation history
            st.session_state.message_history = result.all_messages()

        except Exception:
            st.error("Sorry, something went wrong. Please try again.")
           

