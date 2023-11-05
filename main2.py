import streamlit as st
import random
import time
from utils import anonymize_text, deanonymize_text, chatbot_response
import openai

import openai
import streamlit as st
from utils import extract_pdf_text
from text_effects import highlight_phrases_in_paragraph
from DetectEntity_r2 import Anonymizer

st.set_page_config(page_title="🔒", page_icon="🤫",layout="wide")
st.title("AInonymous")


system_prompt="""You are a helpful assistant, your task is to review an uploaded document\
uploaded by a user.\
The user query is delimited by triple asterisks.\
The reference documents in that message are delimited with triple backticks.\
A user might ask follow up questions. 
"""


# add a selectbox to the sidebar
ent_types_select = st.sidebar.multiselect("Entity list", ["LOC", "PER","ORG",'EMAIL','PHONE'], ["LOC", "PER","ORG"])

# add a clear button to the sidebar
if st.sidebar.button("Clear"):
    st.session_state.chat_hist = []
    st.session_state.messages = []
    st.session_state.anonymizer = None
    
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
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("What is up?"):
    if len(st.session_state.chat_hist)==0:
        # ref_doc = "\n".join(chunks)
        # ref_doc = chunks[0]
        ref_doc = "\n".join(chunks)
        # ref_doc = """ExxonMobil Infrastructure Development Proposal Executive Summary: This comprehensive proposal envisions the construction of ExxonMobil's new operational hub, designed to bolster its strategic expansion and operational excellence within the energy sector. Introduction: We propose to construct a state-of-the-art facility that reflects ExxonMobil's commitment to innovation, sustainability, and global leadership in energy. The project will span a meticulously selected 35,000-square-foot site in Houston, Texas, with the potential to become a landmark of industrial prowess and architectural ingenuity. Project Team: Leading the project will be Chief Project Engineer, Thomas Booker, with over two decades of experience in industrial construction. Architectural design will be spearheaded by Ava Clarke, whose portfolio includes several LEED-certified buildings across Dallas. Our environmental engineering efforts will be led by Dylan Rhodes in Austin, ensuring adherence to the most stringent ecological standards. Site and Structure: The facility will be located in the heart of Houston’s Energy Corridor, taking advantage of the area's rich infrastructure and proximity to ExxonMobil’s main operations. Geotechnical assessments and site preparation will be undertaken by San Antonio-based expert, Nora Quintana. The building's framework, designed for resilience and adaptability, will be overseen by structural engineer Alex Johnson from Fort Worth. Sustainability and Environment: Sus##tainability Coordinator, Rachel Santos from Corpus Christi, will implement cutting-edge green technologies, including a state-of-the-art HVAC system designed by El Paso's mechanical engineer, Omar Fernandez. Rainwater harvesting and waste management systems will be developed in collaboration with environmental specialists from Galveston Email address: test@gmail.com 123-456-7890"""
        # llm_prompt = augment_prompt(prompt,chunks[0])
        
        anmz = Anonymizer()

        safe_prompt = anmz.anonymize(prompt,ent_types_select)
        safe_doc = anmz.anonymize(ref_doc,ent_types_select)
        st.session_state.anonymizer = anmz
        llm_prompt = f"***{safe_prompt}***+```{safe_doc}```"
        st.write(safe_prompt)
    else:
        safe_prompt = st.session_state.anonymizer.anonymize(prompt,ent_types_select)
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
    
    decoded_message = st.session_state.anonymizer.deanonymize(full_response)
    phrases_to_highlight = {}
    ent_data = st.session_state.anonymizer.deanonymization_map
    # get values of diciotnary and save as list 
    ent_data = list(ent_data.values())
    for ent in ent_data:
        phrases_to_highlight[ent] = None
    # st.write(phrases_to_highlight)
    highlighted_Text = highlight_phrases_in_paragraph(decoded_message,phrases_to_highlight)
    
    st.markdown("Decoded message:")
    st.markdown(decoded_message)
    st.markdown(highlighted_Text, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.chat_hist.append({'role':'assistant', 'content':highlighted_Text})

# Add a expander to show markdown full text
if len(st.session_state.chat_hist)>0:
    with st.expander("Encrypted document"): 
        highlight_ful_doc = highlight_phrases_in_paragraph(ref_doc,phrases_to_highlight)
        st.markdown(highlight_ful_doc, unsafe_allow_html=True)


