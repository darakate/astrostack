# Astrophotography Stacking
## Purpose
Atmospheric turbulence is a well known problem when it comes to astrophotography; planets will appear blurry and distorted even with a quality microscope.
A classic solution is image stacking where the composite of several images allows for averaging out distortion.

This is a quick and simple project meant to demonstrate competency in python and familiarity with common imaging processing techniques. It has the potential to be expanded on later, but a goal of mine with this project was to complete it in less than a day.
## Overview
### Credits / Inspiration
This project was inspired from a project in the book "Impractical Python Projects" by Lee Vaughn. As such, all images used as inputs are available at https://nostartch.com/impracticalpython/ for reference. I did not include them for download here.

I took a few different approaches compared to the algorithms presented and I will discuss them briefly below. 

### Programs
The programs were called in the following order:
- astro_registration.py
- astro_stack.py
- astro_shrpen.py

The following Jupyter notebooks are included, which I used to work out some details before finalizing them in my code. They show some of the intermediate process from start to finish.
- Crop_Test.ipnyb
- Stacking.ipnyb
- Sharpen_Tests.ipnyb

### Image Cropping
The example text used a bitwise threshold mask to isolate Jupiter.

I used sobel gradients since it is a classic edge detection method. I took the sum over the perpendicular direction of the gradient to find the peaks; this is quick and it has less reliance on single pixel values because it is based on the sumation. Inspired by peak analysis, I opted to rely on the half-max values of the peaks to reliably find the edges.

I output the details of cropping the images into a .csv file so that I could reference the information later if I wanted. This allowed me to see how consistently the image size was once I finished cropping. I was able to use this data when scaling the image to a consistent size.

### Image Scaling
The example text scaled the images to predtermined size and the scaling was performed before cropped images were saved. These images were roughly 4x larger than the actual input image-- I choose against this because I wanted to more strictly adhere to the raw input data.

I performed the scaling during the loading and stacking step, and I used minimal scaling based on the largest image with linear interpolation.

### Image Stacking
The images were stacked in an array. There were some 256 cropped images, but I choose to use the last 20 images alone as this is a commonly used amount for stacking with astrophotography.

Notably, it's not common to use more than 20 images with astrophotography, and there are a few reasons for this. First, around 10 images is enough to produce an increase in image quality compared to one or two images. Second, the objects of interest are not "stationary" from the viewpoint. Objects in the sky will appear to drift over time and the objects will rotate as well. Jupiter, for example, only takes about 10 hours to make a complete rotation.

I took the mean of the images and converted back to integer format for saving.

### Image Sharpening
I used a few classic sharpening methods.

First, a simple sharpening kernel.

Second, I used a laplace filter and subtracted it from the original image. As this filter is highly sensitive to image noise, I used a gaussian blur on the image before applying the lapace filter as is common practice.

I applied the sharpening filters to both the stacked image as well as the first cropped image so that the two images could be compared.

## Future Work
### Image Sharpening
I think post-processing the stacked image could be improved upon, and extended experimentation with a sharpening mask is how I would go about it.

I played around in the free image software GIMP to see what improvements could be made by sharpening the stacked image. I am unhappy to admit that it's better than the ones I programmed, although this process is also a bit more subjective; the more the image is tinkered with the further it gets away from the input source.

### Image Registration
Image registration, or matching the images up could be improved upon. I was initially suspicious that my algorithm for finding the object, Jupiter, would not be all that consistent or reliable.

I no longer think that is the case, and I think the next best step for improving would be to properly line up the objects better. I would like to investiage what the impact of scaling the images to be consistent in size, removing the border surrounding Jupiter, and not scaling at all.

I would also like to investigate more complex methods of image registration, such as detecting Jupiter's features and matching them between successive images as more sophisticated programs do.

### Number of Images
I may investiage how many images it takes to meaningfully produce results, but I think this step only makes sense once matching up Jupiter is improved.