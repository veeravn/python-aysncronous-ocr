import cv2
import numpy as np
import pytesseract
import multiprocessing
from PIL import Image

# Path of working folder on Disk

def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite("removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(img_path, img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path))

    # Remove template file
    #os.remove(temp)

    return result

if __name__ == '__main__':
    print ('--- Start recognizing text from image ---')
    pool = multiprocessing.Pool()
    filename = "" 
    fileList = []
    # Get name of first file to parse
    filename = input("Enter picture location\n")
    # Get list of file names to parse as long as the name is not 'end' to parse asyncronously
    while filename != "end":
        fileList.append(filename)
        filename = input("Enter picture location\n")

    if(filename == "end"):
        # Create a pool to run operation on all image files
        # Run the get_string function for each file in list to parse the text in the image using Tesseract asyncronously
        result_async = [pool.apply_async(get_string, args = (i, )) for i in
                        fileList]
        
        # Once parsing is completed, create a list of the outputs for each asyncronous operation and print results.
        results = [r.get() for r in result_async]
        for num, r in enumerate(results): 
            print("Output {}:\n{}".format(num+1, r))

        print ("------ Done -------")
        