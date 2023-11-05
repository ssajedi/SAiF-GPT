import streamlit as st
from DetectEntity_r2 import Anonymizer

input = st.text_input("Enter text to anonymize")
anonymizer = Anonymizer()
main_text = input
safe_text = anonymizer.anonymize(input,['PER'])
st.write("Anonymized text:", safe_text)