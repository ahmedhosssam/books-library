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
                            sudo aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                            sudo aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                            sudo aws configure set region eu-central-1
                        '''

                        // sudo aws eks update-kubeconfig --name team4 --kubeconfig /home/ahmed/.kube/config
                        // Update kubeconfig
                        sh '''
                            sudo aws eks --region eu-central-1 update-kubeconfig --name team4
                            sudo kubectl config set-context arn:aws:eks:eu-central-1:637423483309:cluster/team4
                        '''

                        // Deploy to EKS
                        sh '''
                            sudo kubectl --kubeconfig $KUBECONFIG_PATH set image deployment/flask-app-deployment flask-app=$DOCKER_IMAGE:1722344581
                        '''
                    }
                }
            }
        }
    }
}

