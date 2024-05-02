import json
import os
import time
import requests
from dotenv import load_dotenv



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
    
    print(f"All ISBNs: {all_isbns}")
    return all_isbns



def get_isbns_openlibrary(title, author):
    """
    This function queries the Open Library API to retrieve the ISBNs of a book given the title and author.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.

    Returns:
        list: A list of ISBNs associated with the book, divided into chunks(lists) of 20.
    """

    # Query the Open Library API
    response = requests.get(f"https://openlibrary.org/search.json?title={title}&author={author}&limit=5")

    result_count = response.json()["numFound"]
    if result_count == 0:
        return ""
    
    # Extract the ISBNs from the response
    isbns = []
    for result in response.json()["docs"]:
        if "isbn" in result:
            isbns.extend(result["isbn"])

    return isbns


def get_isbns_google_books(title, author):
    """
    This function queries the Google Books API to retrieve the ISBNs of a book given the title and author.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.

    Returns:
        list: A list of ISBNs associated with the book, divided into chunks(lists) of 20.
    """

    # Query the Google Books API
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}+inauthor:{author}&maxResults=10")

    result_count = response.json()["totalItems"]
    if result_count == 0:
        return ""

    # Extract the ISBNs from the response
    isbns = []
    for item in response.json()["items"]:
        if "industryIdentifiers" in item["volumeInfo"]:
            for identifier in item["volumeInfo"]["industryIdentifiers"]:
                if identifier["type"] == "ISBN_13" or identifier["type"] == "ISBN_10":
                    isbns.append(identifier["identifier"])

    return isbns


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
    resp = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
    
    if resp.status_code == 200:
        # Get the 'Height' and 'Width' of the book
        book_info = resp.json()
        height, width = get_dimensions(book_info)
        language, cover = get_language_and_cover(book_info)
        return (height, width, language, cover)
    else:
        print(f"Error: {resp.status_code}")
        return None
    


def get_dimensions(book_info):
    height = ""
    width = ""
    height = book_info["book"]["dimensions"]["Height"].lower()
    height = height.replace(" inches", "")
    width = book_info["book"]["dimensions"]["Width"].lower()
    width = width.replace(" inches", "")

    # {'book': {'publisher': 'Atlas Contact', 'language': 'nl', 'image': 'https://images.isbndb.com/covers/28/42/9789025442842.jpg', 'title_long': 'Norwegian wood (Dutch Edition)', 'edition': '01', 'dimensions': 'Height: 8.2677 Inches, Length: 5.31495 Inches, Width: 0.90551 Inches', 'dimensions_structured': {'length': {'value': 5.31495, 'unit': 'inches'}, 'width': {'value': 0.90551, 'unit': 'inches'}, 'height': {'value': 8.2677, 'unit': 'inches'}}, 'pages': 317, 'date_published': '2013', 'authors': ['Murakami, Haruki'], 'title': 'Norwegian wood (Dutch Edition)', 'isbn13': '9789025442842', 'msrp': '0.00', 'binding': 'Paperback', 'isbn': '9025442846', 'isbn10': '9025442846'}}
    if height == "":
        height = book_info["book"]["dimensions_structured"]["height"]["value"]
    if width == "":
        width = book_info["book"]["dimensions_structured"]["width"]["value"]

    return height, width

def get_language_and_cover(book_info):
    language = book_info["book"]["language"]
    cover = book_info["book"]["image"]

    return language, cover

def main():
    isbns = get_potential_isbns("Norwegian Wood", "Haruki Murakami")

    print("\nISBNdb API\n")
    # Get ISBN info for all Open Library ISBNs
    for isbn in isbns:
        get_isbn_info(isbn)
        # wait one second
        time.sleep(1)





if __name__ == "__main__":
    main()