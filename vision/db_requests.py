import os
import time
import requests
from dotenv import load_dotenv

from .utility import log_print

load_dotenv()
ISBNDB_API_KEY = os.getenv("ISBNDB_API_KEY")


# Get potential ISBNs from Open Library and Google Books
def get_potential_isbns(title, author):
    """
    This function takes in an author and title and returns a list of all possible ISBNs from 
    Open Library and Google Books APIs.
    """
    openlibrary_isbns = get_isbns_openlibrary(title, author)
    google_isbns = get_isbns_google_books(title, author)
    
    all_isbns = openlibrary_isbns + google_isbns
    
    log_print(f"\n{title} - {author}: {all_isbns}\n")

    return all_isbns[:10]



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
    if response.status_code != 200:
        log_print(f"Error: {response.status_code}")
        return []
    
    result_count = response.json()["numFound"]
    if result_count == 0:
        return []
    
    # Extract the ISBNs from the response
    isbns = []
    for result in response.json()["docs"]:
        isbns += result.get("isbn", [])
    
    log_print(f"\n\nOpen Library ISBNs for {title} - {author}: {isbns}\n\n")
    return isbns[:10]


def get_isbns_google_books(title, author):
    """
    This function queries the Google Books API to retrieve the ISBNs of a book given the title and author.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.

    Returns:
        list: A list of ISBNs associated with the book, divided into chunks(lists) of 20.
    """

    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    # Query the Google Books API
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}+inauthor:{author}&maxResults=5&key={api_key}")

    # If no results are found or API is down, return an empty list
    if response.status_code != 200:
        log_print(f"Error: {response.status_code}")
        return []
    
    if response.json().get("totalItems", 0) == 0:
        return []
    
    # Extract the ISBNs from the response
    isbns = []
    for item in response.json()["items"]:
        # Check if title matches
        if item["volumeInfo"]["title"].lower() == title.lower():
            if "industryIdentifiers" in item["volumeInfo"]:
                for identifier in item["volumeInfo"]["industryIdentifiers"]:
                    if identifier["type"] == "ISBN_13" or identifier["type"] == "ISBN_10":
                        isbns.append(identifier["identifier"])
    log_print(f"\n\nGoogle Books ISBNs for {title} - {author}: {isbns}\n\n")
    return isbns[:10]


# Get book information using ISBNdb API
def get_isbn_info(isbn):
    """
    This function queries ISBNdb API to retrieve information about a book given its ISBN. Requires a paid API key.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        dict: A dictionary containing information about the book.
    """
    time.sleep(1) # Prevent rate limiting

    h = {'Authorization': ISBNDB_API_KEY}
    response = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
    
    if response.status_code == 200:
        # Get the 'Height' and 'Width' of the book
        book_info = response.json()

        log_print(f"\nData for {isbn}:\n\n{book_info}\n")

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
        }
    else:
        log_print(f"Error: {response.status_code}")
        return None

# Book Info:
# {'book': {'publisher': 'Devir Livraria', 'language': 'pt', 'image': 'https://images.isbndb.com/covers/69/09/9788575326909.jpg', 'title_long': 'Uzumaki', 'dimensions': 'Height: 1.6535433054 Inches, Length: 9.448818888 Inches, Weight: 0 Pounds, Width: 6.4566929068 Inches', 'dimensions_structured': {'length': {'value': 9.448818888, 'unit': 'inches'}, 'width': {'value': 6.4566929068, 'unit': 'inches'}, 'weight': {'value': 0, 'unit': 'pounds'}, 'height': {'value': 1.6535433054, 'unit': 'inches'}}, 'date_published': '2021', 'authors': ['Junji Ito'], 'title': 'Uzumaki', 'isbn13': '9788575326909', 'msrp': '0.00', 'binding': 'Paperback', 'isbn': '8575326902', 'isbn10': '8575326902'}}


def get_dimensions(book_info):
    """
    Extract dimensions from the book_info dictionary.
    """
    height = ""
    width = ""

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
    This function queries ISBNdb API to retrieve information about a book given its ISBN. Requires a paid API key.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        dict: A dictionary containing information about the book.
    """
    time.sleep(1) # Prevent rate limiting

    h = {'Authorization': ISBNDB_API_KEY}
    resp = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
    
    if resp.status_code == 200:
        # Get the 'Height' and 'Width' of the book
        book_info = resp.json()
        return book_info
    else:
        log_print(f"Error: {resp.status_code}")
        return None
    

def get_all_data_google(isbn):
    """
    This function queries Google Books API to retrieve all information about a book given its ISBN.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        dict: A dictionary containing information about the book.
    """
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}")

    if response.status_code == 200:
        book_info = response.json()
        return book_info
    else:
        log_print(f"Error: {response.status_code}")
        return None
    

def get_all_data_openlibrary(isbn):
    """
    This function queries Open Library API to retrieve all information about a book given its ISBN.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        dict: A dictionary containing information about the book.
    """
    response = requests.get(f"https://openlibrary.org/isbn/{isbn}.json")

    if response.status_code == 200:
        book_info = response.json()
        return book_info
    else:
        log_print(f"Error: {response.status_code}")
        return None
    


def test_isbndb_response():
    isbn = "9780099520290"
    book_info = get_all_data_isbndb(isbn)
    log_print(book_info)


if __name__ == "__main__":
    test_isbndb_response()