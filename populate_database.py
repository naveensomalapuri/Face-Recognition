import cv2
import numpy as np
import pandas as pd
from utils.data_preprocessing import connect_to_db, insert_data, create_table
import os
from utils.data_preprocessing import split_data, images, labels

# Define the directory paths
image_dir = 'data/LFW/lfw-deepfunneled/lfw-deepfunneled'
label_file = 'data/LFW/people.csv'

# Load the label file
labels_df = pd.read_csv(label_file)

# Iterate through each folder in the image directory
for folder in os.listdir(image_dir):
    # Get the label for the current folder

    label = labels_df.loc[labels_df['name'] == folder, 'name'].values[0]
    
    # Iterate through each image in the folder
    for image_file in os.listdir(os.path.join(image_dir, folder)):
        # Load the image
        image_path = os.path.join(image_dir, folder, image_file)
        image = cv2.imread(image_path)
        
        # Preprocess the image (if necessary)
        # image = preprocess_image(image)
        
        # Insert the image and label into the database
        conn = connect_to_db()
        create_table(conn)
        insert_data(conn, image, label)
        conn.close()


train_images, test_images, train_labels, test_labels = split_data(images, labels)