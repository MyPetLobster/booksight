import time

import analyze_spine as asp
import detect_spines as ds
import detect_text as dt
import exporter as export
import matcher as match
import utility as util
from utility import log_print 


from classes import Spine, Book


def vision(image_path):

    # Create log file and empty directories
    util.create_log_file()
    util.empty_directories()

    start = time.time()

    ### Book Object Detection ###
    # Detect book spines and create individual spine jpegs
    log_print("\nDetecting book spines in the image...\n")
    spine_images, spine_count = ds.crop_spines(image_path)
    if spine_images == None:
        log_print("\nNo valid books detected. Exiting program.\n")
        return
   
    spine_detection_end = time.time()
    log_print(f"Spine detection complete. Time taken: {round(spine_detection_end - start, 2)} seconds\n")

    if spine_count == 0:
        log_print("\nNo books detected. Exiting program.\n")
        return
    elif 0 < spine_count < 20:
        log_print("\nAnalyzing images and creating Spine objects. This may take several minutes...\n")
    else:
        log_print("\nAnalyzing images and creating Spine objects. This image contains a lot of books. Go stretch your legs. This may take a while...\n")


    ### OCR Text Detection ###
    # Create Spine objects - Detect text, colors, and dimensions
    spines = []
    i = 0
    for image in spine_images:
        avg_color, dominant_color, color_palette, height, width = asp.analyze_spine(image)
        text = dt.detect_text(image)
        spine = Spine(image, avg_color, dominant_color, color_palette, height, width, text)
        spines.append(spine)
        log_print(f"\n- Spine_{i}: {spine}")
        i += 1
    spine_object_end = time.time()
    log_print(f"\nSpine objects created.\nTime taken: {round(spine_object_end - spine_detection_end, 2)} seconds\n")

    # Get all scanned text from each Spine
    all_spine_text = []
    for spine in spines:
        all_spine_text += spine.text 

    log_print("\n************************************************")
    log_print(f"\nAll text detected from all spines:\n\n{all_spine_text}\n")
    log_print("************************************************\n")

    log_print("\nScanning full image for additional text...\n")
    log_print("\nLarge images may take a while to process.\n")

    full_scan_start = time.time()
    full_image_text = dt.detect_text(image_path)
    full_image_text = [text for text in full_image_text if len(text) > 2]
    
    full_image_text_unique = [text for text in full_image_text if text not in all_spine_text] 

    full_scan_end = time.time()
    log_print(f"\nFull image scanned.\nTime taken: {round(full_scan_end - full_scan_start, 2)} seconds\n\n")
    log_print("\n************************************************")

    log_print(f"\nAll additional unique text detected from full image:\n\n{full_image_text_unique}\n")
    log_print("************************************************\n")
    log_print("\nAll image processing and OCR operations complete.\n")
    log_print(f"\nTotal time taken for image processing and OCR: {round(time.time() - start, 2)} seconds\n\n")
    log_print("************************************************\n\n\n\n")

    
    ### Book Identification ###
    log_print("\nBegin book identification process...\n")

    # Clean up text data and retrieve potential ISBNs for each spine
    spines = match.id_possible_matches(spines, full_image_text_unique)

    log_print("\n***********************************************\n")
    log_print("\nAll Spine Objects:\n")
    for spine in spines:
        log_print(spine)
        log_print("\n")
    log_print("\n***********************************************\n")


    ### Book Matching ###
    log_print("\nBegin precise book identification process.\nThis may take a while...\n")
    books = match_spines_to_books(spines)
    log_print("\nBook identification process complete.\n")

    log_print("\n\n\n************************************************")
    log_print("\n\nAll identified books:\n")
    for book in books:
        log_print(f"{book}\n")
    log_print("************************************************\n\n\n")

    log_print(f"Total time taken to identify books: {round(time.time() - start, 2)} seconds\n\n")

    # Export identified books to CSV and JSON
    log_print("\nExporting identified books to CSV and JSON...\n")

    export.export_to_csv(books)
    export.export_to_json(books)

    log_print("\nAll processes complete. Thank you for using Booksight.\n")



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
        found = False
        possible = False
        possible_isbns = spine.possible_matches
        total_potential_isbns += len(possible_isbns)

        while not found:
            for isbn in possible_isbns:
                confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass)

                if confidence >= 0.6:
                    log_print(f"\n{spine.title} identified with ISBN: {isbn}\n")
                    log_print(f"Identification confidence: {confidence}\n")

                    # Create a Book object for the matched spine and populate with data
                    log_print(f"Creating book object for {spine.title}...\n")
                    book = match.create_book_object(isbn, confidence)
                    if len(book.description) > 75:
                        truncated_description = book.description[0:75] + "..."
                    else:
                        truncated_description = book.description

                    log_print(f"""Title: {book.title}\nSubtitles: {book.subtitle}\nAuthors: {book.authors}\nISBN: {book.isbn}\nLang: {book.language}\nPublisher: {book.publisher}\nDate Published: {book.date_published}\nDescription: {truncated_description}\nPage Count: {book.pages}\nThumbnail: {book.image_path}\nIdentification Confidence: {book.confidence}\n\n""")
                    books.append(book)
                    found = True
                    break
                elif 0.1 < confidence < 0.6:
                    log_print(f"\n{spine.title} possibly identified with ISBN: {isbn}\n")
                    log_print(f"Identification confidence: {confidence}\n")
                    log_print("Please verify the identification manually.\n")
                    # Create a Book object for the matched spine and populate with data
                    if possible:
                        if confidence > possible_book.confidence:
                            possible_book = match.create_book_object(isbn, confidence)
                    else:
                        possible_book = match.create_book_object(isbn, confidence)
                    possible = True
                    break

            if not found and not possible and not second_pass:
                log_print(f"\n\nNo Matches found for {spine.title}. Starting second pass, disregarding dimensions. Thank you for your patience...\n\n")
                confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass=True)
                if confidence >= 0.3:
                    log_print(f"\n{spine.title} identified with ISBN: {isbn}\n")
                    log_print(f"Identification confidence: {confidence}\n")


                    # Create a Book object for the matched spine and populate with data
                    book = match.create_book_object(isbn, confidence)
                    books.append(book)
                    found = True
                elif 0.1 < confidence < 0.3:
                    log_print(f"\n{spine.title} possibly identified with ISBN: {isbn}\n")
                    log_print(f"Identification confidence: {confidence}\n")
                    log_print("Please verify the identification manually.\n")
                    # Create a Book object for the matched spine and populate with data
                    if possible:
                        if confidence > possible_book.confidence:
                            possible_book = match.create_book_object(isbn, confidence)
                    else:
                        possible_book = match.create_book_object(isbn, confidence)
                    possible = True
            elif not found and not possible and second_pass:
                log_print(f"\n{spine.title} could not be identified. Please verify the identification manually.\n")
                book = Book()
                book.title = spine.title
                book.authors = spine.author
                book.confidence = 0
                books.append(book)
                found = True
            elif not found and possible:
                log_print(f"\n{spine.title} - Low confidence. Please verify the identification manually.\n")
                books.append(possible_book)
                found = True
                
    end_spine_match = time.time()
    log_print(f"\nSpine matching complete. Time taken: {round(end_spine_match - start_spine_match, 2)} seconds\n")
    log_print(f"\nTotal spines checked: {total_spines}\n")
    log_print(f"\nTime taken per spine: {round((end_spine_match - start_spine_match) / total_spines, 2)} seconds\n")
    log_print(f"\nTotal potential ISBNs checked: {total_potential_isbns}\n")
    log_print(f"Time taken per potential ISBN: {round((end_spine_match - start_spine_match) / total_potential_isbns, 2)} seconds\n")

    return books




if __name__ == "__main__":
    # spines = [
    #     Spine("vision/images/detection_temp/spines/book_0.jpeg", [172, 156, 144], [211, 198, 185], [[211, 198, 185], [18, 14, 11], [242, 230, 215], [211, 67, 32], [101, 93, 93], [191, 172, 156]], 1129, 263, ['uiz', 'UZumakl', 'Uig', 'UZUMAKL', 'JUNII ITO'], "Uzumaki", "Junji Ito", ['8575326902', '9788417490270', '9781421561325', '9788575327302', '6555140577', '1569317143', '9781569317143', '1421513900', '9781421513904']),
    #     Spine("vision/images/detection_temp/spines/book_1.jpeg", [169, 160, 148], [217, 194, 172], [[217, 194, 172], [31, 26, 21], [240, 230, 215], [157, 134, 116], [85, 81, 65], [7, 5, 3]], 1102, 210, ['mistory', 'Arr', '0  O m', 'MARY', 'BFARD', 'KFARD', 'ROMi', '0i Anciint', 'Udsi', 'c  Q x', 'ROME', 'ddsUu'], "SPQR: A History of Ancient Rome", "Mary Beard", ['9785961445169', '9781782839675', '1782839674', '3596031346', '3100022300', '9786064018113', '6064018119', '9788498929799', '8498929792', '6555352167']),
    #     Spine("vision/images/detection_temp/spines/book_2.jpeg", [91, 84, 68], [20, 17, 13], [[20, 17, 13], [245, 240, 227], [115, 89, 47], [12, 123, 87], [185, 174, 151], [50, 42, 32]], 1094, 159, ['nods', 'DESTSELLER', 'Autmon0', 'WAR ipe SEBASTIAI JUHGER 4', 'Mltoat', 'DestSELLeR', 'Muthor or', 'AOa', 'Ing Ptrttgt', 'Wewtoat', 'nheS', 'Jiont', 'IhE ctaftGT', 'Jtoat', '1 WAR ip SEBASTIAII JUHGER'], "War", "Sebastian Junger", ['0446556246', '9780446566971', '9780007362134', '9780007337712', '9781609415013', '0446569763', '9780446569767', '1609415019', '9781609415013', '9780007362134']),
    #     Spine("vision/images/detection_temp/spines/book_3.jpeg", [93, 89, 103], [92, 83, 101], [[92, 83, 101], [243, 232, 220], [11, 15, 10], [103, 97, 133], [48, 55, 50], [184, 166, 158]], 1005, 124, ['haruki Murakami', 'W 0 0', 'N 0 R W E 6 a N'], "Norwegian Wood", "Haruki Murakami", ['009952029X', '9780099520290', '9780307762719', '0307762718', '9722621750', '9789722621755']),
    #     Spine("vision/images/detection_temp/spines/book_4.jpeg", [111, 95, 68], [168, 151, 117], [[168, 151, 117], [56, 46, 31], [111, 83, 42], [243, 237, 223], [23, 17, 12], [135, 113, 74]], 1088, 172, ['InD ardtoti', 'dID', 'Orocotar', 'SELLER', '8888', 'iJC', 'JDHMSON', 'Itorr', 'HE LAUGHing MOMSTERS', 'Toht', 'TtGT', 'Jaor', 'VeS', 'HE LAUGHING MONSTERS 83 DEMIS', 'tallo'], "The Laughing Monsters", "Denis Johnson", ['9781443437998', '9781410476562', '1410476561', '9780374280598', '1443437999', '9780374280598', '0374280592', '9780374709235', '0374709238'])
    # ]
    # books = match_spines_to_books(spines)
    # util.log_print("\nAll identified books:\n")
    # for book in books:
    #     util.log_print(book)
    #     util.log_print("\n")
    vision("vision/images/test_images/test_five.jpeg")
