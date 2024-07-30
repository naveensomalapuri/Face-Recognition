import cv2
import numpy as np
import os
import psycopg2
from sklearn.model_selection import train_test_split

def preprocess_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return None
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Unable to read image - {image_path}")
            return None
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(img_gray, (224, 224))
        img_normalized = img_resized / 255.0
        return img_normalized
    except Exception as e:
        print(f"Error processing image - {image_path}: {str(e)}")
        return None


def preprocess_dataset(dataset_dir):
    preprocessed_images = []
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            image_path = os.path.join(root, file)
            preprocessed_image = preprocess_image(image_path)
            if preprocessed_image is not None:
                preprocessed_images.append(preprocessed_image)
    return preprocessed_images


# Database table creation and connection
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="face_recognition_database",
        user="postgres",
        password="Plnda@999"
    )
    return conn

def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id SERIAL PRIMARY KEY,
            image BYTEA,
            label VARCHAR(255)
        );
    """)
    conn.commit()
    cur.close()

def insert_data(conn, image, label):
    cur = conn.cursor()
    cur.execute("INSERT INTO images (image, label) VALUES (%s, %s)", (psycopg2.Binary(image), label))
    conn.commit()
    cur.close()

# Retrieve data from database fro data split
def retrieve_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT image, label FROM images")
    data = cur.fetchall()
    images = [row[0] for row in data]
    labels = [row[1] for row in data]
    return images, labels

conn = connect_to_db()
images, labels = retrieve_data(conn)


# Data Splitting

def split_data(preprocessed_images, labels):
    train_images, test_images, train_labels, test_labels = train_test_split(
        preprocessed_images, labels, test_size=0.2, random_state=42
    )
    return train_images, test_images, train_labels, test_labels