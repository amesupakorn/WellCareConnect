pipeline {
    agent any

    environment {
        // กำหนด environment variables ที่จำเป็น
        GOOGLE_APPLICATION_CREDENTIALS = './credentials/credentials.json'
    }

     stages {
        stage('Checkout Code') {
            steps {
                // ดึงโค้ดจาก GitHub
                 git url: 'https://github.com/amesupakorn/WellCareConnect.git',
                    branch: 'main',
                    credentialsId: 'github_token'  // ใส่ credentialsId ที่คุณเพิ่มใน Jenkins
       
            }
        }

        stage('Set Up Virtual Environment') {
            steps {
                script {
                    // สร้าง virtual environment และติดตั้ง dependencies
                    sh '''
                    python3 -m venv myvenv
                    source myvenv/bin/activate
                    pip install -r requirements.txt
                    '''
                    
                }
            }
        }

        stage('Migrate Database') {
            steps {
                script {
                    // รัน Django migrations เพื่ออัปเดตฐานข้อมูล
                    sh '''
                    source myvenv/bin/activate
                    python manage.py migrate
                    '''
                }
            }
        }

        stage('Collect Static Files') {
            steps {
                script {
                    // รวบรวมไฟล์ static ของ Django
                    sh '''
                    source myvenv/bin/activate
                    python manage.py collectstatic --noinput
                    '''
                }
            }
        }

        stage('Start Django Server') {
            steps {
                script {
                    // รัน Django development server หรือ Gunicorn
                    sh '''
                    source myvenv/bin/activate
                    python manage.py runserver 0.0.0.0:8000 &
                    '''
                }
            }
        }
    }
}
