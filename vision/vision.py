import time

import analyze_spine as asp
import detect_spines as ds
import detect_text as dt
import exporter as export
import matcher as match
import utility as util


from classes import Spine, Book


def vision(image_path):

    # Create log file and empty directories
    util.create_log_file()
    util.empty_directory("vision/images/detection_temp/debug_images")
    util.empty_directory("vision/images/detection_temp/spines")
    util.empty_directory("vision/images/detection_temp/downloaded_images")
    util.empty_directory("vision/exports/csv")
    util.empty_directory("vision/exports/json")

    # Start timer
    start = time.time()

    # Detect book spines and create individual spine jpegs
    util.log_print("\nDetecting book spines in the image...\n")
    spine_images, spine_count = ds.crop_spines(image_path)
    if spine_images == None:
        util.log_print("\nNo valid books detected. Exiting program.\n")
        return
   
    util.log_print(f"Spine images saved in 'vision/images/detection_temp/spines/'\n")

    spine_detection_end = time.time()
    util.log_print(f"Spine detection complete. Time taken: {round(spine_detection_end - start, 2)} seconds\n")


    # Create Spine objects - Detect text, colors, and dimensions
    if spine_count == 0:
        util.log_print("\nNo books detected. Exiting program.\n")
        return
    elif 0 < spine_count < 20:
        util.log_print("\nAnalyzing images and creating Spine objects. This may take several minutes...\n")
    else:
        util.log_print("\nAnalyzing images and creating Spine objects. This image contains a lot of books. Go stretch your legs. This may take a while...\n")

    spines = []

    i = 0
    for image in spine_images:
        avg_color, dominant_color, color_palette, height, width = asp.analyze_spine(image)
        text = dt.detect_text(image)
        spine = Spine(image, avg_color, dominant_color, color_palette, height, width, text)
        spines.append(spine)
        util.log_print(f"\n- Spine_{i}: {spine}")
        i += 1

    spine_object_end = time.time()
    util.log_print(f"\nSpine objects created.\nTime taken: {round(spine_object_end - spine_detection_end, 2)} seconds\n")


    # Get all scanned text from each Spine
    all_spine_text = []
    for spine in spines:
        all_spine_text += spine.text 

    util.log_print("\n************************************************")
    util.log_print(f"\nAll text detected from all spines:\n\n{all_spine_text}\n")
    util.log_print("************************************************\n")

    util.log_print("\nScanning full image for additional text...\n")
    util.log_print("\nLarge images may take a while to process.\n")

    full_scan_start = time.time()
    # Scan original image for text, apart from individual spines
    full_image_text = dt.detect_text(image_path)
    full_image_text = [text for text in full_image_text if len(text) > 2]
    
    full_image_text_unique = [text for text in full_image_text if text not in all_spine_text] 

    full_scan_end = time.time()
    util.log_print(f"\nFull image scanned.\nTime taken: {round(full_scan_end - full_scan_start, 2)} seconds\n\n")

    util.log_print("\n************************************************")
    util.log_print(f"\nAll additional unique text detected from full image:\n\n{full_image_text_unique}\n")
    util.log_print("************************************************\n")
    
    util.log_print("\nAll image processing and OCR operations complete.\n")
    util.log_print(f"\nTotal time taken for image processing and OCR: {round(time.time() - start, 2)} seconds\n\n")
    util.log_print("************************************************\n\n\n\n")

    # Match books
    util.log_print("\nBegin book identification process...\n")

    # Clean up text data and retrieve potential ISBNs for each spine
    spines = match.id_possible_matches(spines, full_image_text_unique)

    util.log_print("\n***********************************************\n")
    util.log_print("\nAll Spine Objects:\n")
    for spine in spines:
        util.log_print(spine)
        util.log_print("\n")
    util.log_print("\n***********************************************\n")


    util.log_print("\nBegin precise book identification process.\nThis may take a while...\n")

    books = match_spines_to_books(spines)

    util.log_print("\nBook identification process complete.\n")

    util.log_print("\n\n\n************************************************")
    util.log_print("\n\nAll identified books:\n")
    for book in books:
        util.log_print(f"{book}\n")
    util.log_print("************************************************\n\n\n")

    util.log_print(f"Total time taken to identify books: {round(time.time() - start, 2)} seconds\n\n")

    # Export identified books to CSV and JSON
    util.log_print("\nExporting identified books to CSV and JSON...\n")

    export.export_to_csv(books)
    export.export_to_json(books)

    util.log_print("\nAll processes complete. Thank you for using Booksight.\n")



def match_spines_to_books(spines):
    util.empty_directory("vision/images/detection_temp/downloaded_images")

    start_spine_match = time.time()
    total_spines = len(spines)
    total_potential_isbns = 0

    books = []
    color_filter = (1, 1, 1)
    px_to_inches = 1

    for spine in spines:
        second_pass = False
        found = False
        possible = False
        possible_isbns = spine.possible_matches
        total_potential_isbns += len(possible_isbns)

        while not found:
            for isbn in possible_isbns:
                confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass)

                util.log_print(f"Confidence: {confidence}\n")

                if confidence >= 0.6:
                    util.log_print(f"\n{spine.title} identified with ISBN: {isbn}\n")
                    util.log_print(f"Identification confidence: {confidence}\n")

                    # Create a Book object for the matched spine and populate with data
                    util.log_print(f"Creating book object for {spine.title}...\n")
                    book = match.create_book_object(isbn, confidence)
                    if len(book.description) > 75:
                        truncated_description = book.description[0:75] + "..."
                    else:
                        truncated_description = book.description

                    util.log_print(f"""Title: {book.title}\nSubtitles: {book.subtitle}\nAuthors: {book.authors}\nISBN: {book.isbn}\nLang: {book.language}\nPublisher: {book.publisher}\nDate Published: {book.date_published}\nDescription: {truncated_description}\nPage Count: {book.pages}\nThumbnail: {book.image_path}\nIdentification Confidence: {book.confidence}\n\n""")
                    books.append(book)
                    found = True
                    break
                elif 0.1 < confidence < 0.6:
                    util.log_print(f"\n{spine.title} possibly identified with ISBN: {isbn}\n")
                    util.log_print(f"Identification confidence: {confidence}\n")
                    util.log_print("Please verify the identification manually.\n")
                    # Create a Book object for the matched spine and populate with data
                    if possible:
                        if confidence > possible_book.confidence:
                            possible_book = match.create_book_object(isbn, confidence)
                    else:
                        possible_book = match.create_book_object(isbn, confidence)
                    possible = True
                    break

            if not found and not possible and not second_pass:
                util.log_print(f"\n\nNo Matches found for {spine.title}. Starting second pass, disregarding dimensions. Thank you for your patience...\n\n")
                confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass=True)
                if confidence >= 0.3:
                    util.log_print(f"\n{spine.title} identified with ISBN: {isbn}\n")
                    util.log_print(f"Identification confidence: {confidence}\n")


                    # Create a Book object for the matched spine and populate with data
                    book = match.create_book_object(isbn, confidence)
                    books.append(book)
                    found = True
                elif 0.1 < confidence < 0.3:
                    util.log_print(f"\n{spine.title} possibly identified with ISBN: {isbn}\n")
                    util.log_print(f"Identification confidence: {confidence}\n")
                    util.log_print("Please verify the identification manually.\n")
                    # Create a Book object for the matched spine and populate with data
                    if possible:
                        if confidence > possible_book.confidence:
                            possible_book = match.create_book_object(isbn, confidence)
                    else:
                        possible_book = match.create_book_object(isbn, confidence)
                    possible = True
            elif not found and not possible and second_pass:
                util.log_print(f"\n{spine.title} could not be identified. Please verify the identification manually.\n")
                book = Book()
                book.title = spine.title
                book.authors = spine.author
                book.confidence = 0
                books.append(book)
                found = True
            elif not found and possible:
                util.log_print(f"\n{spine.title} - Low confidence. Please verify the identification manually.\n")
                books.append(possible_book)
                found = True
                
    end_spine_match = time.time()
    util.log_print(f"\nSpine matching complete. Time taken: {round(end_spine_match - start_spine_match, 2)} seconds\n")
    util.log_print(f"\nTotal spines checked: {total_spines}\n")
    util.log_print(f"\nTime taken per spine: {round((end_spine_match - start_spine_match) / total_spines, 2)} seconds\n")
    util.log_print(f"\nTotal potential ISBNs checked: {total_potential_isbns}\n")
    util.log_print(f"Time taken per potential ISBN: {round((end_spine_match - start_spine_match) / total_potential_isbns, 2)} seconds\n")

    return books




if __name__ == "__main__":
    vision("vision/images/test_images/test_five.jpeg")
