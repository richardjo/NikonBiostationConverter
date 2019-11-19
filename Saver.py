from pathlib import Path
import os
from Metadata import retrieve_metadata, convert, save_metadata, stitching
import numpy as np

#Starting conditions
home_directory = Path("/Users/richardjo/Desktop/BioStationData/MyData")
bf_tools_directory = "/Users/richardjo/downloads/bftools"
output_directory = Path("/Users/richardjo/Desktop/BioStationData/MyDataOutput")
use_output_directory = True
use_stitching = True

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
                [image_file_list, position_x_list, position_y_list, magnification_list, delta_T, rows, columns] = retrieve_metadata(csv_path)
                metadata_saver(image_file_list, position_x_list, position_y_list, magnification_list, delta_T, sub_directory, rows, columns)

def metadata_saver (image_file_list, position_x_list, position_y_list, magnification_list, delta_T, sub_directory, rows, columns):
    """Converts a list of files to OME Tiff and stores metadata in them
    Parameters: file_names
    file_names (array): List of image files to be converted
    """
    for file in image_file_list:

        #Removes backwards slashes from file path for cross-platform compatability
        file_name = Path(file.replace("\\","/"))

        input_image_path = str(sub_directory / file_name)
        
        #Converts input images files into .ome.tiffs, either in a new, separate directory or an old one
        #and renames them if stitching is needed.
        
        if use_output_directory == True:
            if use_stitching == True:
                stiching_file_name = stitching(str(Path(file_name.stem)), rows, columns)
                output_tiff_path = str(output_directory / Path(stiching_file_name).with_suffix(".ome.tiff"))
                convert(input_image_path, output_tiff_path, bf_tools_directory)
                xml_path = str(output_directory / Path(stiching_file_name).with_suffix(".xml"))
            else: 
                output_tiff_path = str(output_directory / Path(file_name.stem).with_suffix(".ome.tiff"))
                convert(input_image_path, output_tiff_path, bf_tools_directory)
                xml_path = str(output_directory / Path(file_name.stem).with_suffix(".xml"))
        else:
            output_tiff_path = str(sub_directory / file_name.with_suffix(".ome.tiff"))
            convert(input_image_path, output_tiff_path, bf_tools_directory)
            xml_path = str(sub_directory / file_name.with_suffix(".xml"))

        index = np.where(image_file_list == str(file))[0]

        #Saves metadata
        save_metadata(output_tiff_path,position_x_list[index][0], position_y_list[index][0], magnification_list[index][0], delta_T, xml_path, bf_tools_directory)

metadata_retriever()

