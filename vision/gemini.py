import os
from dotenv import load_dotenv

import google.generativeai as genai


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure genai settings
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')


def run_gemini(prompt, model):
    """
    This function interprets OCR text to identify book titles and authors. The OCR text often contains errors and unconventional 
    spacing, which requires intelligent parsing to deduce the correct information. This function uses the Gemini API to generate 
    content based on a prompt.

    Args:
        prompt (str): A string containing prompt for the AI model and the OCR text for each spine.
        model (str): A string containing the name of the AI model to use.

    Returns:
        response.text (str): A string containing the generated content from the AI model.
    """
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)

    print(response.text)
    return response.text




