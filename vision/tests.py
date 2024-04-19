from django.test import TestCase\
from vision.vision import main

# Create your tests here.


class VisionTestCase(TestCase):
    def test_main(self):
        """
        Test the main function of the vision module.
        """
        # Test the main function with a sample jpeg file.
        jpeg_file = "vision/test_images/my_books_01.jpeg"
        spines = main(jpeg_file)
        self.assertEqual(len(spines), 1)
        self.assertEqual(spines[0].text, "The Hidden Palace Helene Wecker")
        self.assertEqual(spines[0].height, 3000)
        self.assertEqual(spines[0].thickness, 582)
        self.assertEqual(spines[0].background_color, (37, 37, 37))
        self.assertEqual(spines[0].text_color, (199, 170, 123))
    
