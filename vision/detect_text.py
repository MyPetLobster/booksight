import math
import time

import cv2 as cv
import numpy as np
import easyocr as ocr

from utility import log_print

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

    def process_image(image, with_threshold, raw_processed):
        if not raw_processed:
            preprocessed_image = preprocess(image, with_threshold)
        else:
            preprocessed_image = image

        result = reader.readtext(preprocessed_image, detail=1)
        draw_bounding_boxes(preprocessed_image, result, "process_image")
        return [text for bbox, text, _ in result if len(text) > 2]

    def alt_process_one(image):
        """
        Preprocesses an image for OCR using EasyOCR.

        Args:
            image_path: Path to the input image.

        Returns:
            preprocessed_image: The preprocessed image ready for OCR.
        """
        # Convert to grayscale
        grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # Adaptive thresholding for better contrast
        thresh = cv.adaptiveThreshold(grayscale_image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, 2)

        # Deskew the image if necessary (adjust threshold as needed)
        coords, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(coords) > 0:
            largest_contour = max(coords, key=cv.contourArea)
            approx = cv.approxPolyDP(largest_contour, 0.02 * cv.arcLength(largest_contour, True), True)
            if len(approx) == 4:
                corners = np.reshape(approx, (4, 2))
                top_left, top_right, bottom_right, bottom_left = corners
                width_top = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
                width_bottom = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
                if abs(width_top - width_bottom) > 10:
                    angle = math.degrees(math.atan((top_right[1] - top_left[1]) / (top_right[0] - top_left[0])))
                    M = cv.getRotationMatrix2D((image.shape[1] // 2, image.shape[0] // 2), angle, 1.0)
                    deskewed_image = cv.warpAffine(thresh, M, (image.shape[1], image.shape[0]))
                    thresh = deskewed_image

        # Noise reduction (adjust kernel size as needed)
        denoised_image = cv.bilateralFilter(thresh, 9, 75, 75)

        # Morphological closing to remove small holes (adjust kernel size as needed)
        kernel = np.ones((5, 5), np.uint8)
        closed_image = cv.morphologyEx(denoised_image, cv.MORPH_CLOSE, kernel)

        # Invert the image for EasyOCR
        preprocessed_image = cv.bitwise_not(closed_image)

        result = reader.readtext(preprocessed_image, detail=1)
        draw_bounding_boxes(preprocessed_image, result, "alt_process_one")
        return [text for bbox, text, _ in result if len(text) > 2]



    def alt_process_two(image):
        # Read the image using OpenCV
        
        if image is None:
            raise FileNotFoundError(f"No image found at the path {image_path}")
        
        # Convert image to grayscale
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Calculate the average brightness of the grayscale image
        brightness = np.mean(gray)
        
        # Adjust brightness and contrast based on the average brightness
        if brightness < 130:
            alpha = 1.5  # Contrast control (1.0-3.0)
            beta = 50    # Brightness control (0-100)
        else:
            alpha = 1.1  # Lesser contrast adjustment
            beta = 20    # Lesser brightness adjustment
        
        adjusted = cv.convertScaleAbs(gray, alpha=alpha, beta=beta)
        
        # Apply GaussianBlur to reduce image noise if it's too high
        blurred = cv.GaussianBlur(adjusted, (5, 5), 0)
        
        # Apply thresholding to get a binary image
        _, thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        
        # Edge enhancement
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        sharpened = cv.filter2D(thresh, -1, kernel)
        
        result = reader.readtext(sharpened, detail=1)
        draw_bounding_boxes(sharpened, result, "alt_process_two")
        return [text for bbox, text, _ in result if len(text) > 2]




    original_image = cv.imread(image_path)

    # If image width is greater than 800 pixels, resize the image while maintaining the aspect ratio
    log_print(f"\nOriginal image shape: {original_image.shape}\n")
    if original_image.shape[1] > 800:
        scale_percent = 800 / original_image.shape[1] * 100
        width = int(original_image.shape[1] * scale_percent / 100)
        height = int(original_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        original_image = cv.resize(original_image, dim, interpolation=cv.INTER_AREA)
        log_print(f"Resized image shape: {original_image.shape}\n\n")

    # Process the raw image and the image rotated 90 degrees counter-clockwise
    log_print(f"Detecting all text from image: {image_path}\n")
    book_text_list = process_image(original_image, False, False)
    log_print(f"Text detected (original image): {book_text_list}\n")
    original_90 = process_image(cv.rotate(original_image, cv.ROTATE_90_COUNTERCLOCKWISE), False, False)
    log_print(f"Text detected (original rotated 90 degrees): {original_90}\n")

    # Basic preprocessing with and without threshold
    full_preprocess = process_image(original_image, True, True)
    log_print(f"Text detected (full preprocess): {full_preprocess}\n")
    full_preprocess_90 = process_image(cv.rotate(original_image, cv.ROTATE_90_COUNTERCLOCKWISE), True, True)
    log_print(f"Text detected (full preprocess rotated 90 degrees): {full_preprocess_90}\n")
    no_threshold = process_image(original_image, False, True)
    log_print(f"Text detected No Threshold: {no_threshold}\n")
    no_threshold_90 = process_image(cv.rotate(original_image, cv.ROTATE_90_COUNTERCLOCKWISE), False, True)
    log_print(f"Text detected Rotate 90 No Threshold: {no_threshold_90}\n")


    # Two alternative preprocessing approaches

    image = cv.imread(image_path)
    alt_preprocessing_01 = alt_process_one(image)
    log_print(f"Text detected (alt preprocess 01): {alt_preprocessing_01}\n")
    alt_preprocessing_01_90 = alt_process_one(cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE))
    log_print(f"Text detected (alt preprocess 01 rotated 90 degrees): {alt_preprocessing_01_90}\n")
    alt_preprocessing_02 = alt_process_two(image)
    log_print(f"Text detected (alt preprocess 02): {alt_preprocessing_02}\n")
    alt_preprocessing_02_90 = alt_process_two(cv.rotate(image, cv.ROTATE_90_COUNTERCLOCKWISE))
    log_print(f"Text detected (alt preprocess 02 rotated 90 degrees): {alt_preprocessing_02_90}\n")


    log_print("\nCompleted text detection. Combining results...\n")    
    book_text_list.extend(original_90)
    book_text_list.extend(full_preprocess)
    book_text_list.extend(full_preprocess_90)
    book_text_list.extend(no_threshold)
    book_text_list.extend(no_threshold_90)
    book_text_list.extend(alt_preprocessing_01)
    book_text_list.extend(alt_preprocessing_01_90)
    book_text_list.extend(alt_preprocessing_02)
    book_text_list.extend(alt_preprocessing_02_90)
    log_print(f"Combined text list: {book_text_list}\n")

    # Remove duplicates and return the list of detected text
    log_print("\nRemoving duplicates...\n")
    book_text_list = list(set(book_text_list))

    log_print("\nbook_text_list: ")
    return book_text_list


def preprocess(image, threshold):
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


def draw_bounding_boxes(image, detections, function_name):
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
    cv.imwrite(f"vision/images/detection_temp/debug_images/text_detection_{timestamp}_{function_name}.jpeg", image_with_boxes)


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
    factor = 120 / brightness 
    brightened_image = cv.multiply(img_float, factor)
    brightened_image = np.clip(brightened_image, 0, 255) 

    return brightened_image.astype(np.uint8)