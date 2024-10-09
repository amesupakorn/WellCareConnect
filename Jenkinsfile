pipeline {
    agent any

    environment {
        // กำหนด environment variables ที่จำเป็น
        GOOGLE_APPLICATION_CREDENTIALS = './credentials/credentials.json'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // ดึงโค้ดจาก GitHub repository
                git url: 'https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                // สร้าง Docker image สำหรับโปรเจค Django
                sh 'docker-compose build'
            }
        }

        stage('Run Migrations') {
            steps {
                // รัน Django migrations เพื่ออัปเดต schema ของฐานข้อมูล
                sh 'docker-compose run web python manage.py migrate'
            }
        }

        stage('Run Tests') {
            steps {
                // รัน unit tests ของโปรเจค Django
                sh 'docker-compose run web python manage.py test'
            }
        }

        stage('Run Application') {
            steps {
                // รัน container ของโปรเจค Django พร้อมกับ Cloud SQL Proxy
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        success {
            echo 'Build, Migrate, and Run completed successfully!'
        }
        failure {
            echo 'There was an error in the Jenkins Pipeline.'
        }
    }
}
