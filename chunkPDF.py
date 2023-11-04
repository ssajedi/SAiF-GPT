import fitz  # PyMuPDF
import PyPDF2
# def pdf_to_text_chunks(pdf_file_object, chunk_size=400):
#     """
#     Extract text from a PDF and split it into chunks of approximately 400 words.
    
#     Parameters:
#     pdf_path (str): Path to the PDF file.
#     chunk_size (int): Number of words per chunk.
    
#     Returns:
#     list: A list of text chunks.
#     """

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


    # # Open the PDF file
    # pdf_document = pdf_reader = PyPDF2.PdfReader(file) # .read()
    
    # # Initialize variables
    # text_chunks = []
    # current_chunk = []
    # word_count = 0
    
    # # Iterate over each page in the PDF
    # for page_num in range(len(pdf_document)):
    #     # Get the page object
    #     page = pdf_document[page_num]
        
    #     # Extract text from the page
    #     page_text = page.get_text("text")
        
    #     # Split the text into words
    #     words = page_text.split()
        
    #     # Iterate over each word
    #     for word in words:
    #         # Add the word to the current chunk
    #         current_chunk.append(word)
    #         word_count += 1
            
    #         # If the current chunk reaches the chunk size
    #         if word_count >= chunk_size:
    #             # Join the words to form a chunk of text
    #             text_chunks.append(" ".join(current_chunk))
    #             # Reset the current chunk and word count
    #             current_chunk = []
    #             word_count = 0
    
    # # Add any remaining words as a final chunk
    # if current_chunk:
    #     text_chunks.append(" ".join(current_chunk))
    
    # # Close the PDF after reading
    # pdf_document.close()
    
    # # Return the list of text chunks
    # return text_chunks

# # Example usage:
# # chunks = pdf_to_text_chunks("example.pdf")
# # for i, chunk in enumerate(chunks, 1):
# #     print(f"Chunk {i}:\n{chunk}\n")

# # Assuming the pdf_to_text_chunks function is already defined above

# # Define the path to your test PDF file
# test_pdf_path = r"C:\Users\clamaral\Documents\GitHub\AInonymous\TestPDF.pdf"

# # Call the function to get the chunks
# text_chunks = pdf_to_text_chunks(test_pdf_path)

# # Iterate over the chunks and print them with an index
# for i, chunk in enumerate(text_chunks, 1):
#     print(f"Chunk {i}:")
#     print(chunk)
#     print('-' * 80)  # Print a line of dashes to separate chunks
