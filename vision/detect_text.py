import time

import cv2 as cv
import numpy as np
import easyocr as ocr



def detect_text(image_path):
    reader = ocr.Reader(lang_list=['en'], gpu=True)
    results = []

    def process_image(image, with_threshold):
        preprocessed_image = preprocess(image, with_threshold)
        result = reader.readtext(preprocessed_image, detail=1)
        draw_bounding_boxes(preprocessed_image, result)
        return [text for bbox, text, _ in result if len(text) > 2]

    original_image = cv.imread(image_path)
    book_text_list = process_image(original_image, True)
    book_text_list += process_image(cv.rotate(original_image, cv.ROTATE_90_COUNTERCLOCKWISE), True)
    book_text_list += process_image(original_image, False)
    book_text_list += process_image(cv.rotate(original_image, cv.ROTATE_90_COUNTERCLOCKWISE), False)

    book_text_list = list(set([text for text in book_text_list if text.isalnum() or text.isspace()]))
    book_text_string = ", ".join(book_text_list)

    results.append(book_text_string)

    return results


def draw_bounding_boxes(image, detections):
    image_with_boxes = image.copy()
    
    for detection in detections:
        bbox, text, _ = detection
        top_left = tuple(map(int, bbox[0])) 
        bottom_right = tuple(map(int, bbox[2]))  
        
        cv.rectangle(image_with_boxes, top_left, bottom_right, (0, 255, 0), 5)
        cv.putText(image_with_boxes, text, top_left, cv.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    cv.imwrite(f"vision/images/detection_temp/debug_images/text_detection_{timestamp}.jpeg", image_with_boxes)


def calculate_brightness(image):
    # Check if the image is already in grayscale
    if len(image.shape) == 2 or image.shape[2] == 1:  # Grayscale image
        grayscale_image = image
    else:
        grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return cv.mean(grayscale_image)[0]


def adjust_brightness(image, brightness):
    img_float = image.astype(np.float32)
    factor = 127 / brightness 
    brightened_image = cv.multiply(img_float, factor)
    brightened_image = np.clip(brightened_image, 0, 255) 
    return brightened_image.astype(np.uint8)


def preprocess(image, threshold=True):
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
    if threshold:
        _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Smoothing
    img = cv.GaussianBlur(img, (5, 5), 0)
    
    return img


def detect_text(image_path):
    reader = ocr.Reader(lang_list=['en'], gpu=True)
    results = []
    
    original_image = cv.imread(image_path)
    preprocessed_image = preprocess(original_image, True)
    result_00 = reader.readtext(preprocessed_image, detail=1)
    draw_bounding_boxes(preprocessed_image, result_00)

    # Rotate original image once and then preprocess
    rotated_image = cv.rotate(original_image, cv.ROTATE_90_COUNTERCLOCKWISE)
    preprocessed_image_90 = preprocess(rotated_image, True)
    result_90 = reader.readtext(preprocessed_image_90, detail=1)
    draw_bounding_boxes(preprocessed_image_90, result_90)

    # If processing without threshold, do it from the original image
    image_00_no_thresh = preprocess(original_image, False)
    result_00_no_thresh = reader.readtext(image_00_no_thresh, detail=1)
    draw_bounding_boxes(image_00_no_thresh, result_00_no_thresh)

    image_90_no_thresh = preprocess(rotated_image, False)
    result_90_no_thresh = reader.readtext(image_90_no_thresh, detail=1)
    draw_bounding_boxes(image_90_no_thresh, result_90_no_thresh)

    book_text_list = [text for bbox, text, _ in result_00]
    book_text_list += [text for bbox, text, _ in result_90]
    book_text_list += [text for bbox, text, _ in result_00_no_thresh]
    book_text_list += [text for bbox, text, _ in result_90_no_thresh]

    book_text_list = [text for text in book_text_list if len(text) > 2]
    book_text_list = list(set(book_text_list)) # Remove dupes

    # Remove all non-alphanumeric characters
    book_text_list = ["".join(c for c in text if c.isalnum() or c.isspace()) for text in book_text_list]

    book_text_string = ", ".join(book_text_list)

    results.append(book_text_string)

    return results