from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_movies(page=1):
    if not TMDB_API_KEY:
        return []
    
    url = f"{TMDB_BASE_URL}/movie/now_playing"
    params = {'api_key': TMDB_API_KEY, 'page': page}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        return response.json().get('results', []) if response.status_code == 200 else []
    except:
        return []

def get_movie(movie_id):
    if not TMDB_API_KEY:
        return None
    
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {'api_key': TMDB_API_KEY, 'append_to_response': 'credits'}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    movies = get_movies(page)
    return render_template('index.html', movies=movies, image_base_url=TMDB_IMAGE_BASE_URL)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = get_movie(movie_id)
    if not movie:
        return "Movie not found", 404
    return render_template('movie.html', movie=movie, image_base_url=TMDB_IMAGE_BASE_URL)

@app.route('/movies')
def movies():
    movies = get_movies()
    return render_template('movies.html', movies=movies, image_base_url=TMDB_IMAGE_BASE_URL)

@app.route('/tv-shows')
def tv_shows():
    movies = get_movies()
    return render_template('tv-shows.html', movies=movies, image_base_url=TMDB_IMAGE_BASE_URL)

@app.route('/new-popular')
def new_popular():
    movies = get_movies()
    return render_template('new-popular.html', movies=movies, image_base_url=TMDB_IMAGE_BASE_URL)

@app.route('/my-list')
def my_list():
    movies = get_movies()
    return render_template('my-list.html', movies=movies, image_base_url=TMDB_IMAGE_BASE_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
