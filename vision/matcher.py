import json 
import math
import os
import requests
import time

from PIL import Image
from io import BytesIO

import analyze_spine as asp
import vision_config as vision_config 
import db_requests as dbr
import gpt as gpt
import gemini as gemini
import utility as util
import token_counter
from classes import Spine, Book

log_print = util.log_print




def check_for_match(spine, isbn, color_filter, nada=False):
    """
    Check for a positive match using dimension ratio comparison, average color, dominant color, and color palette
    comparisons. If a match is found, update the color filter and pixel-to-inch ratio and return a confidence score.

    Args:
        spine (Spine): A Spine object.
        isbn (str): The ISBN of the book.
        color_filter (tuple): A tuple containing the RGB values for the color filter.
        nada (bool): Whether to skip dimension checks.

    Returns:
        tuple: A tuple containing the confidence score, updated color filter, updated pixel-to-inch ratio, and whether it's a second pass.
    """
    # Assign confidence of 0 and get isbn info for this potential match
    confidence = 0

    # Flags for missing data (skip comps)
    missing_dimensions = False
    missing_image = False

    

    # Fetch ISBNdb data for comparison
    p_match = dbr.get_isbn_info(isbn)

    # Check if spine data is incomplete, return only if nada is True
    if not nada:
        # Check if ISBNdb data is found
        if not p_match:
            log_print(f"ISBNdb data not found for {isbn}. Skipping match process.\n")
            return confidence, color_filter, nada, isbn
        # Check if essential dimension data is missing
        if "height" not in p_match or "width" not in p_match:
            log_print("\nEssential dimension data is missing or zero, skipping match checks for this ISBN.\n")
            return confidence, color_filter, nada, isbn

    # Filter out non-English books
    if p_match["language"].lower().strip() not in ["en", "eng", "english"]:
        log_print(f"Language: {p_match['language']}")
        log_print("Booksight only supports English books at this time.\n")
        return confidence, color_filter, nada, isbn

    # Handle spines undetected by torchvision
    if spine.height is None or spine.width is None or spine.text is None:
        log_print(f"\nSpine data is incomplete. This book likely went undetected by torchvision and was picked up by AI in full image OCR text.\n")
        log_print(f"\nPopulating Book Object with general data and skipping match process.\n")
        confidence = 34
        return confidence, color_filter, nada, isbn

    # Confirm that spine.title is included in p_match title
    if spine.title.lower().strip() not in p_match["title"].lower().strip() and p_match["title"].lower().strip() not in spine.title.lower().strip():
        p_match_title = p_match["title"] if p_match else None
        if p_match_title != None:
            log_print(f"Title mismatch: '{p_match['title']}' -- '{spine.title}'\n")
            return confidence, color_filter, nada, isbn
        else:
            log_print(f"Title not found in ISBNdb data.\n")
            return confidence, color_filter, nada, isbn
    
    # Declare match if spine.title is included in p_match title or vice versa
    log_print(f"Title match: '{p_match['title']}' -- '{spine.title}'\n")
        
    # Confirm that the binding is not "Audio Cassette" or "Audio CD"
    if p_match["binding"]:
        if p_match and p_match["binding"].lower().strip() in ["audio cassette", "audio cd"]:
            log_print(f"Audio binding detected: '{p_match['binding']}'\nSkipping match process for isbn - {isbn}.\n")
            return confidence, color_filter, nada, isbn


    # If 'nada', that means none of isbns returned a high enough confidence in first pass.
    if nada:
        if not p_match:
            # Flag to disregard dimension and color checks
            missing_dimensions = True
            missing_image = True
            log_print(f"\nMissing data for {isbn}. Skipping dimension and color checks.\n")
        else:
            # Handle cases where p_match is missing essential data
            if "height" not in p_match or "width" not in p_match:
                missing_dimensions = True
                log_print(f"\nMissing dimension data for {isbn}. Skipping dimension checks.\n")
            if "cover" not in p_match:
                missing_image = True
                log_print(f"\nMissing cover image for {isbn}. Skipping color comparison.\n")


    # BEGIN MATCHING - Max potential confidence is 30
    log_print(f"Data validated, beginning comparison for {isbn}...\n")

    # DIMENSION DATA COMPARISON - Max potential confidence is 1.4
    if not missing_dimensions:
        # Calculate ratios if dimensions are valid
        p_match_height = p_match["height"]
        p_match_width = p_match["width"]
        p_match_ratio = p_match_height / p_match_width if p_match_width else 0
        log_print(f"p_match dimensions:\nheight: {p_match_height}, width: {p_match_width}, ratio: {p_match_ratio}\n")

        spine_ratio = spine.height / spine.width if spine.width else 0

        log_print(f"spine dimensions:\nheight: {spine.height}, width: {spine.width}, ratio: {spine_ratio}\n")

        # Confidence Calculations
        if not nada:
            confidence = calculate_confidence_ratios(p_match_ratio, spine_ratio, confidence, isbn)


    # COLOR DATA COMPARISON - Max potential confidence is 1.5
    if not missing_image: 
        # Download cover image for color comparison
        p_match_cover_path = download_image(p_match["cover"], isbn)
        if p_match_cover_path == None:
            log_print(f"Failed to download cover image for {isbn}. Skipping color comparison.\n")
            return confidence, color_filter, nada, isbn
        confidence, color_filter = compare_colors(spine, p_match_cover_path, confidence, color_filter, isbn)
    else: 
        log_print(f"Local image set for {isbn}. Skipping color comparison.\n")

    
    # Max potential confidence is 3.0
    confidence = round(confidence, 2)
    
    log_print(f"Comparisons for {isbn} complete.\n")
    log_print(f"Match confidence: {confidence}\ncolor_filter: {color_filter}\n")

    return confidence, color_filter, nada, isbn

    
def calculate_confidence_ratios(p_match_ratio, spine_ratio, confidence, isbn):
    log_print(f"Dimension ratio comparison for {isbn}\nCurrent confidence: {confidence}.\n\n")
    thresholds = [
        (0.7, 0.2),
        (0.8, 0.4),
        (0.9, 0.6),
        (0.95, 0.3)
    ]

    for threshold, increment in thresholds:
        if threshold * spine_ratio <= p_match_ratio <= (2 - threshold) * spine_ratio:
            confidence += increment
            log_print(f"p_match ratio match within {int((1 - threshold) * 100)}%, confidence + {increment}")

    return confidence


def compare_colors(spine, p_match_cover_path, confidence, color_filter, isbn):
    log_print(f"\nComparing colors for {isbn}...\nCurrent confidence: {confidence}.\nCurrent color filter: {color_filter}\n")

    # Retrieve color data for cover image
    p_avg_color = asp.find_average_color_simple(p_match_cover_path)
    p_dom_color, p_color_palette, h, w = asp.find_color_palette(p_match_cover_path)
    avg_color, dom_color, color_palette = spine.avg_color, spine.dominant_color, spine.color_palette

    log_print(f"p_match_color_data:\navg:{p_avg_color},\ndom:{p_dom_color},\npalette:{p_color_palette}\n")
    log_print(f"spine_color_data:\navg:{avg_color},\ndom:{dom_color},\npalette:{color_palette}\n")

    # Apply color filter
    avg_color = tuple([avg_color[i] * color_filter[i] for i in range(3)])
    dom_color = tuple([dom_color[i] * color_filter[i] for i in range(3)])
    color_palette = [tuple([color_palette[i][j] * color_filter[j] for j in range(3)]) for i in range(6)]

    log_print(f"Color filter applied to spine data:\navg:{avg_color},\ndom:{dom_color},\npalette:{color_palette}\n")


    # Compare average color - Max potential confidence is 0.5
    log_print(f"Avg Color Comparison for {isbn}...\n(max potential confidence: 0.5)") 
    avg_color_diff = sum([abs(avg_color[i] - p_avg_color[i]) for i in range(3)]) / 3
    log_print(f"avg_color_diff: {avg_color_diff} for {isbn}\n")
    if avg_color_diff < 100:
        confidence + 0.1
        log_print("Avg color weak match. Diff < 100.\nConfidence + 0.05.\nNo change to color filter.\n")

    if avg_color_diff < 40:
        confidence += 0.2
        log_print("Avg color match. Diff < 40.\nConfidence + 0.15.\nNo change to color filter.\n")
    elif avg_color_diff < 60:
        confidence += 0.1
        log_print("Avg color match. Diff < 60.\nConfidence + 0.1.\nNo change to color filter.\n")
    elif avg_color_diff < 80:
        confidence += 0.05 
        log_print("Avg color match. Diff < 80.\nConfidence + 0.05.\nNo change to color filter.\n")

    if avg_color_diff < 20:
        confidence += 0.2
        color_filter = [(p_avg_color[i] / avg_color[i] + (color_filter[i] * 5)) / 6 for i in range(3)]
        log_print("Avg color strong match. Diff < 20.\nConfidence + 0.2.\nColor filter updated with avg color data.\n")

    log_print(f"Avg Color comparison complete.\nColor filter updated to: {color_filter}\n")


    # Compare dominant color - Max potential confidence is 0.5
    log_print(f"Dom Color Comparison for {isbn}...\n(max potential confidence: 0.5)")
    dom_color_diff = sum([abs(dom_color[i] - p_dom_color[i]) for i in range(3)]) / 3
    log_print(f"\ndom_color_diff: {dom_color_diff} for {isbn}\n")

    if dom_color_diff < 150:
        confidence += 0.1
        # No change to filter
        log_print("Dom color weak match. Diff < 150.\nConfidence + 0.1.\nNo change to color filter.\n")
    if dom_color_diff < 100:
        confidence += 0.1
        log_print("Dom color match. Diff < 100.\nConfidence + 0.1.\nNo change to color filter.\n")
    if dom_color_diff < 50:
        confidence += 0.15
        log_print("Dom color strong match. Diff < 65.\nConfidence + 0.15.\nNo change to color filter.\n")
    if dom_color_diff < 30:
        confidence += 0.15
        # Update color filter by dividing p_dom_color by dom_color and averaging with current filter
        color_filter = [(p_dom_color[i] / dom_color[i] + (color_filter[i] * 5)) / 6 for i in range(3)]
        log_print("Dom color match. Diff < 35.\nConfidence + .15.\nColor filter updated with dom color data.\n")

    log_print(f"Dom Color comparison complete.\nColor filter updated to: {color_filter}\n")

    # Compare color palette - Max potential confidence is 0.5
    log_print(f"Color Palette Comparison for {isbn} - will NOT affect color filter\n(max potential confidence: 0.5)")
    palette_diff = 0
    for i in range(6):
        for j in range(3):
            palette_diff += abs(color_palette[i][j] - p_color_palette[i][j])
    palette_diff /= 18  

    log_print(f"\npalette_diff: {palette_diff} for {isbn}\n")

    if palette_diff < 300:
        confidence += 0.1
        log_print("Palette weak match. Diff < 300.\nConfidence + 0.1\n")
    if palette_diff < 200:
        confidence += 0.1
        log_print("Palette weak match. Diff < 200.\nConfidence + 0.1\n")
    if palette_diff < 150:
        confidence += 0.15
        log_print("Palette match. Diff < 150.\nConfidence + 0.15\n")
    if palette_diff < 75:
        confidence += 0.15
        log_print("Palette match. Diff < 75.\nConfidence + 0.15\n")

    log_print(f"Color Palette comparison complete.\nColor filter updated to: {color_filter}\n")
    return confidence, color_filter





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
    directory = "media/detection_temp/downloaded_images"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the path where the image will be saved
    image_path = os.path.join(directory, f"{isbn}.jpg")

    # Request the image from the web
    response = requests.get(url)

    if response.status_code == 200:
        # Open the image and save it to the file, BytesIO is used to handle the image as a file-like object
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
        None: If the AI output is invalid.
    """
    log_print("Preparing text for AI input...\n")
    book_data_prompt = format_AI_input(spines, full_img_text)
    log_print(f"AI Prompt and Raw Book Data:\n{book_data_prompt}\n")

    start_ai_process = time.time()
    book_data_basic = identify_with_AI(book_data_prompt)

    if not validate_ai_output(book_data_basic):
        log_print("AI output is invalid. Please check the AI model and try again.\n")
        return None
    
    book_dict = json.loads(book_data_basic)
    book_count = len(book_dict)
    log_print(f"Number of books identified: {book_count}\n")
    log_print(f"Book Identification (Preliminary):\n{book_data_basic}\n")

    end_ai_process = time.time()

    log_print(f"\nAI processing complete. Time elapsed: {round(end_ai_process - start_ai_process, 2)} seconds.\n")

    start_isbn_retrieval = time.time()
    log_print("\nRetrieving potential ISBNs from OpenLibrary and Google Books...\nUpdating Spine objects with title, author, and possible ISBNs...\n")

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
    
    end_isbn_retrieval = time.time()
    log_print(f"\nISBN retrieval complete. Time elapsed: {round(end_isbn_retrieval - start_isbn_retrieval, 2)} seconds.\n")
    return spines


def identify_with_AI(prompt):
    """
    Identify book titles and authors using AI, fixes typos and formatting errors from OCR. Choose between GPT and Gemini.

    Args:
        prompt (str): The prompt message for the AI model.

    Returns:
        str: The response from the AI model (JSON-formatted string with book titles and authors).
    """
    # Get AI model and temperature from config
    config_data = vision_config.get_config()
    ai_model = config_data.ai_model
    ai_temp = config_data.ai_temp

    # Count prompt tokens
    if ai_model.startswith("gpt"):
        prompt_tokens = token_counter.count_gpt_tokens(prompt, ai_model)
    elif ai_model.startswith("gemini"):
        prompt_tokens, prompt_chars = token_counter.count_gemini_tokens(prompt, 'prompt')

    # Run AI model
    if ai_model.startswith("gpt"):
        log_print(f"Prompt token count for {ai_model}: {prompt_tokens}\n")
        gpt_start = time.time()
        log_print(f"Beginning identification with {ai_model} set to a temperature of {ai_temp}...\n ")
        response = gpt.run_gpt(prompt, ai_model, ai_temp)
        gpt_end = time.time()
        # Count GPT response tokens
        response_tokens = token_counter.count_gpt_tokens(response, ai_model)
        log_print(f"Response token count for {ai_model}: {response_tokens}\n")
        log_print(f"Identification with {ai_model} complete.\nTime elapsed: {round(gpt_end - gpt_start, 2)} seconds.\n")
    elif ai_model.startswith("gemini"):
        log_print(f"Prompt token count for {ai_model}: {prompt_tokens}\n")
        log_print(f"Prompt character count for {ai_model}: {prompt_chars}\n")
        gemini_start = time.time()
        log_print(f"Beginning identification with {ai_model}...\n")
        response = gemini.run_gemini(prompt, ai_model)
        # Count Gemini response tokens
        count_dict = token_counter.count_gemini_tokens(response, 'response')
        response = response.text
        gemini_end = time.time()
        log_print(f"prompt token count: {count_dict["prompt_token_count"]},\ncandidate token count: {count_dict["candidates_token_count"]},\ntotal token count: {count_dict["total_token_count"]}\n\n")
        log_print(f"Identification with {ai_model} complete.\nTime elapsed: {round(gemini_end - gemini_start, 2)} seconds.\n")
    else:
        log_print("Invalid AI option. Please choose 'gpt' or 'gemini'.\n")
        response = None

    return response


def format_AI_input(spines, full_img_text):
    """
    Format all data to be included in prompt message

    Args:
        spines (list): A list of spine objects.
        full_img_text (str): The text detected in the full image.

    Returns:
        str: The formatted prompt message for the AI model.
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
        and include that book in your response. (see example 2 below for a demonstration of this scenario.)

        Use every resource at your disposal to decipher the text and correctly identify all book titles and authors. Accuracy is critical. 

        - DO NOT MAKE UP BOOK TITLES OR AUTHORS. Use all of the data you have to identify a REAL author and REAL book title that would make 
        sense in the context of OCR text from the spine of a book. For Example, if you have some OCR text that says "HARY BFARD ROME Q R mistory", 
        You should be able to look through existing books and realize that the book is "SPQR" by Mary Beard. Do not make up any authors or titles. 

        - If you are only able to identify an author, you should search your knowledge to find all the books that author has written, then 
        use that information along with the other letters in the OCR text in order to determine which title is most likely to be correct. Use the 
        same problem solving logic if you are only able to identify a title.

        - If you cannot verify an author or title, respond with "" for the author or title. Just an empty string for that field.

        - If a book has multiple authors, include both authors with no additional formatting. For example, if a book has two authors,
        "Author 1" and "Author 2", you would include "Author 1 Author 2" in the author field.

        - If you are not 100% certain that a subtitle is 100% accurate, do not include it. Your response will be used to query external APIs for
        ISBN information, so it is important that the data you provide is as accurate as possible.

        - Your response is being decoded directly with Python's json.loads() function. Make sure your response is in the correct format without
        any additional characters or formatting. Do not even label the response as JSON. Just provide the JSON-formatted string.

        - Here are two examples of input and correct output, each example is delimited by three backticks: 
        ```EXAMPLE INPUT 01: '''{example_input_01}'''


        CORRECT OUTPUT FOR EXAMPLE 01: '''{correct_output_01}'''
        ```
        
        ```EXAMPLE INPUT 02: '''{example_input_02}'''


        CORRECT OUTPUT FOR EXAMPLE 02: '''{correct_output_02}'''  
        ```

        * Read all instructions a second time before beginning. *

        Here is the real input text you will be working with, delimited by three backticks: 
        ```{spine_img_text}```

        Check your response. If you enter your response directly into Pythons json.loads() function, will there be any errors? Don't add any 
        additional text in your response whatsoever. Just the JSON object formatted as a string. Do not include any back ticks or quotation marks.
        """
    
    return prompt


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

    # Try ISBNdb if Google Books data is missing. Will not overwrite existing data.
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

    # If confidence is 0 or 34, set edition-specific data to empty strings
    if book.confidence == 0 or book.confidence == 34:
        book.publisher = ""
        book.date_published = ""
        book.binding = ""
        book.isbn13 = ""
        book.isbn10 = ""
        book.isbn = ""
        book.pages = ""

    return book


def validate_ai_output(response):
    """
    Validate the output from the AI model. Must be a valid JSON-formatted string.

    Args:
        response (str): The response from the AI model.

    Returns:
        bool: True if the response is valid, False otherwise.
    """
    try:
        json.loads(response)
        return True
    except json.JSONDecodeError:
        return False
    

### EXAMPLES FOR USE IN PROMPT ###
example_input_01 = """Individual Spine OCR Text:
Book_0: ['uiz', 'Mcbij', 'JUNJI ITO', 'JUNII ITO', 'UZUMAkI', 'UZUMAKL'],
Book_1: ['o} Aistont', 'Ului', 'History', 'ROME', 'o-~ Q m', 'BFARD', 'BEA RD', 'MA RY', 'Wumulii', 'MARY', '0 ~ Q x', '0i Ancieni'],
Book_2: ['HA R U K /', ' 0 R W E 6 |A N', 'W 0 0 D', 'N 0 R W E 6 |a M', 'W 0 0 d', 'haruki Murakami', 'M U R a K a M /'],
Book_3: ['STOrM', 'AVA', 'SEBASTIaI JuIGeR', 'New Tork', 'AUTHOR OF', 'AVAL', 'Auimor Of', 'NEW YORK', 'Sioat', 'TIMES', 'IME PtaftGT', 'The PERFECT', '1 WAR ipe SEBASTIAI JUHGER', 'D] WAR iI', 'BESTSELLER', 'TNIES'],
Book_4: ['SYR?', 'Rure)', 'LER', 'THE LAUGHIng MONSTERS 8', 'DENIS JOHNSON', 'IER', 'DENIS', 'THE LAUGHING MONSTERS', 'JDANSOM'],

Full Image OCR Text:
['0, HKtONT', 'BEARD', 'DEMIS', 'Ha R U k / M U Ra Ka M [', 'WaEJ', 'W 0 0 |', 'UZUMAkL', 'WAR i', 'Jtorm', 'Toinegiam', 'LAUGHING MONSTERS', 'WAR', 'Joci', "Laughing WOnsteRs Qo IeXIS H8XSIX'", 'SEBASTIaI JUIGER 644', 'BYARD', 'Authon Or', 'M0 0 d', 'M 0 R W E 6 |a M', 'THE', 'MEW Tort', 'JDHMSOM', 'Maiuii muiaiami', 'O >', 'DeSTSELLEA', 'ROMF', 'SEBASTIAH JUNGER 64', 'Mennnnt']
"""
correct_output_01 = """{
            "Book_0": {"author": "Junji Ito", "title": "Uzumaki"},
            "Book_1": {"author": "Mary Beard", "title": "SPQR"},
            "Book_2": {"author": "Haruki Murakami", "title": "Norwegian Wood"},
            "Book_3": {"author": "Sebastian Junger", "title": "War"},
            "Book_4": {"author": "Denis Johnson", "title": "The Laughing Monsters"}}"""

example_input_02 = """Individual Spine OCR Text:
Book_0: ['TIMES', 'of the', 'BESTSELLER', 'MONKEY GOD', 'PRESTON', 'douGLAS', 'MONKEY GOD 38', 'The', '0aa', 'centanl', 'NEW YORK', 'Dun', 'cunaat', 'Ujo', 'OaaND', 'Ovo', 'LOST CITY'],
Book_1: ['JUNGER', 'SEBASTIAN JUNGER', 'THE', 'PERFECT', 'STO RM', 'SEBASTIAN'],

Full Image OCR Text:
['MCRID', 'CARL', 'WORLD', 'THE PERTECT STORM', 'LOST CITY   MONKEY GOD', 'DOUCLAS', 'Housr', 'RiesTOH', 'SEBASTLAX JUNGER', 'DEMON-HAUNIED', "THE PERFECT' STORM", 'SAGAN', 'DLMOMIAUNIID', 'LOST CITY ? MONKEY GOD ]3 %#']"""

correct_output_02 = """{
            "Book_0": {"author": "Douglas Preston", "title": "The Lost City of the Monkey God"},
            "Book_1": {"author": "Sebastian Junger", "title": "The Perfect Storm"}}
            "Book_2": {"author": "Carl Sagan", "title": "Demon-Haunted World"}}"""