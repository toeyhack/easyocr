# Easyocr run on docker GPU
1. git clone all to folder
2. docker build -t easyocr-gpu-api .
3. sudo docker run --gpus all -d -p 7861:7860 --name easyocr_gpu_service easyocr-gpu-api
# Remove when change 
1. sudo docker rm -f easyocr_gpu_service
2. docker build -t easyocr-gpu-api .
3. sudo docker run --gpus all -d -p 7861:7860 --name easyocr_gpu_service easyocr-gpu-api
# Testing with curl
 1. กำหนด Path ของไฟล์รูปภาพ JPG/PNG
FILE_PATH="./my_photo.jpg" 

2. กำหนด MIME Type ให้เหมาะสม
#    - สำหรับ JPG: "image/jpeg"
#    - สำหรับ PNG: "image/png"
#    - MIME_TYPE="application/pdf"
MIME_TYPE="image/jpeg" 

3. รันคำสั่ง cURL เพื่อส่ง Base64 และรับผลลัพธ์
curl -X POST http://localhost:7861/run/predict \
     -H "Content-Type: application/json" \
     -d "{\"fn_index\":0,\"data\":[\"data:${MIME_TYPE};base64,$(base64 -w 0 ${FILE_PATH})\"], \"session_hash\":\"\"}"
