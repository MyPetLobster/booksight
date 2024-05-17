from django.conf import settings
from django.core.mail import EmailMessage

import time
import csv
import json

import vision.utility as util


def export_to_csv(books):
    """
    This function takes a list of Book objects and exports them to a CSV file.
    
    Args:
        books (list): A list of Book objects.

    File saved to 'vision/exports/csv/books_<timestamp>.csv'
    """
    
    # Get the current timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Define the CSV file path
    csv_file = f"vision/exports/csv/books_{timestamp}.csv"
    
    # Define the fieldnames for the CSV file
    fieldnames = ['Title', 'Subtitle', 'Authors', 'Language', 'Publisher', 'Publish Date', 'Description', 'ISBN', 'ISBN10', 'ISBN13', 'Pages', 'Binding', 'Image Path', 'Confidence']
    
    # Write the Book objects to the CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for book in books:
            writer.writerow({
                'Title': book.title,
                'Subtitle': book.subtitle,
                'Authors': book.authors,
                'Language': book.language,
                'Publisher': book.publisher,
                'Publish Date': book.date_published,
                'Description': book.description,
                'ISBN': book.isbn,
                'ISBN10': book.isbn10,
                'ISBN13': book.isbn13,
                'Pages': book.pages,
                'Binding': book.binding,
                'Image Path': book.image_path,
                'Confidence': book.confidence
            })
    
    util.log_print(f"\nBooks exported to CSV: {csv_file}\n\n")

    with open(csv_file, mode='r') as file:
        util.log_print(file.read())
        util.log_print("\n\n")


def export_to_json(books):
    """
    This function takes a list of Book objects and exports them to a JSON file.
    
    Args:
        books (list): A list of Book objects.

    File saved to 'vision/exports/json/books_<timestamp>.json'
    """
    
    # Get the current timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Define the JSON file path
    json_file = f"vision/exports/json/books_{timestamp}.json"
    
    # Write the Book objects to the JSON file
    with open(json_file, 'w') as file:
        json.dump([book.__dict__ for book in books], file, indent=4)
    
    util.log_print(f"\nBooks exported to JSON: {json_file}\n\n")

    with open(json_file, mode='r') as file:
        util.log_print(file.read())
        util.log_print("\n\n")


def email_file(file_path, user_email):
    """
    This function sends an email with the specified file as an attachment.
    
    Args:
        file_path (str): The path to the file to be attached.
    """
    subject = 'Booksight Exported File'
    message = 'Thank you for using Booksight! Your exported file is attached.'
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user_email])
    email.attach_file(file_path)
    email.send()
    
    util.log_print(f"Email sent to: {user_email}\n")