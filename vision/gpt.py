from openai import OpenAI

from . import config


def run_gpt(prompt, model, temperature):
    """
    This function interprets OCR text to identify book titles and authors. The OCR text often contains errors and unconventional 
    spacing, which requires intelligent parsing to deduce the correct information. This function uses the OpenAI API to generate 
    content based on a prompt.

    Args:
        prompt (str): A string containing OCR text for each spine.
        model (str): A string containing the name of the AI model to use.
        temperature (float): A float value indicating the randomness of the generated text.

    Returns:
        chat_response (str): A string containing the generated content from the AI model.
    """
    # Configure OpenAI settings
    
    # Automatically uses OPENAI_API_KEY env var
    client = OpenAI()
    instructions = {
        "role": "system", 
        "content": prompt
    }

    response = client.chat.completions.create(
        model=model,
        messages=[instructions],
        temperature=temperature,
        max_tokens=4000,
    )

    return response.choices[0].message.content.strip()