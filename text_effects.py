import streamlit as st
import re
from colorsys import hls_to_rgb

def generate_pale_color(hue):
    """
    Generates a pale color given a hue value.
    
    Args:
    - hue (float): Hue value (from 0 to 1) for the HSL color model.
    
    Returns:
    - str: Hex representation of the pale color.
    """
    # Fixed saturation at 60% and lightness at 90% to ensure paleness
    rgb_color = hls_to_rgb(hue, 0.9, 0.6)
    # Convert RGB to hex
    hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb_color[0]*255), int(rgb_color[1]*255), int(rgb_color[2]*255))
    return hex_color

def highlight_phrases_in_paragraph(paragraph, phrases_to_colors):
    """
    Highlights specific phrases within a paragraph in Streamlit markdown using generated pale colors and rounded edges.
    
    Args:
    - paragraph (str): The paragraph of text where phrases will be highlighted.
    - phrases_to_colors (dict): Dictionary where keys are phrases to be highlighted. Colors will be generated automatically.
    
    Returns:
    - None: Directly renders the HTML in Streamlit using markdown.
    """
    # Filter out phrases that don't exist in the paragraph
    phrases_present = {phrase: color for phrase, color in phrases_to_colors.items() if re.search(re.escape(phrase), paragraph, re.IGNORECASE)}

    # Sort phrases by length in descending order to handle nested phrases
    phrases_sorted = sorted(phrases_present.keys(), key=len, reverse=True)

    # Initialize a hue value
    hue = 0
    hue_increment = 1 / len(phrases_sorted) if phrases_sorted else 0  # Prevent division by zero
    
    # Escape phrases for regex and replace them with highlighted HTML
    for phrase in phrases_sorted:
        color_code = generate_pale_color(hue)
        hue += hue_increment  # Increment hue to get a different color
        
        escaped_phrase = re.escape(phrase)
        pattern = r'\b' + escaped_phrase + r'\b'  # Use word boundaries
        replacement = (
            f'<span style="background-color: {color_code}; '
            f'border-radius: 0.5em; padding: 0.3em 0.6em;">{phrase}</span>'
        )
        paragraph = re.sub(pattern, replacement, paragraph, flags=re.IGNORECASE)
    
    # Render the HTML in Streamlit using the markdown function with unsafe_allow_html set to True
    # st.markdown(paragraph, unsafe_allow_html=True)
    return paragraph



# Example usage:
paragraph_text = "This is a test paragraph where certain phrases will be highlighted. Test paragraph is food"
phrases_to_highlight = {
    "test paragraph": None,  # Color will be generated
    "certain phrases": None,  # Color will be generated
    # Add more phrases as needed
}

highlight_phrases_in_paragraph(paragraph_text, phrases_to_highlight)
