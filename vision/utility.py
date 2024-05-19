import os
import shutil
import time

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



# Delete all files temp files
def empty_directories():
    directories = ["vision/images/detection_temp/debug_images", "vision/images/detection_temp/spines", "vision/images/detection_temp/downloaded_images"]
    for directory in directories:
        empty_directory(directory)


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