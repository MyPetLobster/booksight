import os
import pathlib
import textwrap
from dotenv import load_dotenv

import google.generativeai as genai


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')


text = """
    Individual Spine OCR Text:
    Book_0: ['JUNII ITO, uiz, UZMAkL, UZUMAKL'],
    Book_1: ['0  O x, Oduci, History, BFARD, MARY, Romi, ROME,   O x, Hisiory, 01 ANCIENT, of AFciini, Ului'],
    Book_2: ['Haruki MuRakami, N 0 R W E 6 a N, W 0 0 d'],
    Book_3: ['Tilss, DESTSELLER, Jont, MhE etattgt, Metoat, Mue etaftGT, AVAL, Jiond, Wetoat, WAR ip SEBASTIAI JUIGER p4, Author or, nheS, 1 WAR ile SEBASTIAII JUHGER, Iuthor0'],
    Book_4: ['Rure, ThE LAUGHING MONSTERS, DEMIS J0HNSOM, IER, 2134, THE LAUGHING MONSTERS'],

    Full Image OCR Text:
    ['THELa, uiz, 1 WAR ie SEBASTIAI JUHGER, IMe ctaftGT, Ha R U K  M U Ra ka M , ROMe, TInIes, 0 Aneont, sioat, DESTSELLER, 0  O x, Mhl ctattGT, JDANSOM, Auimor Of, 0 Hicont, DENIS, Bestsellea, BARY, Auimor 0f, H1R U K M U Ra ka m , n  O e, Stoat, Uig, n 0 R W E gian W 0 0 d, New Yori, JUNII ITO, Syre, 05 BENIS J0hMSIM, ROME, DNes, N 0 R W E g a nW 0 0 d, BVARS, UZUMAKL, THE LAUGHING MONSTERS 8, Wew York, 1 WAR ipe SEBASTIAI JUIGER']
    """

prompt = f"""You will receive a string formatted as list of text detected from spines of books, formatted like this --
        "Book_X: <OCR text>,". You must interpret the OCR text and identify each book's title and author. The OCR text may contain errors,
        unconventional spacing, or other issues that require intelligent parsing to deduce the correct information. Return a JSON-formatted
        string where each "Book_X" identifier is associated with an "author" and "title" key. If a book title and/or author cannot be confidently
        identified, use "Unknown" as the value. Correct all spelling and spacing errors in your response.
        
        The input text that follows "Full Image OCR Text: " is a scan of the full input image. If you have trouble identifying a spine's 
        text, there may be additional clues in the full image text. Additionally, there may be books whose spines went undetected. 
        If you identify additional books within that text, include them in the response, but you will have to add additional "Book_X" identifiers.

        Use every resource at your disposal to decipher the text and correctly identify all book titles and authors. Accuracy is critical. 

        - DO NOT MAKE UP BOOK TITLES OR AUTHORS. Use all of the data you have to identify a REAL author and REAL book title that would make 
        sense in the context of OCR text from the spine of a book. For Example, if you have some OCR text that says "HARY BFARD ROME Q R mistory", 
        You should be able to look through existing books and realize that the book is "SPQR" by Mary Beard. Do not include
        subtitles. Do not make up any authors or titles. 

        - If you are only able to identify an author, you should search your knowledge to find all the books that author has written, then 
        use that information along with the other letters in the OCR text in order to determine which title is most likely to be correct. Use the 
        same problem solving logic if you are only able to identify a title.

        - Your response is being decoded directly with Python's json.loads() function. Make sure your response is in the correct format without
        any additional characters or formatting.

        Here is the input text you will be working with: 

        ```{text}```
        """

def run_gemini(prompt):
    response = model.generate_content(prompt)
    print(response.text)



if __name__ == '__main__':
    run_gemini(prompt)



