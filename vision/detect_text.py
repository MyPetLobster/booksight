import cv2 as cv
import numpy as np
import easyocr as ocr

def calculate_brightness(image):
    grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return cv.mean(grayscale_image)[0]

def adjust_brightness(image, brightness):
    # Convert to float to prevent data type overflow/underflow
    img_float = image.astype(np.float32)
    if brightness < 100:
        factor = 110 / brightness  # scale factor to increase brightness
    elif brightness > 160:
        factor = 90 / brightness  # scale factor to decrease brightness
    else:
        return image  # return original if brightness is in a normal range
    brightened_image = cv.multiply(img_float, factor)
    brightened_image = np.clip(brightened_image, 0, 255)  # limit the values between 0 and 255
    return brightened_image.astype(np.uint8)


def preprocess(image):

    # Adjust the brightness of the image
    brightness = calculate_brightness(image)
    image = adjust_brightness(image, brightness)

    # Normalize the image
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    img = cv.normalize(image, norm_img, 0, 255, cv.NORM_MINMAX)

    # Noise removal
    img = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)

    # Convert to grayscale
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


    # Thresholding
    _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Smoothing
    img = cv.GaussianBlur(img, (5, 5), 0)

    cv.imshow("Image", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    return img


def detect_text(image_path):
    reader = ocr.Reader(lang_list=['en'], gpu=True)
    results = []
    
    image = preprocess(cv.imread(image_path))
    result_00 = reader.readtext(image, detail=0)

    image_90 = preprocess(cv.rotate(cv.imread(image_path), cv.ROTATE_90_COUNTERCLOCKWISE))
    result_90 = reader.readtext(image_90, detail=0)

    book_text_list = result_00 + result_90
    book_text_list = [text for text in book_text_list if len(text) > 2]
 
    book_text_string = ", ".join(book_text_list)

    results.append(book_text_string)

    print(results)
    return results


def main():
    detect_text("vision/spines/book_0.jpeg")




if __name__ == "__main__":
    main()