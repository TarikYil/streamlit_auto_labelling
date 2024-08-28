import os
import shutil
from minio.error import S3Error
from dotenv import load_dotenv
from minio_handler import *
from autodistill.detection import CaptionOntology
from autodistill_grounded_sam import GroundedSAM
import datetime
import torch
load_dotenv()

# def ensure_directory(bucket_name, directory_name):
#     s3_client = create_minio_client()
#     result = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=directory_name)

#     if 'Contents' in result:
#         # Dizinde içerik varsa, hepsini silin
#         for item in result['Contents']:
#             s3_client.delete_object(Bucket=bucket_name, Key=item['Key'])
#         print(f"Directory {directory_name} exists and was cleared.")
#     else:
#         print(f"Directory {directory_name} does not exist or is empty. No action needed.")

# def generate_unique_filename(directory_name, original_filename):
#     name, ext = os.path.splitext(original_filename)
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     return f"{directory_name}/{name}_{timestamp}{ext}"
def process_images_from_folder(minio_client, bucket_name: str, minio_folder: str, local_folder: str):
    # Yerel klasörü oluştur, yoksa
    os.makedirs(local_folder, exist_ok=True)

    # Mevcut dosyaları temizle
    if os.listdir(local_folder):
        for file in os.listdir(local_folder):
            file_path = os.path.join(local_folder, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Dosyayı veya sembolik bağlantıyı sil
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Klasörü ve içeriğini sil
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    try:
        # MinIO'daki tüm nesneleri listele
        response = minio_client.list_objects_v2(Bucket=bucket_name, Prefix=minio_folder)

        if 'Contents' in response:
            for obj in response['Contents']:
                object_name = obj['Key']  # dict tipinde Key kullanılır
                local_file_path = os.path.join(local_folder, os.path.basename(object_name))
                
                try:
                    minio_client.download_file(bucket_name, object_name, local_file_path)
                    print(f"Downloaded {object_name} to {local_file_path}")
                except ClientError as e:
                    print(f"Error downloading {object_name}: {e}")
        else:
            print("No objects found in the specified folder.")
    except Exception as e:
        print(f"Error listing objects: {e}")

def create_auto_label(input_path, output_path):
    
    ontology = CaptionOntology({
        "human": "human"
    })
    # Temel Model oluşturma
    # Local path içindeki dosyaları kontrol et ve varsa sil
    if os.path.exists(output_path) and os.listdir(output_path):
        shutil.rmtree(output_path)  # Klasörü ve içindekileri sil
        os.makedirs(output_path)  # Klasörü tekrar oluştur
        print(f"Cleared existing files in '{output_path}'")

    base_model = GroundedSAM(ontology=ontology)
    base_model.label(
        input_folder=input_path,
        extension=".png",
        output_folder=output_path)