
#%% IMPORT MULTIPLE IMAGES

###### Library imports

import rasterio
import numpy as np
import os
import tensorflow as tf

###### Define functions

def read_image(image_path):
    with rasterio.open(image_path, 'r') as ds:
        return ds.read()


# Define a custom sorting key function
def get_number(filename):
    return int(filename.split('_')[1].split('.')[0])

    
###### Define main program

def load_images(img_folder):
    """
    The function reads and processes georeferenced RGBI and CHM raster tiles.
    
    The process is as follows:
            1. Create empty list
            2. Load five band raster composite containing (R,G,B,NIR,CHM)
            3. Append to list
            4. Convert to numpy array
    """
    
    img_files = [file for file in os.listdir(img_folder) if file.endswith('.tif')]
    
    sorted_img_files = sorted(img_files, key=get_number)
    
    tiles = [] 
    for filename in sorted_img_files:
        # Extract paths to images
        img_path = os.path.join(img_folder, filename)
        
        # Load images
        image = read_image(img_path)

        # Change order of dimensions
        image = tf.transpose(image, perm=[1, 2, 0])
        
        # Append current tile to list of tiles
        tiles.append(image)
        
    # Convert list of tiles to numpy array
    tiles = np.asarray(tiles)
    
    return tiles

if __name__ == "__main__":
    data = load_images()      

#%%

import rasterio
import os
    
def load_mask(mask_folder):
    """
    Loads mask tiles from a directory or a single .tif file

    If mask_folder is a directory, it load all .tif files withint it
    If mask_folder is a single .tif file, it loads that file alone
    """
    
    tiles = []

    if os.path.isdir(mask_folder):
        # Get all .tif files in the directory
        mask_files = [file for file in os.listdir(mask_folder) if file.endswith('.tif')]
    
    elif os.path.isfile(mask_folder) and mask_folder.endswith('.tif'):
        # Handle a single .tif file
        mask_files = [os.path.basename(mask_folder)]
        mask_folder = os.path.dirname(mask_folder) # Update folder path for correct os.path.join 

    else:
        raise ValueError(f"The provided path '{mask_folder}' is neither a directory nor a valid .tif file")

    # Sort mask files if there are multiple
    sorted_mask_files = sorted(mask_files, key=get_number)
    
    for filename in sorted_mask_files:
        # Extract path to masks
        mask_path = os.path.join(mask_folder, filename)
        
        # Load mask
        tile = read_image(mask_path)

        # Change order of dimensions
        tile = tf.transpose(tile, perm=[1, 2, 0])
        
        # Append current tile to list of tiles
        tiles.append(tile)
    
    # Convert list of tiles to numpy array
    tiles = np.asarray(tiles)
    
    return tiles
    
    
