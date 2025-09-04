# Netflix Web UI Clone - DevSecOps Flask Application

A comprehensive DevSecOps project featuring a Netflix-inspired web application with TMDB API integration, automated security scanning, and a CI/CD pipeline.

![Flask](https://img.shields.io/badge/Flask-3.1.2-green) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-blue) ![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-orange) ![SonarQube](https://img.shields.io/badge/SonarQube-Security-blue) ![Trivy](https://img.shields.io/badge/Trivy-Vulnerability-red)

## 🚀 Phase 1: Local Development Setup

### Prerequisites
- Python 
- TMDB API Key
- Docker (optional, for containerized deployment)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Naman-S-Sondhiya/Netflix-flask-clone.git
cd Netflix-flask-clone
```

### Step 2: Obtain TMDB API Key

1. Visit [TMDB Website](https://www.themoviedb.org/)
2. Create a free account and log in
3. Navigate to Profile → Settings → API
4. Generate a new API key and accept the terms

### Step 3: Run Application Locally with Python

```bash
# Create environment file
echo "TMDB_API_KEY=your_api_key_here" > .env

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the Flask application
python app.py

# Access the application at:
http://localhost:5000
```

### Step 4: Run Application with Docker

```bash
sudo apt-get update
sudo apt-get install docker.io -y
sudo usermod -aG docker $USER

newgrp docker
sudo chmod 777 /var/run/docker.sock

docker build -t netflix-clone .
docker run -d --name netflix-app -p 5000:5000 -e TMDB_API_KEY=your_api_key netflix-clone

# Alternatively, use the pre-built image with your TMDB_API_KEY
docker run -d --name netflix-app -p 5000:5000 -e TMDB_API_KEY=your_api_key namanss/netflix-clone:latest

# Access the application at:
http://localhost:5000
```

## 🔒 Phase 2: Security Implementation

### Install SonarQube

Using the official SonarQube Docker image for security scanning:

```bash
docker run -itd --name sonar -p 9000:9000 sonarqube:lts-community
```

Access SonarQube at: http://localhost:9000  
Default credentials: `admin` / `admin`

### Install Trivy Security Scanner

```bash
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# Scan Docker image
trivy image netflix-clone
```

## 🔄 Phase 3: CI/CD Pipeline Setup

### Install Jenkins

```bash
# Install Java 17
sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version

# Install Jenkins
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

Access Jenkins at: http://localhost:8080  
Get initial password:  
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Required Jenkins Plugins

Install via `Manage Jenkins` → `Plugin Manager`:

- SonarQube Scanner (`sonar`)
- OWASP Dependency-Check (`dependency-check-jenkins-plugin`)
- Docker Pipeline (`docker-workflow`)
- Git (`git`)
- Pipeline (`workflow-aggregator`)
- Credentials Binding (`credentials-binding`)

### Configure Jenkins Tools

Go to `Manage Jenkins` → `Tools`:

#### SonarQube Scanner
- Name: `Sonar` (case sensitive)
- Install automatically: Latest version

#### OWASP Dependency Check
- Name: `owasp` (case sensitive)
- Install automatically: Latest version

### Configure SonarQube Integration

1. `Manage Jenkins` → `System` → `SonarQube servers`
2. Name: `Sonar` (case sensitive)
3. Server URL: `http://localhost:9000`
4. Server authentication token: Create in SonarQube and add as Jenkins credential

Create SonarQube token in SonarQube → Administration → Security → Users → Tokens  
Add token to Jenkins credentials as `Sonar-token`

### Required Jenkins Credentials

Configure in `Manage Jenkins` → `Credentials` → `Global`:

- `tmdb-api-key` (Secret text): Your TMDB API key
- `dockerhub-creds` (Username/Password) - Optional: Docker Hub username and access token
- `Sonar-token` (Secret text): SonarQube authentication token

### Pipeline Configuration

Create a new Pipeline job with this `Jenkinsfile`:

```groovy
pipeline {
    agent any

    parameters {
        booleanParam(name: 'LOCAL_DEPLOYMENT', defaultValue: true, description: 'Deploy Docker image locally')
        booleanParam(name: 'PUSH_TO_DOCKERHUB', defaultValue: false, description: 'Push Docker image to Docker Hub')
    }
    environment {
        SONAR_EV = tool 'Sonar'
    }

    stages {
        stage('Clone Code from Github') {
            steps {
                git url:"https://github.com/Naman-S-Sondhiya/Netflix-flask-clone.git", branch: "main"
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
```

## 📁 Project Structure

```
Netflix-flask-clone/
├── app.py              # Flask application
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Container configuration
├── Jenkinsfile         # CI/CD pipeline
├── requirements.txt    # Python dependencies
├── .dockerignore       # Docker ignore file
├── .env                # API key (local only)
├── static/             # CSS/JS assets
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   └── js/
│       └── main.js     # JavaScript functionality
└── templates/          # HTML templates
    ├── index.html      # Home page
    ├── movie.html      # Movie detail page
    ├── movies.html     # Movies listing
    ├── my-list.html    # User list page
    ├── new-popular.html# New & popular
    └── tv-shows.html   # TV shows page
```

## 🎯 Features

- **Netflix-style UI**: Responsive design across 5 pages
- **TMDB Integration**: Real movie data and posters
- **Security Scanning**: SonarQube, OWASP Dependency Check, Trivy
- **Prometheus Metrics**: `/metrics` endpoint
- **Health Check**: `/health` endpoint
- **Docker Ready**: Containerized deployment
- **CI/CD Pipeline**: Automated testing and deployment

## 🚨 Troubleshooting

### Docker Permission Issues

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Jenkins Pipeline Failures

- Verify tool names: `Sonar` and `owasp` (case sensitive)
- Check SonarQube server configuration
- Ensure required plugins are installed
- Verify credentials exist with correct IDs

### Application Issues

- Verify TMDB API key validity
- Check Docker container logs: `docker logs netflix-app`
- Ensure port 5000 is accessible

## 📦 Dependencies

- Flask               # Web framework
- requests            # HTTP client
- python-dotenv       # Environment variables
- prometheus-client   # Metrics

## 🔗 Useful Links

- **Pre-built Image**: [namanss/netflix-clone](https://hub.docker.com/repository/docker/namanss/netflix-clone/)
- **TMDB API**: [Get API Key](https://www.themoviedb.org/settings/api)
- **SonarQube**: Default login `admin/admin`

---

**Complete DevSecOps Pipeline Ready!** 🚀
