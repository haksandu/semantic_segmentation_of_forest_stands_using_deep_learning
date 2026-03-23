import os
import glob
import pandas as pd
from sklearn.model_selection import train_test_split
import csv
import shutil

# Set directory to some directory containing all 809 files
os.chdir("./data/img_tiles/images")


# Create list of all .tif files in directory
tif_files = []
for file in glob.glob("*.tif"):
    tif_files.append(file)

# Check length
len(tif_files) # 809 image tiles in total

#%% Create list over usable images

# Define path to document containing usableness
# Images were visually inspected for dissagreement between the RGBI and CHM
# Image tiles with large deviations were excluded
io = "./data/usable_tiles_MEV.xlsx"

# Read data
images = pd.read_excel(io, header=0, usecols="A,H")

# Create empty list
usable_images = []

# Iterate over rows in the DataFrame and append to list if 'Usable' == 1
for index, row in images.iterrows():
    # Check if usableness is 0
    if row['Usable'] == 1:
        # Extract the corresponding image filename
        image_filename = f"tile_{row['Image']}.tif"
        # Check if the image filename exists in the original list
        if image_filename in tif_files:
            usable_images.append(image_filename)

del(io, image_filename, file, images, index, row)


#%% Splitting the data


# Split data into training and test sets
temp_instances, testData = train_test_split(usable_images, test_size=0.15, random_state=42)

# Further split temp set into training and validation sets
trainingData, validationData = train_test_split(temp_instances, test_size=0.1764, random_state=42)

del(temp_instances, tif_files, usable_images)


#%% Write result to file

with open("./data/data_split.csv", 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['TrainingData', 'ValidationData', 'TestData']) # write header
    max_length = max(len(trainingData), len(validationData), len(testData))
    
    for i in range(max_length):
        row = [trainingData[i] if i < len(trainingData) else '',
               validationData[i] if i < len(validationData) else '',
               testData[i] if i < len(testData) else '']
        writer.writerow(row)
    
    


#%% Check for overlapping files

# Convert lists to sets
trainingSet = set(trainingData)
validationSet = set(validationData)
testSet = set(testData)

# Find common files
commonFiles = trainingSet.intersection(validationSet).intersection(testSet)

# Print common files if any
if commonFiles:
    print("Common files between the lists:")
    for file in commonFiles:
        print(file)
else:
    print("There are no common files between the lists.")
    
del(trainingSet, validationSet, testSet, commonFiles)



#%%  Copy images to directory

# Source directory where the images are located
image_source_dir = './data/img_tiles/images'

# Destination directory to where the copies should be pasted
train_destination_dir = './data/training/image_MEV'
val_destination_dir ='./data/validation/image_MEV'
test_destination_dir = './data/test/image_MEV'

for file in trainingData:
    image_source_path = os.path.join(image_source_dir, file)
    image_destination_path = os.path.join(train_destination_dir, file)
    shutil.copy2(image_source_path, image_destination_path)

for file in validationData:
    image_source_path = os.path.join(image_source_dir, file)
    image_destination_path = os.path.join(val_destination_dir, file)
    shutil.copy2(image_source_path, image_destination_path)

for file in testData:
    image_source_path = os.path.join(image_source_dir, file)
    image_destination_path = os.path.join(test_destination_dir, file)
    shutil.copy2(image_source_path, image_destination_path)



#%% Copy masks to directory
mask_source_dir = './data/img_tiles/mask'

# Destination directory to where the copies should be pasted
train_destination_dir = './data/training/mask_MEV'
val_destination_dir ='./data/validation/mask_MEV'
test_destination_dir = './data/test/mask_MEV'

for file in trainingData:
    mask_source_path = os.path.join(mask_source_dir, file)
    mask_destination_path = os.path.join(train_destination_dir, file)
    shutil.copy2(mask_source_path, mask_destination_path)

for file in validationData:
    mask_source_path = os.path.join(mask_source_dir, file)
    mask_destination_path = os.path.join(val_destination_dir, file)
    shutil.copy2(mask_source_path, mask_destination_path)

for file in testData:
    mask_source_path = os.path.join(mask_source_dir, file)
    mask_destination_path = os.path.join(test_destination_dir, file)
    shutil.copy2(mask_source_path, mask_destination_path)
