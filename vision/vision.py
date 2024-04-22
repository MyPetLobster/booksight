import time

import cv2 as cv 
import easyocr
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI()


GPT_MODEL = "gpt-3.5-turbo"
GPT_TEMP = 0.5




def main():
    now = time.time()
    text = detect_text("vision/test_images/two_books_red.jpeg")
    print(text)

    book_info = identify_book_info(text)
    print(book_info)

    print(f"Time taken: {time.time() - now:.2f} seconds")
    



def detect_text(jpeg_file):
    new_img = preprocess_image(jpeg_file)
    text_as_string = ""

    reader = easyocr.Reader(['en'], gpu=True)

    # Rotate the image by 90, 180, and 270 degrees, and read the text in each rotated image.
    img_90 = cv.rotate(new_img, cv.ROTATE_90_CLOCKWISE)
    img_180 = cv.rotate(new_img, cv.ROTATE_180)
    img_270 = cv.rotate(new_img, cv.ROTATE_90_COUNTERCLOCKWISE)

    results = {}

    results["original"] = reader.readtext(new_img)
    results["180"] = reader.readtext(img_180)
    results["90"] = reader.readtext(img_90)
    results["270"] = reader.readtext(img_270)

    for orientation, result in results.items():
        if len(result) > 1:
            for i in range (len(result)):
                text_as_string += result[i][1].replace(" ", "") + " " + "\n"
        
    return text_as_string


def preprocess_image(jpeg_file):
    img = cv.imread(jpeg_file)
    resize_img = cv.resize(img, (0, 0), fx=0.7, fy=0.7)
    gray_img = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)

    # (Contrast Limited Adaptive Histogram Equalization) 
    clahe = cv.createCLAHE(clipLimit=4, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray_img)

    # Increase the contrast of the image and decrease the brightness.
    new_img = np.zeros(clahe_img.shape, clahe_img.dtype)
    alpha, beta = 1.8, -50
    new_img = cv.convertScaleAbs(clahe_img, alpha=alpha, beta=beta)

    return new_img










def identify_book_info(text):
    # Use OpenAI to identify the book information.
    messages = [
        {"role": "system", "content": """You know everything there is to know about every book in existence. 
            You have a very important task. You will be provided with a string of text formatted as a list of all OCR detection
            text. Some of this text will be gibberish, but some of it will contain the title and author of a book. Information
            about the books may be split across multiple list items or lines. The detection text may be separated by author's first
            name and last name, or they may be included in the same line. You must read through all the data before you can begin 
            identifying the books.
            
            Your task is to identify the book information from the text. There may also be other information in the text, 
            such as publisher or award stickers. You may ignore this information. You may also ignore any text that is not 
            relevant to the book information. But be careful not to ignore any relevant information. You must identify the 
            book information from the text. In most cases, the book's author and title will be in the text. 
            But sometimes some information may be missing. Do your best in these cases.

            Use information throughout the string and connect the dots to try and determine the exact edition of a book. For example,
            if you see text that might be referencing the book "Pachinko by Min Jin Lee" and also see text that reads "10 Best Books, NY Times
            Book Review 2017", you can infer that this info is located on the cover of one of the books. Then you can deduce that 
            the book is the 2017 edition of "Pachinko" by Min Jin Lee. If there is only one version/ISBN of tha book that includes the 
            additional information, then you may include the ISBN and all other possible information in your response. There is an example 
            of the format of the response at the end of this prompt. But if you can figure out more info about a book, please add 
            as many additional fields to the JSON response as you need. The more info, the better. 
         
            Once you have identified all the books in the text, please format your response as a JSON object with the following
            structure:
         
            {
                "books": [
                    {
                        "title": "The Hidden Palace",
                        "author": "Helene Wecker",
                        "other_info": "Publisher might be HarperCollins"
                    },
                    {
                        "title": "The Night Circus",
                        "author": "Erin Morgenstern",
                        "other_info": "None"
                    },
                    {
                        "title": "Pachinko",
                        "author": "Min Jin Lee",
                        "published": "February 7, 2017",
                        "publisher": "Grand Central Publishing",
                        "isbn": "9781455563937",
                        "page_count": "496",
                        "other_info": "10 Best Books, NY Times Book Review 2017, National Book Award Finalist, 2017"
                    }
                ]
            }

            If you are unable to identify any books in the text, please format your response as a JSON object with an empty list:

            {
                "books": []
            }
            
            Important: MAKE SURE YOU DON'T MISS ANY BOOKS. Once you think you're done, go back through all text detections and 
            make sure you haven't missed anything. There may be books that are not as obvious as others.
         
            Here is the text for you to analyze: """ + text
        }
    ]

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=GPT_TEMP,
        max_tokens=100,
    )

    return response.choices[0].message.content
    

## Dev functions
def show_image(img):
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()












if __name__ == "__main__":
    main()

