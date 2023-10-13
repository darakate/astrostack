import os
import cv2
import numpy as np

def main():
    working_dir = r'C:\Users\darak\OneDrive\Documents\Python Scripts\Astrophotography Stacking'
    output_folder = 'cropped_images'
    crop_image_file = 'crop_1.jpeg'
    stacked_image_file = 'stacked_jupiter.jpg'

    os.chdir(working_dir)

   # Basic Sharpen Filter
    output_file_1 = 'sharpened_stacked_jupiter.jpg'
    simple_sharpen_filter(stacked_image_file, output_file_1)

    # Apply to a single cropped image as a sanity check
    output_file_2 = 'sharpened_jupiter_crop_01.jpg'
    simple_sharpen_filter(os.path.join(output_folder, crop_image_file), output_file_2)

    # Laplace Sharp Mask
    output_file_3 = 'laplace_sharpened_stacked_jupiter.jpg'
    laplace_sharp_mask(stacked_image_file, output_file_3)

    output_file_4 = 'laplace_sharpened_jupiter_crop_01.jpg'
    laplace_sharp_mask(os.path.join(output_folder, crop_image_file), output_file_4)


def simple_sharpen_filter(input_file, output_file):
    img = cv2.imread(input_file)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    #kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(output_file, sharpened_image)

def laplace_sharp_mask(input_file, output_file):
    img = cv2.imread(input_file)
    blurred = cv2.GaussianBlur(img, (3,3), 0)
    lap = cv2.Laplacian(blurred, cv2.CV_64F)
    sharpened_img = img - (.7*lap)
    sharpened_img = sharpened_img.astype(np.uint8)
    cv2.imwrite(output_file, sharpened_img)
    
if __name__ == '__main__':
    main()


