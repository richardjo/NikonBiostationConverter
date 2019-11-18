from pathlib import Path
import os
from Metadata import retrieve_metadata, convert, save_metadata
import numpy as np

home_directory = Path("/Users/richardjo/Desktop/BioStationData/MyData")
bf_tools_directory = "/Users/richardjo/downloads/bftools"

def metadata_saver (image_file_list, position_x_list, position_y_list, magnification_list, delta_T, sub_directory):
    """Converts a list of files to OME Tiff and stores metadata in them
    Parameters: file_names
    file_names (array): List of image files to be converted
    """
    for file in image_file_list:

        #Removes backwards slashes from file path for cross-platform compatability
        file_name = Path(file.replace("\\","/"))

        #Converts input image to an OME Tiff file
        input_image_path = str(sub_directory / file_name)
        tiff_path = str(sub_directory / file_name.with_suffix(".ome.tiff"))
        convert(input_image_path,tiff_path, bf_tools_directory)

        index = np.where(image_file_list == str(file))[0]

        #Generates an xml from OME Tiff FIle, inserts metadata and saves it back
        xml_path = str(sub_directory / file_name.with_suffix(".xml"))
        save_metadata(tiff_path,position_x_list[index][0], position_y_list[index][0], magnification_list[index][0], delta_T, xml_path, bf_tools_directory)

def metadata_retriever ():
    """Parses folder structor of the "home directory" to find metadata to be saved"""

    for directory in home_directory.iterdir():
        directory_path = str(directory)
        if ".DS_Store" in directory_path:
            continue
        if "_macros" in directory_path:
            continue
        if "_headerfiles" in directory_path:
            continue
        for sub_directory in directory.iterdir():
            csv_path = str(sub_directory / "micro.csv")
            if ".DS_Store" in csv_path:
                continue
            else:
                [image_file_list, position_x_list, position_y_list, magnification_list, delta_T] = retrieve_metadata(csv_path)
                metadata_saver(image_file_list, position_x_list, position_y_list, magnification_list, delta_T, sub_directory)

metadata_retriever()