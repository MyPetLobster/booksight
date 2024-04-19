# booksight
App that takes photos of bookshelves and returns a .csv with info about all books in the photos


### Recording my process to use later 

1. Created virtual environment with `python3 -m venv .venv`
2. Activated virtual environment with `source .venv/bin/activate`
3. Installed Django with `python3 -m pip install Django`
4. Created Django project with `django-admin startproject booksight`
5. Created Django apps with 
```
python manage.py startapp dashboard 
python manage.py startapp vision
python manage.py startapp matcher
```
