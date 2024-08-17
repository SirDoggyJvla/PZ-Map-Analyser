# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 23:53:01 2024

@author: SirDoggyJvla
"""
# Imports
import os
import numpy as np
import chardet

# Sets main directory
if __name__=='__main__':
    path = __file__
    path = path.replace("\\","/")
    file_name = os.path.basename(path)
    path = path.replace("/" + file_name,"")
    path_main = path.replace("/src","")
    os.chdir(path)



# Create a 70x70 matrix initialized with empty strings
maps_matrix = np.empty((100, 100), dtype='object')

# Fill the matrix with empty strings
maps_matrix.fill('')


# Path to my workshop mods
original_path = "C:/Program Files (x86)/Steam/steamapps/workshop/content/108600"

# Change path to my workshop mods
os.chdir(original_path)

# path_to string format
path_to = "{}/{}"

# link string format
link = "{}\n{}"

# /workshopID
map_mods = {}
for workshopID in os.listdir():
    
    #workshopID = 3166609443 # military checkpoint
    #workshopID = 2800337234 # Trelai 4x4
    
    store_mod = {"paths":{}}
    #map_mods[workshopID] = {"paths":{}}
    #map_mods["paths"]["workshopID"] = original_path + "/" + str(workshopID) + "/mods"
    store_mod["paths"]["workshopID"] = path_to.format(original_path,str(workshopID)+"/mods")
    os.chdir(store_mod["paths"]["workshopID"])
    
    # /modFolderName
    for modFolderName in os.listdir():
        store_mod["paths"][modFolderName] = path_to.format(store_mod["paths"]["workshopID"],modFolderName)
        os.chdir(store_mod["paths"][modFolderName])
        
        main_path = store_mod["paths"][modFolderName]
        
        # check exists /media
        found = False
        for media in os.listdir():
            if media == "media":
                found = True
                
        if not found:
            print(str(modFolderName)+": \t media not found")
            continue
        
        store_mod["paths"]["media"] = path_to.format(store_mod["paths"][modFolderName],"media")
        os.chdir(store_mod["paths"]["media"])
        
        # check exists /maps
        found = False
        for maps in os.listdir():
            if maps == "maps":
                found = True
                
        if not found:
            print(str(modFolderName)+": \t maps not found")
            continue
        
        store_mod["paths"]["maps"] = path_to.format(store_mod["paths"]["media"],"maps")
        os.chdir(store_mod["paths"]["maps"])
        
        # goes through every maps in this workshopID
        for maps in os.listdir():
            
            #skip for that bitch ass mod that decided to have that file in his map folder
            if maps == "mod.info.info":
                continue
            
            # iterate through every maps and get the cells if present
            store_mod["paths"][maps] = path_to.format(store_mod["paths"]["maps"],maps)
            
            # Skip if it's a file, not a directory
            if not os.path.isdir(store_mod["paths"][maps]):
                continue
            
            os.chdir(store_mod["paths"][maps])
            
            # Verifies it's a "Muldraugh, KY" map
            good = False
            for cells in os.listdir():
                if cells != "map.info":
                    continue
                print(workshopID)
                
                # Exceptions
                if workshopID == "2914532881" or workshopID == "3109572404":
                    good = False
                    break
                with open('map.info', 'rb') as file:
                    raw_data = file.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']
                    print(encoding)
                # Open the mod.info file and get the name of the mod
                with open('map.info', 'r', encoding=encoding) as file:
                    # Read the file line by line
                    print(file)
                    for line in file:
                        # Split each line based on the '=' character
                        parts = line.strip().split('=')
                        # Check if the split operation produced exactly two parts
                        if len(parts) == 2:
                            key, value = parts
                            # Check if the key is 'name'
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
                    y = parts[1]
                    x = parts[2].split(".")[0]
                    if modFolderName not in store_mod:
                        store_mod[modFolderName] = {}
                    if "cells" not in store_mod[modFolderName]:
                        store_mod[modFolderName]["cells"] = {}
                    if maps not in store_mod[modFolderName]["cells"]:
                        store_mod[modFolderName]["cells"][maps] = []
                    
                    store_mod[modFolderName]["cells"][maps].append([x,y])
                    
                    if path not in store_mod[modFolderName]:
                        store_mod[modFolderName]["path"] = main_path
                    os.chdir(store_mod[modFolderName]["path"])
                    
                    if "Mod name" not in store_mod[modFolderName]:
                        # Open the mod.info file and get the name of the mod
                        with open('mod.info', 'rb') as file:
                            raw_data = file.read()
                            result = chardet.detect(raw_data)
                            encoding = result['encoding']
                            print(encoding)
                        # Open the mod.info file and get the name of the mod
                        with open('mod.info', 'r', encoding=encoding) as file:
                        # with open('mod.info', 'r') as file:
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
                    
                    print(workshopID,name,x,y)
                    string = maps_matrix[int(x),int(y)]
                    if string == "":
                        maps_matrix[int(x),int(y)] = name
                    else:
                        maps_matrix[int(x),int(y)] = string + "\n" + name
                    
                    #maps_matrix[int(x),int(y)] = "test"
        
        # store info and cells if exists
        if modFolderName in store_mod:
            print(str(modFolderName)+": \t append list of cells from map mod")
            map_mods[workshopID] = store_mod
    
        
        
# sets back main directory
os.chdir(path)

# Export into an excel file
import pandas as pd

# Convert numpy array to a pandas DataFrame
df = pd.DataFrame(maps_matrix)

# Write DataFrame to Excel file
df.to_excel('output.xlsx', index=False)  # Change 'output.xlsx' to your desired file name


















  