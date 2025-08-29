from flask import Flask, render_template, request, abort
import requests
from config import Config, validate_config

app = Flask(__name__)
app.config.from_object(Config)

validate_config()

def get_latest_movies(api_key, page=1):
    url = f"{Config.TMDB_BASE_URL}/movie/now_playing"
    params = {
        'api_key': api_key,
        'language': 'en-US',
        'page': page
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"TMDB API Error: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_movie_details(api_key, movie_id):
    url = f"{Config.TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': api_key,
        'language': 'en-US',
        'append_to_response': 'credits'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"TMDB API Error for movie {movie_id}: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request failed for movie {movie_id}: {e}")
        return None

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    movies_data = get_latest_movies(app.config['TMDB_API_KEY'], page)
    movies = []
    total_pages = 1
    if movies_data:
        movies = movies_data.get('results', [])
        total_pages = movies_data.get('total_pages', 1)
    return render_template('index.html', movies=movies, image_base_url=Config.TMDB_IMAGE_BASE_URL, page=page, total_pages=total_pages)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie_data = get_movie_details(app.config['TMDB_API_KEY'], movie_id)
    if not movie_data:
        abort(404, description="Movie not found")
    
    return render_template('movie.html', movie=movie_data, image_base_url=Config.TMDB_IMAGE_BASE_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
