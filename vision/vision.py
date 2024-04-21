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
    text = detect_text("vision/test_images/two_books.jpeg")
    book_info = identify_book_info(text)
    print(book_info)


def detect_text(jpeg_file):
    now = time.time()

    # Load the image from the jpeg file.
    img = cv.imread(jpeg_file)
    
    # Resize the image to a smaller size.
    img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)

    # Convert the image to grayscale.
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Increase the contrast of the image.
    clahe = cv.createCLAHE(clipLimit=4, tileGridSize=(8, 8))

    # Apply the contrast limited adaptive histogram equalization (CLAHE) to the image.
    clahe_img = clahe.apply(gray_img)

    # Apply a Gaussian blur to the image.
    blur_img = cv.GaussianBlur(clahe_img, (5, 5), 0)

    new_img = np.zeros(blur_img.shape, blur_img.dtype)

    alpha = 1.3
    beta = -50

    new_img = cv.convertScaleAbs(blur_img, alpha=alpha, beta=beta)

    # cv.imshow("FINAL", new_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    reader = easyocr.Reader(['en'], gpu=True)

    # Rotate the image by 90, 180, and 270 degrees, and read the text in each rotated image.
    img_90 = cv.rotate(new_img, cv.ROTATE_90_CLOCKWISE)
    img_180 = cv.rotate(new_img, cv.ROTATE_180)
    img_270 = cv.rotate(new_img, cv.ROTATE_90_COUNTERCLOCKWISE)

    result = reader.readtext(new_img)
    result_90 = reader.readtext(img_90)
    result_180 = reader.readtext(img_180)
    result_270 = reader.readtext(img_270)

    # Combine the results from the four rotations.
    result.extend(result_90)
    result.extend(result_180)
    result.extend(result_270)

    text_as_string = ""

    # detections stored as 3-tuples: (bbox, text, prob)
    print("DETECTIONS:")
    for detection in result:
        if len(detection[1]) > 2:
            # remove spaces 
            print(detection[1].replace(" ", ""))
            text_as_string += detection[1].replace(" ", "") + " "
    
    print("Time taken: ", time.time() - now)

    return text_as_string


def identify_book_info(text):
    # Use OpenAI to identify the book information.
    messages = [
        {"role": "system", "content": """You know everything there is to know about every book in existence. 
            You have a very important task. You will be provided with a string of text. Some of this text will be gibberish,
            but some of it will contain the title and author of a book. Your task is to identify the book information from 
            the text. There may also be other information in the text, such as publisher or award stickers. You may ignore this
            information. You may also ignore any text that is not relevant to the book information. But be careful not to ignore 
            any relevant information. You must identify the book information from the text. In most cases, the book's author 
            and title will be in the text. But sometimes some information may be missing. Do your best in these cases.
         
            Once you have identified all the books in the text, please format your response as a JSON object with the following
            structure:
         
            {
                "books": [
                    {
                        "title": "The Hidden Palace",
                        "author": "Helene Wecker"
                    },
                    {
                        "title": "The Night Circus",
                        "author": "Erin Morgenstern"
                    }
                ]
            }

            If you are unable to identify any books in the text, please format your response as a JSON object with an empty list:

            {
                "books": []
            }

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
    

    













if __name__ == "__main__":
    main()

