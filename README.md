# Nikon Biostation CT Converter

## Introduction
This project takes files outputted by the Nikon Biostation CT microscope, 
converts the image files (png) into the open source OME image format and writes metadata from the data files (csv) to the image files (ome.tiff). Files can also be renamed in order to support Fiji's ([https://fiji.sc/](https://fiji.sc/)) stitching plug-in.

The program makes use of existing command line tools, provided by the Open Microscopy Environment (OME), which can convert and write data to the ome.tiff format. The program includes a rudimentary GUI using the Tkinter library in order to make the operation of the program easier for imaging specialists without experience in the computer science field. 


As of now, the current iteration of the project supports:

 - Writing of x and y position, magnification and time delta metadata.
 - Processing of images with multiple time points.
 - Processing of images for stitching.
 - Outputting of images to a desired output directory with different folders to indicate separate time points.

![Imgur](https://i.imgur.com/SXR9w85.jpg)

This project was completed under the guidance of Dr. David Kirchenbuechler and Dr. Dina Arvanitis at The Center of Advanced Microscopy at Northwestern's Feinberg School of Medicine.

## Getting Started
**Prerequisites**

Python 3

Packages
 - Data Analysis/Manipulation: ElementTree, pandas, numpy
 - File Management: pathlib, os
 - Command Line Interaction: subprocess
 - Date/Time: datetime
 - GUI: tkinter

Bioformats Command Line Tools: [https://www.openmicroscopy.org/bio-formats/downloads/](https://www.openmicroscopy.org/bio-formats/downloads/)
"This work is derived in part from the OME specification. Copyright (C) 2002-2016 Open Microscopy Environment"

## Installation/Operation
**Installation**

Option 1 (Harder, better performance)
 1. Install all prerequisites.
 2. `git clone <url-of-the-project>` or alternatively, download the repository directly from the GitHub site.
 3. Run the GUI.py program or navigate

Option 2 (Easier, slower performance)

 1. `git clone <url-of-the-project>` or alternatively, download the repository directly from the GitHub site.
 2. Navigate to the "dist" folder in the download, run the executable and then click on the actual application. Be patient - this process can take a long time (this feature has not been completed yet).

**Operation**
 1. Locate the directory containing input images using the dropdown menu.
 2. Locate a directory for output images, using the dropdown menu, and ensure that the folder has read/write access. That folder could be the input directory.
 3. Choose whether stitching is required or not. If stitching is not selected and the input images are tiled, the data files will not be read correctly, regardless if renaming of the files is desired.
 4. Click the convert button. Once the conversion process is completed, the "spinning beach bubble" will disappear. Again, be patient - this process can take a very long time, especially for a large image/dataset.

![Imgur](https://i.imgur.com/gvtGLUT.png)

© Richard Jo

richardjo2023@u.northwestern.edu
