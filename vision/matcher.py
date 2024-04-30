from openai import OpenAI
from dotenv import load_dotenv

from classes import Spine



load_dotenv()
client = OpenAI()


GPT_MODEL = "gpt-3.5-turbo"
GPT_TEMP = 0.7




def match_books(spines, full_img_text):
    book_info_string = identify_basic_info(book_data)

    print(f"\nbook_info_string: {book_info_string}\n")



def identify_basic_info(text):
    """
    This function interprets OCR text to identify book titles and authors. The OCR text often contains errors and unconventional spacing, 
    which requires intelligent parsing to deduce the correct information.

    Args:
        text (str): OCR-generated text, potentially containing book titles and author names mixed with gibberish.

    Returns:
        str: A comma-separated list of "<Title> - <Author>, " for each book identified.
    """

    instructions = {
        "role": "system", 
        "content": f"""You are a sophisticated text analysis tool designed to extract book titles and authors from noisy OCR data. 
        Here is how you should approach the task:
        
        - The input text '{text}' contains potential book data with various OCR-induced errors like misplaced spaces and misinterpreted characters.
        - Your goal is to sift through the noise and accurately identify each book's title and author. Consider strategies like ignoring extraneous spaces or 
          substituting visually similar characters (e.g., '0' with 'O').
        - Generate a response in the format 'Title - Author,' for each book you identify. If a book cannot be confidently identified, use 'Unknown - Unknown'.
        - Accuracy is critical, as your output will guide further data retrieval. Ensure that names and titles are correctly spelled.
        - Remove duplicate books from the list. If the same book is identified multiple times, include it only once.

        Example of expected output format:
        'Train Dreams - Denis Johnson, Great Expectations - Charles Dickens, '

        If uncertain about any data piece, review it once more, aiming to resolve ambiguities. If still in doubt, opt for 'Unknown - Unknown' rather than risking incorrect information.
        
        Finally, end your response with "Number of books identified: X," where X is the total number of books you have identified.
        """
    }

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[instructions],
        temperature=GPT_TEMP,
        max_tokens=1000,
    )

    return response.choices[0].message.content.strip()







def retrieve_google_books_info(text):
    # Split the text at commas, create list where each item is formatted as "<Title> - <Author>"
    book_list = text.split(", ")
    
    # Remove the "-" from each item
    book_list = [book.replace(" - ", " ") for book in book_list]

    results = []
    for book in book_list:
        results += search_google_books(book)

    return results



def search_google_books(query):
    ...



def identify_book_info():
    # Conversion constants
    px_to_in_multiplier = 1
    color_modifier = (1, 1, 1)







def main():
    spines = [
        Spine(
            image_path="vision/spines/book_0.jpeg",
            avg_color=[155, 185, 174],
            dominant_color=[189, 224, 214],
            color_palette=[
                [189, 224, 214],
                [10, 5, 4],
                [103, 103, 91],
                [146, 146, 132],
                [169, 209, 198],
                [54, 40, 32]
            ],
            height=2702,
            width=542,
            text=['280, Finnegans Wake, JAMES JOYcE']
        ),
        Spine(
            image_path="vision/spines/book_1.jpeg",
            avg_color=[133, 112, 103],
            dominant_color=[156, 133, 125],
            color_palette=[
                [156, 133, 125],
                [14, 6, 4],
                [127, 102, 92],
                [204, 189, 181],
                [142, 118, 110],
                [81, 63, 48]
            ],
            height=2758,
            width=263,
            text=['VINTAG E, PALE FIRE, N A B 0 KO V']
        ),
        Spine(
            image_path="vision/spines/book_2.jpeg",
            avg_color=[180, 137, 94],
            dominant_color=[156, 124, 92],
            color_palette=[
                [156, 124, 92],
                [28, 16, 13],
                [225, 205, 181],
                [234, 182, 107],
                [205, 83, 61],
                [97, 59, 35]
            ],
            height=2830,
            width=583,
            text=['Jom<", Picadoa, 37o s, Iror`, Jok, PicadoR, OF SMOKE, Dmo, DEnIs, DENis, TREE, TREE OF SMORE, from, JOHNSON, DENIS']
        ),
        Spine(
            image_path="vision/spines/book_3.jpeg",
            avg_color=[91, 72, 66],
            dominant_color=[180, 164, 158],
            color_palette=[
                [180, 164, 158],
                [67, 40, 34],
                [14, 6, 4],
                [240, 233, 225],
                [128, 88, 73],
                [187, 209, 200]
            ],
            height=2487,
            width=520,
            text=['ARTIST, 4 |Ome, (.issIcs, THE, IARNES, PORTRAIT, IiRi;s, 4 TOBe, and, YOUNG MAN, James Joyce, CSSICS, DUBLINERS']
        ), 
        Spine(
            image_path="vision/spines/book_4.jpeg",
            avg_color=[115, 93, 84],
            dominant_color=[21, 12, 10],
            color_palette=[
                [21, 12, 10],
                [143, 137, 132],
                [220, 206, 197],
                [188, 40, 36],
                [109, 104, 102],
                [243, 201, 97]
            ],
            height=2836,
            width=221,
            text=['NOBODV MOVE  DENLS JOHNSON, (o ?0, (Dicador, NOBODY MOVE_ DENIS JOHNSON']
        ),
        
    ]

    full_img_text = ['']

    match_books(spines, full_img_text)




if __name__ == "__main__":
    main()