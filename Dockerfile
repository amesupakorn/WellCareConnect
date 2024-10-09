# เลือก Base Image เป็น Python เวอร์ชันที่คุณใช้
FROM python:3.9

# ตั้งค่า Working directory
WORKDIR /app

# คัดลอกไฟล์ requirements.txt และติดตั้ง dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# คัดลอกโค้ดทั้งหมดเข้าไปใน container
COPY . /app/

# รัน Django server หรือ Gunicorn
CMD ["python3", "/wellcare/manage.py", "runserver", "0.0.0.0:8000"]