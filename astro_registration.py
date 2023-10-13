import os
import sys
import shutil
import cv2
import numpy as np
import csv

def main():
    input_dir = r'C:\Users\darak\OneDrive\Documents\Python Scripts\Impractical_Python_Projects-master\Impractical_Python_Projects-master\Chapter_15\video_frames'
    working_dir = r'C:\Users\darak\OneDrive\Documents\Python Scripts\Astrophotography Stacking'
    output_folder = 'cropped_images'

    # Prep folders
    os.chdir(working_dir)
    empty_folder(output_folder)
    shutil.copytree(input_dir, output_folder)

    # Cleanup by deketing copies
    crop_prefix = 'crop'
    crop_images(output_folder, crop_prefix, padding=15)
    clean_folder(output_folder, crop_prefix)

def crop_images(image_folder, crop_prefix, padding):
    # Start Log File
    csv_filename = 'output_dimension_log.csv'
    with open(csv_filename, newline='', mode='w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Input File', 'Output File', 'YMIN', 'YMAX', 'XMIN', 'XMAX', 'YDIM', 'XDIM'])
    # Open Files
    file_list = os.listdir(image_folder)
    for file_num, file in enumerate(file_list, start=1):
        filename = os.path.join(image_folder, file)
        if os.path.isfile(filename):
            print("Opening file", filename)
            img = cv2.imread(filename)

            # Grayscale easier to work with
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Use Sobel Filter Gradient across X and Y Directions, as this provides edge detection
            sobel_x_grad = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y_grad = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

            # Take the sum across the filtered images in relavant direction -- this reduces noise and single pixel dependency and stacks the "bright" and "dark" areas the filter identifies
            sum_grad_x = np.sum(sobel_x_grad, axis=0)
            sum_grad_y = np.sum(sobel_y_grad, axis=1)

            # Apply Smoothing Filter - peak is still noisy
            ksize = 5
            kernel = np.ones((ksize),np.float32)/ksize
            smooth_x = np.convolve(kernel, sum_grad_x)
            smooth_y = np.convolve(kernel, sum_grad_y)

            # Find value of "Half Max" of the Min and Max Peaks -- Half-max will be a consistent way to identify near the edge of the object, more consistent than peak alone
            x_grad_half_max = np.amax(smooth_x)/2
            x_grad_half_min = np.amin(smooth_x)/2
            y_grad_half_max = np.amax(smooth_y)/2
            y_grad_half_min = np.amin(smooth_y)/2

            # Initialize min, max values
            xmin = 0
            ymin = 0
            xmax = len(sum_grad_x)
            ymax = len(sum_grad_y)

            # Get X Min
            for i in range(1, len(sum_grad_x)):
                if smooth_x[i] >= x_grad_half_max:
                    xmin = i - padding
                    break
            # Get Y Min
            for i in range(1, len(sum_grad_y)):
                if smooth_y[i] >= y_grad_half_max:
                    ymin = i - padding
                    break
            # Get X Max
            for i in range(1, len(sum_grad_x)):
                if smooth_x[-i] <= x_grad_half_min:
                    xmax = len(sum_grad_x) - i + padding
                    break
            # Get Y Max
            for i in range(1, len(sum_grad_y)):
                if smooth_y[-i] <= y_grad_half_min:
                    ymax = len(sum_grad_y) - i + padding
                    break

            # Validate Padding / Bounding Box Size
            size_error = False
            if xmin < 0:
                size_error = True
            elif ymin < 0:
                size_error = True
            elif xmax > len(sum_grad_x):
                size_error = True
            elif ymax > len(sum_grad_y):
                size_error = True
            elif ymin > ymax:
                size_error = True
            elif xmin > xmax:
                size_error = True

            if size_error == False:
                cropped_image = img[ymin:ymax, xmin:xmax]
                output_file = crop_prefix + '_{}.jpeg'.format(file_num)
                cv2.imwrite(os.path.join(image_folder, output_file), cropped_image)
                with open(csv_filename, newline='', mode='a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([file, output_file, ymin, ymax, xmin, xmax, ymax-ymin, xmax-xmin])
            else:
                print("Error with image file size. No image written.")

# Empty Folder
def empty_folder(output_folder):
    for item in os.listdir():
        if os.path.isdir(item) and item.startswith(output_folder):
            shutil.rmtree(item)

# Remove the copy files, keep the cropped ones
def clean_folder(folder_name, crop_name):
    for item in os.listdir(folder_name):
        if not item.startswith(crop_name):
            os.remove(os.path.join(folder_name, item))

if __name__ == '__main__':
    main()