import json 

from openai import OpenAI
from dotenv import load_dotenv

import db_requests as dbr
from classes import Spine



load_dotenv()
client = OpenAI()


GPT_MODEL = "gpt-4"
GPT_TEMP = 0.3




def match_books(spines, full_img_text):
    print("\nPreparing text for GPT input...\n")
    book_data = format_GPT_input(spines, full_img_text)
    print(f"\nBook Data (Raw):\n{book_data}\n")

    print(f"\nIdentifying basic book info using {GPT_MODEL} set to a temperature of {GPT_TEMP}...\n")
    book_data_basic = identify_basic_info(book_data)
    print(f"\nBook Data (Basic):\n{book_data_basic}\n")

    book_dict = json.loads(book_data_basic)
    book_count = len(book_dict)

    print(f"\nNumber of books positively identified: {book_count}\n")
    
    # Update spines -- spine.author, spine.title
    for i, spine in enumerate(spines):
        book = book_dict[f"Book_{i}"]
        spine.author = book["author"]
        spine.title = book["title"]

    # Retrieve potential ISBN's from OpenLibrary and update spine.possible_matches with list of ISBN's
    for spine in spines:
        spine.possible_matches = dbr.get_isbns_openlibrary(spine.title, spine.author)

    print(f"All Spine Object:\n\n{spines}\n\n")



def format_GPT_input(spines, full_img_text):
    """
    Format all data to be included in prompt message

    inputs: 
        - spines: list of spine objects
        - full_img_text: list of text detected in the full image

    output:
        - book_data: String containing all book data in the format 'Book_X: <spine_text>,\n'
    """

    book_data = ""
    for i, spine in enumerate(spines):
        book_data += f"Book_{i}: {spine.text},\n"

    return book_data


def identify_basic_info(text):
    """
    This function interprets OCR text to identify book titles and authors. The OCR text often contains errors and unconventional spacing, 
    which requires intelligent parsing to deduce the correct information.

    Args:
        text (str): A string containing OCR text for each spine.

    Returns:
        str: A JSON-formatted string containing the book titles and authors.
    """

    instructions = {
        "role": "system", 
        "content": f"""You will receive a string formatted as list of text detected from spines of books, formatted like this --
        "Book_X: <OCR text>,\n". You must interpret the OCR text and identify each book's title and author. The OCR text may contain errors,
        unconventional spacing, or other issues that require intelligent parsing to deduce the correct information. Return a JSON-formatted
        string where each "Book_X" identifier is associated with an "author" and "title" key. If a book title and/or author cannot be confidently
        identified, use "Unknown" as the value. Correct all spelling and spacing errors in your response.
        
        The input text that follows "Full Image OCR Text: " is a scan of the full input image. If you have trouble identifying a spine's 
        text, there may be additional clues in the full image text. Additionally, there may be books whose spines went undetected. 
        If you identify additional books within that text, include them in the response, but you will have to add additional "Book_X" identifiers.

        Use every resource at your disposal to decipher the text and correctly identify all book titles and authors. Accuracy is critical. 

        - DO NOT MAKE UP BOOK TITLES OR AUTHORS. Use all of the data you have to identify a REAL author and REAL book title that would make 
        sense in the context of OCR text from the spine of a book. For Example, if you have some OCR text that says "HARY BFARD ROME Q R mistory", 
        You should be able to look through existing books and realize that the book is "SPQR - A History of Ancient Rome" by Mary Beard. 

        - If you are only able to identify an author, you should search your knowledge to find all the books that author has written, then 
        use that information in order to determine which title is most likely to be correct.

        Here is the input text you will be working with: \n\n  {text}
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









    # You are a sophisticated text analysis tool designed to extract book titles and authors from noisy OCR data. You are an expert
    #     at identifying book titles and authors, even when the text is riddled with errors. You know every English language book ever published and can
    #     recognize them with ease.

    #     Here is how you should approach the task:
        
    #     - The input text contains potential book data with various OCR-induced errors like misplaced spaces and misinterpreted characters.
    #     - There may be instances where the OCR detects a few books individually, but then also recognizes the grouping of multiple spines 
    #         as a single book. If this occurs, treat each book as a separate entity, but be careful not to include the same book twice. 
    #         For example, let's say you get the text "Book_04: ..." and you are able to identify three books in the text. But you already detected
    #         two of those books in "Book_03" and "Book_02." In this case, you should only include the new book in the response. However, if you then
    #         get to "Book_05" and it is a repeat of "Book_04", you should fill in "Book_05" as you normally would. Then go back and replace "Book_04"
    #         reponse with: "Book_04: IGNORE - BAD SCAN, DUPES"
    #     - We need to maintain order with the books because the next step of the process will be to add the info you provide (author and title) to
    #         a list of Python "Spine" objects that already exist. The info provided to you comes from this list of spines. 
    #     - Your goal is to sift through the noise and accurately identify each book's title and author. Consider strategies like ignoring extraneous spaces or 
    #       substituting visually similar characters (e.g., '0' with 'O' or '$' with 'S'). Ignore spaces between characters if doing so helps identify the correct title or author.
    #     - Generate a response in the format 'Title - Author,' for each book you identify. If a book cannot be confidently identified, use 'Unknown - Unknown'.
    #     - Accuracy is critical, as your output will guide further data retrieval. Be sure to correct all spelling errors and spacing errors. Your responses
    #         will be used to query databases. 
    #     - Remove duplicate books from the list. If the same book is identified multiple times, include it only once. Only include one 
    #         instance of each unique book. But be sure to associate it with the correct book number as stated earlier.

    #     Example of expected output format:
    #     'Book_01: Train Dreams - Denis Johnson,\n Book_02: Great Expectations - Charles Dickens, '

    #     - Be sure to keep book information labelled with the corresponding 'Book_X' identifier. And if you detect additional books in the full image text, 
    #         include them in the same format, adding Book_X identifiers as needed.

    #     If uncertain about any data piece, review it once more, aiming to resolve ambiguities. If you are still unsure, mark it as 'Unknown - Unknown.' 
    #     This should be a last resort.
        
    #     Finally, end your response with "Number of books identified: X," where X is the total number of books you have identified.
    #     """