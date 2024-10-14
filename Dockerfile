# เลือก Base Image เป็น Python เวอร์ชันที่คุณใช้
FROM python:3.10

# ตั้งค่า Working directory
WORKDIR /app

RUN pip install --upgrade pip

# อัปเดต pip และ setuptools
RUN pip install --upgrade pip setuptools wheel
# คัดลอกไฟล์ requirements.txt และติดตั้ง dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

# คัดลอกโค้ดทั้งหมดเข้าไปใน container
COPY . /app/

# รัน Django server หรือ Gunicorn
CMD ["python3", "/wellcare/manage.py", "runserver", "0.0.0.0:8000"]