import os
import shutil
import time

timestamp = time.strftime("%Y%m%d-%H%M%S")

def create_log_file():
    """ Creates a log file for the current session. """
    
    with open(f'vision/logs/booksight_{timestamp}.log', 'w') as file:
        file.write(f"Booksight Log - {timestamp}\n\n")

def log_print(message):
    """ Prints a message and logs it to a text file. """
    
    with open(f'vision/logs/booksight_{timestamp}.log', 'a') as file:
        file.write(f"{message}\n")
    print(message)



# Delete all files temp files
def empty_directories():
    directories = ["vision/images/detection_temp/debug_images", "vision/images/detection_temp/spines", "vision/images/detection_temp/downloaded_images", "vision/exports/csv", "vision/exports/json"]
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