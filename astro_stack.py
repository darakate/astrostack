import os
import sys
import shutil
import cv2
import numpy as np
import pandas as pd

def main():
    working_dir = r'C:\Users\darak\OneDrive\Documents\Python Scripts\Astrophotography Stacking'
    csv_filename = 'output_dimension_log.csv'
    image_folder = 'cropped_images'
    os.chdir(working_dir)

    # Read CSV File For Metadata
    df = pd.read_csv(csv_filename)

    # Grab last 20 Images Only - This is a typical amount in astrophotography
    df = df.tail(20)
    df = df.reset_index()
    n_images = 20

    # Get Image Dimensions
    max_values = df.max(axis=0)
    x_dim = max_values['XDIM']
    y_dim = max_values['YDIM']
    #n_images = 256

    # Create Dummy Image
    image_stack_B = np.zeros((x_dim, y_dim, n_images))
    image_stack_G = np.zeros((x_dim, y_dim, n_images))
    image_stack_R = np.zeros((x_dim, y_dim, n_images))
    for index, row in df.iterrows():
        img_file = row["Output File"]
        img = cv2.imread(os.path.join(image_folder, img_file))
        resize_img = cv2.resize(img, (y_dim, x_dim), interpolation=cv2.INTER_LINEAR)

        image_stack_B[:,:, index] = resize_img[:,:, 0]
        image_stack_G[:,:, index] = resize_img[:,:, 1]
        image_stack_R[:,:, index] = resize_img[:,:, 2]

    # Flatten Color Channels
    new_image = np.zeros((x_dim, y_dim, 3))
    new_image[:,:, 0] = image_stack_B.mean(axis=2)
    new_image[:,:, 1] = image_stack_G.mean(axis=2)
    new_image[:,:, 2] = image_stack_R.mean(axis=2)
    new_image = new_image.astype(int)
    
    # Save File
    output_filename = 'stacked_jupiter_2.jpg'
    cv2.imwrite(output_filename, new_image)

if __name__ == '__main__':
    main()