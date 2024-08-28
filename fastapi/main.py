from fastapi import FastAPI, File, UploadFile, HTTPException
import io
from minio_handler import *
from helper import *
from autodistill_yolov8 import YOLOv8
from fastapi.responses import FileResponse, JSONResponse
import uuid
from fastapi.middleware.cors import CORSMiddleware
import base64
from typing import List
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# the minio create from after application start
# @app.on_event("startup")
# async def startup_event():
#     create_bucket()

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    bucket_name = os.getenv("MINIO_BUCKET_NAME")
    create_bucket(bucket_name)

    for file in files:
        try:
            print(f"Received file: {file.filename}")
            file_content = await file.read()
            print(f"File size: {len(file_content)} bytes")
            
            # Benzersiz dosya adı oluştur
            unique_filename = f"{uuid.uuid4()}"
            image_path = f"/user/project/image{unique_filename}.png"
            
            # Dosyayı MinIO'ya kaydet
            save_image_to_minio(file, image_path)
            
            print(f"Successfully uploaded {file.filename} as {unique_filename}")

        except Exception as e:
            print(f"Failed to process file {file.filename}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Failed to process file {file.filename}: {str(e)}")
    
    return {"message": "Files successfully processed and uploaded to MinIO"}




@app.get("/automatic_label")  # 6
async def automatic_label(): 
    
    local_input_path = './image/'
    output_path = './lab/'  
    bucket_name = os.getenv("MINIO_BUCKET_NAME")
    s3_client = create_bucket(bucket_name)
    minio_folder = "user/project/"
    # MinIO'dan dosyaları indir
    process_images_from_folder(s3_client,bucket_name,minio_folder,local_input_path)

    # prefix = f"images/user_{user_id}/project_{project_name}/label/"

    try:
        print("successs")
        create_auto_label(local_input_path, output_path)
        return JSONResponse(status_code=200, content={"success":True, "message": "Automatic labeling completed."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success":False, "message": f"Failed to label images. Error: {str(e)}"})

@app.get("/create_model_image")  # 7
async def create_model_image():
    # bucket_name = os.getenv("MINIO_BUCKET_NAME")
    # s3_client = create_bucket(bucket_name)
    

    print("DENEME CONTROL")



    target_model = YOLOv8("yolov8n.pt")
    target_model.train("D:\\streamlit_autodistill\\fastapi\\lab\\data.yaml", epochs=2)
    # destination_dir = f"./best_models/"
    # if not os.path.exists(destination_dir):
    #     os.makedirs(destination_dir)

    # source_path = "./runs/detect/train/weights/best.pt"
    # destination_path = f"./best_models/best_model.pt"
    # shutil.copy(source_path, destination_path)


    return JSONResponse(status_code=200, content={
        "success": True,
        "message": "Model created successfully.",
    })