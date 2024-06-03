from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


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

    chat_response = response.choices[0].message.content.strip()
    print(chat_response)

    return chat_response