# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 03:56:53 2024

@author: simon
"""

import os

path = "C:/Program Files (x86)/Steam/steamapps/workshop/content/108600/522891356/mods"
os.chdir(path)
# Open the mod.info file
with open('mod.info', 'r') as file:
    # Read the file line by line
    for line in file:
        # Split each line based on the '=' character
        key, value = line.strip().split('=')
        # Check if the key is 'name'
        if key.strip() == 'name':
            # Print the value associated with 'name'
            print("Name:", value.strip())