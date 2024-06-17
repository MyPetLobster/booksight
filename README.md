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

<!-- PROJECT STATUS -->
**Project Status - 6/17/2024 - Pre-Alpha, Submitted for Review for CS50w**

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

**Note:** Much of this README is here for my own benefit. I like to be able to look back at my projects to see how much I've progressed and what I've learned. All the standard stuff you'd expect to find in a README file is here, but you might need to scroll through basically my diary to get to it. Thanks for even being curious enough to check out my project!

## Background 
My first substantial project was my final project for CS50x, which I completed in January of this year (currently, it's May 29th, 2024). That project, called Bookcase Database, is a simple web application that lets users search for books, add them to their bookcase, and rate them. It utilizes the Google Books API to fetch book information and stores user data, such as bookcase content and ratings, in a SQLite database.

While I was pleased with the outcome, the initial vision for Bookcase Database—transforming it into a tool I'd use over Goodreads or LibraryThing—wasn't fully realized. I envisioned an application that could identify books in a photo just by their spines, including all the specific details of each edition. This exciting idea was the driving force behind Bookcase Database. However, I quickly realized I wasn't yet equipped to create such a tool and decided to build a stronger foundation first.

Fast forward several months, and I've since completed CS50 Python, CS50 SQL, Odin Foundations, and spent countless hours on personal coding projects, reading about coding, and tackling coding challenges. With all I've learned, I'm now ready to take on the challenge of creating BookSight.

## Building Process
The process began with extensive research and experimentation with various technologies and techniques. I had no prior experience working with any kind of computer vision or OCR technology, so I spent a significant amount of time just reading about how all of that works. Throughout the entire process, I've continued to learn more about Python, Django, and web development in general, while also exploring a whole different side of programming with things like PyTorch and OpenCV. 

### Here’s a breakdown of the main steps:
* **Image Processing and OCR:** I started by learning how to process and edit images using Python libraries like OpenCV and Pillow. Understanding how Optical Character Recognition (OCR) works was crucial, so I experimented with EasyOCR to extract text from images.
* **Computer Vision for Object Detection:** To identify book spines in images, I delved into computer vision concepts and used PyTorch and Torchvision for object detection. This involved training and fine-tuning models to accurately detect book spines.
* **Integrating Multiple Book Databases:** I integrated several book databases, including Google Books, Open Library, and ISBNdb, to enhance the accuracy of book identification. This required handling API requests and combining data from multiple sources.
* **Building the Web Application:**I chose Django for the web application, setting up both front-end and back-end components. This involved creating models, views, and templates, as well as implementing user authentication and image upload functionality.
* **Asynchronous Processing and Logging:** Given the potentially long-running nature of the book identification process, I implemented asynchronous processing using Django’s background task handling. Custom log files were created to track the identification process step-by-step.
* **Front-End Enhancements:** To improve user experience, I used AJAX to update the front-end with real-time progress updates. This way, users could see the status of their book identification without refreshing the page.
* **Multiple Export Formats:** I implemented functionality to export the identified book data in various formats, including CSV, JSON, XML, and TXT. This required careful formatting and data handling to ensure compatibility and usability.
* **AI Integration:** For initial book identification and cleaning up OCR results, I incorporated AI models from OpenAI and explored other models for comparison. Implementing a token counter for API calls helped manage usage and costs.
This project has been an incredible learning experience, and I'm excited to see how it continues to evolve.


### **Project Goals (04/29/2024):**
* Create a terminal application that can identify the ISBNs of all books in a given image.
* Incorporate the logic of the core functionality of the terminal application into a web application.
* Create a web application that allows users to upload an image of a bookshelf and receive a list of all the books in the image.
* Export the list of books and details to CSV, JSON, XML, and/or TXT. 

### **Personal Learning Goals (5/15/2024):**
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


### **Reflections (6/17/2024 (GO CELTICS!)):**
* I actually achieved all of my personal learning goals and project goals. I'm really proud of that. There is, however, a small caveat. The overall accuracy of Booksight is...well, let's just say it's not 20/20. I'm still working on improving the accuracy of the book identification process and intend to continue to work on this project after it's been submitted. I had to force myself to stop working on it for now and finish up this README. My next step will be to dive deeper into the math of it all and really try to understand how I can improve my matching algorithms as well as the image pre-processing and OCR settings. 
* Some specific areas where the application struggles -- 
    - Reflective spines are a nightmare. Any preprocessing that solves that issue only cause more issues with other spines. I've accepted defeat here for now. I scan all the spine images for OCR, then I also scan the entire original image for OCR. This picks up the text from any missing spines and 9/10 times the AI can suss that out and I'm able to create a spine object for that book. However, it is missing the color and dimensions of the spine, so I can only provide basic/generic data for those books. (I may look into training my own model to detect reflective spines in the future, or supplementing the AI models with a model that can detect reflective spines.)
    - Differentiating between the hardcover and paperback versions of the same book if the book covers are identical and the proportions are roughly the same. (I'm not sure where to start solving this issue honestly. Early in the process I was converting pixels to inches if I found a confident match, but to keep things balanced while tracking confidence scores, that meant I had to run the entire matching process again if the px_to_inches multiplier changed. I decided to just use the ratios for dimension matching. But I guess if I did have a way to get the actual dimensions, I could differentiate between the two versions of the book. I'll have to look into that.)
    - Reading text if the spines are not very close to perfectly upright or flat. If not at 90 or 180 degrees, the OCR results are often pretty terrible. At one point, I had this solved by rotating the images multiple times and scanning each one, but that was too slow and I had to abandon that idea. (One possible solution is to train a model to detect the angle of the spine and rotate the image accordingly before scanning for text....Just thought of that while typing this.)
    - The entire process is bottlenecked by ISBNdb's rate limiting. One call per second when I have to check 10+ ISBNs per book means the process can take forever. (I am definitely going to figure out an alternative to using ISBNdb. I may be able to use Open Library and Google Books combined to get all the data that I need from the ISBNs.)

* It's wild how fast AI models are changing. In the two months or so I've been working on the project, I've had to update my OpenAI model options twice and Gemini models once. I made that aspect of the code more modular so that I can easily update the models in the future. It's really so exciting to be working with these tools and to be starting my coding journey at a time when AI is advancing so rapidly. I was pleased with how I incorporated the AI models into the project, and quite proud of the token counter I created to keep track of usage for all the different models.
* I'm really happy with the web application. I think it looks great and it's very simple/user friendly. I'm especially proud of the AJAX implementation. I had never used AJAX before, and I was able to figure it out and implement it in a way that I think really enhances the user experience by continuously updating a pseudo-terminal with the progress of the book identification process. This includes photos of the bounding boxes around books and individua spine OCR results. 
* Like I said, the interface is very simple in design. But I feel like the elements all work together seamlessly and I love how the animations came out across the site. Little things like the navbar icon disappearing when the user scrolls down and the footer only fading into existence when the user hits the bottom of the page, are things that would have been impossible for me to do just a few months ago. I'm really proud of the way the site looks and feels. This was by far the quickest and easiest part of the project for me. 
* The mobile styling was also a breeze. I remember being overwhelmed trying to setup media queries for my CS50x project. This time around, I was able to do it quickly with no stress at all.
* I set up my own logging system for the project. It records all the steps of the process and doubles as what the user sees in the CLI version of the application. It's very detailed and I think it's very clear and easy to read. The log files have been a lifesaver many times throughout the coding process and I think some people would be interested in  reading through some of the process. The log files are included along with the export files in the email that the user receives when the book identification process is complete.
* The CLI version of the application also came out great. I created that after the web app, so it was a good learning process to translate things like the web app submission form and image uploading process into a CLI. The CLI version is a fun way to experience Booksight. It's a little more interactive than the web app, and I think it's a great way to show off the core functionality of the project. I'm really happy with how it came out.

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
<img src="https://i.imgur.com/A8hQTne.gif" alt="CLI Process Gif">
<p>
  <img src="https://i.imgur.com/gqzU6pR.png" alt="Desktop Landing Page" width="32%">
  <img src="https://i.imgur.com/Am0EaLB.png" alt="Desktop Upload Form" width="32%">
  <img src="https://i.imgur.com/UwMRJGb.png" alt="Desktop About" width="32%">
</p>

</br>

### Desktop Vision Process:
<p>
  <img src="https://i.imgur.com/DokvKTO.png" alt="Desktop Vision 1" width="48%">
  <img src="https://i.imgur.com/L1PJDjx.png" alt="Desktop Vision 2" width="48%">
  <img src="https://i.imgur.com/49iW24T.png" alt="Desktop Vision 3" width="48%">
  <img src="https://i.imgur.com/qc56jzE.png" alt="Desktop Vision 4" width="48%">
  <img src="https://i.imgur.com/DhJqb1n.png" alt="Desktop Vision 5" width="48%">
  <img src="https://i.imgur.com/5yCE9dq.png" alt="Desktop Vision 6" width="48%">
  <img src="https://i.imgur.com/1qpiA5M.png" alt="Desktop Vision 7" width="48%">
</p>

</br>

## CLI Booksight Application (Vision CLI):
![cli-full-run-fast-ezgif com-optimize](https://github.com/MyPetLobster/booksight/assets/6979547/b7dcfd9e-e019-4978-a71c-31eb0609b754)
<img src="https://i.imgur.com/2g14eNb.png" alt="CLI Process 01" width="48%">
<img src="https://i.imgur.com/ooYlVpF.png" alt="CLI Process 02" width="48%">
<img src="https://i.imgur.com/vfW1wfk.png" alt="CLI Process 03" width="48%">
<img src="https://i.imgur.com/6rAWCyy.png" alt="CLI Process 04" width="48%">
<img src="https://i.imgur.com/2ocOZIa.png" alt="CLI Process 05" width="48%">
<img src="https://i.imgur.com/oT1jwDB.png" alt="CLI Process 06" width="48%">
<img src="https://i.imgur.com/wBVWet1.png" alt="CLI Process 07" width="48%">
<img src="https://i.imgur.com/Qo2jYCy.png" alt="CLI Process 08" width="48%">

</br>

## Booksight Mobile Application:

### Landing, About, and Tips Pages:

<img src="https://github.com/MyPetLobster/booksight/assets/6979547/2822aba5-c3f1-4d7d-8be2-3a8bc7f7ab43" width="32%">
<img src="https://github.com/MyPetLobster/booksight/assets/6979547/7d563ad1-adac-439a-b599-3182d6e5458c" width="32%">
<img src="https://github.com/MyPetLobster/booksight/assets/6979547/08e2e15e-c491-4dcc-9b58-c2f45b89f6bd" width="32%">

### Full Process (5 Parts):
<img src="https://github.com/MyPetLobster/booksight/assets/6979547/9c2dc6ca-9d75-414c-93fd-651ddbb06ceb" width="32%">
<img src="https://github.com/MyPetLobster/booksight/assets/6979547/2208104d-b0f3-4ffe-b766-5cb6dd775748" width="32%">
<img src="https://github.com/MyPetLobster/booksight/assets/6979547/a20e86ff-4757-4aaa-af0f-ac53632e753e" width="32%">
<img src="https://github.com/MyPetLobster/booksight/assets/6979547/5f38fee9-34e7-48f1-a116-c6aa83eb4e05" width="32%">
<img src="https://github.com/MyPetLobster/booksight/assets/6979547/8e1bbb7b-fd21-42d5-9533-b100a76b264a" width="32%">

</br>

# Getting Started
To get a local copy up and running follow these steps.

### Prerequisites
BookSight is built with Django, so you'll need to have Python installed on your machine. You can download Python [here](https://www.python.org/downloads/).


## Installation

**Note:** As of 6/17/2024, I have started using the Google Console API to access the Google Books and Google Gemini APIs. And the Gemini token counter uses Vertex AI, which also uses Google Console. This all requires a billing account to be set up. I've done a ton of testing and have yet to actually be charged for anything, so you should be able to mess around without incurring any charges. The only API key that you will have to shell out at least one month of fees for is ISBNdb. The rate limit is very strict and calls are limited to between 1,000 and 10,000 per day depending on the plan you choose. For reference -- on average, it takes Booksight about 10 calls to ISBNdb to identify EACH book in an image.

* API Keys Required for BookSight
    - OpenAI API Key (paid - free credits often available)
    - Google Gemini API Key (available for free as of 5/31/2024)
    - Open Library API Key
    - ISBNdb API Key  (paid)

    </br>
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
    **Note:** The GMAIL_USERNAME and GMAIL_PASSWORD are used to send emails to users when their book identification process is complete. Feel free to modify the email settings to use the email service of your choice. If you use google, you will need to setup an app password for your gmail account. Remember to change the code that retrieves the email and password from the .env file to match the variable names you choose. That can be found in 'booksight/booksight/settings.py'.

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

</br>


# Usage

## Web Application
1. Use the form on the landing page to upload an image of a bookshelf/bookcase, enter your email address, and choose the export format.
2. Submit the form.
3. Sit back and relax while the application identifies all the books in the image. You will receive an email when the process is complete.

</br>

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

</br>


<!-- CONTACT -->
# Contact

Cory Suzuki - bookcasedatabase@gmail.com

Project Link: [https://github.com/MyPetLobster/booksight](https://github.com/MyPetLobster/booksight)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

</br>


<!-- ACKNOWLEDGMENTS -->
# Acknowledgments

* [Img Shields](https://shields.io)
* [OpenCV Docs](https://docs.opencv.org/master/index.html)



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
