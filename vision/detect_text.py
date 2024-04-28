import easyocr as ocr
import cv2 as cv
import numpy as np




def preprocess(image):
    # Normalize the image
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    img = cv.normalize(image, norm_img, 0, 255, cv.NORM_MINMAX)

    # Noise removal
    img = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)

    # Convert to greyscale
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Thresholding
    _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    return img


def detect_text(image_path):
    image = cv.imread(image_path)

    image = preprocess(image)

    reader = ocr.Reader(['en'])

    results = []

    result = reader.readtext(image, detail=0)
   
    # rotate img 90 degrees counter-clockwise
    image90 = preprocess(cv.rotate(cv.imread(image_path), cv.ROTATE_90_COUNTERCLOCKWISE))
    result90 = reader.readtext(image90, detail=0)

    book_text_list = result + result90
    book_text_string = " ".join(book_text_list)

    results.append(book_text_string)

    return results


def main():
    detect_text("vision/spines/book_01.jpeg")




if __name__ == "__main__":
    main()