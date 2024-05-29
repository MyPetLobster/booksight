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
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
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


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
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

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

<Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.>

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

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
