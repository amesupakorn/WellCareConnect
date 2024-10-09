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

        stage("Build") {
            steps {
                echo "Building the Docker image"
                sh "docker build -t todo-list-app ."
            }
        }

        stage("Push to Docker Hub") {
            steps {
                echo "Pushing the Docker image to Docker Hub"
                withCredentials([usernamePassword(credentialsId: "dockerHub", passwordVariable: "dockerHubPass", usernameVariable: "dockerHubUser")]) {
                    sh "docker tag todo-list-app ${env.dockerHubUser}/todo-list-app:latest"
                    sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPass}"
                    sh "docker push ${env.dockerHubUser}/todo-list-app:latest"
                }
            }
        }

        stage("Deploy") {
            steps {
                echo "Deploying the container"
                sh "docker-compose down && docker-compose up -d"
            }
        }
    }
}