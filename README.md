# Streamlit Auto-Labeling & YOLOv8 Training Pipeline

This repository contains a complete pipeline for automatically labeling images using the Autodistill library, training a YOLOv8 model, and delivering the trained model to the user. The entire process is containerized using Docker, with a user-friendly interface built using Streamlit and FastAPI for managing image uploads and handling the workflow.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Setup](#setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Configure Environment Variables](#2-configure-environment-variables)
  - [3. Build the Docker Containers](#3-build-the-docker-containers)
  - [4. Run the Application](#4-run-the-application)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project automates the workflow of uploading a folder of images, auto-labeling them, training a YOLOv8 model, and delivering the trained model file to the user. It uses MinIO for storage, Autodistill for auto-labeling, and YOLOv8 for training.

## Features

- **Streamlit Interface**: A user-friendly interface for uploading image folders.
- **FastAPI Backend**: Handles the uploading process and communicates with the MinIO storage.
- **MinIO Storage**: Secure storage solution for uploaded images and processed data.
- **Autodistill Integration**: Automatically labels the uploaded images.
- **YOLOv8 Training**: Trains a YOLOv8 model on the labeled images.
- **Dockerized Deployment**: The entire application is containerized for easy deployment.

## Architecture

1. **Image Upload**: Users upload a folder of images via the Streamlit interface.
2. **Storage**: The folder is uploaded to MinIO storage via FastAPI.
3. **Auto-Labeling**: The images are auto-labeled using the Autodistill library.
4. **Training**: A YOLOv8 model is trained using the labeled data.
5. **Model Delivery**: The trained model is provided to the user.

## Requirements

- Docker
- Docker Compose

## Setup

### 1. Clone the Repository


$ git clone https://github.com/TarikYil/streamlit_auto_labelling.git

$ cd streamlit_auto_labelling/fastapi


### 2. Build the Docker Containers


$ docker-compose build

### 3. Run the Application


$ docker-compose up

### **The application will be available at**:

1. **Streamlit**: http://localhost:8502
2. **FastAPI**: http://localhost:8001
3. **MinIO Console**: http://localhost:9006

### Usage

1. **Upload Images**: Use the Streamlit interface to upload a folder containing images.
1. **Auto-Labeling**: The application will automatically label the images.
1. **Training**: YOLOv8 will be trained on the labeled images.
1. **Download the Model**: Once training is complete, download the trained model from the interface.

## Customization

**MinIO Configuration**

You can customize the MinIO configuration (e.g., access keys, secret keys) in the .env file.

**Training Parameters**

Training parameters for YOLOv8 can be adjusted in the yolov8_config.yaml file or directly within the training script.

**Contributing**

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.