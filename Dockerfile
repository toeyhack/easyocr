# ใช้ NVIDIA CUDA Base Image (ตัวอย่างเช่น CUDA 11.8)
# Image นี้จะมี CUDA และ CuDNN libraries ที่จำเป็น
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# ติดตั้ง Python และ pip (ไม่ได้มาพร้อมกับ CUDA base image)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip \
    # ติดตั้ง system libs สำหรับ pdf2image และ image processing
    poppler-utils \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/python3 /usr/bin/python

# กำหนด Working Directory
WORKDIR /app

# คัดลอก requirements.txt และติดตั้ง Python Dependencies
# เมื่อรันในสภาพแวดล้อม CUDA, PyTorch/EasyOCR จะใช้ GPU โดยอัตโนมัติ
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์แอปพลิเคชัน
COPY app.py .

# เปิดพอร์ต
EXPOSE 7860

# คำสั่งสำหรับรันแอปพลิเคชัน
CMD ["python", "app.py"]