pipeline {
    agent any
    
    parameters {
        booleanParam(name: 'LOCAL_DEPLOYMENT', defaultValue: true, description: 'Deploys Docker image locally')
        booleanParam(name: 'PUSH_TO_DOCKERHUB', defaultValue: false, description: 'Push Docker image to Docker Hub')
    }
    environment {
        SONAR_EV = tool 'Sonar'
    }
    
    stages {
        stage('Clone Code from Github') {
            steps {
                git url:"https://github.com/Naman-S-Sondhiya/Netflix-flask-clone.git", branch: "master_1"
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
                dependencyCheck additionalArguments: "--scan ./", odcInstallation: 'owasp'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Trivy File Scan') {
            steps {
                sh 'trivy fs --exit-code 0 --format table -o trivy-fs-report.html --severity HIGH,CRITICAL --no-progress . || true'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t netflix-clone .'
            }
        }
        stage('Deploy Locally') {
            when {
                expression { params.LOCAL_DEPLOYMENT }
            }
            steps {
                withCredentials([string(credentialsId: 'tmdb-api-key', variable: 'TMDB_API_KEY')]) {
                    sh 'docker stop netflix-app || true'
                    sh 'docker rm netflix-app || true'
                    sh 'docker run -d -p 5000:5000 -e TMDB_API_KEY=$TMDB_API_KEY --name netflix-app netflix-clone'
                }
            }
        }
        stage('Push to DockerHub') {
            when {
                expression { params.PUSH_TO_DOCKERHUB }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh 'docker tag netflix-clone namanss/netflix-clone:latest'
                    sh 'echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin'
                    sh 'docker push namanss/netflix-clone:latest'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}