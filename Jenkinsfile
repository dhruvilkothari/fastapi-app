pipeline {
    agent {
        label 'fastapi-ci'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements-dev.txt
                    .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    env.IMAGE_TAG = sh(
                        script: 'git rev-parse --short=12 HEAD',
                        returnStdout: true
                    ).trim()

                    sh '''
                        docker build -t fastapi-devops:$IMAGE_TAG .
                    '''
                }
            }
        }
        stage('Push Docker Image') {
    steps {
        sh '''
            docker tag fastapi-devops:$IMAGE_TAG local-registry:5000/fastapi-devops:$IMAGE_TAG
            docker push local-registry:5000/fastapi-devops:$IMAGE_TAG
        '''
    }
}

        stage('Verify Docker Image') {
            steps {
                sh '''
                    docker image inspect fastapi-devops:$IMAGE_TAG
                '''
            }
        }
    }

    post {
        success {
            echo 'FastAPI CI pipeline passed!'
        }
        failure {
            echo 'FastAPI CI pipeline failed.'
        }
    }
}