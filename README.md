<div id="readme-top"></div>
<br />
<div align="center">
  <a href="https://github.com/MyPetLobster/booksight">
    <img src="https://i.imgur.com/STBuqEM.png" alt="Logo" width="200px">
  </a>

  <h3 align="center">BookSight</h3>

  <p align="center">
    A web application that identifies the specific ISBNs of all books in a given image.
    <br />
    <br />
    <br />
    <a href="#">View Youtube Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### Desktop/Mobile Landing Pages

<div style="display:flex; gap:40px"><img src="https://i.imgur.com/bWEa4Q8.png" alt="Desktop Landing Page" height="400px"><img src="https://i.imgur.com/MOvQ5Gl.png" alt="Mobile Landing Page" height="400px"></div>

<br />

My first 'real' project was my final project for CS50x which I completed in January of this year (it's May 29th, 2024 as I type this). That project is called Bookcase Database. It's a simple web application that allows users to search for books, add books to their bookcase, and rate books. The application uses the Google Books API to search for books and retrieve book information. The application also uses a SQLite database to store user information, book information, and book ratings. 

I was pleased with the final result, but the initial idea that I had to make Bookcase Database a tool I'd actually use over something like Goodreads or LibraryThing was never realized. I wanted the ability to take a picture of a bookshelf then have an application identify all the books in the photo by the spine alone. And not just the title and author, but all the details unique to each particular
edition of each book. So that was the spark/exciting idea that inspired me to create Bookcase Database originally. I was quickly humbled and made aware of how far I was from being able to create such a tool. I had no idea where to even start. That was my first time really working on anything that wasn't a simple single web page or one of CS50's assigned projects. So I decided to build a strong foundation first and return to the idea when I felt I might be ready. 

So here I am. Since finishing Bookcase Database, I've completed CS50 Python, CS50 SQL, Odin Foundations, and spent every free moment I have working on personal coding projects, reading about coding, or working on coding challenges. I've learned a lot and I'm ready to take on the challenge of creating BookSight.

Project Goals:
* Create a terminal application that can identify the ISBNs of all books in a given image.
* Incorporate the logic of the core functionality of the terminal application into a web application.
* Create a web application that allows users to upload an image of a bookshelf and receive a list of all the books in the image.
* Export the list of books and details to CSV, JSON, XML, and/or TXT.

Personal Learning Goals:
* How to process/edit images with Python.
* What is OCR and how to do I use it to extract text from images?
* How does computer vision work? How do I use it to implement object detection?
* I've used Google Books API before, but how can I incorporate several other book databases to get more accurate results?
* Make a separate app for the front end and back end with my Django project.
* Explore everything about Django now that I'm creating this from scratch and not using a template provided by CS50w.
* Create custom log files for the full book identification process.
* Learn how to use ajax to update the front end with the results of the book identification process.
* I've used OpenAI's API for my Character Chat project, but I want to use it again to help make initial identification of books and clean up OCR results. 
* Explore and compare other AI models.
* Implement token counter for AI API calls.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With
Languages, frameworks, and libraries used in the project.

* [![Python][Python.shield]][Python.url]
* [![JavaScript][JavaScript.shield]][JavaScript.url]
* [![Sass][Sass.shield]][Sass.url]
* [![Django][Django.shield]][Django.url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![OpenAI][OpenAI.shield]][OpenAI.url]
* [![Google Gemini API][Google.shield]][Google.url]

#### Other Python Libraries Used (see requirements.txt for full list)
* EasyOCR
* Matplotlib
* Numpy
* OpenCV
* Pillow
* Requests
* Rich
* Scikit-learn
* Tiktoken
* Torch
* Torchvision

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Project logic, flow and structure



## Getting Started

To get a local copy up and running follow these steps.

### Prerequisites

BookSight is built with Django, so you'll need to have Python installed on your machine. You can download Python [here](https://www.python.org/downloads/).


### Installation

* API Keys Required for BookSight
    - OpenAI API Key
    - Google Gemini API Key
    - Open Library API Key
    - ISBNdb API Key 

1. Clone the repo
   ```sh
   git clone
    ```
2. Create a virtual environment and activate it
   ```sh
   python -m venv .venv
   python .venv/bin/activate
   ```

3. Install the required packages
   ```sh
    pip install -r requirements.txt
    ```
4. Create a .env file in the root directory and add the following variables
    ```sh
    export GOOGLE_BOOKS_API_KEY = "your-google-books-api-key"
    export ISBNDB_API_KEY = "your-isbndb-api-key"
    export OPENAI_API_KEY = "your-openai-api-key"
    export GMAIL_PASSWORD = "your-gmail-password"
    export GMAIL_USERNAME = "your-gmail-username"
    ```
    **Note:** The GMAIL_USERNAME and GMAIL_PASSWORD are used to send emails to users when their book identification process is complete.
    Feel free to modify the email settings to use the email service of your choice. If you use google, you will need to setup an app password for your gmail account.

    **Note:** ISBNdb has a monthly fee and a strict rate limit. This is the biggest bottleneck in the project. I'm currently looking for a better alternative.

    **Note:** At the time of this writing (5/31/2024), Google's Generative AI API does not require an API key.

    **Note:** OpenAI's API requires an API key. You can get one [here](https://beta.openai.com/signup/). The latest model used in the project is GPT-4o. 

5. Run the server
    ```sh
    python manage.py runserver
    ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

### Web Application
1. Use the form on the landing page to upload an image of a bookshelf/bookcase, enter your email address, and choose the export format.
2. Submit the form.
3. Sit back and relax while the application identifies all the books in the image. You will receive an email when the process is complete.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Terminal Application
1. Run the terminal application
    ```sh
    python vision.py
    ```
2. Follow the prompts to upload an image of a bookshelf/bookcase and choose the export format/destination.
3. Watch the magic happen by following the progress logs in the terminal. 







## File Structure
<pre>booksight
    |- .venv
    |- booksight/
    |   |- __pycache__
    |   |- logs/
    |   |- __init__.py
    |   |- asgi.py
    |   |- settings.py
    |   |- urls.py
    |   |- wsgi.py
    |- dashboard/
    |   |- __pycache__
    |   |- migrations/
    |   |- static/
    |   |   |- dashboard/
    |   |   |   |- css/
    |   |   |   |   |- style.css
    |   |   |   |   |- style.css.map
    |   |   |   |- images/
    |   |   |   |- javascript/
    |   |   |   |- sass/
    |   |   |   |   |-stye_sass.scss
    |   |   |- public/
    |   |   |   |- style_sass.css
    |   |   |   |- style_sass.css.map
    |   |- templates/
    |   |   |- about.html
    |   |   |- index.html
    |   |   |- layout.html
    |   |   |- tips.html
    |   |   |- vision_complete.html
    |   |   |- vision_failed.html
    |   |   |- vision.html
    |   |- __init__.py
    |   |- admin.py
    |   |- apps.py
    |   |- models.py
    |   |- tests.py
    |   |- urls.py
    |   |- views.py
    |- media/
    |   |- detection_temp/
    |   |- uploaded_images/
    |- vision/
    |   |- __pycache__
    |   |- exports/
    |   |   |- csv/
    |   |   |- json/
    |   |   |- text/
    |   |   |- xml/
    |   |- images/
    |   |   |- test_images/
    |   |- migrations/
    |   |- __init__.py
    |   |- admin.py
    |   |- analyze_spine.py
    |   |- apps.py
    |   |- classes.py
    |   |- config.py
    |   |- db_requests.py
    |   |- detect_spines.py
    |   |- detect_text.py
    |   |- exporter.py
    |   |- gemini.py
    |   |- gpt.py
    |   |- matcher.py
    |   |- models.py
    |   |- tests.py
    |   |- token_counter.py
    |   |- utility.py
    |   |- vision_cli.py
    |   |- vision.py
    |- .env
    |- .gitignore
    |- db.sqlite3
    |- manage.py
    |- README.md
    |- requirements.txt</pre>




# Before running the CLI, make sure to set the DJANGO_SETTINGS_MODULE and PYTHONPATH environment variables
# export DJANGO_SETTINGS_MODULE=booksight.settings
# export PYTHONPATH=/Users/corysuzuki/Documents/repos/booksight





<!-- CONTACT -->
## Contact

Cory Suzuki - bookcasedatabase@gmail.com

Project Link: [https://github.com/MyPetLobster/booksight](https://github.com/MyPetLobster/booksight)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Img Shields](https://shields.io)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python.shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python.url]: https://www.python.org/
[Django.shield]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django.url]: https://www.djangoproject.com/
[OpenAI.shield]: https://img.shields.io/badge/OpenAI-FF6600?style=for-the-badge&logo=openai&logoColor=white
[OpenAI.url]: https://www.openai.com/
[Google.shield]: https://img.shields.io/badge/Google_Gemini_API-4285F4?style=for-the-badge&logo=google&logoColor=white
[Google.url]: https://gemini.google.com/
[JavaScript.shield]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript.url]: https://www.javascript.com/
[Sass.shield]: https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white
[Sass.url]: https://sass-lang.com/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
