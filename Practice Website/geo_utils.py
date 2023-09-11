import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Google Maps Geocoding API Key (replace with your own key)
api_key = os.getenv("api_key")

# Function to fetch geolocation data based on an address
def get_geolocation(address, city, state, zip_code):
    location_query = f'{address}, {city}, {state}, {zip_code}'
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': location_query, 'key': api_key}
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location
    else:
        print('Address not found.')
        return None