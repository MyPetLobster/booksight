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