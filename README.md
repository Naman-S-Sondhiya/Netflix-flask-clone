# Netflix Clone - Movie Discovery App

A modern Netflix-inspired web application that displays currently playing movies using the TMDB API. Built with Flask, Docker, and beautiful responsive design.

![Netflix Clone](https://img.shields.io/badge/Netflix-Clone-red) ![Python](https://img.shields.io/badge/Python-3.9-blue) ![Flask](https://img.shields.io/badge/Flask-2.0-green) ![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🎬 Features

- **Movie Discovery**: Browse currently playing movies in theaters
- **Movie Details**: View detailed information including cast, ratings, and overview
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Netflix-style UI**: Beautiful gradients, animations, and hover effects
- **Docker Support**: Easy containerized deployment
- **Pagination**: Browse through multiple pages of movies

## 🚀 Quick Start

### Prerequisites
- Python 
- Docker (optional)
- TMDB API key ([Get one here](https://www.themoviedb.org/settings/api))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Naman-S-Sondhiya/Netflix-flask-clone.git
   cd Netflix
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up your API key** **required create a TMDB account and acquire the TMDB API key, & provide your actual API key**
   ```bash
   # Create a .env file (not tracked by git)
   echo "TMDB_API_KEY=your_actual_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t netflix-app --build-arg TMDB_API_KEY=your_actual_api_key_here .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 netflix-app
   ```

3. **Access the application**
   Open `http://localhost:5000` in your browser

## 📁 Project Structure

```
Netflix/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── .gitignore         # Git ignore rules
├── .dockerignore      # Docker ignore rules
├── README.md          # This file
└── templates/         # HTML templates
    ├── index.html     # Main movie listing page
    └── movie.html     # Movie detail page
```

## 🎨 UI Features

- **Modern Design**: Netflix-inspired dark theme with red accents
- **Smooth Animations**: Fade-in effects and hover transitions
- **Responsive Grid**: Adaptive movie card layout
- **Movie Details**: Comprehensive information with cast photos
- **Mobile Friendly**: Optimized for all screen sizes

## 🔧 Configuration

The app uses environment variables for configuration:

- `TMDB_API_KEY`: Your TMDB API key (required)
- `FLASK_ENV`: Set to 'production' or 'development'
- `DEBUG`: Enable debug mode (true/false)

## 📦 Dependencies

- **Flask**: Web framework
- **Requests**: HTTP client for API calls
- **Python-dotenv**: Environment variable management
- **Gunicorn**: Production WSGI server
- **Werkzeug**: WSGI utilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Important Notes

- Keep your TMDB API key secure - never commit it to version control
- The `.env` file is automatically excluded by `.gitignore`
- For production use, consider adding proper error handling and logging

## 🆘 Support

If you encounter any issues:
1. Check that your API key is valid
2. Ensure all dependencies are installed
3. Verify Docker is running (if using containers)

---

**Enjoy exploring movies!** 🍿
