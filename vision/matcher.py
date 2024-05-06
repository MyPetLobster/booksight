import json 
import os
import requests
import time
from PIL import Image
from io import BytesIO

import analyze_spine as asp
import db_requests as dbr
import utility as util
from utility import log_print
from classes import Spine, Book

import gpt
import gemini


# Choose between 'gpt' and 'gemini'
AI_OPTION = "gpt"

# OpenAI config. Valid GPT models for Booksight (as of 2024-05-04): gpt-4-turbo, gpt-4, gpt-3.5-turbo
GPT_MODEL = "gpt-4"
GPT_TEMP = 0.3

# Gemini config. Valid Gemini models for Booksight (as of 2024-05-04): gemini-pro (alias for gemini-1.0-pro)
GEMINI_MODEL = "gemini-pro"


def check_for_match(spine, isbn, color_filter, px_to_inches, second_pass=False):
    """
    Check for a positive match using dimension ratio comparison, average color, dominant color, and color palette
    comparisons. If a match is found, update the color filter and pixel-to-inch ratio and return a confidence score.

    Args:
        spine (Spine): A Spine object.
        isbn (str): The ISBN of the book.
        color_filter (list): A list of RGB values to filter colors.
        px_to_inches (float): The pixel-to-inch ratio.
        second_pass (bool): Whether to skip dimension checks.

    Returns:
        tuple: A tuple containing the confidence score, updated color filter, updated pixel-to-inch ratio, and whether a second pass is needed.
    """
    if spine.height == None or spine.width == None or spine.text == None:
        log_print(f"\nSpine data is incomplete. This book likely went undetected by torchvision and was picked up by AI in full image OCR text.\n")
        log_print(f"\nPopulating Book Object with general data and skipping match process.\n")
        confidence = 0
        p_match = dbr.get_isbn_info(isbn)
        # Check if english language
        if p_match and p_match["language"].lower().strip() not in ["en", "eng", "english", "English", "EN", "ENG", "ENGLISH", "En"]:
            log_print(f"Language: {p_match['language']}")
            log_print("Booksight only supports English books at this time.\n")
            return confidence, color_filter, px_to_inches, second_pass, isbn
        else:
            confidence = 5
            return confidence, color_filter, px_to_inches, second_pass, isbn
    
    set_local_img = False
    confidence = 0
    p_match = dbr.get_isbn_info(isbn)

    # Try to get an isbn13 if the provided isbn is not 13 digits
    if len(isbn) != 13:
        p_match_isbn13 = p_match["isbn13"] if p_match else None
        if p_match_isbn13 != None:
            isbn = p_match["isbn13"]
            p_match = dbr.get_isbn_info(isbn)

    # Confirm that language is English 
    # TODO: Add language detection
    
    if p_match and p_match["language"].lower().strip() not in ["en", "eng", "english", "English", "EN", "ENG", "ENGLISH", "En"]:
        log_print(f"Language: {p_match['language']}")
        log_print("Booksight only supports English books at this time.\n")
        return confidence, color_filter, px_to_inches, second_pass, isbn
    
    # Confirm that spine.title is included in p_match title
    if p_match and spine.title.lower().strip() in p_match["title"].lower().strip():
        pass
    else:
        p_match_title = p_match["title"] if p_match else None
        if p_match_title != None:
            log_print(f"Title mismatch: '{p_match['title']}' -- '{spine.title}'\n")
            return confidence, color_filter, px_to_inches, second_pass, isbn
        else:
            log_print(f"Title not found in ISBNdb data.\n")
            return confidence, color_filter, px_to_inches, second_pass, isbn
    
    # Check if essential data is missing or incorrect
    if second_pass:
        log_print("\nSecond pass, skipping dimension checks.\n")
        if not p_match:
            # Create a fake p_match with the spine dimensions
            p_match = {
                "height": spine.height * px_to_inches if px_to_inches else spine.height,
                "width": spine.width * px_to_inches if px_to_inches else spine.width,
                "cover": spine.image_path
            }
            set_local_img = True
        elif "height" not in p_match or "width" not in p_match or not p_match["height"] or not p_match["width"]:
            p_match["height"] = spine.height * px_to_inches if px_to_inches else spine.height
            p_match["width"] = spine.width * px_to_inches if px_to_inches else spine.width
            if "cover" not in p_match:
                p_match["cover"] = spine.image_path
                set_local_img = True

    else:
        if not p_match or "height" not in p_match or "width" not in p_match or not p_match["height"] or not p_match["width"]:
            log_print("\nEssential dimension data is missing or zero, skipping match checks for this ISBN.\n")
            return confidence, color_filter, px_to_inches, second_pass, isbn

    # Calculate ratios if dimensions are valid
    p_match_height = p_match["height"]
    p_match_width = p_match["width"]
    p_match_ratio = p_match_height / p_match_width if p_match_width else 0
    log_print(f"\np_match dimensions:\nheight: {p_match_height}, width: {p_match_width}, ratio: {p_match_ratio}\n")

    spine_height = spine.height * px_to_inches if px_to_inches else spine.height
    spine_width = spine.width * px_to_inches if px_to_inches else spine.width
    spine_ratio = spine_height / spine_width if spine_width else 0
    log_print(f"\nspine dimensions:\nheight: {spine_height}, width: {spine_width}, ratio: {spine_ratio}\n")

    # Dimension checks
    if not second_pass:
        if px_to_inches != 1:
            if 0.8 * spine_height <= p_match_height <= 1.2 * spine_height:
                confidence += 0.3
                log_print("\np_match height match within 20%, confidence + 0.25\n")
            if 0.8 * spine_width <= p_match_width <= 1.2 * spine_width:
                confidence += 0.2
                log_print("\np_match width match within 20%, confidence + 0.25\n")

        # Ratio checks
        if p_match_ratio and 0.7 * p_match_ratio <= spine_ratio <= 1.3 * p_match_ratio:
            confidence += 0.3
            px_to_inches = p_match["height"] / spine.height
            log_print("\np_match ratio match within 30% , confidence + 0.3\n\npx_to_inches set to: {px_to_inches}\n")
            if 0.8 * p_match_ratio <= spine_ratio <= 1.2 * p_match_ratio:
                confidence += 0.2
                log_print("\np_match ratio match within 20%, confidence + 0.2\n")


    # Download cover image
    p_match_cover_url = p_match["cover"]

    if set_local_img:
        p_match_cover_path = p_match_cover_url
    else:
        p_match_cover_path = download_image(p_match_cover_url, isbn)

    # Retrieve color data for cover image
    p_avg_color = asp.find_average_color_simple(p_match_cover_path)
    p_dom_color, p_color_palette, h, w = asp.find_color_palette(p_match_cover_path)
    avg_color, dom_color, color_palette = spine.avg_color, spine.dominant_color, spine.color_palette

    log_print(f"\np_match_color_data:\navg:{p_avg_color},\n{p_dom_color},\n{p_color_palette}\n")
    log_print(f"\nspine_color_data:\navg:{avg_color},\n{dom_color},\n{color_palette}\n")

    # Apply color filter
    avg_color = tuple([avg_color[i] * color_filter[i] for i in range(3)])
    dom_color = tuple([dom_color[i] * color_filter[i] for i in range(3)])
    color_palette = [tuple([color_palette[i][j] * color_filter[j] for j in range(3)]) for i in range(6)]

    # Compare average color
    avg_color_diff = sum([abs(avg_color[i] - p_avg_color[i]) for i in range(3)]) / 3
    log_print(f"\navg_color_diff: {avg_color_diff} for {isbn}\n")
    if avg_color_diff < 100:
        confidence += 0.2
        # if color_filter not 1, 1, 1 find average color filter
        if color_filter != [1, 1, 1]:
            old_filter = color_filter
            new_filter = [p_avg_color[i] / avg_color[i] for i in range(3)]
            color_filter = [(new_filter[i] + old_filter[i]) / 2 for i in range(3)]
        else:
            color_filter = [p_avg_color[i] / avg_color[i] for i in range(3)]

        # dilute the filter to avoid overfitting, 80% dilution
        color_filter = [(color_filter[i] + 4) / 5 for i in range(3)]

        log_print(f"\navg color match, confidence + 0.2\n\nColor filter set to: {color_filter}\n ")
    if avg_color_diff < 50:
        confidence += 0.3
        log_print("\navg color match, confidence + 0.3\n")
    # Compare dominant color
    dom_color_diff = sum([abs(dom_color[i] - p_dom_color[i]) for i in range(3)]) / 3
    log_print(f"\ndom_color_diff: {dom_color_diff} for {isbn}\n")
    if dom_color_diff < 100:
        confidence += 0.2
        log_print("\ndom color match, confidence + 0.2\n")
    if dom_color_diff < 50:
        confidence += 0.3
        log_print("\ndom color match, confidence + 0.2\n")

    # Compare color palette
    palette_diff = 0
    for i in range(6):
        palette_diff += sum([abs(color_palette[i][j] - p_color_palette[i][j]) for j in range(3)]) / 3

    log_print(f"\npalette_diff: {palette_diff} for {isbn}\n")
    if palette_diff < 600:
        confidence += 0.2
        log_print("\npalette match, confidence + 0.2\n")
    if palette_diff < 300:
        confidence += 0.3
        log_print("\npalette match, confidence + 0.3\n")


    log_print(f"\nMatch confidence: {confidence}\ncolor_filter: {color_filter}\npx_to_inches: {px_to_inches}\n")
    return confidence, color_filter, px_to_inches, second_pass, isbn


def download_image(url, isbn):
    """
    Download an image from a URL and save it to a local directory.

    Args:
        url (str): The URL of the image to download.
        isbn (str): The ISBN of the book to use in the filename.

    Returns:
        str: The path to the downloaded image.
    """
    # Ensure the directory exists where the images will be saved
    directory = "vision/images/detection_temp/downloaded_images"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the path where the image will be saved
    image_path = os.path.join(directory, f"{isbn}.jpg")

    # Request the image from the web
    response = requests.get(url)
    if response.status_code == 200:
        # Open the image and save it to the file
        image = Image.open(BytesIO(response.content))
        image.save(image_path)
        log_print(f"Image saved to {image_path}")
        return image_path
    else:
        log_print(f"Failed to download the image. HTTP status: {response.status_code}")
        return None


### AI OCR Text Cleanup and External API ISBN Identification Functions ###
def id_possible_matches(spines, full_img_text):
    """
    Identify possible matches for each spine using AI and external APIs.

    Args:
        spines (list): A list of spine objects.
        full_img_text (str): The text detected in the full image.

    Returns:
        list: A list of spine objects with updated data.
    """
    log_print("\nPreparing text for AI input...\n")
    book_data_prompt = format_AI_input(spines, full_img_text)
    log_print(f"\nAI Prompt and Raw Book Data:\n{book_data_prompt}\n")

    start_ai_process = time.time()
    book_data_basic = identify_with_AI(book_data_prompt)
    book_dict = json.loads(book_data_basic)
    book_count = len(book_dict)
    end_ai_process = time.time()

    log_print(f"\nAI processing complete. Time elapsed: {round(end_ai_process - start_ai_process, 2)} seconds.\n")
    log_print(f"Number of books identified: {book_count}\n")
    log_print(f"\nBook Identification (Preliminary):\n\n{book_data_basic}\n")
    log_print("\n\n*****************************************************************************************\n\n")
    log_print("\nRetrieving potential ISBN's from OpenLibrary and Google Books...\nUpdating Spine objects with title, author, and possible ISBNs...\n")

    spine_count = len(spines)
    if book_count > spine_count:
        # create new spine objects for additional books (added to the end of the list)
        for i in range(spine_count, book_count):
            spines.append(Spine())

    # Update spines -- spine.author, spine.title
    for i, spine in enumerate(spines):
        book = book_dict[f"Book_{i}"]
        spine.author = book["author"]
        spine.title = book["title"]

    # Retrieve potential ISBN's from OpenLibrary/Google Books and update spine.possible_matches with list of ISBN's
    for spine in spines:
        spine.possible_matches = dbr.get_potential_isbns(spine.title, spine.author)
        
    return spines


def identify_with_AI(prompt):
    """
    Identify book titles and authors using AI. Choose between GPT and Gemini.

    Args:
        prompt (str): The prompt message for the AI model.

    Returns:
        str: The response from the AI model.
    """
    if AI_OPTION == "gpt":
        gpt_start = time.time()
        log_print(f"Beginning identification with {GPT_MODEL} set to a temperature of {GPT_TEMP}...\n ")
        response = gpt.run_gpt(prompt, GPT_MODEL, GPT_TEMP)
        gpt_end = time.time()
        log_print(f"Identification with {GPT_MODEL} complete.\nTime elapsed: {round(gpt_end - gpt_start, 2)} seconds.\n")
    elif AI_OPTION == "gemini":
        gemini_start = time.time()
        log_print(f"Beginning identification with {GEMINI_MODEL}...\n")
        response = gemini.run_gemini(prompt, GEMINI_MODEL)
        gemini_end = time.time()
        log_print(f"Identification with {GEMINI_MODEL} complete.\nTime elapsed: {round(gemini_end - gemini_start, 2)} seconds.\n")
    else:
        log_print("Invalid AI option. Please choose 'gpt' or 'gemini'.\n")
        response = None

    return response

correct_output = """{
            "Book_0": {"author": "Junji Ito", "title": "Uzumaki"},
            "Book_1": {"author": "Mary Beard", "title": "SPQR: A History of Ancient Rome"},
            "Book_2": {"author": "Haruki Murakami", "title": "Norwegian Wood"},
            "Book_3": {"author": "Sebastian Junger", "title": "War"},
            "Book_4": {"author": "Denis Johnson", "title": "The Laughing Monsters"}}"""

def format_AI_input(spines, full_img_text):
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

    spine_img_text = f"\nIndividual Spine OCR Text:\n{book_data}\nFull Image OCR Text:\n{full_img_text}"

    prompt = f"""You will receive a string formatted as list of text detected from spines of books, formatted like this --
        "Book_X: <OCR text>,". You must interpret the OCR text and identify each book's title and author. The OCR text may contain errors,
        unconventional spacing, or other issues that require intelligent parsing to deduce the correct information. Return a JSON-formatted
        string where each "Book_X" identifier is associated with an "author" and "title" key. If a book title and/or author cannot be confidently
        identified, use "Unknown" as the value. Correct all spelling and spacing errors in your response.
        
        The input text that follows "Full Image OCR Text: " is a scan of the full input image. If you have trouble identifying a spine's 
        text, there may be additional clues in the full image text. Additionally, there may be books whose spines went undetected. 
        The text from those books will not be included in the individual spine OCR text, but may be present in the full image OCR text. It is
        very important to cross-reference the individual spine text with the full image text to ensure all books are accounted for. If you receive
        OCR text for only two spines, but the full image text contains three book titles, you must identify the third book using the full image text
        and include that book in your response.

        Use every resource at your disposal to decipher the text and correctly identify all book titles and authors. Accuracy is critical. 

        - DO NOT MAKE UP BOOK TITLES OR AUTHORS. Use all of the data you have to identify a REAL author and REAL book title that would make 
        sense in the context of OCR text from the spine of a book. For Example, if you have some OCR text that says "HARY BFARD ROME Q R mistory", 
        You should be able to look through existing books and realize that the book is "SPQR" by Mary Beard. Do not make up any authors or titles. 

        - If you are only able to identify an author, you should search your knowledge to find all the books that author has written, then 
        use that information along with the other letters in the OCR text in order to determine which title is most likely to be correct. Use the 
        same problem solving logic if you are only able to identify a title.

        - If you cannot verify an author or title, respond with "" for the author or title. Just an empty string for that field.

        - Your response is being decoded directly with Python's json.loads() function. Make sure your response is in the correct format without
        any additional characters or formatting. Do not even label the response as JSON. Just provide the JSON-formatted string.

        - Here is an example of input and correct output, delimited by three backticks: 
        ```EXAMPLE INPUT: {spine_img_text}


        CORRECT OUTPUT FOR EXAMPLE: {correct_output}
        ```
        
        Here is the input text you will be working with, delimited by three backticks: 
        ```{spine_img_text}```

        Check your response. If you enter your response directly into Pythons json.loads() function, will there be any errors? Don't add any 
        additional text in your response whatsoever. Just the JSON object formatted as a string.
        """
    
    return prompt


### Book Identification and Metadata Retrieval. Create Book Object ###
def create_book_object(isbn, confidence):
    """
    Once a positive identification is made, this function creates a Book object and populates it with data from multiple sources,
    utilizing fallbacks if specific data points are missing.

    Args:
        isbn (str): The ISBN of the book.
        confidence (float): Confidence level in the book identification.

    Returns:
        Book: A Book object populated with metadata.
    """
    # Fetch data from multiple sources
    isbndb_data = dbr.get_all_data_isbndb(isbn)
    google_data = dbr.get_all_data_google(isbn)

    # Initialize the book object
    book = Book()

    # Utilize data from Google Books as primary source
    if google_data and 'items' in google_data and google_data['items']:
        volume_info = google_data['items'][0]['volumeInfo']
        book.title = volume_info.get('title', "")
        book.subtitle = volume_info.get('subtitle', "")
        book.authors = volume_info.get('authors', [])
        book.language = volume_info.get('language', "")
        book.publisher = volume_info.get('publisher', "")
        book.date_published = volume_info.get('publishedDate', "")
        book.description = volume_info.get('description', "")
        book.pages = volume_info.get('pageCount', 0)
        book.image_path = volume_info.get('imageLinks', {}).get('thumbnail', "")
        # Check if ISBN-13 is present
        if 'industryIdentifiers' in volume_info:
            for identifier in volume_info['industryIdentifiers']:
                if identifier['type'] == 'ISBN_13':
                    book.isbn13 = identifier['identifier']
                    book.isbn = book.isbn13
                elif identifier['type'] == 'ISBN_10':
                    book.isbn10 = identifier['identifier']

    # Try ISBNdb if Google Books data is missing. Do not overwrite existing data.
    if isbndb_data:
        isbndb_data = isbndb_data['book']
        if book.title == "" or book.title is None:
            book.title = isbndb_data.get('title', "")
        if book.subtitle == "" or book.subtitle is None:
            book.subtitle = isbndb_data.get('title_long', "")
        if book.authors == [] or book.authors is None:
            book.authors = isbndb_data.get('authors', [])
        if book.language == "" or book.language is None:
            book.language = isbndb_data.get('language', "")
        if book.publisher == "" or book.publisher is None:
            book.publisher = isbndb_data.get('publisher', "")
        if book.date_published == "" or book.date_published is None:
            book.date_published = isbndb_data.get('date_published', "")
        if book.description == "" or book.description is None:
            book.description = isbndb_data.get('description', "")
        if book.isbn13 == "" or book.isbn13 is None:
            book.isbn13 = isbndb_data.get('isbn13', "")
        if book.isbn10 == "" or book.isbn10 is None:
            book.isbn10 = isbndb_data.get('isbn10', "")
        if book.isbn == "" or book.isbn is None:
            book.isbn = book.isbn13 or book.isbn10
        if book.pages == 0 or book.pages is None:
            book.pages = isbndb_data.get('pages', 0)
        book.binding = isbndb_data.get('binding', "Unknown")
    
    # Set the confidence
    book.confidence = confidence

    return book