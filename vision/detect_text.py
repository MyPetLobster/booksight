import os
import time

import cv2 as cv
import numpy as np
import easyocr as ocr

from booksight.settings import MEDIA_ROOT
from . import utility as util

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
    # Initialize the OCR reader
    reader = ocr.Reader(lang_list=['en'], gpu=True)

    # Define inner function to process the image
    def process_image(image, with_threshold, to_preprocess):
        """
        This function processes an image by applying preprocessing and text detection.

        Args:
            image (numpy.ndarray): The image array.
            with_threshold (bool): A boolean indicating whether to apply a threshold to the image.
            to_preprocess (bool): A boolean indicating whether to preprocess the image.

        Returns:
            list: A list of strings containing the detected text.
        """
        util.log_print(f"preprocess: {to_preprocess}\nthreshold: {with_threshold}\n")
        if to_preprocess:
            preprocessed_image = preprocess(image, with_threshold)
        else:
            preprocessed_image = image

        # Detect text in the preprocessed image, detail=1 returns bounding box coordinates, text, and confidence score
        result = reader.readtext(preprocessed_image, detail=1)

        # Use data from the OCR results to draw bounding boxes around the detected text and save image with the boxes
        bboxes_drawn = draw_bounding_boxes(preprocessed_image, result, image_path)

        if bboxes_drawn:
            util.log_print(f"Bounding boxes drawn for image: {image_path}\n")
            # Return a list of detected text greater than 2 characters
            return [text for bbox, text, _ in result if len(text) > 2]
        else:
            util.log_print(f"Bounding boxes not drawn for image: {image_path}\n")
            return []

    # Read the image and resize if necessary
    original_image = cv.imread(image_path)
    util.log_print(f"\nOriginal image shape: {original_image.shape}\n")

    # If og_image.shape[1] (number of columns) is greater than 800, resize the image while maintaining aspect ratio
    if original_image.shape[1] > 800:
        scale_percent = 800 / original_image.shape[1] * 100
        width = int(original_image.shape[1] * scale_percent / 100)
        height = int(original_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        original_image = cv.resize(original_image, dim, interpolation=cv.INTER_AREA)
        util.log_print(f"Resized image shape: {original_image.shape}\n\n")

    # Process the raw image and the image rotated 90 degrees counter-clockwise
    util.log_print(f"Detecting all text from image: {image_path}\n")
    book_text_list = process_image(original_image, False, False)
    util.log_print(f"Text detected (original image): {book_text_list}\n")
    original_90 = process_image(cv.rotate(original_image, cv.ROTATE_90_COUNTERCLOCKWISE), False, False)
    util.log_print(f"Text detected (original rotated 90 degrees): {original_90}\n")

    # Basic preprocessing with and without threshold
    no_threshold = process_image(original_image, False, True)
    util.log_print(f"Text detected No Threshold: {no_threshold}")
    no_threshold_90 = process_image(cv.rotate(original_image, cv.ROTATE_90_COUNTERCLOCKWISE), False, True)
    util.log_print(f"Text detected Rotate 90 No Threshold: {no_threshold_90}\n")

    # Combine all detected text lists
    util.log_print("\nCompleted text detection. Combining results...\n")    
    book_text_list.extend(original_90)
    book_text_list.extend(no_threshold)
    book_text_list.extend(no_threshold_90)
    util.log_print(f"\nCombined text list: {book_text_list}\n")

    # Remove duplicates and return the list of detected text
    util.log_print("Removing duplicates...\n")
    book_text_list = list(set(book_text_list))
    util.log_print(f"Unique text list: {book_text_list}\n\n")

    return book_text_list


def preprocess(image, threshold):
    """
    This function preprocesses an image by adjusting the brightness, normalizing the image, removing noise, converting to
    grayscale, and smoothing. A threshold can be applied to the image for potential text detection improvements.

    Args:
        image (numpy.ndarray): The image array.
        threshold (bool): A boolean indicating whether to apply a threshold to the image.

    Returns:
        img (numpy.ndarray): The preprocessed image array.
    """
    img = adjust_brightness(image)
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    img = cv.normalize(image, norm_img, 0, 255, cv.NORM_MINMAX)
    img = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if threshold:
        # cv.threshold returns a tuple of retval and the thresholded image, we only need the image
        _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    return img


def draw_bounding_boxes(image, detections, image_path):
    """
    This function draws bounding boxes around the detected text in an image. It saves the image with the bounding boxes 
    in the 'vision/images/detection_temp' directory.

    Args:
        image (numpy.ndarray): The image array.
        detections (list): A list of tuples containing the bounding box coordinates, text, and confidence score.
        image_path (str): The path to the image file.

    Returns:
        bool: A boolean indicating whether the bounding boxes were drawn and saved successfully.
    """
    # Copy the image to draw bounding boxes
    image_with_boxes = image.copy()
    
    for detection in detections:
        bbox, text, _ = detection

        # Convert the bounding box coordinates to integers
        top_left = tuple(map(int, bbox[0])) 
        bottom_right = tuple(map(int, bbox[2]))  
        
        # Draw the bounding box and include the OCR text on the image (defining font, scale, color, and thickness)
        cv.rectangle(image_with_boxes, top_left, bottom_right, (0, 255, 0), 5)
        cv.putText(image_with_boxes, text, top_left, cv.FONT_HERSHEY_COMPLEX_SMALL, 0.85, (255, 0, 0), 2)
    
  
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = image_path.split("/")[-1].split(".")[0]
    
    # If file already exists with same timestamp, add incrementing number to filename
    if os.path.exists(os.path.join(MEDIA_ROOT, f"detection_temp/debug_images/{filename}_text_detection_{timestamp}.jpeg")):
        i = 1
        while os.path.exists(os.path.join(MEDIA_ROOT, f"detection_temp/debug_images/{filename}_text_detection_{timestamp}-{i}.jpeg")):
            i += 1
        timestamp = f"{timestamp}-{i}"

    # Save text detection images to media/detection_temp/debug_images    
    text_detect_path = os.path.join(MEDIA_ROOT, f"detection_temp/debug_images/{filename}_text_detection_{timestamp}.jpeg")
    cv.imwrite(text_detect_path, image_with_boxes)

    # Return True if the image was saved successfully
    if os.path.exists(text_detect_path):
        return True


def adjust_brightness(image):
    """
    This function adjusts the brightness of an image by calculating the average brightness and applying a factor to
    normalize the image. Target brightness is set to 120.

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
    factor = 120 / brightness 
    brightened_image = cv.multiply(img_float, factor)
    brightened_image = np.clip(brightened_image, 0, 255) 

    return brightened_image.astype(np.uint8)