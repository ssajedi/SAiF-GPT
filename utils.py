import re
from collections import defaultdict
import PyPDF2


def augment_prompt(prompt,ref_doc):
    aug_prompt = f"***{prompt}***+```{ref_doc}```"
    return aug_prompt

def extract_pdf_text(file):
    """
    Extracts text paragraphs from a PDF file.
    """
    pdf_reader = PyPDF2.PdfReader(file)
    pdf_dict={}
    for ip in range(len(pdf_reader.pages)):
        pdf_dict[ip] = pdf_reader.pages[ip].extract_text()
    dataset = [pdf_dict[ip] for ip in range(len(pdf_reader.pages))]
    return pdf_dict,dataset


# Sample regular expressions for detecting entities - these are simplistic
# and can be replaced with more sophisticated entity recognition if needed.
entity_patterns = {
    # 'name': re.compile(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'),
    # 'organization': re.compile(r'\b([A-Z][A-Z0-9& ]{2,})\b'),
    'email': re.compile(r'\b(\S+@\S+\.\S+)\b'),
    'phone': re.compile(r'\b(\+?\d{1,3}[-.\s]??\d{1,4}[-.\s]??\d{1,4}[-.\s]??\d{1,4})\b'),
}

# Dictionary to hold the mappings from placeholders to actual data
entity_codebook = defaultdict(dict)

def anonymize_text(text):
    # Replace entities with placeholders
    for entity_type, pattern in entity_patterns.items():
        for match in pattern.findall(text):
            placeholder = f'[{entity_type.upper()}]'
            entity_codebook[placeholder][match] = len(entity_codebook[placeholder])
            text = text.replace(match, f"{placeholder}{entity_codebook[placeholder][match]}")
    return text

def deanonymize_text(text):
    # Replace placeholders with actual data
    for placeholder, code_dict in entity_codebook.items():
        for original_entity, code in code_dict.items():
            text = text.replace(f"{placeholder}{code}", original_entity)
    return text

# Function to simulate interaction with an AI chatbot
def chatbot_response(anonymized_query):
    # Here you would have the code to send the anonymized query to the chatbot and receive the response
    # For the sake of this example, we'll just echo back the anonymized query
    response = f"AI chatbot response to your query: {anonymized_query}"
    return response

# Main interaction sequence
user_query = "Contact John Doe at john.doe@example.com or call +123456789. Also reach out to Acme Corp."
reference_document = "John Doe is a representative at Acme Corp, which can be contacted via email contact@acme.com."

# Anonymize user query and reference document
anonymized_query = anonymize_text(user_query)
anonymized_document = anonymize_text(reference_document)


# print("Anonymized Query:", anonymized_query)
# print("Anonymized Document:", anonymized_document)

# Get the response from the chatbot
chatbot_answer = chatbot_response(anonymized_query)

# print("Chatbot Answer:", chatbot_answer)

# Deanonymize the chatbot response
real_answer = deanonymize_text(chatbot_answer)

# print("Real Answer:", real_answer)