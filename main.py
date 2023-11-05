import streamlit as st
import random
import time
from utils import anonymize_text, deanonymize_text, chatbot_response
import openai

import openai
import streamlit as st
from utils import extract_pdf_text
from text_effects import highlight_phrases_in_paragraph
from DetectEntity import DetectEntity

st.title("AInonymous")

system_prompt="""You are a helpful assistant, your task is to review an uploaded document\
uploaded by a user.\
The user query is delimited by triple asterisks.\
The reference documents in that message are delimited with triple backticks.\
A user might ask follow up questions.
"""


# add a selectbox to the sidebar
st.sidebar.multiselect("Entity list", ["email", "phone",'location'], ["email", "phone","location"])

# add a clear button to the sidebar
if st.sidebar.button("Clear"):
    st.session_state.chat_hist = []
    st.session_state.messages = []
    st.session_state.cls = None
# add 
# add a n upload pdf button to the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", accept_multiple_files=False)
if uploaded_file is not None:
    _,chunks = extract_pdf_text(uploaded_file)
    # st.write(chunks)

with open("hack_secret.txt") as f:
    # st.write("Using OpenAI API key:", f.read())
    openai.api_key = f.read()

# Building a front end with streamlit
# ref: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_hist = []

for message in st.session_state.chat_hist:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    if len(st.session_state.chat_hist)==0:
        # ref_doc = "\n".join(chunks)
        ref_doc = chunks[0]
        # llm_prompt = augment_prompt(prompt,chunks[0])
        
        
        cls = DetectEntity(ref_doc)
        cls.Detect()
        cls.RemoveDetected()
        cls.InfillDetected(cls.text)

        safe_prompt = cls.UserPromptReplace(prompt)
        safe_doc = cls.text
        st.session_state.cls = cls
        llm_prompt = f"***{safe_prompt}***+```{safe_doc}```"

    else:
        safe_prompt = st.session_state.cls.UserPromptReplace(prompt)
        llm_prompt = safe_prompt
        st.write(llm_prompt)

    st.session_state.messages.append({"role": "user", "content": llm_prompt})
    st.session_state.chat_hist.append({'role':'user', 'content':prompt})
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

    # entities
    
    decoded_message = st.session_state.cls.ReplyToUser(full_response)
    phrases_to_highlight = {}
    ent_data = st.session_state.cls.replacedData
    for eny_type in st.session_state.cls.replacedData:
        ents = st.session_state.cls.replacedData[eny_type]
        if type(ents) == dict: ents = [ents]
        for ent in ents:
            phrases_to_highlight[ent['original']] = None
    # st.write(phrases_to_highlight)
    highlighted_Text = highlight_phrases_in_paragraph(decoded_message,phrases_to_highlight)
    
    st.markdown("Decoded message:")
    st.markdown(decoded_message)
    st.markdown(highlighted_Text, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.chat_hist.append({'role':'assistant', 'content':decoded_message})

