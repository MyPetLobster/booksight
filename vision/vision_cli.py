# Before running the CLI, make sure to set the DJANGO_SETTINGS_MODULE and PYTHONPATH environment variables
# export DJANGO_SETTINGS_MODULE=booksight.settings
# export PYTHONPATH=/Users/corysuzuki/Documents/repos/booksight

import argparse
import os 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booksight.settings')
django.setup()

from .vision import vision_core, create_scan
from . import config as config
from . import utility as util

from dotenv import load_dotenv
load_dotenv()

log_print = util.log_print

def main():
    """Main entry point for the CLI. Parses command line arguments and calls the vision_core function."""
    # Clear all temp directories
    util.empty_export_dirs()
    util.empty_directory('media/uploaded_images')
    util.empty_directory('media/detection_temp/debug_images')
    util.empty_directory('media/detection_temp/downloaded_images')
    util.empty_directory('media/detection_temp/spines')

    # Create log file for new session
    util.create_log_file()

    log_print('Welcome to the Booksight Vision CLI\n')

    parser = argparse.ArgumentParser(description='Booksight Vision CLI')
    parser.add_argument('image_path', type=str, help='Path to the image to be processed')
    parser.add_argument('--ai-model', type=str, default='gpt-4o', help='AI model to use for image classification')
    parser.add_argument('--ai-temp', type=float, default=0.3, help='Temperature parameter for the AI model')
    parser.add_argument('--torch-confidence', type=float, default=0.79, help='Confidence threshold for TorchVision')
    args = parser.parse_args()

 
    image_path = args.image_path

    # Check to make sure image_path is valid
    i = 0
    while not os.path.exists(image_path):
        log_print('Invalid image path, please try again. Or press Ctrl+C to exit.')
        image_path = input('Enter the path to the image to be processed: ')
        if i > 2:
            log_print('Tip: You can drag and drop the image into the terminal to get the path.')
        i += 1

    log_print("Your settings:")
    log_print(f"Image Path: {args.image_path}")
    log_print(f"AI Model: {args.ai_model}")
    log_print(f"AI Temp: {args.ai_temp}")
    log_print(f"Torch Confidence: {args.torch_confidence}\n")

    settings_okay = input("Are these settings okay? (y/n): ")
    if settings_okay.lower() != 'y':
        image_path = input("Enter the path to the image to be processed: ")
        ai_model = input("Choose the AI model to use for image classification\nValid options: gpt-4o, gpt-3.5-turbo, gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-turbo\nEnter the model name: ")
        ai_temp = float(input("Enter the temperature parameter for the AI model (0.00-1.00): "))
        torch_confidence = float(input("Enter the confidence threshold for TorchVision (0.00-1.00): "))
    else: 
        image_path = args.image_path
        ai_model = args.ai_model
        ai_temp = args.ai_temp
        torch_confidence = args.torch_confidence
    
    log_print("As noted in the README, you must have a .env file in the root directory of the project.")
    log_print("This file should contain the following keys:")
    log_print("GOOGLE_GEMINI_KEY=<Your Google Gemini GenAI API Key>")
    log_print("GOOGLE_BOOKS_KEY=<Your Google Books API Key>")
    log_print("ISBNDB_KEY=<Your ISBNdb API Key>")
    log_print("OPENAI_API_KEY=<Your OpenAI API Key>\n")
    
    env_okay = input("Do you have a .env file with the required keys? (y/n): ")
    if env_okay.lower() != 'y':
        log_print("Do you want to manually enter the API keys now?")
        log_print("If you choose not to, the program will exit.")
        log_print("Only one of google_gemini_key and openai_key is required. The other two are mandatory.\n")
        enter_keys = input("Enter API keys? (y/n): ")
        if enter_keys.lower() != 'y':
            return
        google_gemini_key = input("Enter your Google Gemini GenAI API Key: ")
        google_books_key = input("Enter your Google Books API Key: ")
        isbndb_key = input("Enter your ISBNdb API Key: ")
        openai_key = input("Enter your OpenAI API Key: ")

    else:
        google_gemini_key = os.getenv('GOOGLE_GEMINI_KEY')
        google_books_key = os.getenv('GOOGLE_BOOKS_KEY')
        isbndb_key = os.getenv('ISBNDB_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')

    api_keys = {
        'google_gemini_key': google_gemini_key,
        'google_books_key': google_books_key,
        'isbndb_key': isbndb_key,
        'openai_key': openai_key
    }   
    
    log_print("Choose what format(s) you would like to export the results in.\nValid options: json, csv, txt, xml, all\n")
    log_print("You can choose multiple formats by separating them with a comma (e.g. json, csv)\n")
    formats = input("Enter the format(s): ").split(',')
    if 'all' in formats:
        formats = ['json', 'csv', 'txt', 'xml']

    log_print("Your files will be saved in the 'booksight/vision/exports' directory.\n")
    
    log_print("One last thing, do you want to receive an email with the results?")
    log_print("You must have a Gmail account and generate an 'app password' for this to work.")
    log_print("Alternatively, if you know your way around Python, feel free to modify the Django project settings to use the email provider of your choice.\n")
    send_email = input("Send email? (y/n): ")
    if send_email.lower() == 'y':
        email = input("Enter your email address: ")
    else:
        email = None

    
    vision_config = config.VisionConfig(email, formats, ai_model, ai_temp, torch_confidence, api_keys)
    config.set_config(vision_config)

    
    new_scan_image = image_path
    new_scan = create_scan(new_scan_image)

    
    # Run the vision_core function
    vision_core(image_path, new_scan)


if __name__ == '__main__':
    main()
