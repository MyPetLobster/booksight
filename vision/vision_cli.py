import argparse
import os
import time

from rich.console import Console
from rich import box
from rich.table import Table
from rich.text import Text

import db_requests as dbr
import utility as util
import vision_config
from vision import vision_core, create_scan

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

    # Create log header to specify Vision launched with CLI
    log_print("\n\n\n\nBeginning new session with the BookSight Vision CLI app\n\n\n\n")

    # Create intro table, begin CLI setup
    intro_table = Table(box=box.SQUARE_DOUBLE_HEAD, border_style="bold")
    intro_table.add_column("Welcome to the Booksight Vision CLI App", justify="center", header_style="bold")
    intro_table.add_row(" ")
    intro_table.add_row("The web app might look cool but this is more fun, let's be honest", style="thistle3")
    intro_table.add_row(" ")
    intro_table.add_row("Created by Cory Suzuki", style="bold")
    intro_table.add_row(" ")
    intro_table.add_row("Contact Me: BookcaseDatabase@gmail.com", style="misty_rose3")
    intro_table.add_row("My GitHub: https://github.com/MyPetLobster", style="thistle3")
    intro_table.add_row(" ")
    console.print(intro_table, justify="center")
    time.sleep(2)

    console.print("\n\n[bold thistle1]Initializing the CLI setup...[/bold thistle1]\n", justify="left")
    time.sleep(0.3)

    # silly_tricks()

    console.print("[bold pink3]Parsing arguments...[/bold pink3]", justify="left")
    time.sleep(0.3)


    # PARSE ARGS and SETUP SETTINGS
    parser = argparse.ArgumentParser(description='Booksight Vision CLI')
    parser.add_argument('image_path', type=str, help='Path to the image to be processed')
    parser.add_argument('--ai-model', type=str, default='gpt-4o', help='AI model to use for image classification')
    parser.add_argument('--ai-temp', type=float, default=0.3, help='Temperature parameter for the AI model')
    parser.add_argument('--torch-confidence', type=float, default=0.78, help='Confidence threshold for TorchVision')
    args = parser.parse_args()

    image_path = args.image_path.strip()
    ai_model = args.ai_model
    ai_temp = args.ai_temp
    torch_confidence = args.torch_confidence
    
    # Settings check
    settings_okay = 'n'
    while settings_okay.lower() != 'y':
        console.print("\n[bold hot_pink2]Your settings:[/bold hot_pink2]", justify="left")
        settings_table = Table(show_header=False, border_style="bold hot_pink2")
        settings_table.add_row("Image Path:", image_path, style="plum3")
        settings_table.add_row("AI Model:", ai_model, style="pink3")
        settings_table.add_row("AI Temp:", str(ai_temp), style="light_pink3")
        settings_table.add_row("Torch Confidence:", str(torch_confidence), style="light_salmon3")
        console.print(settings_table, justify="center")
        time.sleep(0.3)

        settings_okay = console.input("\n[bold]Are these settings okay? ([chartreuse3]y[/chartreuse3]/[red1]n[/red1]):[/bold] ")
        settings_okay = settings_okay[0].lower()

        if settings_okay != 'y':
            time.sleep(1)
            console.print("\n\n[bold violet]No problem, let's enter the settings manually.[/bold violet]")
            console.print("\n[bold red]WARNING: [/bold red][red]If you are not sure about the settings, please refer to the README or stick with the defaults.[/red]\n")
            time.sleep(1.5)
            image_path = console.input("\n[dark_sea_green2][bold]Image path[/bold] must be valid absolute or relative path to the image file.[/dark_sea_green2]\n\n[bold]Enter the path to the image to be processed: [/bold]")
            ai_model = console.input("\n\n[pale_green1]Choose the [bold]AI model[/bold] to use for image classification\n[italic]Valid options: gpt-4o, gpt-3.5-turbo, gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-pro[/italic][/pale_green1]\n\n[bold]Enter the model name: [/bold]")
            ai_temp = float(console.input("\n\n[dark_olive_green2][bold]Temperature[/bold] is a setting used for OpenAI GPT models to determine the randomness of a response.\nValid range: 0.0 to 2.0\nBookSight recommended temperature is [bold]0.3[/bold]\n[italic]If you are not using an OpenAi model, enter 0 for temperature.[/italic][/dark_olive_green2]\n\n[bold]Enter the temperature parameter for the AI model:[/bold] "))
            torch_confidence = float(console.input("\n\n[green_yellow][bold]Torchvision confidence threshold[/bold]. Valid range: 0.00 to 1.00\nBookSight recommended threshold is [bold]0.79[/bold][/green_yellow]\n\n[bold]Enter the confidence threshold for TorchVision:[/bold] "))
            time.sleep(1.5)


    # VALIDATE INPUTS

    # Check if image path is valid
    console.print("\n\n[bold honeydew2]Checking image path...[/bold honeydew2]", justify="left")
    time.sleep(0.5)
    i = 0
    while not os.path.exists(image_path):
        console.print("\n[bold red]Invalid image path, please try again. Or press Ctrl+C to exit.[/bold red]")
        if i > 1:
                console.print("\n\n[bold yellow]Tip: You can drag and drop the image into the terminal to get the path.[/bold yellow]\n\n")
        image_path = console.input('\n[bold]Enter the path to the image to be processed: [bold]')
        i += 1
        
    console.print("[bold dark_sea_green1]Image path is valid.[/bold dark_sea_green1]\n", justify="left")
    
    # Check if AI model is valid
    console.print("[bold dark_sea_green2]Checking AI model...[/bold dark_sea_green2]", justify="left")
    time.sleep(0.2)

    valid_models = ['gpt-4o', 'gpt-3.5-turbo', 'gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.0-turbo']
    ai_model = ai_model.lower()
    is_ai_valid = False
    while not is_ai_valid:
        if ai_model in valid_models:
            is_ai_valid = True
        else:
            console.print("\n[bold red]Invalid AI model entered. Please try again.[/bold red]\n")
            ai_model = console.input("[bold]Enter the model name: [/bold]")
            ai_model = ai_model.lower()

    console.print("[bold dark_sea_green3]AI model is valid.[/bold dark_sea_green3]\n", justify="left")

    # Check if AI temperature and Torch confidence are valid (both should be between 0 and 1)
    console.print("[bold dark_sea_green]Checking AI temperature and Torch confidence...[/bold dark_sea_green]", justify="left")
    time.sleep(0.4)

    is_valid_floats = False
    while not is_valid_floats:
        if ai_temp < 0 or ai_temp > 1:
            ai_temp = float(console.input("\n[bold]Invalid AI temperature entered. Please enter a value between 0.00 and 1.00:[/bold] "))
        elif torch_confidence < 0 or torch_confidence > 1:
            torch_confidence = float(console.input("\n[bold]Invalid Torch confidence entered. Please enter a value between 0.00 and 1.00:[/bold] "))
        else:
            if ai_temp >= 0 and ai_temp <= 1 and torch_confidence >= 0 and torch_confidence <= 1:
                if type(ai_temp) == float and type(torch_confidence) == float:
                    is_valid_floats = True

    console.print("[bold spring_green4]AI temperature and Torch confidence are valid.[/bold spring_green4]\n\n", justify="left")


    # ENV FILE SETUP
    time.sleep(0.5)
    console.print("[bold light_slate_blue]Great! Now let's set up the API keys and export formats.[/bold light_slate_blue]\n\n", justify="left")
    time.sleep(1)

    console.print("[bold plum4]As noted in the README, you must have a .env file in the root directory of the project.[/bold plum4]\n", justify="left")
    time.sleep(1)
    console.print("[bold medium_orchid3]This file should contain the following keys:[/bold medium_orchid3]\n", justify="left")
    env_table = Table(show_header=False, border_style="bold medium_orchid3")
    env_table.add_row("GOOGLE_GEMINI_KEY", "<Your Google Gemini GenAI API Key>", style="light_slate_blue")
    env_table.add_row("GOOGLE_BOOKS_KEY", "<Your Google Books API Key>", style="medium_purple")
    env_table.add_row("ISBNDB_KEY", "<Your ISBNdb API Key>", style="light_slate_grey")
    env_table.add_row("OPENAI_API_KEY", "<Your OpenAI API Key>", style="grey53")
    env_table.add_row("GMAIL_USERNAME", "<Your Gmail Username>", style="plum4")
    env_table.add_row("GMAIL_PASSWORD", "<Your Gmail Password>", style="light_pink4")
    console.print(env_table, justify="center")
    time.sleep(0.5)
    
    env_okay = console.input("[bold]\nDo you have a .env file with the required keys? ([chartreuse3]y[/chartreuse3]/[red1]n[/red1]):[/bold] ")
    env_okay = env_okay[0].lower()

    if env_okay.lower() != 'y':
        console.print("\n[bold medium_purple]All good. Do you want to manually enter the API keys now?[/bold medium_purple]\n")
        time.sleep(0.5)
        console.print("[bold orange_red1]If you choose not to, the program will exit.[/bold orange_red1]\n")
        time.sleep(0.5)
        console.print("[bold light_slate_grey]Note: Only one of google_gemini_key and openai_key is required. The other two API keys are mandatory.[/bold light_slate_grey]\n\n")
        time.sleep(0.5)
        console.print("[bold grey53]Gmail credentials are required if you want to receive an email with the results.[/bold grey53]\n")
        console.print("[bold grey53]You must generate an 'app password' for your Gmail account.[/bold grey53]\n")
        console.print("[bold grey53]If you don't want to receive an email, just press enter with an empty field.[/bold grey53]\n")

        valid_input = False
        while not valid_input:
            enter_keys = console.input("[bold]Enter API keys? ([chartreuse3]y[/chartreuse3]/[red1]n[/red1]): [/bold]")
            if enter_keys[0].lower() not in ['y', 'n']:
                console.print("\n[bold red]Invalid input. Please try again.[/bold red]\n")
            else:
                valid_input = True

            enter_keys = enter_keys[0].lower()
            if enter_keys.lower() != 'y':
                return
            
        console.print("\n[bold red]WARNING: This process will overwrite the entire existing .env file.[/bold red]\n")
        google_gemini_key = console.input("\n[bold light_slate_blue]Enter your Google Gemini GenAI API Key: [/bold light_slate_blue]")
        google_books_key = console.input("\n[bold medium_purple]Enter your Google Books API Key: [/bold medium_purple]")
        isbndb_key = console.input("\n[bold light_slate_grey]Enter your ISBNdb API Key: [/bold light_slate_grey]")
        openai_key = console.input("\n[bold grey53]Enter your OpenAI API Key: [/bold grey53]")
        gmail_user = console.input("\n[bold plum4]Enter your Gmail Username: [/bold plum4]")
        gmail_pass = console.input("\n[bold light_pink4]Enter your Gmail Password: [/bold light_pink4]")

        # Overwrite the .env file
        with open('.env', 'w') as f:
            f.write(f"GOOGLE_GEMINI_KEY={google_gemini_key}\n")
            f.write(f"GOOGLE_BOOKS_KEY={google_books_key}\n")
            f.write(f"ISBNDB_KEY={isbndb_key}\n")
            f.write(f"OPENAI_API_KEY={openai_key}\n")
            f.write(f"GMAIL_USERNAME={gmail_user}\n")
            f.write(f"GMAIL_PASSWORD={gmail_pass}\n")

        console.print("\n[bold light_slate_blue]New credentials have been saved to the .env file[/bold light_slate_blue]\n", justify="left")

    # Validate API Keys
    console.print("\n[bold light_slate_blue]Validating API keys...[/bold light_slate_blue]", justify="left")
    dbr.validate_api_keys()
    console.print("[bold medium_purple3]API keys have been validated successfully.[/bold medium_purple3]", justify="left")
    time.sleep(0.5)

    console.print("\n\n[bold dodger_blue1]Wonderful! API keys have been set up successfully.[/bold dodger_blue1]\n\n", justify="left")

    console.print("[bold sky_blue1]Choose what format(s) you would like to export the results in.[/bold sky_blue1]\n", justify="left")
    time.sleep(0.3)
    console.print("[bold dark_slate_gray3]Valid options: json, csv, txt, xml, all[/bold dark_slate_gray3]\n", justify="left")
    time.sleep(0.6)
    console.print("[bold aquamarine3]You can choose multiple formats by separating them with a comma [/bold aquamarine3](e.g. [italic]Enter the format(s) you want: json, csv[/italic])\n", justify="left")
    time.sleep(0.5)

    # Check valid formats entered
    valid_formats = False
    while not valid_formats:
        formats = console.input("[bold]Enter the format(s) you want: [/bold]")
        formats = formats.split(',')
        formats = [f.strip() for f in formats]
        valid_formats = all(f in ['json', 'csv', 'txt', 'xml', 'all'] for f in formats)
        if not valid_formats:
            console.print("\n[bold red]Invalid format(s) entered. Please try again.[/bold red]\n")
            time.sleep(0.5)
        else:
            valid_formats = True

    if 'all' in formats:
        formats = ['json', 'csv', 'txt', 'xml']
    time.sleep(1.5)
    console.print("\n[bold cyan]Formats have been set up successfully.[/bold cyan]\n", justify="left")

    console.print("\n[bold sea_green3]Your files will be saved in the 'booksight/vision/exports' directory.[/bold sea_green3]\n\n", justify="left")
    time.sleep(1)
    

    # EMAIL SETUP
    console.print("[bold dark_turquoise]One last thing, do you want to receive an email with the results?[/bold dark_turquoise]\n")
    time.sleep(0.5)
    console.print("[bold light_sea_green]You must have a Gmail account and generate an 'app password' for this to work.[/bold light_sea_green]\n")
    time.sleep(0.5)
    console.print("[italic dark_cyan]If you know your way around Python, you can modify the Django project settings to use the email provider of your choice.[/italic dark_cyan]\n\n")
    time.sleep(0.2)

    send_email = console.input("[bold]Send email? ([chartreuse3]y[/chartreuse3]/[red1]n[/red1]): [/bold]") 
    if send_email.lower() == 'y':
        valid_email = False
        i = 0
        while not valid_email:
            email = console.input("[bold]Email address to receive exported files: [/bold]")

            if email == '':
                email = None
                valid_email = True

            if '@' in email and '.' in email:
                valid_email = True
            else:
                if i > 2:
                    console.print("\n[bold red]Invalid email address entered. Please try again.[/bold red]\n")
                    time.sleep(1)
                    console.print("[bold yellow]If you want to proceed without email, just press enter with an empty field this time.[/bold yellow]")
                    time.sleep(1)
                else:
                    console.print("\n[bold red]Invalid email address entered. Please try again.[/bold red]\n")
                    time.sleep(1)

        console.print("\n")
    else:
        email = None

    if email:
        console.print("\n[bold sea_green3]Email has been set up successfully.[/bold sea_green3]\n", justify="left")
        time.sleep(2)
        console.print(f"\n[bold chartreuse3]An email with the attached files you requested will be sent to {email} once the process is complete.[/bold chartreuse3]\n", justify="left")
        time.sleep(1)
    config_data_terminal = vision_config.VisionConfig(email, formats, ai_model, ai_temp, torch_confidence)

    
    new_scan_image = image_path
    new_scan = create_scan(new_scan_image)

    console.print("\n\n[bold chartreuse1]Now sit back and watch the magic happen (or not, it's a WIP)...[/bold chartreuse1]\n\n")
    time.sleep(2)
    # Run the vision_core function
    vision_processed = vision_core(image_path, new_scan, config_data_terminal)

    if vision_processed: 
        console.print("\n\n[bold chartreuse3]The process is complete. Check the 'exports' folder for your results.[/bold chartreuse3]\n\n")
        time.sleep(1)
        if email: 
            console.print("\n[bold sea_green3]An email has been sent to you with the results.[/bold sea_green3]\n")
            console.print("\nIf you do not receive the email, refer to the README for help setting up Django email settings.\n\n")
            time.sleep(1)
        console.print("\n[bold steel_blue1]If you have any questions or feedback, please reach out to me at BookcaseDatabase@gmail.com[/bold steel_blue1]\n\n")
        console.print("\n\n[bold medium_turquoise]Thank you for using the Booksight Vision CLI app![/bold medium_turquoise]\n\n")
        time.sleep(2.5)
        draw_ascii_owl()
        return
    else:
        console.print("\n\n[bold red]We're Sorry! There was an error processing the image. Please check the logs for more information.[/bold red]\n\n")
        console.print("\n\n[bold red]Email logs to BookcaseDatabase@gmail.com for further assistance.[/bold red]\n\n")
        return
    

def silly_tricks():
    console.print("[bold red]Pay very close attention to the following instructions:[/bold red]\n", justify="left")
    time.sleep(2)
    console.print("struct group_info init_groups = { .usage = ATOMIC_INIT(2) };")
    time.sleep(.6)
    console.print("struct group_info *groups_alloc(int gidsetsize){")
    time.sleep(.4)
    console.print("    struct group_info *group_info;")
    time.sleep(.3)
    console.print("    int nblocks;")
    time.sleep(.2)
    console.print("    int i;")
    time.sleep(.5)
    console.print("    nblocks = (gidsetsize + NGROUPS_PER_BLOCK - 1) / NGROUPS_PER_BLOCK;")
    time.sleep(.3)
    console.print("    nblocks = nblocks ? : 1;")
    time.sleep(.5)
    console.print("    group_info = kmalloc(sizeof(*group_info) + nblocks*sizeof(gid_t *), GFP_USER);")
    time.sleep(.3)
    console.print("    if (!group_info)")
    time.sleep(.2)
    console.print("        return NULL;")
    time.sleep(.4)
    console.print("    group_info->ngroups = gidsetsize;\n")
    time.sleep(.3)
    console.print("[bold]Please provide your response now[/bold][bold yellow3]...[/bold yellow3]"), 
    time.sleep(1.5)
    console.print("[bold]Please provide your response now[/bold][bold orange3]......[/bold orange3]")
    time.sleep(1.2)
    console.print("[bold]Please provide your response now[/bold][bold red].........[/bold red]\n")
    time.sleep(1.2)
    console.print("[bold red]WARNING: INPUT FAILURE. SYSTEM WIDE ERASURE IMMINENT[/bold red]\n")
    time.sleep(0.5)
    console.print("[bold green3]10[/bold green3]")
    time.sleep(1)
    console.print("[bold green3]9[/bold green3]")
    time.sleep(1)
    console.print("[bold green3]8[/bold green3]")
    time.sleep(0.7)
    console.print("[bold yellow3]7[/bold yellow3]")
    time.sleep(0.5)
    console.print("[bold yellow3]6[/bold yellow3]")
    time.sleep(0.4)
    console.print("[bold orange3]5[/bold orange3]")
    time.sleep(0.3)
    console.print("[bold orange3]4[/bold orange3]")
    time.sleep(0.2)
    console.print("[bold red]3[/bold red]")
    time.sleep(0.15)
    console.print("[bold red]2[/bold red]")
    time.sleep(0.1)
    console.print("[bold red]1[/bold red]\n")
    time.sleep(0.4)
    console.print("[bold red]AHHHHHHH!!!![/bold red]\n\n")
    time.sleep(2)

    console.print(Text("lol jk i don't have a clue what any of that code is. Shout out https://hackertyper.net/", justify="center"), style="italic thistle1")
    time.sleep(2)

    # Begin CLI setup for real
    console.print("\n\n\n[bold orchid1]Ok for real now. Let's get started with the CLI setup...[/bold orchid1]\n\n", justify="left")
    time.sleep(2)
      

def draw_ascii_eyes():
    console.print("\n")
    console.print("""
                       #@@@@@@@@@@@@@#+                      *@@@@@@@@@@@@@%*                       
                   #@@@@@@@%##%@@@@@@@@@@#                %@@@@@@@@@@##%@@@@@@@%*                   
                 %%*  =#%@@@@@@@@%*  *@@@@@%           %@@@@@#  +#@@@@@@@@@%+  *%@+                 
               + %@@@@@@@@@%%@%@@@@@@@@##%@@@*        @@@@#*%@@@@@@@@@%%@@@@@@@@@%++                
             *%@@@@%+ %%%%@@@@@%#%* #@@@@@*%@@#     *@@@ #@@@@%= %%%@@@@@%%#%* #@@@@@#              
           =@@@# +%@@@@@@@@@@@@@@@@@@@# %@@% @@*    @@##@@%# %@@@@@@@@@@@@@@@@@@@# #@@@#            
          %@% #@@@@@@@@%%*#+*%#%%@@@@@@@@##@@=%@   @@ @@#*%@@@@@@@@%%#*+*##%%@@@@@@@% #@@           
         @*#@@@%* #%#%@@@@@@@@@@@%## %@@@@@#%@ #*  % %%%@@@@@%* %#%@@@@@@@@@@@%## +%@@@# @#         
         #@#* #@@@@@@%#%@@@#**%@@@@@@@% #@@@@ = =  =- @@@@% #@@@@@@@%#+#@@@@%%@@@@@@%  #@#          
       -# *@@@%#+     %@@%#@@@@@@@@@@@@@@%#@@@*      @@@%*@@@@@@@@@@@%@@%#@@@*     #%@@@# #+        
        *%           %@@@%@@@@@@@@  %@@%@@@*#@@     @@% @@@%@@@@@@@@*  %@##@@%           #*         
              *      %@@#%@@@@@@@@@@@@@% %@@@ %%   -@*%@@@#*@@@@@@@@@@@@@@:@@@      ++              
             +@#     %@@%#@@@@@@@@@@@@@%  #@@@+=   * @@@%  #@@@@@@@@@@@@@%*@@@     #@%              
             +@@%+    %@@*#@@@@@@@@@@@@    +@@@     @@@#    %@@@@@@@@@@@%+@@@#    @@@#              
              @#%@@*   @@@@*%%@@@@@@@@*     *@@@   %@@#      %@@@@@@@@%=%@@@#   %@@*@%              
              @@#%@@@%* #@@@@@@@@@@@#        #@@+  @@#        *@@@@@@@@@@@%  %@@@@*@@               
               @@%-%@@@@@#  +*%**             #@% #@@             =%##*  *%@@@@@=#@@#               
               *@@@% %@@@@@@@@@@@@@@@@@@% *%  #@@ =@%  #% #@@@@@@@@@@@@@@@@@@@##@@@#                
                 %@@@@# %@@@@@@@@@@@@# #@@%    %#  @+   #@@%*#@@@@@@@@@@@@%**%@@@@+                 
                   @@@@@@@#+     :#%@@@@@      *   %      %@@@@%*+     +*@@@@@@@+                   
                     %@@@@@@@@@@@@@@@@%                     #%@@@@@@@@@@@@@@@%*                     
                         +%%@@@@%#*                             +%@@@@@%%*                      
                    
""", style="steel_blue")


def draw_ascii_owl():
    console.print("\n\n")
    time.sleep(0.05)
    console.print("                           [light_goldenrod1]################[/light_goldenrod1]                               ")
    time.sleep(0.05)
    console.print("                       [light_goldenrod1]########################[/light_goldenrod1]                           ")
    time.sleep(0.05)
    console.print("                   [light_goldenrod1]######################[/light_goldenrod1]                                 ")
    time.sleep(0.05)
    console.print("                [light_goldenrod1]#############[/light_goldenrod1]                                     [pale_turquoise4]##[/pale_turquoise4]       ")
    time.sleep(0.05)
    console.print("             [light_goldenrod1]############[/light_goldenrod1]                                       [pale_turquoise4]#######    ")
    time.sleep(0.05)
    console.print("           [light_goldenrod1]############[/light_goldenrod1]                         [light_goldenrod1]##[/light_goldenrod1]             [pale_turquoise4]############ ")
    time.sleep(0.05)
    console.print("          [light_goldenrod1]###########[/light_goldenrod1]    [pale_turquoise4]##[/pale_turquoise4]                    [light_goldenrod1]####[/light_goldenrod1]           [pale_turquoise4]#############[/pale_turquoise4]   ")
    time.sleep(0.05)
    console.print("        [light_goldenrod1]###########[/light_goldenrod1]       [pale_turquoise4]######[/pale_turquoise4]                [light_goldenrod1]###[/light_goldenrod1]         [pale_turquoise4]#################[/pale_turquoise4] ")
    time.sleep(0.05)
    console.print("       [light_goldenrod1]###########[/light_goldenrod1]        [pale_turquoise4]##########                   ###################[/pale_turquoise4]  ")
    time.sleep(0.05)
    console.print("      [light_goldenrod1]##########[/light_goldenrod1]           [pale_turquoise4]############               ####################[/pale_turquoise4]  ")
    time.sleep(0.05)
    console.print("     [light_goldenrod1]##########[/light_goldenrod1]            [pale_turquoise4]###############          #####################[/pale_turquoise4]   ")
    time.sleep(0.05)
    console.print("    [light_goldenrod1]###########[/light_goldenrod1]             [pale_turquoise4]################       ######################[/pale_turquoise4]   ")
    time.sleep(0.05)
    console.print("    [light_goldenrod1]##########[/light_goldenrod1]                [pale_turquoise4]###############      #####################[/pale_turquoise4]    ")
    time.sleep(0.05)
    console.print("   [light_goldenrod1]###########[/light_goldenrod1]                  [pale_turquoise4]###############   #####################[/pale_turquoise4]     ")
    time.sleep(0.05)
    console.print("   [light_goldenrod1]##########[/light_goldenrod1]                     [pale_turquoise4]####   ######## ####################[/pale_turquoise4]      ")
    time.sleep(0.05)
    console.print("   [light_goldenrod1]##########[/light_goldenrod1]                     [pale_turquoise4]#   #### ##########################[/pale_turquoise4]       ")
    time.sleep(0.05)
    console.print("  [light_goldenrod1]###########[/light_goldenrod1]                     [pale_turquoise4]####### #########################[/pale_turquoise4]         ")
    time.sleep(0.05)
    console.print("  [light_goldenrod1]###########[/light_goldenrod1]                     [pale_turquoise4]###     #######################[/pale_turquoise4]           ")
    time.sleep(0.05)
    console.print("   [light_goldenrod1]###########[/light_goldenrod1]                    [pale_turquoise4]#     ########################[/pale_turquoise4]            ")
    time.sleep(0.05)
    console.print("   [light_goldenrod1]###########[/light_goldenrod1]                     [pale_turquoise4]##########################[/pale_turquoise4]               ")
    time.sleep(0.05)
    console.print("   [light_goldenrod1]###########[/light_goldenrod1]                       [pale_turquoise4]##############################[/pale_turquoise4]         ")
    time.sleep(0.05)
    console.print("    [light_goldenrod1]###########[/light_goldenrod1]                        [pale_turquoise4]#############################[/pale_turquoise4]        ")
    time.sleep(0.05)
    console.print("    [light_goldenrod1]############[/light_goldenrod1]                         [pale_turquoise4]##############################[/pale_turquoise4]     ")
    time.sleep(0.05)
    console.print("     [light_goldenrod1]############[/light_goldenrod1]                            [pale_turquoise4]#########################[/pale_turquoise4]     ")
    time.sleep(0.05)
    console.print("      [light_goldenrod1]#############[/light_goldenrod1]                                  [pale_turquoise4]#################[/pale_turquoise4]      ")
    time.sleep(0.05)
    console.print("       [light_goldenrod1]#############[/light_goldenrod1]                                   [pale_turquoise4]# ##########[/pale_turquoise4]         ")
    time.sleep(0.05)
    console.print("        [light_goldenrod1]##############[/light_goldenrod1]                                                     ")
    time.sleep(0.05)
    console.print("         [light_goldenrod1]###############                               ##[/light_goldenrod1]                   ")
    time.sleep(0.05)
    console.print("           [light_goldenrod1]################                       #####[/light_goldenrod1]                    ")
    time.sleep(0.05)
    console.print("            [light_goldenrod1]####################              #######[/light_goldenrod1]                      ")
    time.sleep(0.05)
    console.print("               [light_goldenrod1]####################################[/light_goldenrod1]                        ")
    time.sleep(0.05)
    console.print("                 [light_goldenrod1]################################[/light_goldenrod1]                          ")
    time.sleep(0.05)
    console.print("                     [light_goldenrod1]########################[/light_goldenrod1]                              ")
    time.sleep(0.05)
    console.print("                         [light_goldenrod1]################[/light_goldenrod1]                                   ")
    time.sleep(0.5)
    console.print("\n\n")

if __name__ == '__main__':
    main()
