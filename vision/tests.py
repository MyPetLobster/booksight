from django.test import TestCase

from classes import Spine


# Data for each spine
spine_data = [
    ("vision/images/detection_temp/spines/book_0.jpeg", [172, 156, 144], [211, 198, 185], 
     [[211, 198, 185], [19, 15, 12], [242, 230, 215], [191, 172, 156], [103, 94, 93], [211, 67, 32]], 
     1117, 248, ['JUNII ITO, uiz, UZMAkL, JUNII ITO, uiz, UZUMAKL'], "Uzumaki", "Junji Ito", 
     ['8575326902', '9788417490270', '9781421561325', '9788575327302', '6555140577', '1421561328', '9786555140576', '8417490272', '8575327305', '9788575326909']),
    ("vision/images/detection_temp/spines/book_1.jpeg", [167, 160, 146], [15, 122, 86], 
     [[15, 122, 86], [239, 230, 214], [15, 12, 9], [52, 41, 33], [137, 109, 87], [206, 182, 159]], 
     1138, 211, ['MARY, BFARD, Hisiory, of AFciini, Romi, Odluci,  ~ O x, MARY, BFARD, History, 0i Ancieni, ROME, Ului, 0 ~ Q x'], "SPQR: A History of Ancient Rome", "Mary Beard", 
     ['9781631491252', '1631491253', '9781631491252', '1631491253']),
    ("vision/images/detection_temp/spines/book_2.jpeg", [92, 88, 101], [73, 74, 75], 
     [[73, 74, 75], [185, 167, 157], [27, 34, 25], [102, 96, 129], [6, 5, 3], [243, 232, 219]], 
     1030, 128, ['n 0 R W E 6 /A n, W 0 0 d, HaR Uki M U Rakam /, N 0 R W E 6 |a M, W 0 0 d, haruki Murakami'], "Norwegian Wood", "Haruki Murakami", 
     ['9025442846', '9789025442842', '009952029X', '9780099520290', '9786074211214', '6074211213', '9784062748698', '406274869X', '9780307762719', '0307762718']),
    ("vision/images/detection_temp/spines/book_3.jpeg", [90, 83, 68], [49, 42, 32], 
     [[49, 42, 32], [245, 240, 228], [113, 87, 46], [20, 17, 13], [13, 123, 87], [185, 173, 151]], 
     1107, 153, ['Newtoai, nues, BESTSELLER, Muthor 0f, Mhltangt, Jion, WAR ip, SEBASTIAI JINGER M4, New Tork, TNIES, BESTSELLER, Auimor Of, IME PtaftGT, Sioat, AVAL, 1 WAR ipe SEBASTIAI JUHGER'], "War", "Sebastian Junger", 
     ['0446556246', '9780446566971', '9780007362134', '9780007337712', '9781609415013', '9780007337705', '9781607881988', '9781455500352', '9780446556248', '9781554685554']),
    ("vision/images/detection_temp/spines/book_4.jpeg", [110, 93, 64], [12, 114, 80], 
     [[12, 114, 80], [244, 236, 216], [134, 111, 72], [100, 74, 39], [172, 154, 116], [34, 25, 16]], 
     1145, 171, ['THE LAUGHING MONSTERS, @ui Jiuou, IER, THE LAUGHIng MONSTERS 8, DENIS, JDANSOM, Rure)'], "The Laughing Monsters", "Denis Johnson", 
     ['9781443437998', '9781410476562', '1410476561', '9780374280598', '1443437999', '0374280592', '9781427252272', '1846559359', '1427252270', '9781784700225'])
]

# Creating the list of Spine objects
spines = [Spine(*data) for data in spine_data]


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



# 







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