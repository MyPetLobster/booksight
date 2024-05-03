import time

from classes import Spine, Book

import analyze_spine as asp
import detect_spines as ds
import detect_text as dt
import utility as util

import db_requests as dbr
import exporter as export
import matcher as match


def vision():

    # Empty temp image directories
    util.empty_directory("vision/images/detection_temp/debug_images")
    util.empty_directory("vision/images/detection_temp/spines")
    util.empty_directory("vision/images/detection_temp/downloaded_images")

    # Get image file path from user
    jpeg_file = input("\nEnter the path to the image file: ")
    if jpeg_file == "":
        jpeg_file = "vision/images/test_images/test_five.jpeg"
        print(f"\nUsing default image: {jpeg_file}\n")

    # Start timer
    start = time.time()

    # Detect book spines and create individual spine jpegs
    print("\nDetecting book spines in the image...\n")
    spine_images, spine_count = ds.crop_spines(jpeg_file)
    if spine_images == None:
        print("\nNo valid books detected. Exiting program.\n")
        return
   
    print(f"Spine images saved in 'vision/images/detection_temp/spines/'\n")

    spine_detection_end = time.time()
    print(f"Spine detection complete. Time taken: {round(spine_detection_end - start, 2)} seconds\n")


    # Create Spine objects - Detect text, colors, and dimensions
    if spine_count == 0:
        print("\nNo books detected. Exiting program.\n")
        return
    elif 0 < spine_count < 20:
        print("\nAnalyzing images and creating Spine objects. This may take several minutes...\n")
    else:
        print("\nAnalyzing images and creating Spine objects. This image contains a lot of books. Go stretch your legs. This may take a while...\n")

    spines = []

    i = 0
    for image in spine_images:
        avg_color, dominant_color, color_palette, height, width = asp.analyze_spine(image)
        text = dt.detect_text(image)
        spine = Spine(image, avg_color, dominant_color, color_palette, height, width, text)
        spines.append(spine)
        print(f"\n- Spine_{i}: {spine}")
        i += 1

    spine_object_end = time.time()
    print(f"\nSpine objects created.\nTime taken: {round(spine_object_end - spine_detection_end, 2)} seconds\n")


    # Get all scanned text from each Spine
    all_spine_text = []
    for spine in spines:
        all_spine_text += spine.text 

    print("\n************************************************")
    print(f"\nAll text detected from all spines:\n\n{all_spine_text}\n")
    print("************************************************\n")

    print("\nScanning full image for additional text...\n")
    print("\nLarge images may take a while to process.\n")

    full_scan_start = time.time()
    # Scan original image for text, apart from individual spines
    full_image_text = dt.detect_text(jpeg_file)
    full_image_text = [text for text in full_image_text if len(text) > 2]
    
    full_image_text_unique = [text for text in full_image_text if text not in all_spine_text] 

    full_scan_end = time.time()
    print(f"\nFull image scanned.\nTime taken: {round(full_scan_end - full_scan_start, 2)} seconds\n\n")

    print("\n************************************************")
    print(f"\nAll additional unique text detected from full image:\n\n{full_image_text_unique}\n")
    print("************************************************\n")
    
    print("\nAll image processing and OCR operations complete.\n")
    print(f"\nTotal time taken for image processing and OCR: {round(time.time() - start, 2)} seconds\n\n")
    print("************************************************\n")
    print("************************************************\n")
    print("************************************************\n\n\n\n")
    # Match books
    print("\nBegin book identification process...\n")

    # Clean up text data and retrieve potential ISBNs for each spine
    spines = match.id_possible_matches(spines, full_image_text_unique)

    print("\n***********************************************\n")
    print("\nAll Spine Objects:\n")
    for spine in spines:
        print(spine)
        print("\n")
    print("\n***********************************************\n")


    print("\nBegin precise book identification process.\nThis may take a while...\n")

    books = match_spines_to_books(spines)

    print("\nBook identification process complete.\n")

    print("\n\n\n************************************************")
    print("\n\nAll identified books:\n")
    for book in books:
        print(f"{book}\n")
    print("************************************************\n\n\n")

    print(f"Total time taken to identify books: {round(time.time() - start, 2)} seconds\n\n")

    # Export identified books to CSV and JSON
    print("\nExporting identified books to CSV and JSON...\n")

    export.export_to_csv(books)
    export.export_to_json(books)

    print("\nAll processes complete. Thank you for using Booksight.\n")



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

                print(f"Confidence: {confidence}\n")

                if confidence >= 0.3:
                    print(f"\n{spine.title} identified with ISBN: {isbn}\n")
                    print(f"Identification confidence: {confidence}\n")

                    # Create a Book object for the matched spine and populate with data
                    print(f"Creating book object for {spine.title}...\n")
                    book = match.create_book_object(isbn, confidence)
                    if len(book.description) > 75:
                        truncated_description = book.description[0:75] + "..."
                    else:
                        truncated_description = book.description

                    print(f"""Title: {book.title}\nSubtitles: {book.subtitle}\nAuthors: {book.authors}\nISBN: {book.isbn}\nLang: {book.language}\nPublisher: {book.publisher}\nDate Published: {book.date_published}\nDescription: {truncated_description}\nPage Count: {book.pages}\nThumbnail: {book.image_path}\nIdentification Confidence: {book.confidence}\n\n""")
                    books.append(book)
                    found = True
                    break
                elif 0.1 < confidence < 0.3:
                    print(f"\n{spine.title} possibly identified with ISBN: {isbn}\n")
                    print(f"Identification confidence: {confidence}\n")
                    print("Please verify the identification manually.\n")
                    # Create a Book object for the matched spine and populate with data
                    if possible:
                        if confidence > possible_book.confidence:
                            possible_book = match.create_book_object(isbn, confidence)
                    else:
                        possible_book = match.create_book_object(isbn, confidence)
                    possible = True
                    break

            if not found and not possible and not second_pass:
                print(f"\n\nNo Matches found for {spine.title}. Starting second pass, disregarding dimensions. Thank you for your patience...\n\n")
                confidence, color_filter, px_to_inches, second_pass, isbn = match.check_for_match(spine, isbn, color_filter, px_to_inches, second_pass=True)
                if confidence >= 0.3:
                    print(f"\n{spine.title} identified with ISBN: {isbn}\n")
                    print(f"Identification confidence: {confidence}\n")


                    # Create a Book object for the matched spine and populate with data
                    book = match.create_book_object(isbn, confidence)
                    books.append(book)
                    found = True
                elif 0.1 < confidence < 0.3:
                    print(f"\n{spine.title} possibly identified with ISBN: {isbn}\n")
                    print(f"Identification confidence: {confidence}\n")
                    print("Please verify the identification manually.\n")
                    # Create a Book object for the matched spine and populate with data
                    if possible:
                        if confidence > possible_book.confidence:
                            possible_book = match.create_book_object(isbn, confidence)
                    else:
                        possible_book = match.create_book_object(isbn, confidence)
                    possible = True
            elif not found and not possible and second_pass:
                print(f"\n{spine.title} could not be identified. Please verify the identification manually.\n")
                book = Book()
                book.title = spine.title
                book.authors = spine.author
                book.confidence = 0
                books.append(book)
                found = True
            elif not found and possible:
                print(f"\n{spine.title} - Low confidence. Please verify the identification manually.\n")
                books.append(possible_book)
                found = True
                
    end_spine_match = time.time()
    print(f"\nSpine matching complete. Time taken: {round(end_spine_match - start_spine_match, 2)} seconds\n")
    print(f"\nTotal spines checked: {total_spines}\n")
    print(f"\nTime taken per spine: {round((end_spine_match - start_spine_match) / total_spines, 2)} seconds\n")
    print(f"\nTotal potential ISBNs checked: {total_potential_isbns}\n")
    print(f"Time taken per potential ISBN: {round((end_spine_match - start_spine_match) / total_potential_isbns, 2)} seconds\n")

    return books




if __name__ == "__main__":
    # spines = [
    #     Spine("vision/images/detection_temp/spines/book_0.jpeg", [164, 149, 137], [211, 198, 185], [[211, 198, 185], [18, 14, 11], [242, 230, 215], [211, 67, 32], [101, 93, 93], [191, 172, 156]], 1129, 263, ['uiz', 'UZumakl', 'Uig', 'UZUMAKL', 'JUNII ITO'], "Uzumaki", "Junji Ito", ['8575326902', '9788417490270', '9781421561325', '9788575327302', '6555140577', '1421561328', '9786555140576', '8417490272', '8575327305', '9788575326909', '9781569317143', '1569317143', '9781421513898', '9781421513904', '1421513900', '1421513897', '9781421513911', '9781591160489', '1421513919', '1591160480', '1591160332', '9781591160335', '9781974706952', '1974706958', '1421561328', '9781421561325', '1569317143', '9781569317143', '1421513900', '9781421513904', '1421513919', '9781421513911', '1974713008', '9781974713004', '3486840142', '9783486840148', '9781974715794', '1974715795', '9781974729661', '1974729664']),
    #     Spine("vision/images/detection_temp/spines/book_1.jpeg", [169, 160, 148], [217, 194, 172], [[217, 194, 172], [31, 26, 21], [240, 230, 215], [157, 134, 116], [85, 81, 65], [7, 5, 3]], 1102, 210, ['mistory', 'Arr', '0  O m', 'MARY', 'BFARD', 'KFARD', 'ROMi', '0i Anciint', 'Udsi', 'c  Q x', 'ROME', 'ddsUu'], "SPQR: A History of Ancient Rome", "Mary Beard", ['9781631491252', '1631491253', '9781631491252', '1631491253', '9781631494109', '1631494104', '9780674032187', '0674032187', '0521456460', '9780521456463', '9781847650641', '1847650643', '9780521840620', '0521840627', '9780691222363', '0691222363']),
    #     Spine("vision/images/detection_temp/spines/book_2.jpeg", [91, 84, 68], [20, 17, 13], [[20, 17, 13], [245, 240, 227], [115, 89, 47], [12, 123, 87], [185, 174, 151], [50, 42, 32]], 1094, 159, ['nods', 'DESTSELLER', 'Autmon0', 'WAR ipe SEBASTIAI JUHGER 4', 'Mltoat', 'DestSELLeR', 'Muthor or', 'AOa', 'Ing Ptrttgt', 'Wewtoat', 'nheS', 'Jiont', 'IhE ctaftGT', 'Jtoat', '1 WAR ip SEBASTIAII JUHGER'], "War", "Sebastian Junger", ['0446556246', '9780446566971', '9780007362134', '9780007337712', '9781609415013', '9780007337705', '9781607881988', '9781455500352', '9780446556248', '9781554685554', '0007362137', '1455500356', '1455501581', '1554685559', '1607881985', '0446583286', '000733771X', '0446566977', '9780446583282', '0007337701', '1609415019', '9781455501588', '0446566977', '0446556246', '9780446556248', '9780446566971', '0007352263', '9780007352265', '9780446556248', '0446556246', '9780446569767', '0446569763', '9780446556248', '0446566977', '9780446566971', '0446556246', '9780446556224', '044655622X', '0446569763', '9780446569767', '1609415019', '9781609415013', '3570551768', '9783570551769', '9780007362134', '0007362137']),
    #     Spine("vision/images/detection_temp/spines/book_3.jpeg", [93, 89, 103], [92, 83, 101], [[92, 83, 101], [243, 232, 220], [11, 15, 10], [103, 97, 133], [48, 55, 50], [184, 166, 158]], 1005, 124, ['haruki Murakami', 'W 0 0', 'N 0 R W E 6 a N'], "Norwegian Wood", "Haruki Murakami", ['9025442846', '9789025442842', '009952029X', '9780099520290', '9786074211214', '6074211213', '9784062748698', '406274869X', '9780307762719', '0307762718', '9780307430014', '0307430014', '9722621750', '9789722621755', '4770022328', '9784770022325', '9780451494658', '0451494652', '6074211213', '9786074211214', '9780307762740', '0307762742', '8373198334', '9788373198333', '9781400044610', '1400044618', '9788858407240', '8858407245']),
    #     Spine("vision/images/detection_temp/spines/book_4.jpeg", [111, 95, 68], [168, 151, 117], [[168, 151, 117], [56, 46, 31], [111, 83, 42], [243, 237, 223], [23, 17, 12], [135, 113, 74]], 1088, 172, ['InD ardtoti', 'dID', 'Orocotar', 'SELLER', '8888', 'iJC', 'JDHMSON', 'Itorr', 'HE LAUGHing MOMSTERS', 'Toht', 'TtGT', 'Jaor', 'VeS', 'HE LAUGHING MONSTERS 83 DEMIS', 'tallo'], "The Laughing Monsters", "Denis Johnson", ['9781443437998', '9781410476562', '1410476561', '9780374280598', '1443437999', '0374280592', '9781427252272', '1846559359', '1427252270', '9781784700225', '1784700223', '9781846559358', '1444831208', '9781444831207', '9780374280598', '0374280592', '9780374709235', '0374709238', '0060192488', '9780060192488', '9780812988659', '0812988655', '9780061869464', '0061869465', '9780593469774', '0593469771', '9780061869396', '0061869392', '0887486274', '9780887486272', '9780061869549', '0061869546'])
    # ]
    # books = match_spines_to_books(spines)
    # print("\nAll identified books:\n")
    # for book in books:
    #     print(book)
    #     print("\n")

    vision()
