import os
import time

from . import analyze_spine as asp
from . import config
from . import detect_spines as ds
from . import detect_text as dt
from . import exporter as export
from . import matcher as match
from . import utility as util
from .classes import Spine, Book
from dashboard.models import Scan

from booksight.settings import MEDIA_URL


def vision(image_path, new_scan):
    """
    This function is the main function for the Booksight Vision process. It runs the entire process of detecting book spines, 
    analyzing the spines, detecting text, cleaning up text data, identifying books, and exporting the results. The function 
    is called by the dashboard/views.py file and runs in a separate thread.
    """
    # Delete all scans except most recent - no persistent db storage, one scan at a time.
    Scan.objects.exclude(id=new_scan.id).delete()

    # Set status to running - used for ajax polling
    new_scan.scan_status = "running"
    new_scan.save()

    util.log_print("Welcome to Booksight!\n\nBeginning the Vision process.")

    # Load configuration data from config.py
    config_data = config.get_config()
    email_address = config_data.email
    output_formats = config_data.formats
    torch_confidence = config_data.torch_confidence
    
    util.log_print("\n\n\n**************** PHASE ONE - BOOK SPINE IDENTIFICATION *****************\n\n\n")

    start = time.time()

    ### BOOK OBJECT DETECTION ###
    util.log_print("Beginning book spine detection in the uploaded image...\n")
    util.log_print(f"Image path: {image_path}\n")
    util.log_print("Cropping book spines (see media/detection_temp/spines/ dir)...\n")

    # Detect book spines and create individual spine jpegs and bounding box image
    spine_images, spine_count = ds.crop_detect_spines(image_path, new_scan, torch_confidence)
    util.log_print(f"Spine images saved in 'media/detection_temp/spines/'\n")

    if spine_images == None or spine_count == None:
        util.log_print("\nNo valid books detected. Exiting program.\n")
        new_scan.scan_status = "failed"
        new_scan.save()
        return
    else:
        new_scan.scan_status = "bbox-detected"
        new_scan.save()
   
    spine_detection_end = time.time()

    util.log_print(f"Spine detection complete. Time taken: {round(spine_detection_end - start, 2)} seconds\n")


    ### SPINE ANALYSIS ###
    if spine_count < 10:
        util.log_print("\nAnalyzing images and creating Spine objects. This may take several minutes...\n\n")
    else:
        util.log_print("\nAnalyzing images and creating Spine objects. This image contains a lot of books. Go stretch your legs. This may take a while...\n")

    spines = []
    i = 0

    for image in spine_images:
        # Get the color data and dimensions of the spine
        util.log_print(f"Analyzing detected_spine_{i}. Extracting color data and dimensions.\n")
        avg_color, dominant_color, color_palette, height, width = asp.analyze_spine(image)
        util.log_print(f"Color and dimension data extracted from detected_spine_{i}.\n")

        # Detect text on the spine using EasyOCR
        util.log_print(f"\nBeginning OCR text detection on detected_spine_{i}...\n")
        text = dt.detect_text(image)

        # Create a Spine object
        spine = Spine(image, avg_color, dominant_color, color_palette, height, width, text)
        spines.append(spine)

        util.log_print(f"Detected_spine_{i} analyzed and Spine object created.\n")
        util.log_print(f"Spine_{i} Details: {spine}\n")

        i += 1

    spine_object_end = time.time()
    spine_object_count = len(spines)

    util.log_print(f"\n{spine_object_count} 'Spine' objects created.\nTime taken: {round(spine_object_end - spine_detection_end, 2)} seconds\n")

    # Retrieve all extracted text from each Spine object
    all_spine_text = []
    for spine in spines:
        all_spine_text += spine.text 

    util.log_print(f"All text detected from all spines:\n\n{all_spine_text}\n")

    # Full image OCR scan for additional text on spines that went undetected by torchvision
    util.log_print("\nScanning full image for additional text.\nLarge images may take a while to process...\n")
    full_scan_start = time.time()
    full_image_text = dt.detect_text(image_path)
    full_scan_end = time.time()
    util.log_print(f"Full image scan complete.\nTime taken: {round(full_scan_end - full_scan_start, 2)} seconds\n")

    # Retrieve all debug images from detection_temp/debug_images saved in detect_text.py
    all_debug_images = []
    debug_images = os.listdir("media/detection_temp/debug_images")
    for image in debug_images:
        all_debug_image_paths = os.path.join(MEDIA_URL, f"detection_temp/debug_images/{image}")
        all_debug_images.append(all_debug_image_paths)

    # Convert list of image paths to a string
    all_debug_images = ",".join(all_debug_images)

    # Save all debug images (text detection images) to the Scan object and pass to frontend for display
    new_scan.scan_status = "text-detected"
    new_scan.text_images = all_debug_images
    new_scan.save()

    # Remove any text with less than 2 characters from full image text and any text that is a duplicate of spine text
    full_image_text = [text for text in full_image_text if len(text) > 2]
    full_image_text = [text for text in full_image_text if text not in all_spine_text] 
    util.log_print(f"\nAll additional unique text detected from full image:\n\n{full_image_text}\n")

    ocr_end = time.time()
    util.log_print("\nAll image processing and OCR operations complete.\n")
    util.log_print(f"Total time taken for image processing and OCR: {round(ocr_end - start, 2)} seconds\n")


    ### BOOK IDENTIFICATION ###
    util.log_print("\n\n************** PHASE TWO - BOOK IDENTIFICATION & MATCHING **************\n\n")
    util.log_print("\nBegin precise book identification process...\n")
    
    # Clean up text data using AI and retrieve potential ISBNs for each spine
    util.log_print("Cleaning up text data and making preliminary title/author identification with AI model...\n")
    spines = match.id_possible_matches(spines, full_image_text)
    util.log_print("Text data cleanup and preliminary identification complete.\n")
    ai_end = time.time()
    util.log_print(f"Total time taken for AI processing and ISBN retrieval: {round(ai_end - ocr_end, 2)} seconds\n")

    new_scan.scan_status = "ai-complete"
    new_scan.save()

    util.log_print("\nAll updated Spine objects:\n")
    for spine in spines:
        util.log_print(spine)
        util.log_print("\n")


    ### BOOK MATCHING ###
    util.log_print("\nBegin precise book identification process.\nThis may take a while...\n")
    books = match_spines_to_books(spines)
    match_end = time.time()
    util.log_print(f"\nBook identification process complete.\n\nTotal time taken for book identification: {round(match_end - ai_end, 2)} seconds\n")

    util.log_print("\nAll identified books:\n")
    for book in books:
        util.log_print(f"{book}\n")

    util.log_print("\n\n**************************** VISION COMPLETE ***************************\n\n")
    
    # Calculate statistics and log to file
    total_books = len(books)
    total_confident_books = len([book for book in books if book.confidence > 0])
    end_time = time.time()
    total_time = end_time - start
    time_per_book = total_time / total_books

    util.log_print(f"Total books identified: {total_books}")
    util.log_print(f"Total books with precise identification: {total_confident_books}")
    util.log_print(f"Time taken per book: {round(time_per_book, 2)} seconds")
    util.log_print(f"Total time taken to complete Booksight Vision process: {round(time.time() - start, 2)} seconds\n")


    util.log_print("\n\n**************** PHASE THREE - EXPORTING RESULTS *****************\n\n")

    # Export the results to a text file and email to user
    log_file_path = util.retrieve_last_log_file()
    sent = export.export_books(books, output_formats, email_address, log_file_path)

    if sent:
        new_scan.scan_status = "completed"
        new_scan.save()
        util.log_print("\nExport complete. Results sent to user.\n")
    else:
        new_scan.scan_status = "failed"
        new_scan.save()
        util.log_print("\nExport failed. Results not sent to user.\n")

    util.log_print("\nAll processes complete. Thank you for using Booksight.\n\n")

    
    return


def match_spines_to_books(spines):
    """
    This function matches Spine objects to Book objects by comparing the dimensions and color data from the detected spines to the
    data retrieved from Open Library and Google Books APIs. The function returns a list of Book objects.

    Args:
        spines (list): A list of Spine objects.

    Returns:
        list: A list of Book objects.
    """
    start_spine_match = time.time()
    total_spines = len(spines)
    total_potential_isbns = 0

    books = []

    # Initialize constants/multipliers for spine matching
    color_filter = (1, 1, 1)
    px_to_inches = 1

    def confidence_check(confidence, spine, isbn, threshold):
        """
        This inner function checks the confidence of the identification of a spine. 

        - A confidence of 34 indicates that the spine was not detected by torchvision and was identified with the AI model 
        during OCR cleanup. In this case, because there is no color or dimension data, a Book object is created with only 
        the book's generic information. Confidence 34 will break the loop and skip to the next spine.

        - If confidence is greater than the threshold, the ISBN is added to a dictionary of potential matches.

        Args:
            confidence (int): The confidence of the identification.
            spine (Spine): The Spine object.
            isbn (str): The ISBN of the potential match.
            threshold (float): The threshold for confidence.

        Returns:
            bool: True if a Book object was created, False if not.
        """
        if confidence == 34:
            util.log_print(f"\nSorry, we were unable to identify the specific edition of {spine.title}.\n The spine was undetected by torchvision and identified with AI model during OCR cleanup.\n")
            util.log_print("No dimensions or color to match. General information only for this book.\n")
            book = match.create_book_object(isbn, 0)
            books.append(book)
            util.log_print(f"Book object for {spine.title}: {book}\n")
            return True
        elif confidence > threshold:
            potential_matches[isbn] = confidence
            util.log_print(f"\n{spine.title} identified with ISBN: {isbn}")
            util.log_print(f"Identification confidence: {confidence}\n")
        return False
    

    # Iterate through each spine and check for matches
    for spine in spines:
        book_created = False  
        second_pass = False
        possible_isbns = spine.possible_matches
        potential_matches = {}

        # Global tracking of isbn count for logging purposes outside of loop
        total_potential_isbns += len(possible_isbns)

        # NOTE - book_created will only be True for confidence 34 books (ie books undetected by torchvision but identified 
        # with full image text AI analysis). The rest of the books will be added to potential_matches and a Book object 
        # will be created after the loop has checked all possible ISBNs and compared confidence levels.

        # Check each possible ISBN for a match
        for isbn in possible_isbns:
            confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass)
            book_created = confidence_check(confidence, spine, isbn, 0.2)
            if book_created:
                break

        if book_created:
            # Skip to the next spine if a book has been created
            continue
        
        # If no potential matches were found in the first pass, run a second pass with a lower threshold.
        if len(potential_matches) == 0:
            second_pass = True
            for isbn in possible_isbns:
                confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass)
                book_created = confidence_check(confidence, spine, isbn, 0.0)
                if book_created:
                    break

        if book_created:
            continue

        if len(potential_matches) == 0 and second_pass:
            # This is for the scenario where a spine WAS detected, but no matches were found in either pass
            util.log_print(f"\nWe're sorry! '{spine.title}' could not be identified. Book object created using only detected title and authors.\n")
            book = Book()
            book.title = spine.title
            book.authors = spine.author
            book.confidence = 0
            books.append(book)
            util.log_print(f"\nBook object for {spine.title}: {book}\n")
        else:
            # If potential matches were found, create a Book object with the best match
            best_match = max(potential_matches, key=potential_matches.get)
            util.log_print(f"\n{spine.title} identified with ISBN: {best_match}\n")
            util.log_print(f"Identification confidence: {potential_matches[best_match]}\n")
            book = match.create_book_object(best_match, potential_matches[best_match])
            books.append(book)
            util.log_print(f"\nBook object for {spine.title}: {book}\n")

    end_spine_match = time.time()
    util.log_print(f"Spine matching complete. Time taken: {round(end_spine_match - start_spine_match, 2)} seconds")
    util.log_print(f"Total spines checked: {total_spines}")
    util.log_print(f"Time taken per spine: {round((end_spine_match - start_spine_match) / total_spines, 2)} seconds")
    util.log_print(f"Total potential ISBNs checked: {total_potential_isbns}")
    util.log_print(f"Time taken per potential ISBN: {round((end_spine_match - start_spine_match) / total_potential_isbns, 2)} seconds\n")

    return books