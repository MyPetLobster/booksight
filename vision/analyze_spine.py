from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.image as mpimg
import numpy as np
import cv2 as cv

def analyze_spine(image_path):
    # Process colors
    average_color = find_average_color_simple(image_path)
    dominant_color, color_palette, height, width = find_color_palette(image_path)

    return average_color, dominant_color, color_palette, height, width


def find_average_color_simple(image_path):
    # Load the image
    image = Image.open(image_path)
    image_array = np.array(image, dtype=np.uint8)  # Ensure the array is uint8

    # Calculate the average color of all pixels in the image
    average_color = np.mean(image_array, axis=(0, 1))

    return average_color.astype(int)


def find_color_palette(image_path):
    # Load the image
    image = mpimg.imread(image_path)

    # Get dimensions
    height, width, depth = image.shape

    pixels = image.reshape((height * width, depth))

    n_colors = 6

    # Perform KMeans clustering to find the dominant colors
    kmeans = KMeans(n_clusters=n_colors, random_state=34).fit(pixels)

    color_palette = np.uint8(kmeans.cluster_centers_)
    dominant_color = color_palette[np.argmax(kmeans.labels_.size)]

    return dominant_color, color_palette, height, width


def get_color_data(image_path):
    average_color, dominant_color, color_palette, height, width = analyze_spine(image_path)
    return average_color, dominant_color, color_palette