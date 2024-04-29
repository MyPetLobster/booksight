from PIL import Image
import numpy as np
import cv2 as cv

def analyze_spine(image_path):
    # Load the image
    image = Image.open(image_path)
    image_array = np.array(image, dtype=np.uint8)  # Ensure the array is uint8

    # Get the dimensions of the image and x y coordinates
    x, y, height, width = find_spine_dimensions(image_path)

    # Crop the image to the spine
    image_array = image_array[y:y + height, x:x + width]

    # Process colors
    average_color = find_average_color(image_array)
    dominant_color = find_dominant_color(image_array)

    return average_color, dominant_color, height, width

def find_average_color(image_array):
    # Calculate the average color of the image
    average_color = np.mean(image_array, axis=(0, 1))
    average_color = np.round(average_color).astype(int)
    return average_color

def find_dominant_color(image_array):
    # Reshape the image array to a 2D array of pixels
    pixels = image_array.reshape(-1, 3)
    # Calculate the histogram of colors
    color_histogram = np.histogramdd(pixels, bins=(32, 32, 32), range=[(0, 256), (0, 256), (0, 256)])[0]
    # Find the index of the most frequent color
    most_frequent_index = np.unravel_index(color_histogram.argmax(), color_histogram.shape)
    # Calculate the dominant color
    dominant_color = np.array(most_frequent_index) * 8
    return dominant_color


def find_spine_dimensions(image_path):
    # Load the image and convert to a proper NumPy array
    image = Image.open(image_path)
    image_array = np.array(image, dtype=np.uint8)  # Ensure the array is uint8

    # Convert the image to grayscale
    gray = cv.cvtColor(image_array, cv.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to highlight the spine
    adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv.THRESH_BINARY, 11, 2)

    # Apply edge detection
    edges = cv.Canny(adaptive_thresh, 50, 150, apertureSize=3)

    # Find the contours in the image
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filter out contours that do not have the typical aspect ratio of a book spine
    potential_spines = [cnt for cnt in contours if is_spine(cnt)]

    # Select the contour with the largest area, which should be the spine
    if potential_spines:
        largest_contour = max(potential_spines, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(largest_contour)
        cv.imshow("Spine", image_array[y:y + h, x:x + w])
        cv.waitKey(0)
        cv.destroyAllWindows()
        return x, y, h, w
    else:
        return 0, 0, 0, 0  # Return zeros if no spine-like contours are found

def is_spine(contour):
    _, _, w, h = cv.boundingRect(contour)
    aspect_ratio = h / w
    # Assuming that a book spine has a height greater than its width and within a reasonable range
    return aspect_ratio > 2 and h > 100  # height threshold to avoid very small contours

