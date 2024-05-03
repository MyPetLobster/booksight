import os
import shutil

import cv2 as cv
import easyocr as ocr
import torch
from torchvision import models, transforms
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import utility as util


CONFIDENCE = 0.83


# Load a pre-trained Faster R-CNN model
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Define the image transformation
transform = transforms.Compose([
    transforms.ToTensor(),
])

book_count = 0 

def calculate_brightness(image):
    # Convert the image to grayscale
    grayscale_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # Calculate the average brightness of the image
    brightness = cv.mean(grayscale_image)

    # Return average brightness, range 0-255
    return brightness[0]


def adjust_brightness(image, brightness):
    # Adjust the brightness of the image
    if 80 < brightness < 100:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
    elif 50 < brightness < 80:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.4)
    elif brightness < 50:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.6)
    elif 140 < brightness < 160:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.8)
    elif brightness > 160:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.6)
    
    return image


def load_image(input_path):
    util.log_print("\nLoading image...\n")
    img = Image.open(input_path).convert("RGB")
    
    util.log_print("\nEnhancing image...\n")
    
    # Enhance the image
    img = ImageOps.autocontrast(img)

    brightness = calculate_brightness(cv.imread(input_path))
    img = adjust_brightness(img, brightness)
    
    img = img.filter(ImageFilter.EDGE_ENHANCE)

    # img.show("Enhanced Image")

    if os.path.exists("vision/images/detection_temp/spines/enhanced_image.jpeg"):
        os.remove("vision/images/detection_temp/spines/enhanced_image.jpeg")
    img.save("vision/images/detection_temp/spines/enhanced_image.jpeg")
    util.log_print("\nEnhanced image saved as 'vision/images/detection_temp/spines/enhanced_image.jpeg'\n")

    util.log_print("\nApplying tensor transformation...\n")

    img_tensor = transform(img)

    return img_tensor


def predict(model, img_tensor):
    util.log_print("\nPerforming prediction...\n")
    with torch.no_grad():
        prediction = model([img_tensor])
    return prediction


def draw_boxes(img, prediction):
    util.log_print("\nDrawing bounding boxes...\n")
    plt.figure(figsize=(12, 8))
    plt.imshow(img)
    ax = plt.gca()

    util.log_print("\nProcessing detected objects...\n")
    book_count = 0
    total_book_height = 0
    total_book_thickness = 0

    # Check for each detected object, determine average book height
    for element, label, score in zip(prediction[0]['boxes'], prediction[0]['labels'], prediction[0]['scores']):
        if score > CONFIDENCE and label == 84:  # Label 84 is 'book' in COCO
            total_book_height += element[3] - element[1]
            total_book_thickness += element[2] - element[0]
            util.log_print(f"Book_{book_count} Score: {score}")
            book_count += 1

    if book_count == 0:
        util.log_print("\nNo books detected. Exiting...\n")
        return None
    
    average_book_height = total_book_height / book_count
    average_book_thickness = total_book_thickness / book_count

    util.log_print(f"\n\nPreliminary statistics:\n")
    util.log_print(f"Average book height: {round(float(average_book_height), 2)} pixels\nAverage book thickness: {round(float(average_book_thickness), 2)} pixels\n")

    book_count = 0
    valid_books = []

    # Remove outliers, draw bounding boxes
    util.log_print("\nValidating detected books and drawing bounding boxes...\n")
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
        util.log_print("\nNo valid books detected. Exiting...\n")
        return None

    util.log_print(f"Number of verified books: {book_count}\n")
    util.log_print("Image with bounding boxes saved as 'vision/images/detection_temp/spines/full_detected.jpeg'\n")
    # plt.show()
    
    # delete old full_detected.jpeg
    if os.path.exists("vision/images/detection_temp/spines/full_detected.jpeg"):
        os.remove("vision/images/detection_temp/spines/full_detected.jpeg")

    plt.savefig("vision/images/detection_temp/spines/full_detected.jpeg")

    return valid_books


def detect_spines(jpeg_file):
    input_img = jpeg_file
    
    # Load and transform the image
    img_tensor = load_image(input_img)
    
    # Perform prediction
    prediction = predict(model, img_tensor)
    
    # Load the original image to draw on
    img = Image.open(input_img)

    # Draw bounding boxes on the image and display it
    valid_books = draw_boxes(img, prediction)

    if valid_books == None:
        return None

    return valid_books


def crop_spines(jpeg_file):
    util.log_print("\nCropping book spines (see vision/images/detection_temp/spines/ dir)...\n")

    # Detect book spines in the image
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

    return list_of_spine_images, spine_count