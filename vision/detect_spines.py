import os

import cv2 as cv
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import torch
from torchvision import models, transforms
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

import utility as util

from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL

# Import the weights
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights

# Load a pre-trained Faster R-CNN model with the specified weights
model = models.detection.fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.COCO_V1)
model.eval()

# Define the image transformation
transform = transforms.Compose([
    transforms.ToTensor(),
])

book_count = 0 



def crop_detect_spines(jpeg_file, new_scan, torch_confidence):
    """
    This function detects book spines in an image and creates a new image for each spine.

    Args:
        jpeg_file (str): The path to the image file.

    Returns:    
        list: A list of paths to the cropped book spine images.
        int: The number of book spines detected.
    """
    book_boxes, bbox_path = detect_spines(jpeg_file, torch_confidence)
    if book_boxes == None:
        return None, None
    
    new_scan.bbox_image = bbox_path
    new_scan.save()

    list_of_spine_images = []

    # Create a new image for each book spine and save in 'media/detection_temp/spines/' directory. Use coords to crop OG image
    original_img = Image.open(jpeg_file)
    for i, box in enumerate(book_boxes):
        # Convert tensor to list of integers
        x1, y1, x2, y2 = map(int, box.tolist())
        book_img = original_img.crop((x1, y1, x2, y2))
        spine_path = os.path.join(MEDIA_ROOT, f"detection_temp/spines/spine_{i}.jpeg")
        book_img.save(spine_path)
        list_of_spine_images.append(spine_path)

    spine_count = len(list_of_spine_images)

    return list_of_spine_images, spine_count


def detect_spines(jpeg_file, torch_confidence):
    """
    This function detects book spines in an image and draws bounding boxes around them.

    Args:
        jpeg_file (str): The path to the image file.

    Returns:
        list: A list of bounding boxes for the detected book spines.
        str: The path to the image with bounding boxes.
    """
    input_img = jpeg_file
    img_tensor = load_image(jpeg_file)
    prediction = predict(model, img_tensor)
    img = Image.open(input_img)
    valid_books, bbox_path = draw_boxes(img, prediction, torch_confidence)

    # If no books are detected, rotate the image 90 degrees and try again. For cases where image is sideways (ios issue)
    if valid_books == None:
        img = Image.open(input_img)
        img = img.rotate(90)

        # Save rotated image to media/detection_temp/spines
        if os.path.exists("media/detection_temp/spines/rotated_image.jpeg"):
            os.remove("media/detection_temp/spines/rotated_image.jpeg")
        rotated_image_path = os.path.join(MEDIA_ROOT, "detection_temp/spines/rotated_image.jpeg")
        img.save(rotated_image_path)
        util.log_print("\nRotated image saved as 'media/detection_temp/spines/rotated_image.jpeg'\n")

        img_tensor = load_image(rotated_image_path)
        prediction = predict(model, img_tensor)
        valid_books, bbox_path = draw_boxes(img, prediction, torch_confidence)
  
    if valid_books == None:
        return None, None

    return valid_books, bbox_path


def draw_boxes(img, prediction, torch_confidence):
    """
    This function draws bounding boxes around detected objects in an image. It also validates the detected books using 
    average book height and thickness.

    Args:
        img (PIL.Image): The image to draw bounding boxes on.
        prediction (dict): The prediction results from the model.

    Returns:
        list: A list of bounding boxes for the detected book spines.
    """
    # Set up matplotlib figure. 'Agg' (Anti-Grain Geometry) is the canonical renderer for user interfaces in Matplotlib.
    matplotlib.use('Agg')
    util.log_print("\nDrawing bounding boxes...\n")

    # Create a figure for the bbox image. Figsize is the size of the figure in inches.
    plt.figure(figsize=(12, 8))
    # Does not actually display the img, just loads it into the figure. Should be called imdraw() instead.
    plt.imshow(img)
    # Get the current Axes instance on the figure. gca stands for 'get current axis'.
    ax = plt.gca()

    util.log_print("\nProcessing detected objects...\n")

    # Initialize vars to store total book height and thickness for use in validation (avg book height and thickness)
    total_book_height = 0
    total_book_thickness = 0

    # Filter books and calculate total height and thickness
    books = []
    for element, label, score in zip(prediction[0]['boxes'], prediction[0]['labels'], prediction[0]['scores']):
        if score > torch_confidence and label == 84:  # Label 84 is 'book' in COCO
            box = element.detach().cpu().numpy()
            books.append(box)
            total_book_height += box[3] - box[1]
            total_book_thickness += box[2] - box[0]

    # If no books are detected, return None
    if not books:
        util.log_print("\nNo books detected. Exiting...\n")
        return None, None

    # Calculate average book height and thickness
    book_count = len(books)
    average_book_height = total_book_height / book_count
    average_book_thickness = total_book_thickness / book_count

    util.log_print(f"\n\nPreliminary statistics:\n")
    util.log_print(f"Average book height: {round(float(average_book_height), 2)} pixels\nAverage book thickness: {round(float(average_book_thickness), 2)} pixels\n")

    valid_books = []
    util.log_print("\nValidating detected books and drawing bounding boxes...\n")

    # Validate books and draw bounding boxes
    for box in books:
        height = box[3] - box[1]
        thickness = box[2] - box[0]
        if (average_book_height * 0.7 <= height <= average_book_height * 1.4 and
                average_book_thickness * 0.2 <= thickness <= average_book_thickness * 1.8):
            valid_books.append(box)
            rect = patches.Rectangle((box[0], box[1]), thickness, height, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

    # If no valid books are detected, return None
    if not valid_books:
        util.log_print("\nNo valid books detected. Exiting...\n")
        return None, None

    bbox_image_path = os.path.join(MEDIA_ROOT, "detection_temp/spines/full_detected.jpeg")
    plt.savefig(bbox_image_path)
    bbox_image_url = os.path.join(MEDIA_URL, "detection_temp/spines/full_detected.jpeg")

    util.log_print(f"Number of verified books: {len(valid_books)}\n")
    util.log_print("Image with bounding boxes saved as 'media/detection_temp/spines/full_detected.jpeg'\n")

    return valid_books, bbox_image_url




# HELPER FUNCTIONS

def load_image(input_path):
    """
    This function loads an image, enhances it, and applies a tensor transformation.

    Args:
        input_path (str): The path to the image file.

    Returns:
        torch.Tensor: The transformed image tensor.
    """
    # Use PIL to load the image 
    util.log_print("\nLoading image...\n")
    img = Image.open(input_path).convert("RGB")
    
    # Basic image enhancement - autocontrast, brightness adjustment, edge enhancement
    util.log_print("\nEnhancing image...\n")
    img = ImageOps.autocontrast(img)
    brightness = calculate_brightness(cv.imread(input_path))
    img = adjust_brightness(img, brightness)
    img = img.filter(ImageFilter.EDGE_ENHANCE)

    # Save enhanced image to media/detection_temp/spines
    if os.path.exists("media/detection_temp/spines/enhanced_image.jpeg"):
        os.remove("media/detection_temp/spines/enhanced_image.jpeg")
    enhanced_image_path = os.path.join(MEDIA_ROOT, "detection_temp/spines/enhanced_image.jpeg")
    img.save(enhanced_image_path)
    util.log_print("\nEnhanced image saved as 'media/detection_temp/spines/enhanced_image.jpeg'\n")

    util.log_print("\nApplying tensor transformation...\n")
    # Apply tensor transformation, which converts the image to a tensor and normalizes it
    img_tensor = transform(img)

    return img_tensor


def predict(model, img_tensor):
    """
    This function performs prediction on an image using a pre-trained model.
    
    Args:
        model: The pre-trained model.
        img_tensor (torch.Tensor): The transformed image tensor.
        
    Returns:
        dict: The prediction results from the model.
    """
    util.log_print("\nPerforming prediction...\n")
    # no_grad() disables gradient calculation, which is useful for inference. 
    # This means that the model will not be able to backpropagate/learn from the image.
    # The reason for this is that we are not training the model, only using it to make predictions.
    with torch.no_grad():
        prediction = model([img_tensor])

    return prediction



def calculate_brightness(image):
    """
    This function calculates the average brightness of an image.
    
    Args:
        image (numpy.ndarray): The image to calculate the brightness of.
        
    Returns:
        float: The average brightness of the image (0-255).
    """
    grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    brightness = cv.mean(grayscale_image)

    return brightness[0]


def adjust_brightness(image, brightness):
    """
    This function adjusts the brightness of an image based on the average brightness value. Target brightness ~120.

    Args:
        image (PIL.Image): The image to adjust the brightness of.
        brightness (float): The average brightness of the image (0-255).

    Returns:
        PIL.Image: The adjusted image.
    """
    enhancer = ImageEnhance.Brightness(image)
    factor = 120 / brightness
    image = enhancer.enhance(factor)

    return image