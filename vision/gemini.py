import os
import google.generativeai as genai
import vertexai
from vertexai.generative_models import GenerativeModel



from dotenv import load_dotenv
load_dotenv()

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
location = "us-central1"
vertexai.init(project=project_id, location=location)



def run_gemini(prompt, input_model):
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
    # Configure genai settings
    google_gemini_key = os.getenv('GOOGLE_GEMINI_KEY')
    genai.configure(api_key=google_gemini_key)
    model = GenerativeModel(model_name=input_model)
    response = model.generate_content(prompt)

    return response




