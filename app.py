from flask import Flask, render_template, request, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import requests, os, time
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
REQUEST_COUNT = Counter('requests_total', 'Total requests')

@app.before_request
def track():
    REQUEST_COUNT.inc()

API_KEY = os.getenv('TMDB_API_KEY', '')
API_URL = 'https://api.themoviedb.org/3'
IMG_URL = 'https://image.tmdb.org/t/p/w500'

def get_data(endpoint, movie_id=None):
    if not API_KEY: return [] if not movie_id else None
    url = f"{API_URL}/{endpoint}/{movie_id or 'now_playing'}"
    params = {'api_key': API_KEY, 'append_to_response': 'credits'} if movie_id else {'api_key': API_KEY}
    try:
        r = requests.get(url, params=params, timeout=5)
        return r.json() if r.status_code == 200 and movie_id else r.json().get('results', []) if r.status_code == 200 else (None if movie_id else [])
    except: return None if movie_id else []

@app.route('/')
def index():
    return render_template('index.html', movies=get_data('movie'), image_base_url=IMG_URL)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = get_data('movie', movie_id)
    return render_template('movie.html', movie=movie, image_base_url=IMG_URL) if movie else ("Not found", 404)

@app.route('/<path:page>')
def pages(page):
    if page in ['movies', 'tv-shows', 'new-popular', 'my-list']:
        return render_template(f'{page}.html', movies=get_data('movie'), image_base_url=IMG_URL)
    return "Not found", 404

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
