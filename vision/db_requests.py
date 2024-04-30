import json
import requests
from dotenv import load_dotenv



load_dotenv()


def get_isbns_openlibrary(title, author):
    """
    This function queries the Open Library API to retrieve the ISBNs of a book given the title and author.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.

    Returns:
        list: A list of ISBNs associated with the book.
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


def main():
    title = "The Great Gatsby"
    author = "F. Scott Fitzgerald"
    isbns = get_isbns_openlibrary(title, author)
    print(isbns)

    isbn_count = len(isbns)
    isbn_set = set(isbns)
    
    # divide isbn set into chunks of 100 isbns
    isbn_chunks = [list(isbn_set)[i:i + 100] for i in range(0, len(isbn_set), 100)]
    for chunk in isbn_chunks:
        print("************************")
        print(chunk)


if __name__ == "__main__":
    main()