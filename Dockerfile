# เลือก Base Image เป็น Python เวอร์ชันที่คุณใช้
FROM python:3.9

# ตั้งค่า Working directory
WORKDIR /app

# ติดตั้ง dependencies ที่จำเป็น
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ project เข้าไปใน container
COPY . /app/

# รันคำสั่งที่จะเริ่ม Django server เมื่อ container ทำงาน
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]