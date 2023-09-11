from flask import Flask, render_template, request
from map import generate_nhd_report
from hazard_zones import get_hazard_zones, get_hazard_numbers

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('address_form.html')

@app.route('/process_address', methods=['POST'])
def process_address():
    # Get form input values
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip')
    
    # Call the functions from hazard_zone.py
    fault_zone, liquefaction_zone, landslide_zone = get_hazard_numbers(address, city, state, zip_code)
    
    # Call the hazard_zones function to print the hazard information
    fault_zone_description, liquefaction_zone_description, landslide_zone_description = get_hazard_zones(fault_zone, liquefaction_zone, landslide_zone)

    if fault_zone_description and liquefaction_zone_description and landslide_zone_description:
        # Use the generate_nhd_report function from map.py to generate the report
        nhd_report = generate_nhd_report(address, city, state, zip_code)

        if nhd_report:
            # Render a single HTML template and pass both sets of data
            return render_template('report.html', nhd_report=nhd_report, fault_zone=fault_zone, liquefaction_zone=liquefaction_zone, landslide_zone=landslide_zone, fault_zone_description=fault_zone_description, liquefaction_zone_description=liquefaction_zone_description, landslide_zone_description=landslide_zone_description)
    
    return 'Address not found.'

if __name__ == '__main__':
    app.run(debug=True)