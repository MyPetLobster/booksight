import json
import os
import time
import requests
from dotenv import load_dotenv



load_dotenv()
ISBNDB_API_KEY = os.getenv("ISBNDB_API_KEY")


def get_isbns(title, author):
    """
    This function takes in an author and title and returns a list of all possible ISBNs from 
    Open Library and Google Books APIs.
    """
    openlib_isbns = get_isbns_openlibrary(title, author)
    google_isbns = get_isbns_google_books(title, author)
    
    all_isbns = openlib_isbns + google_isbns
    
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

    isbn_set = set(isbns)
    # isbn_chunks = [list(isbn_set)[i:i + 20] for i in range(0, len(isbn_set), 20)]

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

    isbns

    return isbns


def get_isbn_info(isbn):
    """
    This function queries ISBNdb API to retrieve information about a book given its ISBN. Requires a paid API key.

    Args:
        isbn (str): The ISBN of the book.

    Returns:
        dict: A dictionary containing information about the book.
    """

    h = {'Authorization': ISBNDB_API_KEY}
    resp = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers=h)
    
        
    print("\n**********************\n")
    print(f"\nISBN: {isbn}\n")
    print(resp.json())
    print("\n**********************\n")



def main():
    # title = "Norwegian Wood"
    # author = "Haruki Murakami"
    # isbns = get_isbns_openlibrary(title, author)
    # openlib_result_count = len(isbns)
    # print("\n**********************\n")
    # print("\nOpen Library API\n")
    # print(isbns)
    # print("\n**********************\n")

    # g_isbns = get_isbns_google_books(title, author)
    # print("\n**********************\n")
    # print("\nGoogle Books API\n")
    # print(g_isbns)
    # print("\n**********************\n")

    # print(f"\nOpen Library ISBNs: {openlib_result_count}\n")
    # print(f"Google Books ISBNs: {len(g_isbns)}\n")

    # get first ISBN info
    # print("\n**********************\n")
    # print(f"ISBN Info for {g_isbns[0]}")
    # get_isbn_info(g_isbns[0])

    isbns = get_isbns("Norwegian Wood", "Haruki Murakami")

    print("\nISBNdb API\n")
    # Get ISBN info for all Open Library ISBNs
    for isbn in isbns:
        get_isbn_info(isbn)
        # wait one second
        time.sleep(1)





if __name__ == "__main__":
    main()