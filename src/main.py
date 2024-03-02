# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 23:53:01 2024

@author: SirDoggyJvla
"""
# Sets main directory
if __name__=='__main__':
    import os
    
    path = __file__
    path = path.replace("\\","/")
    file_name = os.path.basename(path)
    path = path.replace("/" + file_name,"")
    path_main = path.replace("/src","")
    os.chdir(path)



original_path = "C:/Program Files (x86)/Steam/steamapps/workshop/content/108600"

# Change directory
target_directory = original_path
#target_directory = 
os.chdir(target_directory)

# path to string format
path_to = "{}/{}"

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
            os.chdir(store_mod["paths"][maps])
            for cells in os.listdir():
                if "world_" in cells:
                    parts = cells.split("_")
                    x = parts[1]
                    y = parts[2].split(".")[0]
                    if modFolderName not in store_mod:
                        store_mod[modFolderName] = {}
                    if "cells" not in store_mod[modFolderName]:
                        store_mod[modFolderName]["cells"] = {}
                    if maps not in store_mod[modFolderName]["cells"]:
                        store_mod[modFolderName]["cells"][maps] = []
                    
                    store_mod[modFolderName]["cells"][maps].append([x,y])
        
        # store info and cells if exists
        if modFolderName in store_mod:
            store_mod[modFolderName]["path"] = main_path
            os.chdir(store_mod[modFolderName]["path"])
            
            # Open the mod.info file
            with open('mod.info', 'r') as file:
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
                            print("Name:", name)
            
            store_mod[modFolderName]["Mod name"] = name
            print(str(modFolderName)+": \t append list of cells from map mod")
            map_mods[workshopID] = store_mod
    
        
        
        
#os.chdir(path)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        