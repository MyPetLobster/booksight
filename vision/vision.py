import cv2 as cv 
import numpy as np

import easyocr 


def main(jpeg_file):

    # Load the image from the jpeg file.
    img = cv.imread(jpeg_file)

    # Convert the image to grayscale.
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Increase the contrast of the image.
    clahe = cv.createCLAHE(clipLimit=4, tileGridSize=(8, 8))

    # Apply the contrast limited adaptive histogram equalization (CLAHE) to the image.
    clahe_img = clahe.apply(gray_img)

    # Apply a Gaussian blur to the image.
    final_img = cv.GaussianBlur(clahe_img, (5, 5), 0)

    np_img = np.zeros(final_img.shape, final_img.dtype)
    alpha = 1.5
    beta = -50

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(img.shape[2]):
                np_img[y,x,c] = np.clip(alpha*img[y,x,c] + beta, 0, 255)




    # reader = easyocr.Reader(['en'], gpu=True)

    # result = reader.readtext(final_img)

    # # Rotate the image by 90 degrees.
    # img_90 = cv.rotate(final_img, cv.ROTATE_90_CLOCKWISE)
    # result_90 = reader.readtext(img_90)

    # # Rotate the image by 180 degrees.
    # img_180 = cv.rotate(final_img, cv.ROTATE_180)
    # result_180 = reader.readtext(img_180)

    # # Rotate the image by 270 degrees.
    # img_270 = cv.rotate(final_img, cv.ROTATE_90_COUNTERCLOCKWISE)
    # result_270 = reader.readtext(img_270)

    # # Combine the results from the four rotations.
    # result.extend(result_90)
    # result.extend(result_180)
    # result.extend(result_270)


    # # detections stored as 3-tuples: (bbox, text, prob)
    # print("DETECTIONS:")
    # for detection in result:
    #     if detection[1].length > 2:
    #         print(detection[1])



    cv.imshow("FINAL", final_img)
    cv.waitKey(0)
    cv.destroyAllWindows()









if __name__ == "__main__":
    # Test the main function with a sample jpeg file.
    jpeg_file = "vision/test_images/two_books.jpeg"
    main(jpeg_file)

