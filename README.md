# Netflix Clone - DevSecOps Flask App

Minimal Netflix-inspired web application with TMDB API integration, Prometheus metrics, and complete CI/CD pipeline.

![Flask](https://img.shields.io/badge/Flask-3.1.2-green) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-blue) ![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-orange)

## 🚀 Local Development

### Prerequisites
- Python 3.12+
- TMDB API key ([Get one here](https://www.themoviedb.org/settings/api))

### Setup & Run

1. **Clone Repository**
   ```bash
   git clone https://github.com/Naman-S-Sondhiya/Netflix-flask-clone.git
   cd Netflix-flask-clone
   ```

2. **Create .env File**
   ```bash
   echo "TMDB_API_KEY=your_actual_api_key_here" > .env
   ```

3. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   venv/bin/pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   ./run.sh
   ```

5. **Access Application**
   - Main app: `http://localhost:5000`
   - Metrics: `http://localhost:5000/metrics`
   - Health: `http://localhost:5000/health`

## 🐳 Docker Deployment

### Option 1: Build Locally
```bash
docker build -t netflix-clone .
docker run -p 5000:5000 -e TMDB_API_KEY=your_api_key netflix-clone
```

### Option 2: Use Pre-built Image
```bash
docker run -p 5000:5000 -e TMDB_API_KEY=your_api_key namanss/netflix-clone:latest
```

**Pre-built Docker Image:** [namanss/netflix-clone](https://hub.docker.com/repository/docker/namanss/netflix-clone/)

## 🔧 Jenkins CI/CD Pipeline

### Pipeline Parameters

The pipeline includes configurable parameters:

- **`LOCAL_DEPLOYMENT`** (default: `true`) - Deploys Docker container locally
- **`PUSH_TO_DOCKERHUB`** (default: `false`) - Pushes image to Docker Hub

### Required Jenkins Credentials

**Minimum Required:**
1. **`tmdb-api-key`** (Secret text)
   - ID: `tmdb-api-key`
   - Secret: Your TMDB API key

**Optional (for Docker Hub push):**
2. **`dockerhub-creds`** (Username/Password)
   - ID: `dockerhub-creds`
   - Username: Your Docker Hub username
   - Password: Your Docker Hub access token

### Jenkins Setup Steps

1. **Add Required Credential**
   - Go to: `Manage Jenkins` → `Credentials` → `Global`
   - Add `tmdb-api-key` credential

2. **Create Pipeline Job**
   - New Item → Pipeline
   - SCM: Git → Repository URL: `https://github.com/Naman-S-Sondhiya/Netflix-flask-clone.git`
   - Branch: `main`
   - Script Path: `Jenkinsfile`

3. **Run Pipeline**
   - **Local deployment only**: Keep defaults (`LOCAL_DEPLOYMENT=true`, `PUSH_TO_DOCKERHUB=false`)
   - **With Docker Hub push**: Set `PUSH_TO_DOCKERHUB=true` and add `dockerhub-creds`

### Pipeline Stages

- ✅ Code Clone
- ✅ SonarQube Analysis
- ✅ OWASP Dependency Check
- ✅ Quality Gate
- ✅ Trivy Security Scan
- ✅ Docker Build
- ✅ Deploy Locally (conditional)
- ✅ Push to Docker Hub (conditional)

## 📁 Project Structure

```
Netflix-flask-clone/
├── app.py              # Minimal Flask app (45 lines)
├── Jenkinsfile         # CI/CD pipeline
├── Dockerfile          # Container config
├── requirements.txt    # Python dependencies
├── .env               # API key (create locally)
├── static/            # CSS/JS assets
└── templates/         # HTML templates (6 files)
```

## 🎯 Features

- **5 Netflix Pages**: Home, Movies, TV Shows, New & Popular, My List
- **Movie Details**: Cast, ratings, overview from TMDB API
- **Prometheus Metrics**: `/metrics` endpoint for monitoring
- **Health Check**: `/health` endpoint
- **DevSecOps Pipeline**: SonarQube, OWASP, Trivy security scans
- **Docker Ready**: Containerized deployment
- **Responsive Design**: Mobile-friendly UI

## 📦 Dependencies

```
Flask                # Web framework
requests             # HTTP client
python-dotenv        # Environment variables
prometheus-client    # Metrics
```

## 🚨 Troubleshooting

**No movies showing?**
- Verify TMDB API key in `.env` or Jenkins credentials
- Check internet connectivity

**Jenkins pipeline fails?**
- Ensure `tmdb-api-key` credential exists
- For Docker Hub push, set `PUSH_TO_DOCKERHUB=true` and add `dockerhub-creds`
- Check tool configurations (SonarQube, OWASP, Trivy)
- Verify Jenkins tools: 'Sonar' and 'owasp' are configured

**Docker issues?**
- Use pre-built image: `namanss/netflix-clone:latest`
- Ensure API key is passed: `-e TMDB_API_KEY=your_key`

---

**Production-ready DevSecOps setup!** 🚀