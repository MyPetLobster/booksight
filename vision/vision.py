import time
import cv2 as cv
import numpy as np
import easyocr
from dotenv import load_dotenv


load_dotenv()


def main():
    start = time.time()
    jpeg_file = "vision/test_images/test_full.jpeg"
    new_image, new_height, new_width = preprocess_image(jpeg_file)
    original_img = cv.imread(jpeg_file)
    original_img = cv.resize(original_img, (new_width, new_height))

    identify_spines(new_image, original_img)

    print(f"Total Time Taken: {time.time() - start:.2f} seconds")


def preprocess_image(jpeg_file):
    img = cv.imread(jpeg_file)
    height, width = img.shape[:2]

    if height > 1000:
        scale = 1000 / height
        new_height = 1000
        new_width = int(width * scale)
    else:
        new_height = height
        new_width = width

    resize_img = cv.resize(img, (new_width, new_height))
    gray_img = cv.cvtColor(resize_img, cv.COLOR_BGR2GRAY)

    # Increase contrast
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_img = clahe.apply(gray_img)

    # Apply Gaussian blur
    blurred_img = cv.GaussianBlur(gray_img, (5, 5), 0)
    
    # Apply edge detection with adaptive thresholding
    edges = cv.adaptiveThreshold(
        blurred_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 21, 3
    )

    return edges, new_height, new_width


def identify_spines(edges, original_img):
    contours, _ = cv.findContours(
        edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        aspect_ratio = h / w
        if 2 <= aspect_ratio <= 10:
            if h > original_img.shape[0] * 0.1:
                cv.rectangle(original_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show_image(edges)
    # show_image(original_img)
    cv.imwrite("vision/progress_images/edges-240427-03.jpeg", edges)
    cv.imwrite("vision/progress_images/boxes-240427-03.jpeg", original_img)
    


def show_image(img):
    cv.imshow("Book Spine Detection", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()