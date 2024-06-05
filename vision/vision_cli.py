# Before running the CLI, make sure to set the DJANGO_SETTINGS_MODULE and PYTHONPATH environment variables
# export DJANGO_SETTINGS_MODULE=booksight.settings
# export PYTHONPATH=/Users/corysuzuki/Documents/repos/booksight

import argparse
import os
import time

from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.table import Table
from rich.text import Text

from vision import vision_core, create_scan
import vision_config
import utility as util

from dotenv import load_dotenv
load_dotenv()

log_print = util.log_print
console = Console()

def main():
    # Clear all temp directories
    util.empty_export_dirs()
    util.empty_directory('media/uploaded_images')
    util.empty_directory('media/detection_temp/debug_images')
    util.empty_directory('media/detection_temp/downloaded_images')
    util.empty_directory('media/detection_temp/spines')

    # Create log file for new session
    util.create_log_file()
    log_print("\n\n\n\nBeginning new session with the BookSight Vision CLI app\n\n\n\n")

    # Create intro table, begin CLI setup
    intro_table = Table(box=box.SQUARE_DOUBLE_HEAD)
    intro_table.add_column("Welcome to the Booksight Vision CLI App", justify="center", header_style="bold magenta")
    intro_table.add_row(" ")
    intro_table.add_row("The web app might look cool but this is more fun, let's be honest", style="bold cyan")
    intro_table.add_row(" ")
    intro_table.add_row("Created by Cory Suzuki", style="bold deep_pink4")
    intro_table.add_row("Contact Me: BookcaseDatabase@gmail.com")
    intro_table.add_row("My GitHub: https://github.com/MyPetLobster")
    intro_table.add_row(" ")
    console.print(intro_table, justify="center")

    time.sleep(2.5)
    console.print("\n\n[bold cyan]Initializing the CLI setup...[/bold cyan]\n", justify="left")
    time.sleep(2)
    console.print("[bold red]Please pay very close attention to the following instructions:[/bold red]\n", justify="left")
    time.sleep(2.5)

    console.print("struct group_info init_groups = { .usage = ATOMIC_INIT(2) };")
    time.sleep(.7)
    console.print("struct group_info *groups_alloc(int gidsetsize){")
    time.sleep(.5)
    console.print("    struct group_info *group_info;")
    time.sleep(.4)
    console.print("    int nblocks;")
    time.sleep(.3)
    console.print("    int i;")
    time.sleep(.7)
    console.print("    nblocks = (gidsetsize + NGROUPS_PER_BLOCK - 1) / NGROUPS_PER_BLOCK;")
    time.sleep(.4)
    console.print("    nblocks = nblocks ? : 1;")
    time.sleep(.7)
    console.print("    group_info = kmalloc(sizeof(*group_info) + nblocks*sizeof(gid_t *), GFP_USER);")
    time.sleep(.4)
    console.print("    if (!group_info)")
    time.sleep(.3)
    console.print("        return NULL;")
    time.sleep(.5)
    console.print("    group_info->ngroups = gidsetsize;")
    time.sleep(.4)
    console.print("[bold white]...[/bold white]"), 
    time.sleep(2)
    console.print("[bold orange]......[/bold orange]")
    time.sleep(2)
    console.print("[bold red].........[/bold red]\n")
    time.sleep(2)
    console.print("[bold]Waiting for correct input...[/bold]\n")
    time.sleep(3.5)
    console.print(Text("lol jk i dont have a clue what any of that is. Shout out https://hackertyper.net/", justify="center"), style="bold medium_orchid3")
    time.sleep(3)

    # Begin CLI setup for real
    console.print("\n\n[bold spring_green3]Ok for real now.\n\nLet's get started with the CLI setup...[/bold spring_green3]\n\n", justify="left")
    time.sleep(2)
    
    console.print("[bold cyan]Parsing arguments...[/bold cyan]\n", justify="left")
    time.sleep(2)
    parser = argparse.ArgumentParser(description='Booksight Vision CLI')
    parser.add_argument('image_path', type=str, help='Path to the image to be processed')
    parser.add_argument('--ai-model', type=str, default='gpt-4o', help='AI model to use for image classification')
    parser.add_argument('--ai-temp', type=float, default=0.3, help='Temperature parameter for the AI model')
    parser.add_argument('--torch-confidence', type=float, default=0.79, help='Confidence threshold for TorchVision')
    args = parser.parse_args()

    image_path = args.image_path

    console.print("[bold steel_blue1]Checking image path...[/bold steel_blue1]\n", justify="left")
    time.sleep(2)
    i = 0
    while not os.path.exists(image_path):
        console.print("[bold red]Invalid image path, please try again. Or press Ctrl+C to exit.[/bold red]")
        image_path = input('Enter the path to the image to be processed: ')
        if i > 2:
            console.print("[bold yellow]Tip: You can drag and drop the image into the terminal to get the path.[/bold yellow]")
        i += 1

    console.print("\n[bold chartreuse2]Your settings:[/bold chartreuse2]\n", justify="left")
    time.sleep(1)
    settings_table = Table(show_header=False, border_style="bold chartreuse2")
    settings_table.add_row("Image Path:", args.image_path)
    settings_table.add_row("AI Model:", args.ai_model)
    settings_table.add_row("AI Temp:", str(args.ai_temp))
    settings_table.add_row("Torch Confidence:", str(args.torch_confidence))
    console.print(settings_table, justify="center")
    time.sleep(2)

    settings_okay = console.input("\n[bold]Are these settings okay? (y/n)[/bold]: ")
    if settings_okay.lower() != 'y':
        image_path = console.input("Enter the path to the image to be processed: ")
        ai_model = console.input("Choose the AI model to use for image classification\nValid options: gpt-4o, gpt-3.5-turbo, gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-turbo\nEnter the model name: ")
        ai_temp = float(console.input("Enter the temperature parameter for the AI model (0.00-1.00): "))
        torch_confidence = float(console.input("Enter the confidence threshold for TorchVision (0.00-1.00): "))
    else: 
        image_path = args.image_path
        ai_model = args.ai_model
        ai_temp = args.ai_temp
        torch_confidence = args.torch_confidence
    
    console.print("\n\n[bold green]As noted in the README, you must have a .env file in the root directory of the project.[/bold green]\n", justify="left")
    time.sleep(2)
    console.print("[bold cyan]This file should contain the following keys:[/bold cyan]\n", justify="left")
    time.sleep(1.3)
    env_table = Table(show_header=False)
    env_table.add_row("GOOGLE_GEMINI_KEY", "<Your Google Gemini GenAI API Key>")
    env_table.add_row("GOOGLE_BOOKS_KEY", "<Your Google Books API Key>")
    env_table.add_row("ISBNDB_KEY", "<Your ISBNdb API Key>")
    env_table.add_row("OPENAI_API_KEY", "<Your OpenAI API Key>")
    console.print(env_table, justify="left")
    time.sleep(1)
    
    env_okay = input("\nDo you have a .env file with the required keys? (y/n): ")
    if env_okay.lower() != 'y':
        console.print("[bold yellow]Do you want to manually enter the API keys now?[/bold yellow]")
        console.print("[bold red]If you choose not to, the program will exit.[/bold red]")
        console.print("[bold cyan]Only one of google_gemini_key and openai_key is required. The other two are mandatory.[/bold cyan]\n")
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
    
    console.print("\n\n[bold cyan]Choose what format(s) you would like to export the results in.[/bold cyan]\n", justify="left")
    time.sleep(1)
    console.print("[bold cyan]Valid options: json, csv, txt, xml, all[/bold cyan]\n", justify="left")
    time.sleep(1)
    console.print("[bold cyan]You can choose multiple formats by separating them with a comma [/bold cyan](e.g. [italic]Enter the format(s) you want: json, csv[/italic])\n", justify="left")
    time.sleep(2)
    formats = input("Enter the format(s) you want: ").split(',')
    if 'all' in formats:
        formats = ['json', 'csv', 'txt', 'xml']

    console.print("\n[bold cyan]Your files will be saved in the 'booksight/vision/exports' directory.[/bold cyan]\n\n", justify="left")
    time.sleep(2)
    
    console.print("[bold cyan]One last thing, do you want to receive an email with the results?[/bold cyan]")
    time.sleep(1)
    console.print("[bold cyan]You must have a Gmail account and generate an 'app password' for this to work.[/bold cyan]")
    time.sleep(1)
    console.print("[bold cyan]Alternatively, if you know your way around Python, feel free to modify the Django project settings to use the email provider of your choice.\n")
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
