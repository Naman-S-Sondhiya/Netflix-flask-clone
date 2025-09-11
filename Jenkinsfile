pipeline {
    agent any
    parameters {
        booleanParam(name: 'LOCAL_DEPLOYMENT', defaultValue: true, description: 'Deploys Docker image locally')
        booleanParam(name: 'PUSH_TO_DOCKERHUB', defaultValue: false, description: 'Push Docker image to Docker Hub')
    }
    tools {
        jdk 'jdk17'
    }
    environment {
        SONAR_EV = tool 'Sonar'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Clone Code from Github') {
            steps {
                git url:"https://github.com/Naman-S-Sondhiya/Netflix-flask-clone.git", branch: "master_3"
            }
        }
        stage('GitLeaks Scan') {
            steps {
                sh 'gitleaks detect --source . -r gitleaks-report.json -f json'
            }
        }
        stage('SonarQube Code Analysis') {
            steps {
                withSonarQubeEnv('Sonar') {
                    sh "${SONAR_EV}/bin/sonar-scanner -Dsonar.projectName=netflix -Dsonar.projectKey=netflix"
                }
            }
        }
        stage('OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: "--scan ./ --format XML", odcInstallation: 'owasp'
                sh 'ls -lhR . | grep dependency-check || true'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Trivy File Scan') {
            steps {
                sh 'trivy fs . > trivyfs.txt'
            }
        }
        stage('Build Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'tmdb-api-key', variable: 'TMDB_API_KEY')]) {
                    sh 'docker build --build-arg TMDB_API_KEY=$TMDB_API_KEY -t netflix-clone .'
                }
            }
        }
        stage('Trivy Image Scan') {
            steps {
                sh 'trivy image netflix-clone > trivyimage.txt'
            }
        }
        stage('Deploy To Container') {
            when {
                expression { params.LOCAL_DEPLOYMENT }
            }
            steps {
                sh 'docker stop netflix-app || true'
                sh 'docker rm netflix-app || true'
                sh 'docker run -d -p 5000:5000 --name netflix-app netflix-clone'
            }
        }
        stage('Push to DockerHub') {
            when {
                expression { params.PUSH_TO_DOCKERHUB }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh 'docker tag netflix-clone namanss/netflix-clone:v${BUILD_NUMBER}'
                    sh 'docker tag netflix-clone namanss/netflix-clone:latest'
                    sh 'echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin'
                    sh 'docker push namanss/netflix-clone:v${BUILD_NUMBER}'
                    sh 'docker push namanss/netflix-clone:latest'
                }
            }
        }
    }
    post {
        always {
            emailext (
                subject: "Build ${currentBuild.result}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Status: ${currentBuild.result}\nBuild: ${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}\n\nReports attached: GitLeaks, Trivy scans",
                to: 'ssnaman4@gmail.com',
                attachmentsPattern: 'gitleaks-report.json,trivyfs.txt,trivyimage.txt'
            )
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}