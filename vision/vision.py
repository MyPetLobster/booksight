import os
import time

from django.contrib.sessions.models import Session


from . import analyze_spine as asp
from . import detect_spines as ds
from . import detect_text as dt
from . import exporter as export
from . import matcher as match
from . import utility as util
from .utility import log_print 
from .classes import Spine, Book
from dashboard.models import Scan

from booksight.settings import MEDIA_URL


def vision(request, image_path, new_scan):
    # Delete all scans except most recent
    Scan.objects.exclude(id=new_scan.id).delete()

    new_scan.scan_status = "running"
    new_scan.save()

    log_print("\n\n************************************************\n")
    log_print("\nWelcome to Booksight!\n")
    log_print("\nBeginning the Vision process.\n")

    email_address = request.session.get('email')
    output_formats = request.session.get('formats')
    ai_model = request.session.get('ai_model')
    ai_temp = request.session.get('ai_temp')
    torch_confidence = request.session.get('torch_confidence')

    log_print("\nAI and Computer Vision Settings:\n")
    if ai_model.startswith("gpt"):
        log_print(f"    - AI Model: {ai_model}\n")
        log_print(f"    - AI Temp: {ai_temp}\n")
    elif ai_model.startswith("gemini"):
        log_print(f"    - AI Model: {ai_model}\n")
    log_print(f"    - Torchvision Confidence Threshold: {torch_confidence}\n")
    
    
    start = time.time()

    log_print("\n\n**************** PHASE ONE - BOOK SPINE IDENTIFICATION *****************\n\n")

    ### Book Object Detection ###
    # Detect book spines and create individual spine jpegs
    log_print("Beginning book spine detection in the uploaded image...\n")
    log_print(f"Image path: {image_path}\n")

    spine_images, spine_count = ds.crop_spines(image_path, new_scan, torch_confidence)
    if spine_images == None:
        log_print("\nNo valid books detected. Exiting program.\n")
        new_scan.scan_status = "failed"
        new_scan.save()
        return
   
    spine_detection_end = time.time()
    log_print(f"Spine detection complete. Time taken: {round(spine_detection_end - start, 2)} seconds\n")
    log_print("\n************************************************\n")
    if spine_count == 0:
        log_print("\nNo books detected. Exiting program.\n")
        return
    elif 0 < spine_count < 20:
        new_scan.scan_status = "bbox-detected"
        new_scan.save()
        log_print("\nAnalyzing images and creating Spine objects. This may take several minutes...\n\n")
    else:
        log_print("\nAnalyzing images and creating Spine objects. This image contains a lot of books. Go stretch your legs. This may take a while...\n")


    ### OCR Text Detection ###
    # Create Spine objects - Detect text, colors, and dimensions
    # TODO - Am I actually using all_text_image_paths?
    all_text_image_paths = []
    spines = []
    i = 0
    for image in spine_images:
        log_print(f"Analyzing detected_spine_{i}. Extracting color data and dimensions.\n")
        avg_color, dominant_color, color_palette, height, width = asp.analyze_spine(image)
        log_print(f"Color and dimension data extracted from detected_spine_{i}.\n")
        log_print(f"\nBeginning OCR text detection on detected_spine_{i}...\n")
        text, idv_spine_text_img_paths = dt.detect_text(image)
        all_text_image_paths = ",".join(idv_spine_text_img_paths)
        spine = Spine(image, avg_color, dominant_color, color_palette, height, width, text)
        spines.append(spine)
        log_print(f"Detected_spine_{i} analyzed and Spine object created.\n")
        log_print(f"Spine_{i} Details: {spine}\n")
        i += 1
    spine_object_end = time.time()
    spine_object_count = len(spines)
    log_print(f"\n{spine_object_count} 'Spine' objects created.\nTime taken: {round(spine_object_end - spine_detection_end, 2)} seconds\n")

    log_print("************************************************\n")
    # Get all scanned text from each Spine
    all_spine_text = []
    for spine in spines:
        all_spine_text += spine.text 

    log_print(f"All text detected from all spines:\n\n{all_spine_text}\n")

    log_print("************************************************\n")
    log_print("\nScanning full image for additional text...\n")
    log_print("\nLarge images may take a while to process.\n")

    full_scan_start = time.time()
    full_image_text, text_image_paths = dt.detect_text(image_path)
    full_scan_end = time.time()
    all_text_image_paths = ",".join(text_image_paths)

    log_print(f"Full image scan complete.\nTime taken: {round(full_scan_end - full_scan_start, 2)} seconds\n")
    log_print("************************************************\n")
    log_print(f"Debug - All text image paths: {all_text_image_paths}\n")

    # TODO - is this the same as all_text_image_paths?
    # get all images from media/detection_temp/debug_images and save paths to all_debug_images
    all_debug_images = []
    debug_images = os.listdir("media/detection_temp/debug_images")
    for image in debug_images:
        all_debug_image_paths = os.path.join(MEDIA_URL, f"detection_temp/debug_images/{image}")
        all_debug_images.append(all_debug_image_paths)

    all_debug_images = ",".join(all_debug_images)

    new_scan.scan_status = "text-detected"
    new_scan.text_images = all_debug_images
    new_scan.save()

    full_image_text = [text for text in full_image_text if len(text) > 2]
    
    full_image_text_unique = [text for text in full_image_text if text not in all_spine_text] 


    log_print(f"\nAll additional unique text detected from full image:\n\n{full_image_text_unique}\n")
    log_print("\nAll image processing and OCR operations complete.\n")
    ocr_end = time.time()
    log_print(f"Total time taken for image processing and OCR: {round(ocr_end - start, 2)} seconds\n")


    ### Book Identification ###
    log_print("\n\n************** PHASE TWO - BOOK IDENTIFICATION & MATCHING **************\n\n")

    log_print("\nBegin precise book identification process...\n")
    
    # Clean up text data using AI and retrieve potential ISBNs for each spine
    log_print("Cleaning up text data and making preliminary title/author identification with AI model...\n")
    spines = match.id_possible_matches(request, spines, full_image_text_unique)
    log_print("Text data cleanup and preliminary identification complete.\n")
    ai_end = time.time()
    log_print(f"Total time taken for AI processing and ISBN retrieval: {round(ai_end - ocr_end, 2)} seconds\n")

    new_scan.scan_status = "ai-complete"
    new_scan.save()

    log_print("\n***********************************************\n")
    log_print("\nAll updated Spine objects:\n")
    for spine in spines:
        log_print(spine)
        log_print("\n")
    log_print("\n***********************************************\n")


    ### Book Matching ###
    log_print("\nBegin precise book identification process.\nThis may take a while...\n")
    books = match_spines_to_books(spines)
    log_print("\nBook identification process complete.\n")
    match_end = time.time()
    log_print(f"Total time taken for book identification: {round(match_end - ai_end, 2)} seconds\n")

    log_print("\nAll identified books:\n")
    for book in books:
        log_print(f"{book}\n")

  
    log_print("\n\n**************************** VISION COMPLETE ***************************\n\n")
    

    total_books = len(books)
    total_confident_books = len([book for book in books if book.confidence > 0])
    end_time = time.time()
    total_time = end_time - start
    time_per_book = total_time / total_books

    log_print(f"Total books identified: {total_books}\n")
    log_print(f"Total books with precise identification: {total_confident_books}\n")
    log_print(f"Time taken per book: {round(time_per_book, 2)} seconds\n")
    log_print(f"Total time taken to complete Booksight Vision process: {round(time.time() - start, 2)} seconds\n\n")


    # Export identified books to CSV and JSON
    log_print("Exporting identified books to CSV, JSON, XML, and TXT\n")

    csv_file = export.export_to_csv(books)
    json_file = export.export_to_json(books)
    xml_file = export.export_to_xml(books)
    txt_file = export.export_to_text(books)
    


    if email_address:
        
        if output_formats == None:
            output_files = [csv_file, json_file, xml_file, txt_file]
        else:
            output_files = []
            if "csv" in output_formats:
                output_files.append(csv_file)
            if "json" in output_formats:
                output_files.append(json_file)
            if "xml" in output_formats:
                output_files.append(xml_file)
            if "txt" in output_formats:
                output_files.append(txt_file)

        log_print("\nOutput files selected for email:\n")
        for file in output_files:
            log_print(file)
            log_print("\n")
        log_print("\nSending email with exports...\n")

        log_file_path = util.retrieve_last_log_file()
        
        export.email_file(output_files, email_address, log_file_path)



    new_scan.scan_status = "completed"
    new_scan.save()

    log_print("\n\nAll processes complete. Thank you for using Booksight.\n")
    
    return



def match_spines_to_books(spines):
    """
    This function matches Spine objects to Book objects by comparing the text detected on the spines to potential ISBNs
    retrieved from Open Library and Google Books APIs. The function returns a list of Book objects.

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

    for spine in spines:
        second_pass = False
        possible_isbns = spine.possible_matches
        total_potential_isbns += len(possible_isbns)
        potential_matches = {}
        book_created = False  # Flag to check if a book has been created

        for isbn in possible_isbns:
            confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass)

            if confidence == 34:
                log_print(f"\nSorry, we were unable to identify the specific edition of {spine.title}.\n The spine was undetected by torchvision and identified with AI model during OCR cleanup.\n")
                log_print("No dimensions or color to match. General information only for this book.\n")
                book = match.create_book_object(isbn, 0)
                books.append(book)
                log_print(f"Book object for {spine.title}: {book}\n")
                log_print("\n************************************************************\n\n")
                book_created = True  # Set the flag to True
                break
            if confidence >= 0.2:
                potential_matches[isbn] = confidence
                log_print(f"\n{spine.title} identified with ISBN: {isbn}\n")
                log_print(f"Identification confidence: {confidence}\n")
        
        if book_created:
            continue  # Skip to the next spine if a book has been created

        if len(potential_matches) == 0:
            second_pass = True
            for isbn in possible_isbns:
                confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass)
                if confidence == 34:
                    log_print(f"\nSorry, we were unable to identify the specific edition of {spine.title}.\n The spine was undetected by torchvision and identified with AI model during OCR cleanup.\n")
                    log_print("No dimensions or color to match. General information only for this book.\n")
                    book = match.create_book_object(isbn, 0)
                    books.append(book)
                    log_print(f"Book object for {spine.title}: {book}\n")
                    log_print("\n************************************************************\n\n")
                    book_created = True  # Set the flag to True
                    break
                if confidence >= 0.0:
                    potential_matches[isbn] = confidence
                    log_print(f"\n{spine.title} identified with ISBN: {isbn}\n")
                    log_print(f"Identification confidence: {confidence}\n")

        if book_created:
            continue  # Skip to the next spine if a book has been created

        if len(potential_matches) == 0 and second_pass:
            log_print(f"\nWe're sorry! '{spine.title}' could not be identified. Book object created with only detected title and authors.\n")
            book = Book()
            book.title = spine.title
            book.authors = spine.author
            book.confidence = 0
            books.append(book)
            log_print(f"\nBook object for {spine.title}: {book}\n")
            log_print("\n************************************************************\n\n")
        else:
            best_match = max(potential_matches, key=potential_matches.get)
            log_print(f"\n{spine.title} identified with ISBN: {best_match}\n")
            log_print(f"Identification confidence: {potential_matches[best_match]}\n")
            book = match.create_book_object(best_match, potential_matches[best_match])
            books.append(book)
            log_print(f"\nBook object for {spine.title}: {book}\n")
            log_print("\n************************************************************\n\n")

    end_spine_match = time.time()
    log_print(f"\nSpine matching complete. Time taken: {round(end_spine_match - start_spine_match, 2)} seconds\n")
    log_print(f"\nTotal spines checked: {total_spines}\n")
    log_print(f"\nTime taken per spine: {round((end_spine_match - start_spine_match) / total_spines, 2)} seconds\n")
    log_print(f"\nTotal potential ISBNs checked: {total_potential_isbns}\n")
    log_print(f"Time taken per potential ISBN: {round((end_spine_match - start_spine_match) / total_potential_isbns, 2)} seconds\n")

    return books




if __name__ == "__main__":
    # import tests
    # current_datetime = time.strftime("%Y%m%d-%H%M%S")
    # log_print(f"*** TESTING MATCHING FUNCTIONALITY ***\n\nTest Run: {current_datetime}\n\n")
    # spines = tests.spines
    # books = match_spines_to_books(spines)
    # util.log_print("\nAll identified books:\n")
    # for book in books:
    #     util.log_print(book)
    #     util.log_print("\n")
    vision("vision/images/test_images/mom_test.jpeg")
