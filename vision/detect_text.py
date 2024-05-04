import time

import cv2 as cv
import numpy as np
import easyocr as ocr


def detect_text(image_path):
    """
    This function detects text in an image and returns the OCR results. Images are preprocessed, then text detection 
    is applied 4 times per image to account for a 90 degree counter-clockwise rotation and with/without a threshold 
    applied. 
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        list: A list of strings containing the detected text.
    """
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


def preprocess(image, threshold=True):
    """
    This function preprocesses an image by adjusting the brightness, normalizing the image, removing noise, converting to
    grayscale, and smoothing. A threshold can be applied to the image for potential text detection improvements.

    Args:
        image (numpy.ndarray): The image array.
        threshold (bool): A boolean indicating whether to apply a threshold to the image.

    Returns:
        numpy.ndarray: The preprocessed image array.
    """
    img = adjust_brightness(image)
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    img = cv.normalize(image, norm_img, 0, 255, cv.NORM_MINMAX)
    img = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if threshold:
        _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    img = cv.GaussianBlur(img, (5, 5), 0)
    
    return img


def draw_bounding_boxes(image, detections):
    """
    This function draws bounding boxes around the detected text in an image. It saves the image with the bounding boxes 
    in the 'vision/images/detection_temp' directory.

    Args:
        image (numpy.ndarray): The image array.
        detections (list): A list of tuples containing the bounding box coordinates, text, and confidence score.

    Returns:
        None
    """
    image_with_boxes = image.copy()
    
    for detection in detections:
        bbox, text, _ = detection
        top_left = tuple(map(int, bbox[0])) 
        bottom_right = tuple(map(int, bbox[2]))  
        
        cv.rectangle(image_with_boxes, top_left, bottom_right, (0, 255, 0), 5)
        cv.putText(image_with_boxes, text, top_left, cv.FONT_HERSHEY_COMPLEX_SMALL, 0.65, (255, 0, 0), 2)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    cv.imwrite(f"vision/images/detection_temp/debug_images/text_detection_{timestamp}.jpeg", image_with_boxes)


def adjust_brightness(image):
    """
    This function adjusts the brightness of an image by calculating the average brightness and applying a factor to
    normalize the image.

    Args:
        image (numpy.ndarray): The image array.

    Returns:
        numpy.ndarray: The adjusted image array.
    """
    if len(image.shape) == 2 or image.shape[2] == 1:
        grayscale_image = image
    else:
        grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    brightness = cv.mean(grayscale_image)[0]

    img_float = image.astype(np.float32)
    factor = 127 / brightness 
    brightened_image = cv.multiply(img_float, factor)
    brightened_image = np.clip(brightened_image, 0, 255) 

    return brightened_image.astype(np.uint8)