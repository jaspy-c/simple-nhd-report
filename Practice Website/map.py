import requests
from hazard_zones import get_hazard_numbers, get_hazard_zones
from geo_utils import get_geolocation
    
# Function to generate a simplified NHD report
def generate_nhd_report(address, city, state, zip_code):
    # Get geolocation data
    location = get_geolocation(address, city, state, zip_code)
    latitude = location["lat"]
    longitude = location["lng"]
    
    if location:
        # Get hazard zone information using functions from hazard_zones.py
        fault_zone, liquefaction_zone, landslide_zone = get_hazard_numbers(address, city, state, zip_code)
        
        # Create the NHD report
        nhd_report = f'NHD Report for Address: {address}, {city}, {state}, {zip_code}<br>'
        nhd_report += f'Latitude: {latitude}, Longitude: {longitude}<br>'
        nhd_report += f'Fault Zone: {fault_zone}<br>'
        nhd_report += f'Liquefaction Zone: {liquefaction_zone}<br>'
        nhd_report += f'Landslide Zone: {landslide_zone}<br>'
        
        return nhd_report
    else:
        return None
    