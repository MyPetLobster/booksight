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

    # book_info = identify_book_info(text)
    # print(book_info)

    print(f"Time taken: {time.time() - now:.2f} seconds")
    



def detect_text(jpeg_file):
    new_img, resized_original = preprocess_image(jpeg_file)
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
                bg_color = extract_detection_bg_color(result[i], resized_original, orientation, i)
                text_as_string += f"#{i}: \n " + "ocr_text: " + result[i][1].replace(" ", "") + " " + "\n" + "bg_color: " + bg_color + "\n\n"
        
    return text_as_string


def preprocess_image(jpeg_file):
    img = cv.imread(jpeg_file)
    resize_img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
    gray_img = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)

    # (Contrast Limited Adaptive Histogram Equalization) 
    clahe = cv.createCLAHE(clipLimit=4, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray_img)

    # Increase the contrast of the image and decrease the brightness.
    new_img = np.zeros(clahe_img.shape, clahe_img.dtype)
    alpha, beta = 1.5, -50
    new_img = cv.convertScaleAbs(clahe_img, alpha=alpha, beta=beta)

    return new_img, resize_img


def extract_detection_bg_color(detection, parent_img, orientation="original", iteration=0):

    bounding_box = detection[0]

    np_array = np.array(bounding_box).astype(int)

    top_left = np_array[0]
    top_right = np_array[1]
    bottom_right = np_array[2]
    bottom_left = np_array[3]

    if orientation == "original":
        color_1 = parent_img[top_left[1], top_left[0]]
        color_2 = parent_img[top_right[1], top_right[0]]
        color_3 = parent_img[bottom_right[1], bottom_right[0]]
        color_4 = parent_img[bottom_left[1], bottom_left[0]]

    elif orientation == "180":
        color_1 = parent_img[top_left[1], top_left[0]]
        color_2 = parent_img[top_right[1], top_right[0]]
        color_3 = parent_img[bottom_right[1], bottom_right[0]]
        color_4 = parent_img[bottom_left[1], bottom_left[0]]

    elif orientation == "90":
        color_1 = parent_img[top_left[0], top_left[1]]
        color_2 = parent_img[top_right[0], top_right[1]]
        color_3 = parent_img[bottom_right[0], bottom_right[1]]
        color_4 = parent_img[bottom_left[0], bottom_left[1]]

    elif orientation == "270":
        color_1 = parent_img[top_left[0], top_left[1]]
        color_2 = parent_img[top_right[0], top_right[1]]
        color_3 = parent_img[bottom_right[0], bottom_right[1]]
        color_4 = parent_img[bottom_left[0], bottom_left[1]]

    # Average the colors
    color = ((color_1 + color_2 + color_3 + color_4) / 4).astype(int)

    # Convert to tuple
    color = tuple(color)
    return f"RGB({color})"









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
    

## Dev functions
def show_image(img):
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()












if __name__ == "__main__":
    main()

