import os
import pathlib
import textwrap
from dotenv import load_dotenv

import google.generativeai as genai


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')


def run_gemini(prompt, model):
    """
    This function interprets OCR text to identify book titles and authors. The OCR text often contains errors and unconventional spacing, 
    which requires intelligent parsing to deduce the correct information. This function uses the Gemini API to generate content based on a prompt.


    Args:
        text (str): A string containing OCR text for each spine.

    Returns:
        str: A JSON-formatted string containing the book titles and authors.
    """
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)

    return response.text




