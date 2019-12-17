#Data Processing Libraries
import pandas as pd
from xml.etree import ElementTree as ET

#Date/Time Library
import datetime

#Command-Line Interactions Libraries
from pathlib import Path
import os
import subprocess
import numpy as np

#Inputs

class MetadataRetriever:

    def __init__(self):
        self.micro_csv_lists = []
        self.csv_dataFile_lists = [] 

        self.dimensions_lists = []

        self.image_file_lists = []
        self.exclusive_image_file_lists = []
        self.position_x_lists = []
        self.position_y_lists = []
        self.magnification_values_lists = []
        self.delta_T_lists = []

        self.rows = 0
        self.columns = 0

    def retrieve_files(self, home_directory):
        home_directory = Path(home_directory)

        for fso in home_directory.iterdir():
            fso = str(fso)
            if "micro.csv" in fso:
                csv_path = str(home_directory / "micro.csv")               
                self.micro_csv_lists.append(csv_path)
                return
        
        for fso in home_directory.iterdir():
            fso = str(fso)
            if ".DS_Store" in fso:
                continue
            else:
                fso = Path(fso)
                self.retrieve_files(fso)
    
    def csv_formatting(self,use_stitching):
        rows = None
        columns = None
        for csv_file in self.micro_csv_lists:
        
        #Formats CSV for data importing
            with open(csv_file,encoding="utf16") as csv:
                
                #Removes whitespace characters
                for line in csv:
                    line = line.strip()
                    if "Width" in str(line):
                        self.rows = str(line)[-2]
                    if "Height" in str(line):
                        self.columns = str(line)[-2]
                        break
            
            self.dimensions_lists.append([rows,columns])
        
            #Converts csv into Pandas Datafile for easy data manipulation
            if use_stitching == True:
                self.csv_dataFile_lists.append(pd.read_csv(csv_file, delimiter = "	", encoding = "utf-16", error_bad_lines=False, header = 4))
            else:
                self.csv_dataFile_lists.append(pd.read_csv(csv_file, delimiter = "	", encoding = "utf-16", error_bad_lines=False))
    
    def retrieve_image_file_list (self):
        for index in range(0,len(self.csv_dataFile_lists)):
            csv_dataFile = self.csv_dataFile_lists[index]
            file_name_list = csv_dataFile["File Name"].values
            self.exclusive_image_file_lists.append(file_name_list)
            directory_name = Path(self.micro_csv_lists[index]).parent
            file_name_list = csv_dataFile["File Name"].values
            file_name_list = [str(directory_name / Path(file_name)) for file_name in file_name_list]
            self.image_file_lists.append(file_name_list)

    def retrieve_position_values (self):
        for csv_dataFile in self.csv_dataFile_lists:
            self.position_x_lists.append(csv_dataFile["Position X(um)"].values)
            self.position_y_lists.append(csv_dataFile["Position Y(um)"].values)
            
    def retrieve_magnification_values (self):
        for csv_dataFile in self.csv_dataFile_lists:
            self.magnification_values_lists.append(csv_dataFile["Magnification"].values)

    def retrieve_delta_T_values (self):
         
        for image_list in self.exclusive_image_file_lists:

            delta_T_list = [0]

            if len(image_list) > 1:

                delta_T_list = [0]

                for x in range(0,len(image_list)-1):
                    index = image_list[x].find("_")
                    hour1 = (image_list[x])[index+1:index+3]
                    minute1 = (image_list[x])[index+3:index+5]
                    hour2 = (image_list[x+1])[index+1:index+3]
                    minute2 = (image_list[x+1])[index+3:index+5]
                    
                    #Removes leading zeros from time values
                    if hour1[0] == 0:
                        hour1 = hour1[1]
                    if hour2[0] == 0:
                        hour2 = hour2[1]
                    if minute1[1] == 0:
                        minute1 = minute1[1]
                    if minute2[1] == 0:
                        minute2 = minute1[1]

                    delta_T = datetime.timedelta(hours = int(hour2), minutes = int(minute2)) - datetime.timedelta(hours = int(hour1),minutes = int(minute1))
                    delta_T_list.append(int(delta_T.seconds))
                
            self.delta_T_lists.append(delta_T_list)

class MetadataSaver:
    def __init__(self, image_file_list, output_directory, use_stitching, position_x_list=[], position_y_list=[], magnification_list=[], 
    delta_T_list=[],rows=None, columns=None):
        
        self.input_image_path_list = []
        self.output_image_path_list = []
        self.xml_path_list = []

        self.position_x_list = position_x_list
        self.position_y_list = position_y_list
        self.magnification_list = magnification_list
        self.delta_T_list = delta_T_list
        self.rows = rows
        self.columns = columns
        self.use_stitching = use_stitching
        self.output_directory = output_directory
        self.time_counter = 0

        for index in range(0,len(image_file_list)):
            #Removes backwards slashes from file path for cross-platform compatability
            input_file_path = Path(image_file_list[index].replace("\\","/"))

            self.input_image_path_list.append(str(input_file_path))
            
            #Converts input images files into .ome.tiffs, either in a new, separate directory or an old one
            #and renames them if stitching is needed.
            
            #If stitching is needed, files names are renamed to work with FIJI's stitching plug-in
            if use_stitching == True:
                file_name = str(input_file_path.name)
                time_index = file_name.find("T")
                element_number = str((int(file_name[time_index+5:time_index+6]) - 1) * int(columns) + int(file_name[time_index+8:time_index+9]))
                if len(element_number) == 1:
                    element_number = "0" + element_number
                input_file_path = Path(r"tile_" + element_number)
            
            if delta_T_list[index] > 0:
                self.time_counter += 1
            
            output_directory = Path(self.output_directory) / Path(str(self.time_counter))
            output_file_path = Path(self.output_directory) / Path(str(self.time_counter)) / Path(input_file_path.name)

            if not os.path.exists(str(output_directory)):
                os.makedirs(str(output_directory))

            self.output_image_path_list.append(str(output_file_path.with_suffix(".ome.tiff")))
            self.xml_path_list.append(str(output_file_path.with_suffix(".xml")))
            
    def convert(self, bf_tools_directory):
        for index in range(0,len(self.input_image_path_list)):
            subprocess.run([bf_tools_directory+"/bfconvert", self.input_image_path_list[index], self.output_image_path_list[index]])
            output = subprocess.Popen([bf_tools_directory + "/tiffcomment", self.output_image_path_list[index]], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            raw_xml = output.communicate()
            formatted_xml = str(raw_xml).replace("(b'","").replace(r"\n', None)","")
            with open(self.xml_path_list[index],"w+") as output:
                output.write(formatted_xml)

    def magnification_metadata(self):
        for index in range(0,len(self.input_image_path_list)):
            self.XML = ET.parse(self.xml_path_list[index])
            self.XML_root = self.XML.getroot()
            ET.SubElement(self.XML_root, "Instrument", {"ID": "https://cam.facilities.northwestern.edu/instruments/"})
            ET.SubElement(self.XML.find("Instrument"), "Objective", {"CalibratedMagnification": str(self.magnification_list[index]), "ID":"https://cam.facilities.northwestern.edu/instruments/"})
            ET.SubElement(self.XML.find("Instrument"), "Microscope", {"Manufacturer":"Nikon", "Model":"Nikon Biostation CT"})
            self.XML.write(self.xml_path_list[index],short_empty_elements=False)

    def pixel_size_metadata(self):
        for index in range(0,len(self.input_image_path_list)):
            self.XML = ET.parse(self.xml_path_list[index])
            self.XML_root = self.XML.getroot()
            if self.magnification_list[index] == 2:
                self.XML_root[0][0].set("PhysicalSizeX",str(4.016))
                self.XML_root[0][0].set("PhysicalSizeY",str(4.016))
            if self.magnification_list[index] == 4:
                self.XML_root[0][0].set("PhysicalSizeX",str(1.976))
                self.XML_root[0][0].set("PhysicalSizeY",str(1.976))
            if self.magnification_list[index] == 10:
                self.XML_root[0][0].set("PhysicalSizeX",str(0.791))
                self.XML_root[0][0].set("PhysicalSizeY",str(0.791))
            if self.magnification_list[index] == 20:
                self.XML_root[0][0].set("PhysicalSizeX",str(0.397))
                self.XML_root[0][0].set("PhysicalSizeY",str(0.397))
            if self.magnification_list[index] == 40:
                self.XML_root[0][0].set("PhysicalSizeX",str(0.200))
                self.XML_root[0][0].set("PhysicalSizeY",str(0.200))
            self.XML.write(self.xml_path_list[index],short_empty_elements=False)

    def delta_T_metadata(self):
        for index in range(0,len(self.input_image_path_list)):
            self.XML = ET.parse(self.xml_path_list[index])
            self.XML_root = self.XML.getroot()
            ET.SubElement(self.XML_root[0][0], "Plane", {"DeltaT":str(self.delta_T_list[index]), "TheC": "0", "TheT":"0", "TheZ":"0"})
            self.XML.write(self.xml_path_list[index],short_empty_elements=False)

    def save_metadata(self, bf_tools_directory):
        for index in range(0,len(self.input_image_path_list)):
            subprocess.run([bf_tools_directory+"/tiffcomment", "-set", self.xml_path_list[index], self.output_image_path_list[index]])

