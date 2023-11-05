from text_effects import highlight_phrases_in_paragraph
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