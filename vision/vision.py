import time

import cv2 as cv 
import easyocr
import numpy as np

from dotenv import load_dotenv



load_dotenv()


def main():
    start = time.time()
    text = detect_text("vision/test_images/five_books.jpeg")

    print(f"TEXT: \n {text}")
    print(f"Total Time Taken: {time.time() - start:.2f} seconds")
    


def preprocess_image(jpeg_file):
    img = cv.imread(jpeg_file)

    height, width = img.shape[:2]

    if height > 750:
        scale = 750 / height
        new_height = 750
        new_width = int(width * scale)
    else:
        new_height = height
        new_width = width

    resize_img = cv.resize(img, (new_width, new_height))
    gray_img = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)

    # (Contrast Limited Adaptive Histogram Equalization) 
    clahe = cv.createCLAHE(clipLimit=4, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray_img)

    # Increase the contrast of the image and decrease the brightness.
    new_img = np.zeros(clahe_img.shape, clahe_img.dtype)
    alpha, beta = 1.8, -50
    new_img = cv.convertScaleAbs(clahe_img, alpha=alpha, beta=beta)

    cv.imwrite("vision/test_images/preprocessed_image.jpeg", new_img)
    return new_img


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
                text_as_string += result[i][1].replace(" ", "") + " "
        
    return text_as_string











    

## Dev functions
def show_image(img):
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()












if __name__ == "__main__":
    main()

