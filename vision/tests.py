from django.test import TestCase

from classes import Spine


# Test Data
spines = [
    Spine(
        image_path="vision/spines/book_0.jpeg",
        avg_color=[155, 185, 174],
        dominant_color=[189, 224, 214],
        color_palette=[
            [189, 224, 214],
            [10, 5, 4],
            [103, 103, 91],
            [146, 146, 132],
            [169, 209, 198],
            [54, 40, 32]
        ],
        height=2702,
        width=542,
        text=['280, Finnegans Wake, JAMES JOYcE']
    ),
    Spine(
        image_path="vision/spines/book_1.jpeg",
        avg_color=[133, 112, 103],
        dominant_color=[156, 133, 125],
        color_palette=[
            [156, 133, 125],
            [14, 6, 4],
            [127, 102, 92],
            [204, 189, 181],
            [142, 118, 110],
            [81, 63, 48]
        ],
        height=2758,
        width=263,
        text=['VINTAG E, PALE FIRE, N A B 0 KO V']
    ),
    Spine(
        image_path="vision/spines/book_2.jpeg",
        avg_color=[180, 137, 94],
        dominant_color=[156, 124, 92],
        color_palette=[
            [156, 124, 92],
            [28, 16, 13],
            [225, 205, 181],
            [234, 182, 107],
            [205, 83, 61],
            [97, 59, 35]
        ],
        height=2830,
        width=583,
        text=['Jom<", Picadoa, 37o s, Iror`, Jok, PicadoR, OF SMOKE, Dmo, DEnIs, DENis, TREE, TREE OF SMORE, from, JOHNSON, DENIS']
    ),
    Spine(
        image_path="vision/spines/book_3.jpeg",
        avg_color=[91, 72, 66],
        dominant_color=[180, 164, 158],
        color_palette=[
            [180, 164, 158],
            [67, 40, 34],
            [14, 6, 4],
            [240, 233, 225],
            [128, 88, 73],
            [187, 209, 200]
        ],
        height=2487,
        width=520,
        text=['ARTIST, 4 |Ome, (.issIcs, THE, IARNES, PORTRAIT, IiRi;s, 4 TOBe, and, YOUNG MAN, James Joyce, CSSICS, DUBLINERS']
    ), 
    Spine(
        image_path="vision/spines/book_4.jpeg",
        avg_color=[115, 93, 84],
        dominant_color=[21, 12, 10],
        color_palette=[
            [21, 12, 10],
            [143, 137, 132],
            [220, 206, 197],
            [188, 40, 36],
            [109, 104, 102],
            [243, 201, 97]
        ],
        height=2836,
        width=221,
        text=['NOBODV MOVE  DENLS JOHNSON, (o ?0, (Dicador, NOBODY MOVE_ DENIS JOHNSON']
    ),
    
]


# spines = [
#     Spine("vision/images/detection_temp/spines/book_0.jpeg", [172 156 144], [211 198 185], [[211, 198, 185], [18, 14, 11], [242, 230, 215], [211, 67, 32], [101, 93, 93], [191, 172, 156]], 1129, 263, ['uiz', 'UZumakl', 'Uig', 'UZUMAKL', 'JUNII ITO'], "Uzumaki", "Junji Ito", ['8575326902', '9788417490270', '9781421561325', '9788575327302', '6555140577', '1569317143', '9781569317143', '1421513900', '9781421513904']),
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




prompt = f"""You will receive a string formatted as list of text detected from spines of books, formatted like this --
        "Book_X: <OCR text>,". You must interpret the OCR text and identify each book's title and author. The OCR text may contain errors,
        unconventional spacing, or other issues that require intelligent parsing to deduce the correct information. Return a JSON-formatted
        string where each "Book_X" identifier is associated with an "author" and "title" key. If a book title and/or author cannot be confidently
        identified, use "Unknown" as the value. Correct all spelling and spacing errors in your response.
        
        The input text that follows "Full Image OCR Text: " is a scan of the full input image. If you have trouble identifying a spine's 
        text, there may be additional clues in the full image text. Additionally, there may be books whose spines went undetected. 
        If you identify additional books within that text, include them in the response, but you will have to add additional "Book_X" identifiers.

        Use every resource at your disposal to decipher the text and correctly identify all book titles and authors. Accuracy is critical. 

        - DO NOT MAKE UP BOOK TITLES OR AUTHORS. Use all of the data you have to identify a REAL author and REAL book title that would make 
        sense in the context of OCR text from the spine of a book. For Example, if you have some OCR text that says "HARY BFARD ROME Q R mistory", 
        You should be able to look through existing books and realize that the book is "SPQR" by Mary Beard. Do not include
        subtitles. Do not make up any authors or titles. 

        - If you are only able to identify an author, you should search your knowledge to find all the books that author has written, then 
        use that information along with the other letters in the OCR text in order to determine which title is most likely to be correct. Use the 
        same problem solving logic if you are only able to identify a title.

        - Your response is being decoded directly with Python's json.loads() function. Make sure your response is in the correct format without
        any additional characters or formatting.

        Here is the input text you will be working with: 
        Individual Spine OCR Text:
        Book_0: ['JUNII ITO, uiz, UZMAkL, UZUMAKL'],
        Book_1: ['0  O x, Oduci, History, BFARD, MARY, Romi, ROME,   O x, Hisiory, 01 ANCIENT, of AFciini, Ului'],
        Book_2: ['Haruki MuRakami, N 0 R W E 6 a N, W 0 0 d'],
        Book_3: ['Tilss, DESTSELLER, Jont, MhE etattgt, Metoat, Mue etaftGT, AVAL, Jiond, Wetoat, WAR ip SEBASTIAI JUIGER p4, Author or, nheS, 1 WAR ile SEBASTIAII JUHGER, Iuthor0'],
        Book_4: ['Rure, ThE LAUGHING MONSTERS, DEMIS J0HNSOM, IER, 2134, THE LAUGHING MONSTERS'],

        Full Image OCR Text:
        ['THELa, uiz, 1 WAR ie SEBASTIAI JUHGER, IMe ctaftGT, Ha R U K  M U Ra ka M , ROMe, TInIes, 0 Aneont, sioat, DESTSELLER, 0  O x, Mhl ctattGT, JDANSOM, Auimor Of, 0 Hicont, DENIS, Bestsellea, BARY, Auimor 0f, H1R U K M U Ra ka m , n  O e, Stoat, Uig, n 0 R W E gian W 0 0 d, New Yori, JUNII ITO, Syre, 05 BENIS J0hMSIM, ROME, DNes, N 0 R W E g a nW 0 0 d, BVARS, UZUMAKL, THE LAUGHING MONSTERS 8, Wew York, 1 WAR ipe SEBASTIAI JUIGER']
        """