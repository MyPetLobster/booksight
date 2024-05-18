import os

import cv2 as cv
import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import torch
from torchvision import models, transforms
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from vision.utility import log_print


# Load a pre-trained Faster R-CNN model
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Confidence threshold for detected objects
CONFIDENCE = 0.79

# Define the image transformation
transform = transforms.Compose([
    transforms.ToTensor(),
])

book_count = 0 


def crop_spines(jpeg_file):
    """
    This function detects book spines in an image and creates a new image for each spine.

    Args:
        jpeg_file (str): The path to the image file.

    Returns:    
        list: A list of paths to the cropped book spine images.
        int: The number of book spines detected.
    """
    # Detect book spines
    log_print("\nCropping book spines (see vision/images/detection_temp/spines/ dir)...\n")
    book_boxes = detect_spines(jpeg_file)
    if book_boxes == None:
        return None, None
    list_of_spine_images = []

    # Create a new image for each book spine and save in 'vision/spines' directory
    original_img = Image.open(jpeg_file)
    for i, box in enumerate(book_boxes):
        # Convert tensor to list of integers
        x1, y1, x2, y2 = map(int, box.tolist())
        book_img = original_img.crop((x1, y1, x2, y2))
        book_img.save(f"vision/images/detection_temp/spines/book_{i}.jpeg")
        book_img_path = f"vision/images/detection_temp/spines/book_{i}.jpeg"
        list_of_spine_images.append(book_img_path)

    spine_count = len(list_of_spine_images)
    log_print(f"Spine images saved in 'vision/images/detection_temp/spines/'\n")

    return list_of_spine_images, spine_count


def detect_spines(jpeg_file):
    """
    This function detects book spines in an image and draws bounding boxes around them.

    Args:
        jpeg_file (str): The path to the image file.

    Returns:
        list: A list of bounding boxes for the detected book spines.
    """
    input_img = jpeg_file
    img_tensor = load_image(input_img)
    prediction = predict(model, img_tensor)
    img = Image.open(input_img)
    valid_books = draw_boxes(img, prediction)

    if valid_books == None:
        return None

    return valid_books


def load_image(input_path):
    """
    This function loads an image, enhances it, and applies a tensor transformation.

    Args:
        input_path (str): The path to the image file.

    Returns:
        torch.Tensor: The transformed image tensor.
    """
    log_print("\nLoading image...\n")
    img = Image.open(input_path).convert("RGB")
    
    log_print("\nEnhancing image...\n")
    
    # Enhance the image
    img = ImageOps.autocontrast(img)
    brightness = calculate_brightness(cv.imread(input_path))
    img = adjust_brightness(img, brightness)
    img = img.filter(ImageFilter.EDGE_ENHANCE)

    # Save enhanced image
    if os.path.exists("vision/images/detection_temp/spines/enhanced_image.jpeg"):
        os.remove("vision/images/detection_temp/spines/enhanced_image.jpeg")
    img.save("vision/images/detection_temp/spines/enhanced_image.jpeg")

    log_print("\nEnhanced image saved as 'vision/images/detection_temp/spines/enhanced_image.jpeg'\n")
    log_print("\nApplying tensor transformation...\n")

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
    log_print("\nPerforming prediction...\n")
    with torch.no_grad():
        prediction = model([img_tensor])
    return prediction


def draw_boxes(img, prediction):
    """
    This function draws bounding boxes around detected objects in an image. It also validates the detected books using 
    average book height and thickness.

    Args:
        img (PIL.Image): The image to draw bounding boxes on.
        prediction (dict): The prediction results from the model.

    Returns:
        list: A list of bounding boxes for the detected book spines.
    """
    log_print("\nDrawing bounding boxes...\n")
    matplotlib.use('Agg')
    plt.figure(figsize=(12, 8))
    plt.imshow(img)
    ax = plt.gca()
    log_print("\nProcessing detected objects...\n")
    book_count = 0
    total_book_height = 0
    total_book_thickness = 0

    # Check for each detected object, if it is a book and meets the confidence threshold
    for element, label, score in zip(prediction[0]['boxes'], prediction[0]['labels'], prediction[0]['scores']):
        if score > CONFIDENCE and label == 84:  # Label 84 is 'book' in COCO
            total_book_height += element[3] - element[1]
            total_book_thickness += element[2] - element[0]
            log_print(f"Book_{book_count} Score: {score}")
            book_count += 1

    if book_count == 0:
        log_print("\nNo books detected. Exiting...\n")
        return None
    
    average_book_height = total_book_height / book_count
    average_book_thickness = total_book_thickness / book_count

    log_print(f"\n\nPreliminary statistics:\n")
    log_print(f"Average book height: {round(float(average_book_height), 2)} pixels\nAverage book thickness: {round(float(average_book_thickness), 2)} pixels\n")

    book_count = 0
    valid_books = []

    # Remove outliers, draw bounding boxes
    log_print("\nValidating detected books and drawing bounding boxes...\n")
    for element, label, score in zip(prediction[0]['boxes'], prediction[0]['labels'], prediction[0]['scores']):
        if score > CONFIDENCE and label == 84:  # Label 84 is 'book' in COCO
            box = element.detach().cpu().numpy()
            if box[3] - box[1] > average_book_height * 1.4 or box[3] - box[1] < average_book_height * 0.7:
                continue
            elif box[2] - box[0] > average_book_thickness * 2 or box[2] - box[0] < average_book_thickness * 0.3:
                continue
            else: 
                book_count += 1
                valid_books.append(box)
                
                rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
                                     linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
    
    if book_count == 0:
        log_print("\nNo valid books detected. Exiting...\n")
        return None

    plt.savefig("vision/images/detection_temp/spines/full_detected.jpeg")

    log_print(f"Number of verified books: {book_count}\n")
    log_print("Image with bounding boxes saved as 'vision/images/detection_temp/spines/full_detected.jpeg'\n")

    return valid_books


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