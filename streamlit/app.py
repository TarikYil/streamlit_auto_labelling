import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# API URL'leri
FASTAPI_UPLOAD_URL = "http://localhost:8000/upload"
FASTAPI_LABEL_URL = "http://localhost:8000/automatic_label"
FASTAPI__CREATE_MODEL_URL = "http://localhost:8000/create_model_image"
# Birden fazla dosya seçimi için file_uploader
uploaded_files = st.file_uploader("Choose images to upload...", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

# Dosyaları yüklemek için bir buton
if uploaded_files:
    if st.button("Upload"):
        # 'files' parametresi form-data olarak dosyaları içerir
        files = [('files', (file.name, file.getvalue(), file.type)) for file in uploaded_files]
        response = requests.post(FASTAPI_UPLOAD_URL, files=files)

        if response.status_code == 200:
            st.success("Files successfully uploaded!")
        else:
            st.error("Failed to upload files")
            st.write(response.text)

# Görselleri indirmek için "Get Images" butonu
if st.button("Get Images"):
    # GET isteği gönder
    response = requests.get(FASTAPI_LABEL_URL)

    if response.status_code == 200:
        st.success("Images successfully downloaded!")
        st.write("Images have been processed and downloaded.")
    else:
        st.error("Failed to download images")
        st.write(response.text)

# "Get" butonu
if st.button("Get"):
    
    # FastAPI'ye POST isteği gönder
    response = requests.get(FASTAPI__CREATE_MODEL_URL)
    
    if response.status_code == 200:
        st.success("Model created and uploaded successfully!")
        st.json(response.json())  # JSON yanıtını göster
    else:
        st.error("Failed to create and upload model")
        st.write(response.text)
   