import cv2 as cv 
import numpy as np

import easyocr 

import time


def main(jpeg_file):
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

    # detections stored as 3-tuples: (bbox, text, prob)
    print("DETECTIONS:")
    for detection in result:
        if len(detection[1]) > 2:
            # remove spaces 
            print(detection[1].replace(" ", ""))

    print("Time taken: ", time.time() - now)












if __name__ == "__main__":
    # Test the main function with a sample jpeg file.
    jpeg_file = "vision/test_images/two_books.jpeg"
    main(jpeg_file)

