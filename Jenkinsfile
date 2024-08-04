pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'ahmedhosssam/flask-app'
        DOCKER_CREDENTIALS_ID = 'ec6825c0-99e6-4970-a914-0d16ad8cd8e9'
        AWS_CREDENTIALS_ID = 'aws_creeed'
        EKS_CLUSTER_NAME = 'team4'
        KUBECONFIG_PATH = '/home/ahmed/.kube/config'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', credentialsId: 'github-cred', url: 'https://github.com/ahmedhosssam/books-library.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE, '-f Dockerfile .')
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: DOCKER_CREDENTIALS_ID, url: 'https://index.docker.io/v1/']) {
                    script {
                        docker.image(DOCKER_IMAGE).push('1722344581')
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding', 
                    credentialsId: AWS_CREDENTIALS_ID
                ]]) {
                    script {
                        // Configure AWS CLI
                        sh '''
                            aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                            aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                            aws configure set region us-east-1
                        '''

                        // Update kubeconfig
                        sh '''
                            aws eks update-kubeconfig --name $EKS_CLUSTER_NAME --kubeconfig $KUBECONFIG_PATH
                        '''

                        // Deploy to EKS
                        sh '''
                            kubectl --kubeconfig $KUBECONFIG_PATH set image deployment/flask-app-deployment flask-app=$DOCKER_IMAGE:1722344581
                        '''
                    }
                }
            }
        }
    }
}

