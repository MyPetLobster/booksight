import tiktoken
import os
from dotenv import load_dotenv

import vertexai
from vertexai.generative_models import GenerativeModel

import vision_config

load_dotenv()




def count_gpt_tokens(string: str, model: str) -> int:
    """
    This function counts the number of tokens in a given string based on the encoding of a specific OpenAI Model.

    Args:
        string (str): A string for which the number of tokens needs to be counted.
        model (str): A string containing the name of the AI model.

    Returns:
        num_tokens (int): An integer representing the number of tokens in the given string.
    """
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def count_gemini_tokens(input, type):
    """
    This function counts the number of tokens in a given string based on the encoding of a specific Google Gemini model.

    Args:
        input (str): A string for which the number of tokens needs to be counted.
        type (str): A string indicating whether the input is a prompt or a response.

    Returns:
        if type == 'prompt':
            prompt_token_count (int): An integer representing the number of tokens in the given prompt.
            prompt_character_count (int): An integer representing the number of billable characters in the given prompt.
        elif type == 'response':
            prompt_token_count (int): An integer representing the number of tokens in the given prompt.
            candidates_token_count (int): An integer representing the number of tokens in the candidates.
            total_token_count (int): An integer representing the total number of tokens.
    """
    # Retrieve and configure project service account credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/corysuzuki/Documents/repos/creds/gen-lang-credentials.json'

    # Initialize Vertex AI
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = "us-central1"
    vertexai.init(project=project_id, location=location)

    # Initialize Gemini Generative Model
    model = GenerativeModel(model_name=model)

    # Load Vision Configuration
    config = vision_config.get_config()
    model = config['ai_model']

    # Process input based on type (prompt: str, response: object)
    if type == 'prompt':
        return count_gemini_prompt_tokens(input, model)
    elif type == 'response':
        return count_gemini_response_tokens(input, model)


def count_gemini_prompt_tokens(prompt: str, model: str="gemini-1.5-pro"):
    """
    This function counts the number of tokens in a given prompt based on the encoding of a specific Google Gemini model.
    
    Args:
        prompt (str): A string containing the prompt for the AI model.
        model (str): A string containing the name of the AI model to use.
        
    Returns:
        prompt_token_count (int): An integer representing the number of tokens in the given prompt.
        prompt_character_count (int): An integer representing the number of billable characters in the given prompt.
    """
    response = model.count_tokens(prompt)
    prompt_token_count = response.total_tokens
    prompt_character_count = response.total_billable_characters

    return prompt_token_count, prompt_character_count


def count_gemini_response_tokens(response: object):
    """
    This function counts the number of tokens in a given response based on the encoding of a specific Google Gemini model.

    Args:
        response (object): An object containing the response from the AI model.

    Returns:
        prompt_token_count (int): An integer representing the number of tokens in the given prompt.
        candidates_token_count (int): An integer representing the number of tokens in the candidates.
        total_token_count (int): An integer representing the total number of tokens.
    """
    usage_metadata = response.usage_metadata
    prompt_token_count = usage_metadata.prompt_token_count
    candidates_token_count = usage_metadata.candidates_token_count
    total_token_count = usage_metadata.total_token_count

    return {
        'prompt_token_count': prompt_token_count,
        'candidates_token_count': candidates_token_count,
        'total_token_count': total_token_count
    }
        