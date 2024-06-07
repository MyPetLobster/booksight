import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans




def analyze_spine(image_path):
    """
    This function analyzes the spine of a book image to find the average color, dominant color, and color palette, 
    as well as the height and width of the image.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        tuple: A tuple containing the average color, dominant color, color palette, height, and width of the image.
    """
    average_color = find_average_color_simple(image_path)
    dominant_color, color_palette, height, width = find_color_palette(image_path)

    return average_color, dominant_color, color_palette, height, width


def find_average_color_simple(image_path):
    """
    This function finds the average color of a book spine image using a simple np.mean calculation.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        np.array: An array containing the average color values.
    """
    # Open image with PIL and convert to numpy array with uint8 data type
    image = Image.open(image_path)
    image_array = np.array(image, dtype=np.uint8)

    # Find average color by taking the mean of all pixel values
    average_color = np.mean(image_array, axis=(0, 1)).astype(int)

    return average_color


def find_color_palette(image_path):
    """
    This function finds the dominant color and color palette of a book spine image using KMeans clustering.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: A tuple containing the dominant color, color palette, height, and width of the image.
    """
    # Read image using matplotlib and reshape pixel values for KMeans clustering
    image = mpimg.imread(image_path)
    height, width, depth = image.shape
    pixels = image.reshape((height * width, depth))
    n_colors = 6

    # Perform KMeans clustering to find the dominant colors and color palette
    kmeans = KMeans(n_clusters=n_colors, random_state=34).fit(pixels)
    color_palette = np.uint8(kmeans.cluster_centers_)
    dominant_color = color_palette[np.argmax(kmeans.labels_.size)]

    return dominant_color, color_palette, height, width