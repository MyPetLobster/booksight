import os
import time
import requests

import gemini
import gpt
import utility as util

from dotenv import load_dotenv
load_dotenv()

ISBN_COUNT = 10
ISBN_COUNT_COMBINED = 15

log_print = util.log_print


# Get potential ISBNs from Open Library and Google Books
def get_potential_isbns(title, author):
    """
    This function takes in an author and title and returns a list of all possible ISBNs from 
    Open Library and Google Books APIs.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.

    Returns:
        list: A list of ISBNs associated with the book.
    """
    openlibrary_isbns = get_isbns_openlibrary(title, author)
    google_isbns = get_isbns_google_books(title, author)
    
    all_isbns = openlibrary_isbns + google_isbns
    
    log_print(f"{title} - {author} all ISBNS: {all_isbns[:ISBN_COUNT_COMBINED]}\n")

    return all_isbns[:ISBN_COUNT_COMBINED]


def get_isbns_openlibrary(title, author):
    """
    This function queries the Open Library API to retrieve the ISBNs of a book given the title and author.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.

    Returns:
        list: A list of ISBNs associated with the book
    """
    # Query the Open Library API
    response = requests.get(f"https://openlibrary.org/search.json?title={title}&author={author}&limit=5")

    # If no results are found or API is down, return an empty list
    if response.status_code != 200 or response.json().get("numFound", 0) == 0:
        log_print(f"-- OpenLibrary API --\nError: {response.status_code}\nNumber of results: {response.json().get('numFound', 0)}\n")
        return []
    
    # Extract the ISBNs from the response
    isbns = []
    for result in response.json()["docs"]:
        isbns += result.get("isbn", [])
    
    log_print(f"Open Library ISBNs for {title} - {author}: {isbns}\n")

    return isbns[:ISBN_COUNT]


def get_isbns_google_books(title, author):
    """
    This function queries the Google Books API to retrieve the ISBNs of a book given the title and author.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.

    Returns:
        list: A list of ISBNs associated with the book
    """
    google_books_key = os.getenv("GOOGLE_BOOKS_KEY")

    # Query the Google Books API
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}+inauthor:{author}&maxResults=5&key={google_books_key}")

    # If no results are found or API is down, return an empty list
    if response.status_code != 200 or response.json().get("totalItems", 0) == 0:
        log_print(f"\n-- Google Books API --\nError: {response.status_code}\nNumber of results: {response.json().get('totalItems', 0)}\n")
        return []

    # Extract the ISBNs from the response
    isbns = []
    for item in response.json()["items"]:
        if item["volumeInfo"]["title"].lower() == title.lower():
            if "industryIdentifiers" in item["volumeInfo"]:
                for identifier in item["volumeInfo"]["industryIdentifiers"]:
                    if identifier["type"] == "ISBN_13" or identifier["type"] == "ISBN_10":
                        isbns.append(identifier["identifier"])

    log_print(f"Google Books ISBNs for {title} - {author}: {isbns}\n")

    return isbns[:ISBN_COUNT]


def get_isbn_info(isbn):
    """
    This function queries ISBNdb API to retrieve information about a book given its ISBN. Requires a paid API key.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        dict: A dictionary containing information about the book.
    """
    # Prevent rate limiting
    time.sleep(1)

    isbndb_key = os.getenv("ISBNDB_KEY")

    h = {'Authorization': isbndb_key}
    response = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
    
    if response.status_code == 200:
        # Get the 'Height' and 'Width' of the book
        book_info = response.json()

        log_print(f"ISBNdb Data for {isbn}:\n{book_info}\n")

        height, width = get_dimensions(book_info)
        language, cover = get_language_and_cover(book_info)

        return {
            "title": book_info["book"]["title"] if "title" in book_info["book"] else None,
            "height": height, 
            "width": width,
            "language": language,
            "cover": cover,
            "isbn13": book_info["book"]["isbn13"] if "isbn13" in book_info["book"] else None,
            "isbn10": book_info["book"]["isbn10"] if "isbn10" in book_info["book"] else None,
            "isbn": book_info["book"]["isbn"] if "isbn" in book_info["book"] else None,
            "binding": book_info["book"]["binding"] if "binding" in book_info["book"] else None,
        }
    else:
        log_print(f"Error: {response.status_code}")
        return None


def get_dimensions(book_info):
    """
    Extract dimensions from the book_info dictionary.

    Args:
        book_info (dict): A dictionary containing information about the book.

    Returns:
        tuple: A tuple containing the height and width of the book (float, float)
    """
    height = ""
    width = ""

    # Extract height and width from the book_info dictionary
    try:
        book_dimension_string = book_info["book"]["dimensions"]
        if "Height" in book_dimension_string:
            height = book_dimension_string.split(",")[0].split(":")[1].strip()
            height = height.split(" ")[0]
        if "Width" in book_dimension_string:
            width = book_dimension_string.split(",")[2].split(":")[1].strip()
            width = width.split(" ")[0]
    except KeyError:
        pass
    
    # Extraction if not found in the previous step. Account for different formats in API response.
    try:
        if height == "":
            height = book_info["book"]["dimensions_structured"]["height"]["value"]
        if width == "":
            width = book_info["book"]["dimensions_structured"]["width"]["value"]
    except KeyError:
        pass

    if height == "":
        height = 0
    else:
        height = float(height)

    if width == "":
        width = 0
    else:
        width = float(width)

    return height, width


def get_language_and_cover(book_info):
    """
    Extract language and cover from the book_info dictionary.

    Args:
        book_info (dict): A dictionary containing information about the book.

    Returns:
        tuple: A tuple containing the language and cover of the book (str, str)
    """
    if "language" not in book_info["book"] or book_info["book"]["language"] == "":
        language = "Unknown"
    else:
        language = book_info["book"]["language"]

    if "image" not in book_info["book"] or book_info["book"]["image"] == "":
        cover = "Unavailable"
    else:
        cover = book_info["book"]["image"]

    return language, cover


def get_all_data_isbndb(isbn):
    """
    This function queries ISBNdb API to retrieve information about a book given its ISBN.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        book_info (dict): A dictionary containing information about the book.
    """
    time.sleep(1) # Prevent rate limiting

    isbndb_key = os.getenv("ISBNDB_KEY")

    h = {'Authorization': isbndb_key}
    response = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
    
    if response.status_code == 200:
        book_info = response.json()
        return book_info
    else:
        log_print(f"\nError: {response.status_code}")
        return None
    

def get_all_data_google(isbn):
    """
    This function queries Google Books API to retrieve all information about a book given its ISBN.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        book_info (dict): A dictionary containing information about the book.
    """
    google_books_key = os.getenv("GOOGLE_BOOKS_KEY")
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={google_books_key}")

    if response.status_code == 200:
        book_info = response.json()
        return book_info
    else:
        log_print(f"\nError: {response.status_code}")
        return None
    

def get_all_data_openlibrary(isbn):
    """
    This function queries Open Library API to retrieve all information about a book given its ISBN.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        book_info (dict): A dictionary containing information about the book.
    """
    response = requests.get(f"https://openlibrary.org/isbn/{isbn}.json")

    if response.status_code == 200:
        book_info = response.json()
        return book_info
    else:
        log_print(f"\nError: {response.status_code}")
        return None
    

def validate_api_keys():
    """
    This function validates the API keys provided by the user. Only one of OpenAI or Google Gemini is required. 
    The rest of the keys are mandatory.
    
    Args:
        None: The API keys are stored in the environment variables.
        
    Returns:
        bool: True if all the keys are valid and necessary keys are present. False otherwise.
    """
    
    if not validate_google_books_api_key() or not validate_isbndb_api_key():
        return False
    if not validate_openai_api_key() and not validate_gemini_api_key():
        return False
    return True
    

def validate_google_books_api_key():
    """
    This function validates the Google Books API key provided by the user.

    Args:
        None: The Google Books API key is automatically set in the environment variables.

    Returns:
        bool: True if the key is valid. False otherwise.
"""
    google_books_key = os.getenv("GOOGLE_BOOKS_KEY")
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=sheltering+skyResults=5&key={google_books_key}")
    if response.status_code != 200:
        return False
    return True


def validate_isbndb_api_key():
    """
    This function validates the ISBNdb API key provided by the user.

    Args:
        None: The ISBNdb API key is automatically set in the environment variables. 
    Returns:
        bool: True if the key is valid. False otherwise.
    """
    isbndb_key = os.getenv("ISBNDB_KEY")
    h = {'Authorization': isbndb_key}
    response = requests.get(f"https://api2.isbndb.com/book/9780099520290", headers=h)
    if response.status_code != 200:
        return False
    return True


def validate_openai_api_key():
    """
    This function validates the OpenAI API key provided by the user.

    Args:
        None: The OpenAI API key is automatically set in the environment variables and is retrieved within the function.

    Returns:
        bool: True if the key is valid. False otherwise.
    """
    prompt = "In 50 words or less, describe the plot of the book 'Train Dreams' by Denis Johnson."
    model = 'gpt-4o'
    temperature = 0.5

    response = gpt.run_gpt(prompt, model, temperature)

    if not response:
        return False
    
    return True


def validate_gemini_api_key():
    """
    This function validates the Google Gemini API key provided by the user.

    Args:
        None: The Google Gemini API key is automatically set in the environment variables and is retrieved within the function.

    Returns:    
        bool: True if the key is valid. False otherwise.
    """
    prompt = "In 50 words or less, describe the plot of the book 'Tigana' by Guy Gavriel Kay."
    model = 'gemini-1.5-pro'
    
    response = gemini.run_gemini(prompt, model)

    if not response:
        return False
    
    return True

