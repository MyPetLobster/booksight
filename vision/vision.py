import time

from classes import Spine

import analyze_spine as asp
import detect_spines as ds
import detect_text as dt
import utility as util

import matcher



def vision():

    # Empty temp image directories
    util.empty_directory("vision/debug_images")
    util.empty_directory("vision/spines")

    # Get image file path from user
    jpeg_file = input("\nEnter the path to the image file: ")
    if jpeg_file == "":
        jpeg_file = "vision/test_images/test_five.jpeg"
        print(f"\nUsing default image: {jpeg_file}\n")

    # Start timer
    start = time.time()

    # Detect book spines and create individual spine jpegs
    print("\nDetecting book spines in the image...\n")
    spine_images, spine_count = ds.crop_spines(jpeg_file)
    print("\nBook spines detected. Images saved in 'vision/spines' directory.\n")
    spines_detected = len(spine_images)
    print(f"Number of book spines detected: {spines_detected}\n")

    spine_detection_end = time.time()
    print(f"Spine detection complete. Time taken: {round(spine_detection_end - start, 2)} seconds\n")


    # Create Spine objects - Detect text, colors, and dimensions
    if spine_count == 0:
        print("\nNo books detected. Exiting program.\n")
        return
    elif 0 < spine_count < 20:
        print("\nCreating Spine objects. This may take several minutes...\n")
    else:
        print("\nCreating Spine objects. This image contains a lot of books. Go stretch your legs. This may take a while...\n")

    spines = []

    i = 0
    for image in spine_images:
        avg_color, dominant_color, color_palette, height, width = asp.analyze_spine(image)
        text = dt.detect_text(image)
        spine = Spine(image, avg_color, dominant_color, color_palette, height, width, text)
        spines.append(spine)
        print(f"\nBook_{i}:\n{spine}")
        i += 1

    spine_object_end = time.time()
    print(f"\nSpine objects created. Time taken: {round(spine_object_end - spine_detection_end, 2)} seconds\n")


    # Get all scanned text from each Spine
    all_spine_text = []
    for spine in spines:
        all_spine_text += spine.text 

    print("\n************************************************")
    print(f"\nAll text detected from all spines:\n\n{all_spine_text}\n")
    print("************************************************\n\n")

    print("\nScanning full image for additional text...\n")
    print("\nLarge images may take a while to process.\n")

    full_scan_start = time.time()
    # Scan original image for text, apart from individual spines
    full_image_text = dt.detect_text(jpeg_file)
    full_image_text = [text for text in full_image_text if len(text) > 2]
    
    full_image_text_unique = [text for text in full_image_text if text not in all_spine_text] 

    full_scan_end = time.time()
    print(f"\nFull image scanned. Time taken: {round(full_scan_end - full_scan_start, 2)} seconds\n\n")

    print("\n************************************************")
    print(f"\nAll additional unique text detected from full image:\n\n{full_image_text_unique}\n")
    print("************************************************\n\n")
    
    

    print("\nAll processes complete.\n")
    end = time.time()
    print(f"\nTotal time taken: {round(end - start, 2)} seconds\n")


    # Match books

    print("\nBegin book identification process...\n")
    matcher.match_books(spines, full_image_text_unique)



if __name__ == "__main__":
    vision()
