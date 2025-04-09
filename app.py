import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request, redirect, url_for, session
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify API setup
sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
    scope='playlist-modify-public playlist-modify-private'
)

def get_weather_mood(city):
    """Get weather data and determine mood based on weather conditions"""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code != 200:
        return None
    
    weather = data['weather'][0]['main'].lower()
    temp = data['main']['temp']
    
    # Map weather conditions to moods
    weather_mood_map = {
        'clear': 'happy',
        'clouds': 'chill',
        'rain': 'melancholic',
        'snow': 'cozy',
        'thunderstorm': 'energetic'
    }
    
    mood = weather_mood_map.get(weather, 'neutral')
    
    # Adjust mood based on temperature
    if temp > 25:
        mood = 'energetic'
    elif temp < 10:
        mood = 'cozy'
    
    return mood

def create_playlist(sp, mood, city):
    """Create a personalized playlist based on mood and weather"""
    user_id = sp.current_user()['id']
    playlist_name = f"Weather Mood: {mood.capitalize()} in {city}"
    
    # Create playlist
    playlist = sp.user_playlist_create(
        user_id,
        playlist_name,
        public=True,
        description=f"Personalized playlist based on {mood} mood in {city}"
    )
    
    # Search for tracks based on mood
    mood_keywords = {
        'happy': 'upbeat pop',
        'chill': 'lo-fi chill',
        'melancholic': 'sad indie',
        'cozy': 'acoustic folk',
        'energetic': 'dance pop',
        'neutral': 'indie pop'
    }
    
    results = sp.search(q=mood_keywords[mood], limit=20, type='track')
    track_uris = [track['uri'] for track in results['tracks']['items']]
    
    # Add tracks to playlist
    sp.playlist_add_items(playlist['id'], track_uris)
    
    return playlist['external_urls']['spotify']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('create_playlist_page'))

@app.route('/create-playlist', methods=['GET', 'POST'])
def create_playlist_page():
    if 'token_info' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        city = request.form['city']
        mood = get_weather_mood(city)
        
        if not mood:
            return render_template('error.html', message="Could not fetch weather data")
        
        sp = spotipy.Spotify(auth=session['token_info']['access_token'])
        playlist_url = create_playlist(sp, mood, city)
        
        return render_template('success.html', playlist_url=playlist_url)
    
    return render_template('create_playlist.html')

if __name__ == '__main__':
    app.run(debug=True) 