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
            docker tag fastapi-devops:$IMAGE_TAG localhost:5001/fastapi-devops:$IMAGE_TAG
            docker push localhost:5001/fastapi-devops:$IMAGE_TAG
        '''
    }
}
stage('Update GitOps Repository') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: 'github-fastapi-infra',
            usernameVariable: 'GIT_USER',
            passwordVariable: 'GIT_TOKEN'
        )]) {
            sh '''
                set -eu
                set +x

                rm -rf fastapi-infra
                git clone https://github.com/dhruvilkothari/fastapi-infra.git fastapi-infra
                cd fastapi-infra

                git config user.name "Jenkins CI"
                git config user.email "jenkins@localhost"

                sed -i -E "s/^(  tag:).*/\\1 \\"$IMAGE_TAG\\"/" charts/fastapi/values.yaml

                git add charts/fastapi/values.yaml

                if git diff --cached --quiet; then
                    echo "Image tag already up to date"
                    exit 0
                fi

                git commit -m "Deploy FastAPI image $IMAGE_TAG"

                
git -c credential.helper='!f() { echo "username=$GIT_USER"; echo "password=$GIT_TOKEN"; }; f' \
    push https://github.com/dhruvilkothari/fastapi-infra.git HEAD:master

            '''
        }
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