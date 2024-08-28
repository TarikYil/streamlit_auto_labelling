import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import boto3
from botocore.config import Config
from fastapi import HTTPException
from helper import *
# update .env files
load_dotenv()

# get to .env files for Minio info
MINIO_ENDPOINT= os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY= os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY= os.getenv("MINIO_ROOT_PASSWORD")
MINIO_BUCKET_NAME= os.getenv("MINIO_BUCKET_NAME")

# minio' s launch
def create_minio_client():
    return boto3.client(
        's3',
        endpoint_url="http://localhost:9005/",
        aws_access_key_id="admin",
        aws_secret_access_key="secretpassword"
    )


# minio_client = boto3.client('s3',
#                     endpoint_url="http://minio:9005/",
#                     aws_access_key_id=MINIO_ACCESS_KEY,
#                     aws_secret_access_key=MINIO_SECRET_KEY,
#                     config=Config(signature_version='s3v4'))

# create bucket
def create_bucket(bucket_name):
    s3_client = create_minio_client()
    
    try:
        # Bucket'ın zaten mevcut olup olmadığını kontrol edin
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"----> Bucket '{bucket_name}' already exists. No action needed.")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            # Eğer bucket yoksa, yeni bir bucket oluştur
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"----> Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Error occurred: {e}")
            return {"error": str(e), "code": 500, "message": "Bucket creation failed"}

    return s3_client

# update files to bucket
# def upload_file_to_minio(file_obj, object_name, bucket_name=None):
#     try:
#         bucket_name= "autodistill-bucket"
#         # Dosyayı MinIO'ya yükle
#         minio_client.upload_fileobj(file_obj, bucket_name, object_name)
#         print(f"Uploaded {object_name} to {bucket_name}/{object_name}")
#     except ClientError as e:
#         print(f"Error occurred: {e}")
#         return {"error": str(e), "code": 500, "message": "File upload failed"}
    
#     return {"message": "File uploaded successfully"}

# def save_file_to_minio(directory_name, file_name, file_content):
#     s3_client = create_minio_client()
#     bucket_name = os.getenv("MINIO_BUCKET_NAME")

    

#     try:
#         s3_client.put_object(
#             Bucket=bucket_name,
#             Key=unique_file_name,
#             Body=file_content
#         )
#         print(f"Uploaded file {unique_file_name} to {directory_name}")
#         return f"{bucket_name}/{unique_file_name}"
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'XMinioObjectExistsAsDirectory':
#             print(f"An error occurred: {file_name} exists as a directory. Trying to upload with a different name.")
#             unique_file_name = generate_unique_filename(directory_name, f"new_{file_name}")
#             s3_client.put_object(
#                 Bucket=bucket_name,
#                 Key=unique_file_name,
#                 Body=file_content
#             )
#             print(f"Uploaded file with new name: {unique_file_name} to {directory_name}")
#             return f"{bucket_name}/{unique_file_name}"
#         else:
#             print(f"An error occurred while uploading {unique_file_name} to {directory_name}: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"An error occurred while uploading {unique_file_name} to {directory_name}: {str(e)}")


def save_image_to_minio(image_data, image_path):
    '''Görseli MinIO'ya kaydetme'''
    bucket = os.getenv("MINIO_BUCKET_NAME")

    s3_res = create_minio_client()

    try:
        # UploadFile tipi ise dosyayı doğrudan işle
        if hasattr(image_data, 'file'):
            # Dosya işaretçisini başa al
            image_data.file.seek(0)
            # Dosya içeriğini al
            image_data = image_data.file.read()

        # MinIO'ya dosya yükle
        s3_res.put_object(Bucket=bucket,Key=image_path, Body=image_data)
        print(f"Image '{image_path}' saved to '{bucket}' bucket in MinIO.")
        
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"MinIO error occurred: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading: {str(e)}")
    
# download files from the bucket
# def download_folder_from_minio():
#     bucket_name = "autodistill-bucket"  # Statik bucket adı
#     object_name_prefix = "images/image/"  # Statik object_name dizini
#     local_dir="./image/"
#     try:
#         # MinIO'daki nesneleri listele
#         objects = minio_client.list_objects_v2(Bucket=bucket_name, Prefix=object_name_prefix)
        
#         # Yerel dizinin var olduğundan emin ol
#         os.makedirs(local_dir, exist_ok=True)
        
#         for obj in objects.get('Contents', []):
#             # Nesne adını al ve yerel dosya yolunu hesapla
#             object_name = obj['Key']
#             local_file_path = os.path.join(local_dir, os.path.relpath(object_name, object_name_prefix))
            
#             # Yerel dizini oluştur
#             local_file_dir = os.path.dirname(local_file_path)
#             os.makedirs(local_file_dir, exist_ok=True)
            
#             # MinIO'dan dosyayı indir
#             minio_client.download_file(bucket_name, object_name, local_file_path)
#             print(f"Downloaded {object_name} to {local_file_path}")
    
#     except ClientError as e:
#         print(f"Error occurred: {e}")
#         return {"error": str(e), "code": 500, "message": "Folder download failed"}
    
#     return {"message": "Folder downloaded successfully"}
    
