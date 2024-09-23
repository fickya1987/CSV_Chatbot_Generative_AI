import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_csv_agent
from streamlit_chat import message
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# Fetch the API key from the environment
google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key is None:
    raise ValueError("Google API key not found. Please add it to your .env file.")



st.title("📈Chat With Your CSV File🚀")
uploaded_file = st.file_uploader("Upload your CSV file", type = "csv")

gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", google_api_key=google_api_key, temperature=0.9)

if uploaded_file is not None:
    agent = create_csv_agent(gemini_llm, uploaded_file, verbose=True, allow_dangerous_code=True)


    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤖"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey!"]

    with st.form(key= 'my_form', clear_on_submit=True):
        user_question = st.text_input("Query:", placeholder="Talk to your data here", key = 'inpt')
        submit_button = st.form_submit_button(label = "Send")

    if user_question is not None and user_question != "":
        with st.spinner(text = "In progress..."):
            output = agent.invoke(user_question)['output']

            st.session_state['past'].append(user_question)
            st.session_state['generated'].append(output)


    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user= True, avatar_style= "initials", seed="Anil")
            message(st.session_state['generated'][i], avatar_style="bottts", seed=12)
