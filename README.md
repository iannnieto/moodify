# Moodify - Weather-Based Spotify Playlist Generator

Moodify is a web application that creates personalized Spotify playlists based on your local weather conditions and mood. It uses the Spotify API for playlist creation and the OpenWeather API for weather data.

## Features

- Create personalized playlists based on weather conditions
- Automatic mood detection based on weather
- Beautiful, modern UI with Tailwind CSS
- Secure authentication with Spotify

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/moodify.git
cd moodify
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Get your Spotify API credentials from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Get your OpenWeather API key from [OpenWeather](https://openweathermap.org/api)
   - Fill in the credentials in the `.env` file

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Click "Connect with Spotify" to authenticate
2. Enter your city name
3. Click "Generate Playlist"
4. Your personalized playlist will be created and you'll be redirected to Spotify

## Technologies Used

- Python
- Flask
- Spotify API
- OpenWeather API
- Tailwind CSS

## License

MIT
