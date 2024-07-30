from utils.data_preprocessing import preprocess_dataset

dataset_dir = 'data/LFW/lfw-deepfunneled/lfw-deepfunneled'
preprocessed_images = preprocess_dataset(dataset_dir)
print("Image preprocessing complete!")

