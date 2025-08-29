import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # TMDB API Configuration
    TMDB_API_KEY = os.getenv('TMDB_API_KEY') or os.getenv('API_KEY') or ''
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Application Settings
    MOVIES_PER_PAGE = 20

def validate_config():
    """Validate that required configuration is set"""
    if not Config.TMDB_API_KEY:
        print("Warning: TMDB_API_KEY not set. API calls may fail.")
