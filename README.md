# Netflix Clone - Minimal Flask App

Ultra-minimal Netflix-inspired web application with TMDB API integration, Prometheus metrics, and Docker support.

![Flask](https://img.shields.io/badge/Flask-3.1.2-green) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-blue) ![Prometheus](https://img.shields.io/badge/Prometheus-0.22.1-orange)

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- TMDB API key ([Get one here](https://www.themoviedb.org/settings/api))

### Setup & Run

1. **Clone & Navigate**
   ```bash
   git clone <repo-url>
   cd Netflix-flask-clone
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

3. **Install Dependencies**
   ```bash
   venv/bin/python -m pip install -r requirements.txt
   ```

4. **Set API Key**
   ```bash
   echo "TMDB_API_KEY=your_api_key_here" > .env
   ```

5. **Run Application**
   ```bash
   ./run.sh
   # OR
   venv/bin/python app.py
   ```

6. **Access Application**
   - Main app: `http://localhost:5000`
   - Metrics: `http://localhost:5000/metrics`
   - Health: `http://localhost:5000/health`

### Docker Deployment

1. **Build & Run**
   ```bash
   docker build -t netflix-clone .
   docker run -p 5000:5000 --env-file .env netflix-clone
   ```

## 📁 Project Structure

```
Netflix-flask-clone/
├── app.py              # Ultra-minimal Flask app (45 lines)
├── requirements.txt    # 4 dependencies with versions
├── Dockerfile          # Container config
├── .dockerignore       # Docker ignore
├── .env               # API key (not in git)
├── run.sh             # Run script (executable)
├── venv/              # Virtual environment
└── templates/         # HTML templates (6 files)
    ├── index.html     # Home page
    ├── movie.html     # Movie details
    ├── movies.html    # Movies page
    ├── tv-shows.html  # TV shows page
    ├── new-popular.html # New & popular
    └── my-list.html   # My list
```

## 🎯 Features

- **5 Pages**: Home, Movies, TV Shows, New & Popular, My List
- **Movie Details**: Cast, ratings, overview
- **Prometheus Metrics**: `/metrics` endpoint
- **Health Check**: `/health` endpoint
- **Responsive Design**: Mobile-friendly
- **Docker Ready**: Containerized deployment

## 📦 Dependencies

```
Flask==3.1.2          # Web framework
requests==2.31.0      # HTTP client
python-dotenv==1.0.0  # Environment variables
prometheus-client==0.22.1  # Metrics
```

## 🔧 Environment Variables

- `TMDB_API_KEY`: Required TMDB API key

## 🚨 Troubleshooting

**No movies showing?**
- Check your TMDB API key in `.env`
- Verify internet connection

**Import errors?**
- Use virtual environment: `venv/bin/python app.py`
- Install dependencies: `venv/bin/pip install -r requirements.txt`

**Docker issues?**
- Ensure `.env` file exists
- Use `--env-file .env` flag

## 🔍 Code Overview

**app.py (45 lines total):**
- 4 imports + dotenv setup
- 1 prometheus counter
- 1 unified data function
- 6 routes (/, /movie/id, /pages, /metrics, /health)
- Handles all 5 template pages

**Key Features:**
- Single route handles 4 pages: `/movies`, `/tv-shows`, `/new-popular`, `/my-list`
- Unified `get_data()` function for API calls
- Prometheus metrics tracking
- Docker containerization
- Virtual environment setup

---

**Ultra-minimal setup, maximum functionality!** 🎬
