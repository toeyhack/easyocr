import easyocr
import gradio as gr
from PIL import Image
from pdf2image import convert_from_path
import os
import numpy as np 

# กำหนดภาษาที่ต้องการใช้ในการอ่านข้อความ (ตัวอย่าง: ไทยและอังกฤษ)
reader = easyocr.Reader(['th', 'en'])

def perform_ocr(file_path):
    """
    ฟังก์ชันหลักในการประมวลผล OCR สำหรับไฟล์ที่อัปโหลด (JPG/PNG หรือ PDF)
    """
    if file_path is None:
        return "❌ กรุณาอัปโหลดไฟล์"

    file_extension = os.path.splitext(file_path)[1].lower()
    all_text = []

    try:
        if file_extension in ['.jpg', '.jpeg', '.png']:
            # จัดการไฟล์รูปภาพ: โหลดไฟล์และแปลงเป็น NumPy Array
            img = Image.open(file_path) # <--- โหลดไฟล์
            np_image = np.array(img)   # <--- แปลงเป็น NumPy Array
            result = reader.readtext(np_image, detail=0)
            all_text.extend(result)

        elif file_extension == '.pdf':
            # จัดการไฟล์ PDF: แปลงแต่ละหน้าเป็น NumPy Array
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                # แปลง PIL Image เป็น NumPy Array ก่อนส่งให้ EasyOCR
                np_image = np.array(image)
                result = reader.readtext(np_image, detail=0) 
                
                # เพิ่มข้อความที่สกัดได้ พร้อมระบุหน้า
                all_text.append(f"\n--- หน้าที่ {i+1} ---\n")
                all_text.extend(result)
                
        else:
            return f"❌ ไม่รองรับประเภทไฟล์: {file_extension}. รองรับเฉพาะ JPG, PNG, และ PDF"

    except Exception as e:
        return f"❌ เกิดข้อผิดพลาดในระหว่างทำ OCR: {e}"

    # รวมผลลัพธ์ทั้งหมด
    return "\n".join(all_text)


# ตั้งค่า Gradio Interface
iface = gr.Interface(
    fn=perform_ocr,
    inputs=gr.File(type="filepath", label="อัปโหลดไฟล์ PDF หรือ JPG/PNG file"),
    outputs=gr.Textbox(label="Extracted Text", lines=20),
    title="EasyOCR Docker Service (Gradio Testing Interface)",
    description="อัปโหลดไฟล์ **PDF** หรือ **รูปภาพ (.jpg, .png)** เพื่อดึงข้อความด้วย EasyOCR (รองรับภาษาไทยและอังกฤษ)",
    allow_flagging='never'
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
