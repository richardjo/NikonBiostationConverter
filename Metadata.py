import subprocess
import pandas as pd
from xml.etree import ElementTree as ET
import datetime
from pathlib import Path
import numpy as np

ET.register_namespace('', 'http://www.openmicroscopy.org/Schemas/OME/2016-06')

def retrieve_metadata(csv_file_path, use_stitching):
    """Retrieves image metadata from a CSV file
    Parameters:
    csv_file_path (str): The absolute path of a CSV file.

    Returns:
    image_file_list (array): An array of image file names.
    position_x_list (array): An array of x positions for each image file.
    position_y_list (array): An array of y positions for each image file.
    """
    rows = None
    columns = None
    
    #Formats CSV for data importing
    with open(csv_file_path,encoding="utf16") as csv_file:
        #Removes whitespace characters
        for line in csv_file:
            line = line.strip()
            if "Width" in str(line):
                rows = str(line)[-1]
            if "Height" in str(line):
                columns = str(line)[-1]

    #Converts csv into Pandas Datafile for easy data manipulation
    if use_stitching == True:
        csv_dataFile = pd.read_csv(csv_file_path, delimiter = "	", encoding = "utf-16", error_bad_lines=False, header = 4)
    else:
        csv_dataFile = pd.read_csv(csv_file_path, delimiter = "	", encoding = "utf-16", error_bad_lines=False)

    #Obtains list of image files
    image_file_list = csv_dataFile["File Name"].values

    #Obtains list of position values
    position_x_list = csv_dataFile["Position X(um)"].values
    position_y_list = csv_dataFile["Position Y(um)"].values

    #Obtains list of magnification values
    magnification_list = csv_dataFile["Magnification"].values

    #Obtains list of time values
    time_list = csv_dataFile["Time Stamp"].values
    delta_T_list = np.array([0])
    
    if len(time_list) > 1:
        for x in range(0,length(time_list)-1):
            [hour1, minute1] = (time_list[x])[-5:].split(":")
            [hour2, minute2] = (time_list[x+1])[-5:].split(":")
            delta_T = datetime.timedelta(hours = int(hour2), minutes = int(minute2)) - datetime.timedelta(hours = int(hour1),minutes = int(minute1))
            delta_T.append(int(delta_T.seconds))

    return image_file_list, position_x_list, position_y_list, magnification_list, delta_T_list, rows, columns

def convert(input_file_path, output_file_path, bf_tools_directory):
    """Converts an image file to the OME Tiff format.
    Parameters:
    input_file_path (str): The absolute path of the input file.
    output_file_path (str): The absolute path of the converted output file in the OME Tiff format.
    bf_tools_directory (str): The absolute path of the bioformats command line tools.
    """

    #Runs BIOFORMATS command line script to convert input files into output files
    subprocess.run([bf_tools_directory+"/bfconvert", input_file_path, output_file_path])

def save_metadata(input_file_path, position_x, position_y, magnification, delta_T, xml_file_path, bf_tools_directory):
    """Saves metadata from an XML file into an OME Tiff
    Parameters:
    input_file_path (str): The absolute path of the input OME Tiff file.
    position_x (str): The x-axis position of the input OME Tiff file.
    position_y (str): The y-axis position of the input OME Tiff file.
    magnification (str): The objective magnification of the input OME Tiff file.
    delta_T (str): The difference in time between adjacent input OME Tiff files.
    xml_file_path (str): The absolute path of the xml_file containing corresponding metadata for the OME Tiff file.
    bf_tools_directory (str): The absolute path of the bioformats command line tools.
    """

    #Runs BIOFORMATS command line script to obtain existing XML in a converted OME Tiff file
    output = subprocess.Popen([bf_tools_directory + "/tiffcomment", input_file_path], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    raw_xml = output.communicate()

    #Removes special characters from raw XML file
    formatted_xml = str(raw_xml).replace("(b'","").replace(r"\n', None)","")

    #Saves XML into a XML file
    with open(xml_file_path,"w+") as output:
        output.write(formatted_xml)

    #Opens XML data in the XML file for writing
    XML = ET.parse(xml_file_path)
    XML_root = XML.getroot()

    #Writes magnification metadata
    ET.SubElement(XML_root, "Instrument", {"ID": "https://cam.facilities.northwestern.edu/instruments/"})
    ET.SubElement(XML.find("Instrument"), "Objective", {"CalibratedMagnification": str(magnification), "ID":"https://cam.facilities.northwestern.edu/instruments/"})
    ET.SubElement(XML.find("Instrument"), "Microscope", {"Manufacturer":"Nikon", "Model":"Nikon Biostation CT"})
    
    #Writes position and time metadata
    if delta_T != None:
        ET.SubElement(XML_root[0][0], "Plane", {"DeltaT":str(delta_T), "TheC": "0", "TheT":"0", "TheZ":"0", "PositionX":str(position_x), "PositionY":str(position_y)})
    else:
        ET.SubElement(XML_root[0][0], "Plane", {"TheC": "0", "TheT":"0", "TheZ":"0", "PositionX":str(position_x), "PositionY":str(position_y)})
    
    #Writes pixel size metadata
    if magnification == 2:
         XML_root[0][0].set("PhysicalSizeX",str(4.016))
         XML_root[0][0].set("PhysicalSizeY",str(4.016))
    if magnification == 4:
         XML_root[0][0].set("PhysicalSizeX",str(1.976))
         XML_root[0][0].set("PhysicalSizeY",str(1.976))
    if magnification == 10:
         XML_root[0][0].set("PhysicalSizeX",str(0.791))
         XML_root[0][0].set("PhysicalSizeY",str(0.791))
    if magnification == 20:
         XML_root[0][0].set("PhysicalSizeX",str(0.397))
         XML_root[0][0].set("PhysicalSizeY",str(0.397))
    if magnification == 40:
         XML_root[0][0].set("PhysicalSizeX",str(0.200))
         XML_root[0][0].set("PhysicalSizeY",str(0.200))
    
    #Saves it
    XML.write(xml_file_path,short_empty_elements=False)

    #Runs BIOFORMATS command line script to save new XML into the OME Tiff file
    subprocess.run([bf_tools_directory+"/tiffcomment", "-set", xml_file_path, input_file_path])

def stitching(input_file_path, rows, columns):
    """Renames files for stitching in FIJI
    Parameters:
    input_file_path(str): Absolute path of the input OME Tiff file.
    rows(str): Number of rows in each "cell".
    columns(str): Number of columns in each "cell".
    """
    
    index = input_file_path.find("T")
    element_number = (int(input_file_path[index+5:index+6]) - 1) * int(columns) + int(input_file_path[index+8:index+9])
    element_number = str(element_number)
    if len(element_number) == 1:
        element_number = "0" + element_number
    renamed_file_path = r"tile_" + element_number
    return renamed_file_path
