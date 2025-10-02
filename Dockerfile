# �� NVIDIA CUDA Base Image (������ҧ�� CUDA 11.8)
# Image ������ CUDA ��� CuDNN libraries ������
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# �Դ��� Python ��� pip (������Ҿ�����Ѻ CUDA base image)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip \
    # �Դ��� system libs ����Ѻ pdf2image ��� image processing
    poppler-utils \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender1 && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/python3 /usr/bin/python

# ��˹� Working Directory
WORKDIR /app

# �Ѵ�͡ requirements.txt ��еԴ��� Python Dependencies
# ������ѹ���Ҿ�Ǵ���� CUDA, PyTorch/EasyOCR ���� GPU ���ѵ��ѵ�
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# �Ѵ�͡����ͻ���पѹ
COPY app.py .

# �Դ����
EXPOSE 7860

# ���������Ѻ�ѹ�ͻ���पѹ
CMD ["python", "app.py"]