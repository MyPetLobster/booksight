import base64
import os
import shutil
import time
from PIL import Image

from mimetypes import guess_type
from rich import print as rprint

timestamp = time.strftime("%Y%m%d-%H%M%S")
date = time.strftime("%Y%m%d")


def create_log_file():
    """ Creates a log file for the current session. """
   # Create new log dir for each day formatted like 'booksight/logs/240515/booksight_{timestamp}.log'
    if not os.path.exists(f'booksight/logs/{date}'):
        print(f"Creating new log directory for {date}")
        os.makedirs(f'booksight/logs/{date}')

    print(f"Creating new log file for {timestamp} ****")
    with open(f'booksight/logs/{date}/booksight_{timestamp}.log', 'w') as file:
        file.write(f"Booksight log file for {timestamp}\n") 
    

def log_print(message):
    """ Prints a message and logs it to a text file. """
    
    with open(f'booksight/logs/{date}/booksight_{timestamp}.log', 'a') as file:
        file.write(f"{message}\n")
    rprint(message)


def retrieve_last_log_file():
    """ Returns the path to the most recent log file. """
    
    log_dir = f'booksight/logs/{date}'
    log_files = os.listdir(log_dir)
    log_files.sort(reverse=True)
    
    return os.path.join(log_dir, log_files[0])


def empty_directory(directory): 
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            log_print(f"Failed to delete {file_path}. Reason: {e}")


def empty_export_dirs():
    """ This function deletes all except the 5 most recent exports in each export directory.
     'vision/exports/csv', 'vision/exports/json', 'vision/exports/xml', 'vision/exports/text'"""

    export_directories = ['csv', 'json', 'xml', 'text']

    for directory in export_directories:
        export_dir = f'vision/exports/{directory}'
        files = os.listdir(export_dir)
        files.sort()
        for file in files[:-5]:
            file_path = os.path.join(export_dir, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                log_print(f"Failed to delete {file_path}. Reason: {e}")


def convert_img_to_data(image_path):
    """ Converts an image file to base64 data. """

    mime_type, _ = guess_type(image_path)

    if mime_type is None:
        mime_type = "image/jpeg"
    with open(image_path, "rb") as image_file:
        # Shrink image to max size of 500px
        image = Image.open(image_file)
        image.thumbnail((500, 500))

        # save as new image (append _resized to filename)
        image.save(f"{image_path}_resized", "JPEG")
                   
        with open(f"{image_path}_resized", "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:{mime_type};base64,{image_data}"