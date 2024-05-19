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

    return csv_file


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

    return json_file


def export_to_xml(books):
    """
    This function takes a list of Book objects and exports them to an XML file.
    
    Args:
        books (list): A list of Book objects.

    File saved to 'vision/exports/xml/books_<timestamp>.xml'
    """
    
    # Get the current timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Define the XML file path
    xml_file = f"vision/exports/xml/books_{timestamp}.xml"
    
    # Write the Book objects to the XML file
    with open(xml_file, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<books>\n')
        
        for book in books:
            file.write('  <book>\n')
            file.write(f'    <title>{book.title}</title>\n')
            file.write(f'    <subtitle>{book.subtitle}</subtitle>\n')
            file.write(f'    <authors>{book.authors}</authors>\n')
            file.write(f'    <language>{book.language}</language>\n')
            file.write(f'    <publisher>{book.publisher}</publisher>\n')
            file.write(f'    <publish_date>{book.date_published}</publish_date>\n')
            file.write(f'    <description>{book.description}</description>\n')
            file.write(f'    <isbn>{book.isbn}</isbn>\n')
            file.write(f'    <isbn10>{book.isbn10}</isbn10>\n')
            file.write(f'    <isbn13>{book.isbn13}</isbn13>\n')
            file.write(f'    <pages>{book.pages}</pages>\n')
            file.write(f'    <binding>{book.binding}</binding>\n')
            file.write(f'    <image_path>{book.image_path}</image_path>\n')
            file.write(f'    <confidence>{book.confidence}</confidence>\n')
            file.write('  </book>\n')
        
        file.write('</books>')
    
    util.log_print(f"\nBooks exported to XML: {xml_file}\n\n")

    with open(xml_file, mode='r') as file:
        util.log_print(file.read())
        util.log_print("\n\n")

    return xml_file


def export_to_text(books):
    """
    This function takes a list of Book objects and exports them to a text file.
    
    Args:
        books (list): A list of Book objects.

    File saved to 'vision/exports/text/books_<timestamp>.txt'
    """
    
    # Get the current timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Define the text file path
    text_file = f"vision/exports/text/books_{timestamp}.txt"
    
    # Write the Book objects to the text file
    with open(text_file, 'w') as file:
        for book in books:
            file.write(f"Title: {book.title}\n")
            file.write(f"Subtitle: {book.subtitle}\n")
            file.write(f"Authors: {book.authors}\n")
            file.write(f"Language: {book.language}\n")
            file.write(f"Publisher: {book.publisher}\n")
            file.write(f"Publish Date: {book.date_published}\n")
            file.write(f"Description: {book.description}\n")
            file.write(f"ISBN: {book.isbn}\n")
            file.write(f"ISBN10: {book.isbn10}\n")
            file.write(f"ISBN13: {book.isbn13}\n")
            file.write(f"Pages: {book.pages}\n")
            file.write(f"Binding: {book.binding}\n")
            file.write(f"Image Path: {book.image_path}\n")
            file.write(f"Confidence: {book.confidence}\n")
            file.write("\n")
    
    util.log_print(f"\nBooks exported to text: {text_file}\n\n")

    with open(text_file, mode='r') as file:
        util.log_print(file.read())
        util.log_print("\n\n")

    return text_file


def email_file(file_paths, user_email):
    """
    This function sends an email with the specified file as an attachment.
    
    Args:
        file_path (str): The path to the file to be attached.
    """
    file_count = len(file_paths)
    
    if file_count == 1:
        subject = 'Booksight Exported File'
        message = 'Thank you for using Booksight! Your exported file is attached.'
    else:
        subject = 'Booksight Exported Files'
        message = 'Thank you for using Booksight! Your exported files are attached.'

    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user_email])

    bounding_box_image = 'vision/images/detection_temp/spines/full_detected.jpeg'
    email.attach_file(bounding_box_image)
    
    for file_path in file_paths:
        email.attach_file(file_path)
    email.send()
    
    util.log_print(f"Email sent to: {user_email}\n")