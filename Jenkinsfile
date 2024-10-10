pipeline {
    agent any

    environment {
        // กำหนด environment variables ที่จำเป็น
        DOCKER_IMAGE       = '0900803496mm/wellcare:latest'
        DOCKER_CREDENTIALS = credentials('dockerhub')

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

         stage('Build Docker Image') {
            steps {
     
                    sh 'echo "Running in $(pwd)"'
                    sh 'echo start build the Docker image = $DOCKER_IMAGE'
                    sh 'docker build -t $DOCKER_IMAGE .'

                  
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    
                    // Login to Docker Hub
                    sh 'echo $DOCKER_CREDENTIALS_PSW | docker login --username $DOCKER_CREDENTIALS_USR --password-stdin'
                    // Push the image
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }
        stage('Clear Docker Components') {
                steps {
                    script {
                        // Remove Docker images and containers
                        sh 'docker stop $(docker ps -a -q) || true'  
                        sh  'docker rm $(docker ps -a -q) || true' 
                        sh  'docker rmi $(docker images -q) || true'
                        sh 'docker system prune -af'
                    }
                }
            }

        stage('Deploy') {
            steps {
                script {
                    // Pull the Docker image from Docker Hub
                    sh 'docker pull $DOCKER_IMAGE'
                    sh 'docker stop wellcareconnect || true'
                    sh 'docker rm wellcareconnect || true'
                    sh 'docker-compose down && docker-compose up -d'
                }
            }
        }

       
    }
}