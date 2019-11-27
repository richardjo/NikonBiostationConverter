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

def metadata_retriever (directory):
    """Recurses through folder structor of the "home directory" to find metadata to be saved.
    Parameters:
    directory (str): The absolute path of a home directory.
    """
    
    #Generates list of directories and files to iterate over
    FSO_list = [str(x) for x in directory.iterdir()]

    #Iterates over the list of directories and files
    for FSO in FSO_list:
        #If a micro.csv is found, its contents are read and the saving function is initialized
        if "micro.csv" in str(FSO):
            csv_path = str(directory / "micro.csv")
            [image_file_list, position_x_list, position_y_list, magnification_list, delta_T, rows, columns] = retrieve_metadata(csv_path, use_stitching)
            metadata_saver(image_file_list, position_x_list, position_y_list, magnification_list, delta_T, directory, output_directory, rows, columns)
            return

    #Recursive step
    for directory_path in FSO_list:
        if ".DS_Store" in directory_path:
            continue
        elif "_macros" in directory_path:
            continue
        elif "_headerfiles" in directory_path:
            continue
        else:
            directory_path = Path(directory_path)
            metadata_retriever(directory_path)

def metadata_saver (image_file_list, position_x_list, position_y_list, magnification_list, delta_T_list, sub_directory, output_directory, rows, columns):
    """Converts a list of files to OME Tiff and saves metadata to them
    Parameters: 
    image_file_file_names (array): List of image files to be converted.
    position_x_list (array): List of x-axis positions for each image file.
    position_y_list (array): List of y-axis positions for each image file.
    magnification_list (array): List of magnfication values for each image file.
    delta_T_list (array): List of delta_T values of reach image file.
    sub_directory (str): The absolute path of the directory containing files to be converted.
    output_directory (str): The absolute path of the directory to which converted files should be saved.
    rows (str): Rows in a stitched cell.
    columns (str): Columns in a stitched cell.
    """

    time_counter = 0
    time_directory = Path(str(time_counter))
    os.mkdir(str(output_directory / time_directory))

    for file in image_file_list:

        #Removes backwards slashes from file path for cross-platform compatability
        file_name = Path(file.replace("\\","/"))

        input_image_path = str(sub_directory / file_name)
        
        #Converts input images files into .ome.tiffs, either in a new, separate directory or an old one
        #and renames them if stitching is needed.

        index = np.where(image_file_list == str(file))[0][0]

        if use_output_directory == False:
            output_directory = Path(sub_directory)

        #If stitching is needed, files names are renamed to work with FIJI's stitching plug-in
        if use_stitching == True:

            #If a new time point is reached, a new directory is created to separate each stitched cell.
            if delta_T_list[index] > 0:
                time_counter += 1        
                time_directory = Path(str(time_counter))
                os.mkdir(str(output_directory / time_directory))
                   
            file_name = Path(stitching(str(Path(file_name.stem)), rows, columns)).with_suffix(".xml")
            
        else:
            pass

        output_tiff_path = str(output_directory / time_directory / file_name.with_suffix(".ome.tiff"))
        convert(input_image_path, output_tiff_path, bf_tools_directory)
        xml_path = str(output_directory / time_directory / file_name.with_suffix(".xml"))

        #Saves metadata
        save_metadata(output_tiff_path,position_x_list[index], position_y_list[index], magnification_list[index], delta_T_list[index], xml_path, bf_tools_directory)

metadata_retriever(home_directory)

