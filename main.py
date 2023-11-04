import streamlit as st
import random
import time
from utils import anonymize_text, deanonymize_text, chatbot_response
import openai

import openai
import streamlit as st
from chunkPDF import extract_pdf_text

st.title("AInonymous")

system_prompt="""You are a helpful assistant named Gary, your task is to review a series of\
documents returned by a search system and answer the user's question only based on these documents.\
The first user query is delimited by triple asterisks\.
The reference documents in that message are delimited with triple backticks.\
A user might ask follow up questions.
"""


# add a selectbox to the sidebar
st.sidebar.multiselect("Entity list", ["email", "phone",'location'], ["email", "phone","location"])
# add 
# add a n upload pdf button to the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", accept_multiple_files=False)
if uploaded_file is not None:
    _,chunks = extract_pdf_text(uploaded_file)
    st.write(chunks)

with open("secret.txt") as f:
    # st.write("Using OpenAI API key:", f.read())
    openai.api_key = f.read()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})