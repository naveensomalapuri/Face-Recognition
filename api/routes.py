from fastapi import APIRouter, File, UploadFile
from api.models import preprocess_dataset
from utils.data_preprocessing import preprocess_image

router = APIRouter()

@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    image_path = f"uploads/{file.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(file.file.read())
    preprocessed_image = preprocess_image(image_path)
    return {"message": "Image uploaded and preprocessed successfully"}

@router.post("/preprocess_dataset")
async def preprocess_dataset_endpoint():
    dataset_dir = 'data/LFW/lfw-deepfunneled/lfw-deepfunneled' 
    preprocessed_images = preprocess_dataset(dataset_dir)
    return {"message": "Dataset preprocessed successfully"}