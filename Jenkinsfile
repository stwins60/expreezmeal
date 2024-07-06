pipeline {

    agent any

    environment {
        IMAGE_TAG = "v.0.${env.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('5f8b634a-148a-4067-b996-07b4b3276fba')
        DOCKERHUB_USERNAME = 'idrisniyi94'
        DEPLOYMENT_NAME = 'expreezmeal'
        DEV_IMAGE_NAME = "${DOCKERHUB_USERNAME}/${DEPLOYMENT_NAME}-dev:${IMAGE_TAG}"
        PROD_IMAGE_NAME = "${DOCKERHUB_USERNAME}/${DEPLOYMENT_NAME}-prod:${IMAGE_TAG}"
        BRANCH_NAME = "${GIT_BRANCH.split('/')[1]}"
    }

    stages {
        stage("Clean Workspace") {
            steps {
                cleanWs()
            }
        }
        stage("Checkout") {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/dev'], [name: '*/prod']], userRemoteConfigs: [[url: 'https://github.com/stwins60/expreezmeal.git']]])
            }
        }
        stage("Pytest") {
            steps {
                script {
                    sh "pip install -r requirements.txt --no-cache-dir"
                    sh "python -m pytest app-test.py"
                }
            }
        }
        stage("Build Docker Image") {
            steps {
                script {
                    if (BRANCH_NAME == 'dev') {
                        echo "Building Dev Image"
                        sh "docker build -t $DEV_IMAGE_NAME -f Dockerfile.dev ."
                    }
                    else if (BRANCH_NAME == 'prod') {
                        echo "Building Prod Image"
                        sh "docker build -t $PROD_IMAGE_NAME -f Dockerfile.prod ."
                    }
                }
            }
        }
    }
}