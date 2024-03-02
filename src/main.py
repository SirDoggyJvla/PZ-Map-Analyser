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

# List the contents of the new directory
print("Contents of the new directory:")

# /workshopID
for workshopID in os.listdir():
    wworkshopID = 3166609443
    
    path_workshopID = original_path + "/" + workshopID + "/mods"
    os.chdir(path_workshopID)
    
    # /modFolderName
    for modFolderName in os.listdir():
        found = False
        
        path_modFolderName = path_workshopID + "/" + modFolderName
        os.chdir(path_modFolderName)
        
        # check exists /media
        for media in os.listdir():
            if media == "media":
                found = True
        if not found:
            continue
            path_media = path_modFolderName + "/" + media
            print("media found")
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        