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
    img = enhancer.enhance(1.2)  

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)  

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)  

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.8)  

    img = img.filter(ImageFilter.MedianFilter(size=3))  
    img = ImageOps.equalize(img, mask=None)
    img = ImageOps.autocontrast(img, cutoff=0, ignore=None)

    # Enhance edges
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

    # Check for each detected object
    for element, label, score in zip(prediction[0]['boxes'], prediction[0]['labels'], prediction[0]['scores']):
        if score > 0.8 and label == 84:  # Label 84 is 'book' in COCO
            box = element.detach().cpu().numpy()
            rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
                                     linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
    plt.show()

def main():
    input_img = "vision/test_images/test_full.jpeg"
    
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


if __name__ == "__main__":
    main()
