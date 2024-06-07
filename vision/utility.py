import os
import shutil
import time

from rich import print as rprint

date = time.strftime("%Y%m%d")




def create_log_file():
    """Creates new log directory each day and a new log file for each session."""
    global date
    date = time.strftime("%Y%m%d")

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    if not os.path.exists(f'booksight/logs/{date}'):
        os.makedirs(f'booksight/logs/{date}')
    with open(f'booksight/logs/{date}/booksight_{timestamp}.log', 'w') as file:
        file.write(f"Booksight log file for {timestamp}\n") 

        
def log_print(message):
    """Prints a message and logs it to a text file."""
    log_file = retrieve_last_log_file()
    with open(log_file, 'a') as file:
        file.write(f"{message}\n")
    rprint(message)


def retrieve_last_log_file():
    """Returns the path to the most recent log file."""
    date = time.strftime("%Y%m%d")
    log_dir = f'booksight/logs/{date}'
    if not os.path.exists(log_dir):
        yesterday = time.strftime("%Y%m%d", time.gmtime(time.time() - 86400))
        log_dir = f'booksight/logs/{yesterday}'
    log_files = os.listdir(log_dir)
    log_files.sort(reverse=True)
    
    return os.path.join(log_dir, log_files[0])


def empty_directory(directory): 
    """This function deletes all files in a directory."""
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