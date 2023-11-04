import streamlit as st
import re

# Define a library of pale colors
COLOR_LIBRARY = {
    "pale_red": "#ffcccb",
    "pale_green": "#b2fab4",
    "pale_blue": "#add8e6",
    "pale_yellow": "#ffffcc",
    "pale_purple": "#dcb9ff",
    "pale_orange": "#ffedcc",
    "pale_pink": "#ffe0ef",
    "pale_cyan": "#e0ffff",
    "pale_olive": "#d1e0a2",
    "pale_peach": "#ffe5b4",
    # ... add more pale colors as you wish
}

def highlight_phrases_in_paragraph(paragraph, phrases_to_colors):
    """
    Highlights specific phrases within a paragraph in Streamlit markdown using pale colors and rounded edges.
    
    Args:
    - paragraph (str): The paragraph of text where phrases will be highlighted.
    - phrases_to_colors (dict): Dictionary where keys are phrases to be highlighted and values are color names from the library.
    
    Returns:
    - None: Directly renders the HTML in Streamlit using markdown.
    """
    # Sort phrases by length in descending order to handle nested phrases
    phrases_sorted = sorted(phrases_to_colors.keys(), key=len, reverse=True)
    
    # Escape phrases for regex and replace them with highlighted HTML
    for phrase in phrases_sorted:
        escaped_phrase = re.escape(phrase)
        color_code = COLOR_LIBRARY.get(phrases_to_colors[phrase].lower(), "#000000")  # Default to black if color not found
        replacement = (
            f'<span style="background-color: {color_code}; '
            f'border-radius: 0.5em; padding: 0.3em 0.6em;">{phrase}</span>'
        )
        paragraph = re.sub(escaped_phrase, replacement, paragraph, flags=re.IGNORECASE)
    
    # Render the HTML in Streamlit using the markdown function with unsafe_allow_html set to True
    st.markdown(paragraph, unsafe_allow_html=True)

# # Example usage:
# paragraph_text = "This is a test paragraph where certain phrases will be highlighted in pale red and pale blue."
# phrases_to_highlight = {
#     "test paragraph": "pale_blue",
#     "certain phrases": "pale_red",
#     # Add more phrases and their colors as needed
# }

# highlight_phrases_in_paragraph(paragraph_text, phrases_to_highlight)
