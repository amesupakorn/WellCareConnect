# เลือก Base Image เป็น Python เวอร์ชันที่คุณใช้
FROM python:3.9-slim

# ตั้งค่า Working directory
WORKDIR /app

# คัดลอกไฟล์ requirements.txt และติดตั้ง dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดเข้าไปใน container
COPY . /app/

# เข้าไปในโฟลเดอร์ที่มี manage.py
WORKDIR /app/wellcare

# รัน Gunicorn โดย bind กับตัวแปร $PORT ที่ Cloud Run จะสุ่มให้
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 wellcare.wsgi:application