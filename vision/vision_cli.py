# Before running the CLI, make sure to set the DJANGO_SETTINGS_MODULE and PYTHONPATH environment variables
# export DJANGO_SETTINGS_MODULE=booksight.settings
# export PYTHONPATH=/Users/corysuzuki/Documents/repos/booksight

import argparse
import os
import time


from vision import vision_core, create_scan
import vision_config
import utility as util

from dotenv import load_dotenv
load_dotenv()

log_print = util.log_print

def main():
    # Clear all temp directories
    util.empty_export_dirs()
    util.empty_directory('media/uploaded_images')
    util.empty_directory('media/detection_temp/debug_images')
    util.empty_directory('media/detection_temp/downloaded_images')
    util.empty_directory('media/detection_temp/spines')

    # Create log file for new session
    util.create_log_file()
    log_print('\n\n\n\nWelcome to the Booksight Vision CLI App\n\n')
    time.sleep(3.5)
    log_print("The website might look cool but this is more fun, let's be honest\n\n")
    time.sleep(3)
    log_print("First, please pay VERY CLOSE attention to the following instructions:\n")
    time.sleep(1.5)
    log_print("struct group_info init_groups = { .usage = ATOMIC_INIT(2) };")
    time.sleep(.7)
    log_print("struct group_info *groups_alloc(int gidsetsize){")
    time.sleep(.5)
    log_print("    struct group_info *group_info;")
    time.sleep(.4)
    log_print("    int nblocks;")
    time.sleep(.3)
    log_print("    int i;")
    time.sleep(.7)
    log_print("    nblocks = (gidsetsize + NGROUPS_PER_BLOCK - 1) / NGROUPS_PER_BLOCK;")
    time.sleep(.4)
    log_print("    nblocks = nblocks ? : 1;")
    time.sleep(.7)
    log_print("    group_info = kmalloc(sizeof(*group_info) + nblocks*sizeof(gid_t *), GFP_USER);")
    time.sleep(.4)
    log_print("    if (!group_info)")
    time.sleep(.3)
    log_print("        return NULL;")
    time.sleep(.5)
    log_print("    group_info->ngroups = gidsetsize;")
    time.sleep(.4)
    log_print("...")
    time.sleep(2)
    log_print("......")
    time.sleep(2)
    log_print(".........")
    time.sleep(1.5)
    log_print("............type your response anytime...\n\n")
    time.sleep(3)
    log_print("lol jk i dont have a clue what any of that is. Shout out https://hackertyper.net/")
    time.sleep(3)

    log_print("\n\nOk for real now.\nLet's get started with the CLI setup...\n\n")
    time.sleep(3)

    log_print("Parsing arguments...\n")
    time.sleep(2)
    parser = argparse.ArgumentParser(description='Booksight Vision CLI')
    parser.add_argument('image_path', type=str, help='Path to the image to be processed')
    parser.add_argument('--ai-model', type=str, default='gpt-4o', help='AI model to use for image classification')
    parser.add_argument('--ai-temp', type=float, default=0.3, help='Temperature parameter for the AI model')
    parser.add_argument('--torch-confidence', type=float, default=0.79, help='Confidence threshold for TorchVision')
    args = parser.parse_args()

    image_path = args.image_path

    log_print("Checking image path...\n")
    time.sleep(2)
    i = 0
    while not os.path.exists(image_path):
        log_print('Invalid image path, please try again. Or press Ctrl+C to exit.')
        image_path = input('Enter the path to the image to be processed: ')
        if i > 2:
            log_print('Tip: You can drag and drop the image into the terminal to get the path.')
        i += 1

    log_print("Your settings:")
    time.sleep(1)
    log_print(f"Image Path: {args.image_path}")
    time.sleep(0.5)
    log_print(f"AI Model: {args.ai_model}")
    time.sleep(0.5)
    log_print(f"AI Temp: {args.ai_temp}")
    time.sleep(0.5)
    log_print(f"Torch Confidence: {args.torch_confidence}\n")
    time.sleep(2)

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
    
    log_print("\n\nAs noted in the README, you must have a .env file in the root directory of the project.\n")
    time.sleep(2)
    log_print("This file should contain the following keys:")
    time.sleep(1.3)
    log_print("GOOGLE_GEMINI_KEY=<Your Google Gemini GenAI API Key>")
    time.sleep(0.5)
    log_print("GOOGLE_BOOKS_KEY=<Your Google Books API Key>")
    time.sleep(0.5)
    log_print("ISBNDB_KEY=<Your ISBNdb API Key>")
    time.sleep(0.5)
    log_print("OPENAI_API_KEY=<Your OpenAI API Key>\n")
    time.sleep(2.5)
    
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
    
    log_print("\n\nChoose what format(s) you would like to export the results in.\n")
    time.sleep(1)
    log_print("Valid options: json, csv, txt, xml, all\n")
    time.sleep(1)
    log_print("You can choose multiple formats by separating them with a comma (e.g. json, csv)\n")
    time.sleep(2)
    formats = input("Enter the format(s) you want: ").split(',')
    if 'all' in formats:
        formats = ['json', 'csv', 'txt', 'xml']

    log_print("\nYour files will be saved in the 'booksight/vision/exports' directory.\n\n")
    time.sleep(2)
    
    log_print("One last thing, do you want to receive an email with the results?")
    time.sleep(1)
    log_print("You must have a Gmail account and generate an 'app password' for this to work.")
    time.sleep(1)
    log_print("Alternatively, if you know your way around Python, feel free to modify the Django project settings to use the email provider of your choice.\n")
    time.sleep(2)
    send_email = input("Send email? (y/n): ")
    if send_email.lower() == 'y':
        email = input("Enter your email address: ")
    else:
        email = None

    
    config_data_terminal = vision_config.VisionConfig(email, formats, ai_model, ai_temp, torch_confidence, api_keys)

    
    new_scan_image = image_path
    new_scan = create_scan(new_scan_image)

    log_print("\n\nNow sit back and watch the magic happen (or not, it's a WIP)...\n\n")
    
    # Run the vision_core function
    vision_core(image_path, new_scan, config_data_terminal)


if __name__ == '__main__':
    main()
