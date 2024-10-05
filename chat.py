import streamlit as st
import openai
import os

# Set page configuration
st.set_page_config(
    page_title="GPT-4 Chat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Title of the app
st.title("💬 Chat with GPT-4")

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to get GPT-4 response
def get_gpt4_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state['messages'] + [
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        assistant_message = response['choices'][0]['message']['content'].strip()
        return assistant_message
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar for API Key input (optional security measure)
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    help="Enter your OpenAI API key. Alternatively, set the OPENAI_API_KEY environment variable.",
)

# Set OpenAI API key
if api_key:
    openai.api_key = api_key
elif os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    st.warning("Please enter your OpenAI API key in the sidebar or set the OPENAI_API_KEY environment variable.")

# Display chat messages
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    elif msg['role'] == 'assistant':
        st.markdown(f"**GPT-4:** {msg['content']}")

# Input form for user messages
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:", "")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_input:
    # Append user message to session state
    st.session_state['messages'].append({"role": "user", "content": user_input})
    # Display user message
    st.markdown(f"**You:** {user_input}")
    # Get GPT-4 response
    with st.spinner("GPT-4 is typing..."):
        assistant_response = get_gpt4_response(user_input)
    # Append assistant message to session state
    st.session_state['messages'].append({"role": "assistant", "content": assistant_response})
    # Display assistant message
    st.markdown(f"**GPT-4:** {assistant_response}")