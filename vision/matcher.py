from openai import OpenAI
from dotenv import load_dotenv

from classes import Spine



load_dotenv()
client = OpenAI()


GPT_MODEL = "gpt-3.5"
GPT_TEMP = 0.7




def match_books(spines, full_img_text):
    book_data = format_GPT_input(spines, full_img_text)
    book_info_string = identify_basic_info(book_data)


    print(f"\nbook_info_string: {book_info_string}\n")



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
        book_data += f"Text: {spine}\n"
        # book_data += f"Height: {spine.height}\n"
        # book_data += f"Thickness: {spine.thickness}\n"
        # book_data += f"Background Color: {spine.background_color}\n"
        # book_data += f"Text Color: {spine.text_color}\n\n"

    book_data += "Full Image Text: \n"
    book_data += "\n".join(full_img_text)

    return book_data


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
        "content": f"""You are a sophisticated text analysis tool designed to extract book titles and authors from noisy OCR data. You are an expert
        at identifying book titles and authors, even when the text is riddled with errors. You know every English language book ever published and can
        recognize them with ease.
        
        Here is how you should approach the task:
        
        - The input text contains potential book data with various OCR-induced errors like misplaced spaces and misinterpreted characters.
        - There may be instances where the OCR detects a few books individually, but then also recognizes the grouping of multiple spines 
            as a single book. If this occurs, treat each book as a separate entity, but be careful not to include the same book twice. 
            For example, let's say you get the text "Book_04: ..." and you are able to identify three books in the text. But you already detected
            two of those books in "Book_03" and "Book_02." In this case, you should only include the new book in the response. However, if you then
            get to "Book_05" and it is a repeat of "Book_04", you should fill in "Book_05" as you normally would. Then go back and replace "Book_04"
            reponse with: "Book_04: IGNORE - BAD SCAN, DUPES"
        - We need to maintain order with the books because the next step of the process will be to add the info you provide (author and title) to
            a list of Python "Spine" objects that already exist. The info provided to you comes from this list of spines. 
        - Your goal is to sift through the noise and accurately identify each book's title and author. Consider strategies like ignoring extraneous spaces or 
          substituting visually similar characters (e.g., '0' with 'O' or '$' with 'S'). Ignore spaces between characters if doing so helps identify the correct title or author.
        - Generate a response in the format 'Title - Author,' for each book you identify. If a book cannot be confidently identified, use 'Unknown - Unknown'.
        - Accuracy is critical, as your output will guide further data retrieval. Be sure to correct all spelling errors and spacing errors. Your responses
            will be used to query databases. 
        - Remove duplicate books from the list. If the same book is identified multiple times, include it only once. Only include one 
            instance of each unique book. But be sure to associate it with the correct book number as stated earlier.

        Example of expected output format:
        'Book_01: Train Dreams - Denis Johnson,\n Book_02: Great Expectations - Charles Dickens, '

        - Be sure to keep book information labelled with the corresponding 'Book_X' identifier. And if you detect additional books in the full image text, 
            include them in the same format, adding Book_X identifiers as needed.

        If uncertain about any data piece, review it once more, aiming to resolve ambiguities. If you are still unsure, mark it as 'Unknown - Unknown.' 
        This should be a last resort.
        
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