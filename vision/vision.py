import torch
from torchvision import models, transforms
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load a pre-trained Faster R-CNN model
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Define the image transformation
transform = transforms.Compose([
    transforms.ToTensor(),
])

def load_image(input_path):
    img = Image.open(input_path).convert("RGB")
    

    # Enhance the image
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)

    # Enhance edges
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
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
        if score > 0.7 and label == 84:  # Label 84 is 'book' in COCO
            total_book_height += element[3] - element[1]
            total_book_thickness += element[2] - element[0]
            book_count += 1

    average_book_height = total_book_height / book_count
    average_book_thickness = total_book_thickness / book_count

    book_count = 0

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
                rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
                                     linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)

    print(f"Number of books detected: {book_count}")
    plt.show()

def detect_spines(jpeg_file):
    input_img = jpeg_file
    
    # Load and transform the image
    img_tensor = load_image(input_img)
    
    # Perform prediction
    prediction = predict(model, img_tensor)
    
    # Load the original image to draw on
    img = Image.open(input_img)

    
    # Draw bounding boxes on the image and display it
    draw_boxes(img, prediction)

    # Return the coordinates of the bounding boxes
    print(prediction[0]['boxes'])


def main():
    detect_spines("vision/test_images/test_full.jpeg")




if __name__ == "__main__":
    main()
