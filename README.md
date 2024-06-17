<div id="readme-top"></div>
<br />
<div align="center">
  <a href="https://github.com/MyPetLobster/booksight">
    <img src="https://i.imgur.com/KobQZAx.png" alt="Logo" width="200px">
    <br>
    <img src="https://i.imgur.com/zsoNMos.png" alt="BookSight" width="200px">
  </a>

  <p align="center">
    A web application that identifies the specific ISBNs of all books in a given image.
    <br />
    <br />
    <br />
    <a href="#">View Youtube Demo</a>
    ·
    <a href="https://github.com/MyPetLobster/booksight/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/MyPetLobster/booksight/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#about-the-project">Background</a></li>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#python-libraries-used-see-requirementstxt-for-full-list">Python Libraries Used</a></li>
      </ul>
    </li>
    <li>
      <a href="#logic-flow">Logic Flow</a>
    </li>
    <li>
      <a href="#file-structure">File Structure</a>
    </li>
    <li>
      <a href="#screenshotsgifs">Screenshots/GIFs</a>
      <ul>
        <li><a href="#booksight-web-application">Booksight Web Application</a></li>
        <li><a href="#cli-booksight-application-vision-cli">CLI Booksight Application (Vision CLI)</a></li>
        <li><a href="#booksight-mobile-application">Booksight Mobile Application</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li>
      <a href="#contact">Contact</a>
    </li>
    <li>
      <a href="#acknowledgments">Acknowledgments</a>
    </li>
  </ol>
</details>

</br>

<!-- ABOUT THE PROJECT -->
# About The Project

My first 'real' project was my final project for CS50x which I completed in January of this year (it's May 29th, 2024 as I type this). That project is called Bookcase Database. It's a simple web application that allows users to search for books, add books to their bookcase, and rate books. The application uses the Google Books API to search for books and retrieve book information and stores the user's bookcase, ratings, etc. in a SQLite database. 

I was pleased with the final result, but the initial idea that I had to make Bookcase Database into a tool I'd actually use over something like Goodreads or LibraryThing was never realized. I wanted the ability to take a picture of a bookshelf then have an application identify all the books in the photo by the spines alone. And not just the title and author, but all the details unique to each particular edition of each book. That was the spark/exciting idea that inspired me to create Bookcase Database originally. I was quickly humbled and made aware of how far I was from being able to create such a tool. I had no idea where to even start. That was my first time really working on anything that wasn't a simple web page or one of CS50's assigned projects. So I decided to build a strong foundation first and return to the idea when I felt I might be ready. 

So here I am several months later. Since finishing Bookcase Database, I've completed CS50 Python, CS50 SQL, Odin Foundations, and spent every free moment I have working on personal coding projects, reading about coding, or working on coding challenges. I've learned a lot and I'm ready to take on the challenge of creating BookSight.


### **Project Goals:**
* Create a terminal application that can identify the ISBNs of all books in a given image.
* Incorporate the logic of the core functionality of the terminal application into a web application.
* Create a web application that allows users to upload an image of a bookshelf and receive a list of all the books in the image.
* Export the list of books and details to CSV, JSON, XML, and/or TXT. 

### **Personal Learning Goals:**
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

### Python Libraries Used (see requirements.txt for full list)
* EasyOCR
* Google Cloud AI Platform
* Google Gemini
* Matplotlib
* Numpy
* OpenAI
* OpenCV
* Pillow
* PyTorch/Torchvision
* Requests
* Rich
* Scikit-learn
* Tiktoken
* VertexAI

<p align="right">(<a href="#readme-top">back to top</a>)</p>

</br>


# Logic Flow
<img src="https://i.imgur.com/5rutsPc.png" style="width:100%">

<p align="right">(<a href="#readme-top">back to top</a>)</p>

</br>


# File Structure
<pre>booksight
    |- .venv
    |- booksight/
    |   |- __pycache__
    |   |- dev/
    |   |   |- test_suites/
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
    |   |   |   |   |- scripts.js
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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

</br>

# Screenshots/GIFs

## Booksight Web Application: 
<img src="https://i.imgur.com/A8hQTne.gif" alt="CLI Process Gif" width="66%">
</br>
<img src="https://i.imgur.com/gqzU6pR.png" alt="Desktop Landing Page" width="33%">
<img src="https://i.imgur.com/Am0EaLB.png" alt="Desktop Upload Form" width="33%">
<img src="https://i.imgur.com/UwMRJGb.png" alt="Desktop About" width="33%">
</br>

### Desktop Vision Process:

<img src="https://i.imgur.com/DokvKTO.png" alt="Desktop Vision 1" width="45%">
<img src="https://i.imgur.com/L1PJDjx.png" alt="Desktop Vision 2" width="45%"
<img src="https://i.imgur.com/49iW24T.png" alt="Desktop Vision 3" width="45%">
<img src="https://i.imgur.com/qc56jzE.png" alt="Desktop Vision 4" width="45%">
<img src="https://i.imgur.com/DhJqb1n.png" alt="Desktop Vision 5" width="45%">
<img src="https://i.imgur.com/5yCE9dq.png" alt="Desktop Vision 6" width="45%">
<img src="https://i.imgur.com/1qpiA5M.png" alt="Desktop Vision 7" width="45%">

</br>
</br>

## CLI Booksight Application (Vision CLI):
<img src="https://i.imgur.com/88hmmHL.gif" alt="CLI Process Gif" width="66%">
</br>
<img src="https://i.imgur.com/2g14eNb.png" alt="CLI Process 01" width="45%">
<img src="https://i.imgur.com/ooYlVpF.png" alt="CLI Process 02" width="45%">
<img src="https://i.imgur.com/vfW1wfk.png" alt="CLI Process 03" width="45%">
<img src="https://i.imgur.com/6rAWCyy.png" alt="CLI Process 04" width="45%">
<img src="https://i.imgur.com/2ocOZIa.png" alt="CLI Process 05" width="45%">
<img src="https://i.imgur.com/oT1jwDB.png" alt="CLI Process 06" width="45%">
<img src="https://i.imgur.com/wBVWet1.png" alt="CLI Process 07" width="45%">
<img src="https://i.imgur.com/Qo2jYCy.png" alt="CLI Process 08" width="45%">

</br>
</br>

## Booksight Mobile Application:

### Landing, About, and Tips Pages:

<img src="https://i.imgur.com/Tbk0Fl7.gif" alt="Mobile Landing Page" height="600px">
<img src="https://i.imgur.com/vIl7xA8.gif" alt="Mobile Tips Page" height="600px">
<img src="https://i.imgur.com/7ko9m3T.gif" alt="Mobile About Page" height="600px">


</br>

### Full Process (5 Parts):

<img src="https://i.imgur.com/eTcwHJB.gif" alt="Mobile Process Part 1" height="600px">
<img src="https://i.imgur.com/10utTdC.gif" alt="Mobile Process Part 2" height="600px">
<img src="https://i.imgur.com/gRxZIU1.gif" alt="Mobile Process Part 3" height="600px">
<img src="https://i.imgur.com/MdBCbG5.gif" alt="Mobile Process Part 4" height="600px">
<img src="https://i.imgur.com/2SB7vcI.gif" alt="Mobile Process Part 5" height="600px">



</br>
<hr/>
</br>


# Getting Started
To get a local copy up and running follow these steps.

### Prerequisites
BookSight is built with Django, so you'll need to have Python installed on your machine. You can download Python [here](https://www.python.org/downloads/).


## Installation
* API Keys Required for BookSight
    - OpenAI API Key
    - Google Gemini API Key
    - Open Library API Key
    - ISBNdb API Key 

1. Clone the repo
   ```sh
   git clone http-or-ssh-link
    ```
2. Navigate to the project root directory
   ```sh
   cd booksight
   ```
3. Create a virtual environment and activate it
   ```sh
   python -m venv .venv
   python .venv/bin/activate
   ```

4. Install the required packages
   ```sh
    pip install -r requirements.txt
    ```
5. Create a .env file in the root directory and add the following variables
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

6. Run the server
    ```sh
    python manage.py runserver
    ```

7. If you want to access on mobile device to take advantage of the camera, you'll need to run the server with your local IP address. The method I found that works best is to find your local IP address and run the server with the following command:

    ```sh
    python manage.py runserver 0.0.0.0:8000
    ```


Then you can access the web application on your mobile device by typing in your local IP address followed by :8000 in the browser. For example, if your local IP address is 555.555.55.55, you would type in 555.555.55.55:8000 in the browser on your mobile device. With this method, you can still access the web application on your computer by typing in localhost:8000 in the browser. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


# Usage

## Web Application
1. Use the form on the landing page to upload an image of a bookshelf/bookcase, enter your email address, and choose the export format.
2. Submit the form.
3. Sit back and relax while the application identifies all the books in the image. You will receive an email when the process is complete.


## Terminal Application

1. Run the terminal application from project root directory
    ```sh
    python vision/vision_cli.py path/to/image.jpg --ai-model --ai-temp --torch-confidence
    ```

**Note:** The `--ai-model` flag is optional. If not provided, the default model is OpenAI's GPT-4o. 

**Note:** The `--ai-temp` flag is optional. If not provided, the default temperature is 0.3. 

**Note:** The `--torch-confidence` flag is optional. If not provided, the default confidence threshold is 0.78. 

2. Follow the prompts to upload an image of a bookshelf or bookcase and choose the export format/destination.
3. Watch the magic happen by following the progress logs in the terminal. 

 <p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
# Contact

Cory Suzuki - bookcasedatabase@gmail.com

Project Link: [https://github.com/MyPetLobster/booksight](https://github.com/MyPetLobster/booksight)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
# Acknowledgments

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
