import time

from classes import Spine

import analyze_spine as asp
import detect_spines as ds
import detect_text as dt
import utility as util




def vision():
    util.empty_directory("vision/debug_images")
    util.empty_directory("vision/spines")

    jpeg_file = input("\nEnter the path to the image file: ")
    if jpeg_file == "":
        jpeg_file = "vision/test_images/small-shelf.jpeg"
        print(f"\nUsing default image: {jpeg_file}\n")

    start = time.time()

    print("\nDetecting book spines in the image...\n")

    spine_images, spine_count = ds.crop_spines(jpeg_file)

    print("\nBook spines detected and saved in 'vision/spines' directory.\n")
    print(f"Number of book spines detected: {len(spine_images)}\n")

    spine_detection_end = time.time()

    print(f"Spine detection complete. Time taken: {round(spine_detection_end - start, 2)} seconds\n")

    if spine_count == 0:
        print("\nNo books detected. Exiting program.\n")
        return
    elif 0 < spine_count < 20:
        print("\nCreating Spine objects. This may take several minutes...\n")
    else:
        print("\nCreating Spine objects. This image contains a lot of books. Go stretch your legs. This may take a while...\n")

    spines = []

    i = 0
    for spine_image in spine_images:
        avg_color, dominant_color, color_palette, height, width = asp.analyze_spine(spine_image)
        text = dt.detect_text(spine_image)
        spine = Spine(spine_image, avg_color, dominant_color, color_palette, height, width, text)
        spines.append(spine)

        print(f"\nBook_{i}:\n{spine}\n")
        i += 1

    spine_object_end = time.time()

    print(f"\nSpine objects created. Time taken: {round(spine_object_end - spine_detection_end, 2)} seconds\n")


    # Get all text scanned from spines
    all_spine_text = []
    for spine in spines:
        all_spine_text += spine.text
    
    # Scan original image for text
    full_image_text = dt.detect_text(jpeg_file)
    full_image_text = [text for text in full_image_text if len(text) > 2]
    
    full_image_text_unique = [text for text in full_image_text if text not in all_spine_text] 

    print("\n************************************************")
    print(f"\nAll additional unique text detected from full image:\n\n{full_image_text_unique}\n")
    print("************************************************\n\n")
    

    print("\nAll processes complete.\n")
    end = time.time()

    print(f"\nTotal time taken: {round(end - start, 2)} seconds\n")




if __name__ == "__main__":
    vision()
