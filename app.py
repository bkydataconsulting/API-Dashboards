from flask import Flask, render_template
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Dictionary of cities with their coordinates
CITIES = {
    'New York City': {'lat': 40.71, 'lon': -74.01},
    'Austin': {'lat': 30.27, 'lon': -97.74},
    'Astana': {'lat': 51.17, 'lon': 71.47},
    'Paris': {'lat': 48.86, 'lon': 2.35}
}

def get_weather_data():
    """Fetch weather data from Open-Meteo API for multiple cities."""
    all_weather_data = []
    
    for city_name, coords in CITIES.items():
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords['lat'],
            "longitude": coords['lon'],
            "current_weather": "true"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract current weather data
            current_weather = data['current_weather']
            
            # Add city data to our list
            all_weather_data.append({
                'City': city_name,
                'Temperature (°C)': current_weather['temperature'],
                'Wind Speed (km/h)': current_weather['windspeed'],
                'Wind Direction (°)': current_weather['winddirection'],
                'Time': datetime.fromisoformat(current_weather['time']).strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            print(f"Error fetching weather data for {city_name}: {e}")
            # Add error data for this city
            all_weather_data.append({
                'City': city_name,
                'Temperature (°C)': 'Error',
                'Wind Speed (km/h)': 'Error',
                'Wind Direction (°)': 'Error',
                'Time': 'Error'
            })
    
    # Create DataFrame from all cities' data
    return pd.DataFrame(all_weather_data)

@app.route('/')
def index():
    """Display the weather data in a table."""
    weather_data = get_weather_data()
    last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', 
                         weather_data=weather_data.to_html(classes='table table-striped', index=False),
                         last_updated=last_updated)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 