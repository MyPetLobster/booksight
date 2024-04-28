import easyocr as ocr
import cv2 as cv
import numpy as np



def preprocess(image):
    # Convert the image to greyscale
    greyscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Scale the image to 300 dpi
    dpi = 300
    scale_percent = dpi / 96
    width = int(greyscale_image.shape[1] * scale_percent)
    height = int(greyscale_image.shape[0] * scale_percent)
    dim = (width, height)
    resized_image = cv.resize(greyscale_image, dim, interpolation=cv.INTER_AREA)

    # Enhance the image
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(16,16))
    enhanced_image = clahe.apply(resized_image)
    
    return enhanced_image


def detect_text():
    image_path = "vision/spines/book_0.jpeg"
    image = cv.imread(image_path)

    cv.imshow("Original Image", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    image = preprocess(image)

    cv.imshow("Preprocessed Image", image)
    cv.waitKey(0)
    cv.destroyAllWindows()


    reader = ocr.Reader(['en'])

    results = []

    result = reader.readtext(image, detail=0)
    results.append(result)

    # rotate img 90 degrees counter-clockwise
    image90 = preprocess(cv.rotate(cv.imread(image_path), cv.ROTATE_90_COUNTERCLOCKWISE))
    result90 = reader.readtext(image90, detail=0)
    results.append(result90)

    print(results)


def main():
    detect_text()




if __name__ == "__main__":
    main()