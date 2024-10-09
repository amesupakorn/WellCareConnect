# เลือก Base Image เป็น Python เวอร์ชันที่คุณใช้
FROM python:3.9

# ตั้งค่า Working directory
WORKDIR /app

# คัดลอกไฟล์ requirements.txt และติดตั้ง dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดเข้าไปใน container
COPY . /app/

# รวบรวม static files และ migrate database
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# รันแอปพลิเคชันด้วย Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]