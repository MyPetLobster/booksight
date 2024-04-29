from openai import OpenAI
from dotenv import load_dotenv




load_dotenv()
client = OpenAI()


GPT_MODEL = "gpt-3.5-turbo"
GPT_TEMP = 0.3





def format_GPT_input(spines, full_img_text):
    """
    Format all data to be included in prompt message

    inputs: 
        - spines: list of spine objects
        - full_img_text: list of text detected in the full image

    output:
        - book_data: formatted string with all book data
    """

    book_data = ""

    for i, spine in enumerate(spines):
        book_data += f"Book_{i}: \n"
        book_data += f"Text: {spine.text}\n"
        book_data += f"Height: {spine.height}\n"
        book_data += f"Thickness: {spine.thickness}\n"
        book_data += f"Background Color: {spine.background_color}\n"
        book_data += f"Text Color: {spine.text_color}\n\n"

    book_data += "Full Image Text: \n"
    book_data += "\n".join(full_img_text)

    return book_data


def match_books(spines, full_img_text):
    book_data = format_GPT_input(spines, full_img_text)
    






def identify_basic_info(text):
    messages = [
        {"role": "system", "content": f"""
            """
        }
    ]

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=GPT_TEMP,
        max_tokens=1000,
    )

    return response.choices[0].message.content



def identify_book_info(text):
    language = "English"
    messages = [
        {"role": "system", "content": f"""
            

            """
        }
    ]

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=GPT_TEMP,
        max_tokens=1000,
    )

    return response.choices[0].message.content