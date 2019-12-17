# Nikon Biostation CT Converter

## Introduction
This project takes files outputted by the Nikon Biostation CT microscope, 
converts the image files (png) to the open source OME image format and writes metadata from the data files (csv) to the image files (ome.tiff). Files can also be renamed in order to support Fiji's ([https://fiji.sc/](https://fiji.sc/)) stitching plug-in.

The program makes use of existing command line tools, provided by the Open Microscopy Environment (OME), which can convert and write data to the ome.tiff format. The program includes a rudimentary GUI using the Tkinter library in order to make the operation of the program easier for imaging specialists without experience in the computer science field. 


As of now, the current iteration of the project supports:

 - Writing of x and y position, magnification and time delta metadata.
 - Processing of images with multiple time points.
 - Processing of images for stitching.
 - Outputting of images to a desired output directory with different folders to indicate separate time points.

![Tiling](https://lh3.googleusercontent.com/fGrshO5wHH6nf9eh3f0BoqPl6BcsBreHtQb4Xf5k7UPNqp54JpQmxj9NaXQNGw61yocUMRBpgHGTvDhwp_HmHJqILJdDNRUxcxaQxA777H_69eYJnNlykJF2G5GwHIP3j234a97KQc-TrTAMrttN_3I3nyob0Zib763jr-25aJ2D8gycTzm6hDHCY8TcqpgUorfHUPBaASfSYO1kfWNWxR30MXKAtMFwRQ48caVsJBqQQbiMtmNi6StjIAqDEyvUa8X27_YnbTaQkeuS_ZjijFX9DlYkoNYR3xBVUc1R_Z5Wy2GjT3EODrRqi7k3-pQs9WwEdQeBjUIbltUTwr-isJ5RiwX9kJCvujI1V8gwYGn1MTJweg36EgYS3M4iz3EZ_EcNBw4Vjrl8SI5CvNsxk9tN0k9vHYCoXMCmJvV-32pvLFZyEDi9i5T9-eyzfFl7Is8CMtA87OayiJ5tOcNVO2BM2JldlwemXu2rlAVh45kxsFbNjLlsVpppXNiIyiZIhU5SrZmNSMRtxPXzCxReYAlYX82QYQv-OzEltPsMrZZVdvY6rzcgHgde9sXM2soE_DRZ6e5ZRhTGAddOq-h3eaAUYN69dcctShemu02kFTW3uec--wnnLAX10q9XvikFZB3vMNhtYDtn_x1uRgSymgxsgwUw2GlsOIJlFgRIOHB-KnWIdeBO=w770-h573-no)

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
 2. Navigate to the "dist" folder in the download, run the executable and then click on the actual application. Be patient - this process can take a long time.

**Operation**
 1. Locate the directory containing input images using the dropdown menu.
 2. Locate a directory for output images, using the dropdown menu, and ensure that the folder has read/write access. That folder could be the input directory.
 3. Choose whether stitching is required or not. If stitching is not selected and the input images are tiled, the data files will not be read correctly, regardless if renaming of the files is desired.
 4. Click the convert button. Once the conversion process is completed, the "spinning beach bubble" will disappear. Again, be patient - this process can take a very long time, especially for a large image/dataset.

![User Interface](https://lh3.googleusercontent.com/AlpFYvJsBkTgupbVuuZfCv0SizPBezHW7b58ju5Or_yHXn3IKo1LzJamPUAppUuqSdysxHx9tpePOXPXEfeguqacVp7DwEc--ZLA42MNHyYJ3ZZfi6fm8ovvxsSd64ysPdKWtPX0X3-xThra_JbqjaTY0SGmAFPo01npM0YEAaawgfntYvnPI5LtFi_KNkhv_bjjKrcBFe4mGWLMcfiSG5hcJe-CZTR1MxIh80fbinvV94Z_2E76NeTfYQt_LdV15VoTggmi2joYySE7jbajI-YzgEp9MB6bt6Y-lf7ldOU2ObKMxSJY0btcYNh6aajLBAbJmwfzAeQqSl4CvSgYvgB7Eg6l42BDur-r50Bz7liB-jSLmWZ0g_nfWZO3ZR05jzq50NLcrxU8_ukMN2cRdNvNQjaWcYjOitFAsgn6YfI9FhgzJa_OOI1arFrXtKb-ttXUSDWMKL6N4UsGmZ9RFiWsAvP__ZGW0ja_jH1s1s3wgE0E0aC-dyIjYML_Z8g52gb_zgCmaApyf1fvWdqxSWmws3Q_zDUWBOhtVV0nJtoQCVYG6glx0ZtRNceMFJeJd96pR5Ajjz0Rrk0KFwNp-LLAW_c7UU__IaZ0h_WqzddJ4ce-huLi9PQAWS7kgdq4T0g2tgipmsH7TW435d6l6QxRoxfkPsyew_hN12QUd3_g5mlKiiLw=w505-h527-no)
