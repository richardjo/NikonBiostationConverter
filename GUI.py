import tkinter as tk
from tkinter import filedialog
from MetadataSaver import metadata_saver


def input_directory_retriever():
    global input_directory 
    input_directory = filedialog.askdirectory()
    input_directory_entry.insert(0, str(input_directory))

def output_directory_retriever():
    global output_directory
    output_directory = filedialog.askdirectory()
    output_directory_entry.insert(0,str(output_directory))

def bf_directory_retriever():
    global bf_directory 
    bf_directory = filedialog.askdirectory()
    bf_directory_entry.insert(0,str(bf_directory))


root = tk.Tk()

#Title 
root.title("Nikon Biostation Converter")

canvas = tk.Canvas(root, height = 500, width = 500)
canvas.pack()

frame = tk.Frame(root, bg = "blue", bd = 5)
frame.place(relheight = 1, relwidth = 1)


title_label = tk.Label(frame, text = "Biostation CT Converter", bg = "blue", fg = "white", font = ("Calibri",30))
title_label.place(relx = 0.5, rely = 0, anchor = "n")

#Input Directory
output_directory_label = tk.Label(frame, text = "Input Directory", bg = "blue", fg = "white")
output_directory_label.place(relx = 0.5, rely = 0.10, anchor = "n")

input_directory_entry = tk.Entry(frame)
input_directory_entry.place(relx = 0.10, rely = 0.15, relheight = 0.05, relwidth = 0.55, anchor = "nw")

input_directory_button = tk.Button(frame, text = "Select Directory...", command = lambda:input_directory_retriever())
input_directory_button.place(relx = 0.75, rely = 0.15, relheight = 0.05, relwidth = 0.25, anchor = "n")

#Output Directory
output_directory_label = tk.Label(frame, text = "Output Directory", bg = "blue", fg = "white")
output_directory_label.place(relx = 0.5, rely = 0.25, anchor = "n")

output_directory_entry = tk.Entry(frame)
output_directory_entry.place(relx = 0.10, rely = 0.30, relheight = 0.05, relwidth = 0.55, anchor = "nw")

output_directory_button = tk.Button(frame, text = "Select Directory...", command = lambda:output_directory_retriever())
output_directory_button.place(relx = 0.75, rely = 0.30, relheight = 0.05, relwidth = 0.25, anchor = "n")

#Bio-Formats Directory
bf_directory_label = tk.Label(frame, text = "Bioformats Directory", bg = "blue", fg = "white")
bf_directory_label.place(relx = 0.5, rely = 0.40, anchor = "n")

bf_directory_entry = tk.Entry(frame)
bf_directory_entry.place(relx = 0.10, rely = 0.45, relheight = 0.05, relwidth = 0.55, anchor = "nw")

bf_directory_button = tk.Button(frame, text = "Select Directory...", command = lambda:bf_directory_retriever())
bf_directory_button.place(relx = 0.75, rely = 0.45, relheight = 0.05, relwidth = 0.25, anchor = "n")

#Stitching
use_stitching = tk.BooleanVar()
stitching_check = tk.Checkbutton(frame, text="Stitching?", variable=use_stitching, onvalue = True, offvalue = False)
stitching_check.place(relx = 0.5, rely = 0.55, relheight = 0.05, relwidth = 0.30, anchor = "n")

convert_button = tk.Button(frame, text = "Convert Images", command = lambda:metadata_saver(input_directory, output_directory, bf_directory, use_stitching.get()))
convert_button.place(relx = 0.5, rely = 0.75, relheight = 0.10, relwidth = 0.30, anchor = "n")

root.mainloop()

