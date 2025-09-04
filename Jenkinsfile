pipeline {
    agent any
    
    environment {
        TMDB_API_KEY = credentials('tmdb-api-key')
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
        stage('OWASP dependency check') {
            steps {
                dependencyCheck additionalArguments: "--scan ./", odcInstallation: 'owasp'
                dependencyCheckPublisher pattern: '**/dependency-report.xml'
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Trivy File scan') {
            steps {
                sh 'trivy fs --exit-code 1 --format table -o trivy-fs-report.html --severity HIGH,CRITICAL --no-progress . || true'
            }
        }
        stage('Locally Build the Docker-image') {
            steps {
                sh 'docker build -t netflix-clone .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 5000:5000 -e TMDB_API_KEY=$TMDB_API_KEY --name netflix-app netflix-clone'
            }
        }
    }
}