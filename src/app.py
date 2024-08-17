# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 23:53:01 2024

@author: SirDoggyJvla
"""
# Imports
import os
import numpy as np
import chardet
import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Function to prompt user for directory path
def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title="Select Workshop Mods Directory")
    return folder_selected

# Main execution
if __name__ == '__main__':
    path = __file__
    path = path.replace("\\", "/")
    file_name = os.path.basename(path)
    path = path.replace("/" + file_name, "")
    path_main = path.replace("/src", "")
    os.chdir(path)

# Prompt user for the workshop mods directory
original_path = select_directory()
if not original_path:
    print("No directory selected. Exiting.")
    exit()

# Change path to my workshop mods
os.chdir(original_path)

# path_to string format
path_to = "{}/{}"

# /workshopID
map_mods = {}
for workshopID in os.listdir():
    store_mod = {"paths": {}}
    store_mod["paths"]["workshopID"] = path_to.format(original_path, str(workshopID) + "/mods")
    os.chdir(store_mod["paths"]["workshopID"])
    
    # /modFolderName
    for modFolderName in os.listdir():
        store_mod["paths"][modFolderName] = path_to.format(store_mod["paths"]["workshopID"], modFolderName)
        os.chdir(store_mod["paths"][modFolderName])
        
        main_path = store_mod["paths"][modFolderName]
        
        # check exists /media
        found = False
        for media in os.listdir():
            if media == "media":
                found = True
                
        if not found:
            continue
        
        store_mod["paths"]["media"] = path_to.format(store_mod["paths"][modFolderName], "media")
        os.chdir(store_mod["paths"]["media"])
        
        # check exists /maps
        found = False
        for maps in os.listdir():
            if maps == "maps":
                found = True
                
        if not found:
            continue
        
        store_mod["paths"]["maps"] = path_to.format(store_mod["paths"]["media"], "maps")
        os.chdir(store_mod["paths"]["maps"])
        
        # goes through every map in this workshopID
        for maps in os.listdir():
            
            # skip for that mod that has a file in its map folder
            if maps == "mod.info.info":
                continue
            
            # iterate through every map and get the cells if present
            store_mod["paths"][maps] = path_to.format(store_mod["paths"]["maps"], maps)
            
            # Skip if it's a file, not a directory
            if not os.path.isdir(store_mod["paths"][maps]):
                continue
            
            os.chdir(store_mod["paths"][maps])
            
            # Verifies it's a "Muldraugh, KY" map
            good = False
            for cells in os.listdir():
                if cells != "map.info":
                    continue
                
                # Exceptions
                if workshopID == "2914532881" or workshopID == "3109572404":
                    good = False
                    break
                with open('map.info', 'rb') as file:
                    raw_data = file.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']
                # Open the map.info file and get the name of the mod
                with open('map.info', 'r', encoding=encoding) as file:
                    # Read the file line by line
                    for line in file:
                        # Split each line based on the '=' character
                        parts = line.strip().split('=')
                        # Check if the split operation produced exactly two parts
                        if len(parts) == 2:
                            key, value = parts
                            # Check if the key is 'lots'
                            if key.strip() == 'lots':
                                # Print the value associated with 'name'
                                lots = value.strip()
                                if lots == "Muldraugh, KY":
                                    good = True
                                    break
            if not good:
                continue
            
            for cells in os.listdir():
                if "world_" in cells:
                    parts = cells.split("_")
                    y = int(parts[1])
                    x = int(parts[2].split(".")[0])
                    if modFolderName not in store_mod:
                        store_mod[modFolderName] = {}
                    if "cells" not in store_mod[modFolderName]:
                        store_mod[modFolderName]["cells"] = {}
                    if maps not in store_mod[modFolderName]["cells"]:
                        store_mod[modFolderName]["cells"][maps] = []
                    
                    # Append to store_mod only if the value is not already in the list
                    if [x, y] not in store_mod[modFolderName]["cells"][maps]:
                        store_mod[modFolderName]["cells"][maps].append([x, y])
                    
                    if "path" not in store_mod[modFolderName]:
                        store_mod[modFolderName]["path"] = main_path
                    os.chdir(store_mod[modFolderName]["path"])
                    
                    if "Mod name" not in store_mod[modFolderName]:
                        # Open the mod.info file and get the name of the mod
                        with open('mod.info', 'rb') as file:
                            raw_data = file.read()
                            result = chardet.detect(raw_data)
                            encoding = result['encoding']
                        # Open the mod.info file and get the name of the mod
                        with open('mod.info', 'r', encoding=encoding) as file:
                            # Read the file line by line
                            for line in file:
                                # Split each line based on the '=' character
                                parts = line.strip().split('=')
                                # Check if the split operation produced exactly two parts
                                if len(parts) == 2:
                                    key, value = parts
                                    # Check if the key is 'name'
                                    if key.strip() == 'name':
                                        # Print the value associated with 'name'
                                        name = value.strip()
                        
                        store_mod[modFolderName]["Mod name"] = name
                    
                    # Append to map_mods only if the value is not already in the list
                    if workshopID not in map_mods:
                        map_mods[workshopID] = {}
                    if modFolderName not in map_mods[workshopID]:
                        map_mods[workshopID][modFolderName] = {"cells": {}}
                    if maps not in map_mods[workshopID][modFolderName]["cells"]:
                        map_mods[workshopID][modFolderName]["cells"][maps] = []
                    
                    if [x, y] not in map_mods[workshopID][modFolderName]["cells"][maps]:
                        map_mods[workshopID][modFolderName]["cells"][maps].append([x, y])
                    
        # store info and cells if exists
        if modFolderName in store_mod:
            map_mods[workshopID] = store_mod

# sets back main directory
os.chdir(path)


### Start of the GUI app using the generated map_mods ###

# GUI Setup
root = tk.Tk()
root.title("Map Selector")
root.geometry('300x600')  # Set the size of the window

# Extract unique items directly from the map_mods
unique_items = set()
for mod_data in map_mods.values():
    for mod in mod_data.values():
        if "Mod name" in mod:
            unique_items.add(mod["Mod name"])
unique_items = sorted(unique_items)  # Sort the items alphabetically

# Create a scrollable frame for the list of items
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

# Configure the scrollable frame to adjust its size
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

# Add scrollable frame to canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the widgets
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
container.pack(fill="both", expand=True)

# Variable to store selected items
selected_items = []

# Store BooleanVars for checkboxes
item_vars = {}
item_labels = {}
for item in unique_items:
    var = tk.BooleanVar()
    var.set(False)  # Initialize to unchecked
    chk = tk.Checkbutton(scrollable_frame, text=item, variable=var, onvalue=True, offvalue=False, 
                         command=lambda item=item: on_item_check(item))
    chk.pack(anchor='w')
    item_vars[item] = var
    item_labels[item] = chk

# Initialize matplotlib figure and axes
fig, ax = plt.subplots()

def update_grid():
    # Create a copy of the dataframe for coloring purposes
    grid_colors = np.zeros((100, 100), dtype=int)  # Use integers for colors
    
    # Dictionary to track item positions
    item_positions = {item: [] for item in selected_items}
    
    # Identify and color the cells
    for workshopID, mods in map_mods.items():
        for mod_data in mods.values():
            if "cells" in mod_data:
                for map_name, cells in mod_data["cells"].items():
                    for x, y in cells:
                        if x < 100 and y < 100:  # Ensure coordinates are within bounds
                            item_name = mod_data.get("Mod name", "Unknown")
                            if item_name in selected_items:
                                item_positions[item_name].append((x, y))
                                if grid_colors[x, y] == 0:
                                    grid_colors[x, y] = 1  # Set to green
                                else:
                                    grid_colors[x, y] = 2  # Set to red
    
    # Check for conflicts and mark conflicting items in red
    incompatible_items = set()
    for item, positions in item_positions.items():
        for other_item, other_positions in item_positions.items():
            if item != other_item and set(positions).intersection(other_positions):
                incompatible_items.add(item)
                incompatible_items.add(other_item)
    
    # Update the list colors
    for item in unique_items:
        item_label = item_labels[item]
        item_label.config(fg='red' if item in incompatible_items else 'black')
    
    # Update the grid visualization
    cmap = ListedColormap(['white', 'green', 'red'])
    
    # Clear previous plot
    ax.clear()
    
    # Determine the size of the grid based on cell positions
    if item_positions:
        all_positions = np.concatenate(list(item_positions.values()), axis=0)
        max_x = max([x for x, y in all_positions] + [0])
        max_y = max([y for x, y in all_positions] + [0])
        fig.set_size_inches(max(max_y / 10, 10), max(max_x / 10, 10))  # Adjust the factor and set a minimum size

    im = ax.imshow(grid_colors, cmap=cmap, vmin=0, vmax=2)
    plt.title("Map Grid")
    
    # Add a grid to the plot
    ax.grid(True, which='both', color='black', linewidth=0.5)
    ax.set_xticks(np.arange(-0.5, 100, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 100, 1), minor=True)
    
    # Update the canvas with new plot
    plt.draw()
    plt.pause(0.001)

def on_item_check(item):
    if item in selected_items:
        selected_items.remove(item)
    else:
        selected_items.append(item)
    update_grid()

root.mainloop()
