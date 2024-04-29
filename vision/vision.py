import time

from classes import Spine

import detect_spines as ds
import detect_text as dt
import analyze_spine as asp



def vision():
    jpeg_file = input("\nEnter the path to the image file: ")

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

    # # Scan entire image for text
    # spine_text_as_string = ""
    # for spine in spines:
    #     spine_text_as_string += spine.text + " "

    

    print("\nAll processes complete.\n")
    end = time.time()

    print(f"\nTotal time taken: {round(end - start, 2)} seconds\n")




if __name__ == "__main__":
    vision()
