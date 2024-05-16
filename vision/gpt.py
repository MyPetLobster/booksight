from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def run_gpt(prompt, model, temperature):
    """
    This function interprets OCR text to identify book titles and authors. The OCR text often contains errors and unconventional spacing, 
    which requires intelligent parsing to deduce the correct information. This function uses the OpenAI API to generate content based on a prompt.

    Args:
        text (str): A string containing OCR text for each spine.

    Returns:
        str: A JSON-formatted string containing the book titles and authors.
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

    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()