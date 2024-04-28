import os
import shutil

import cv2 as cv
import easyocr as ocr
import torch
from torchvision import models, transforms
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import detect_text as dt

# Load a pre-trained Faster R-CNN model
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Define the image transformation
transform = transforms.Compose([
    transforms.ToTensor(),
])


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
    img = Image.open(input_path).convert("RGB")
    
    # Enhance the image
    img = ImageOps.autocontrast(img)

    brightness = calculate_brightness(cv.imread(input_path))
    img = adjust_brightness(img, brightness)
    
    img = img.filter(ImageFilter.EDGE_ENHANCE)

    img.show()

    img_tensor = transform(img)

    return img_tensor


def predict(model, img_tensor):
    with torch.no_grad():
        prediction = model([img_tensor])
    return prediction


def draw_boxes(img, prediction):
    plt.figure(figsize=(12, 8))
    plt.imshow(img)
    ax = plt.gca()

    book_count = 0
    total_book_height = 0
    total_book_thickness = 0

    # Check for each detected object, determine average book height
    for element, label, score in zip(prediction[0]['boxes'], prediction[0]['labels'], prediction[0]['scores']):
        if score > 0.8 and label == 84:  # Label 84 is 'book' in COCO
            total_book_height += element[3] - element[1]
            total_book_thickness += element[2] - element[0]
            book_count += 1

    average_book_height = total_book_height / book_count
    average_book_thickness = total_book_thickness / book_count

    print(f"Average book height: {average_book_height}")
    print(f"Average book thickness: {average_book_thickness}")

    book_count = 0
    valid_books = []

    # Remove outliers, draw bounding boxes
    for element, label, score in zip(prediction[0]['boxes'], prediction[0]['labels'], prediction[0]['scores']):
        if score > 0.7 and label == 84:  # Label 84 is 'book' in COCO
            box = element.detach().cpu().numpy()
            if box[3] - box[1] > average_book_height * 1.4 or box[3] - box[1] < average_book_height * 0.7:
                continue
            elif box[2] - box[0] > average_book_thickness * 2.5 or box[2] - box[0] < average_book_thickness * 0.3:
                continue
            else: 
                book_count += 1
                valid_books.append(box)
                
                rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
                                     linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)

    print(f"Number of books detected: {book_count}")
    plt.show()
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

    return valid_books


def crop_spines(jpeg_file):
    # Empty the 'vision/spines' directory
    empty_directory("vision/spines")

    # Detect book spines in the image
    book_boxes = detect_spines(jpeg_file)
    list_of_spine_images = []

    # Create a new image for each book spine and save in 'vision/spines' directory
    original_img = Image.open(jpeg_file)
    for i, box in enumerate(book_boxes):
        # Convert tensor to list of integers
        x1, y1, x2, y2 = map(int, box.tolist())
        book_img = original_img.crop((x1, y1, x2, y2))
        book_img.save(f"vision/spines/book_{i}.jpeg")
        book_img_path = f"vision/spines/book_{i}.jpeg"
        list_of_spine_images.append(book_img_path)

    print(list_of_spine_images)
    return list_of_spine_images


def main():
    jpeg_file = "vision/test_images/short-shelf.jpeg"
    spine_images = crop_spines(jpeg_file)

    print("\nText detected on book spines:\n")
    i = 0
    for spine_image in spine_images:
        text = dt.detect_text(spine_image)
        print(f"Book_{i} - {text} \n")
        i += 1


# delete all files in a directory, but keep the directory
def empty_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")





if __name__ == "__main__":
    main()
