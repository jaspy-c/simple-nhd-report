import requests
from geo_utils import get_geolocation
    
def get_details(address, city, state, zip_code):
    headers = {
        'authority': 'services2.arcgis.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,ja-JP;q=0.6,ja;q=0.5,zh-CN;q=0.4,zh;q=0.3',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://maps.conservation.ca.gov',
        'referer': 'https://maps.conservation.ca.gov/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
       
    response = requests.get(
        'https://services2.arcgis.com/zr3KAIbsRSUyARHG/arcgis/rest/services/CA_State_Parcels/FeatureServer/0/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A-13144417%2C%22ymin%22%3A4044436%2C%22xmax%22%3A-13144264%2C%22ymax%22%3A4044588.%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A0.2985821416485123%2C%22extent%22%3A%7B%22type%22%3A%22extent%22%2C%22xmin%22%3A-13849213.2%2C%22ymin%22%3A3833650.07%2C%22xmax%22%3A-12705064.28%2C%22ymax%22%3A5162434.380000003%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D%7D%7D',
        headers=headers,
    )
    data = response.json()
    return data


def transform_data(address, city, state, zip_code):
    # Fetch the data
    data = get_details(address, city, state, zip_code)

    # Perform data transformation
    attributes_list = list(data.values())[8]
    result_list = []

    for item in attributes_list:
        parcel_details = list(item.values())
        result_list.append(parcel_details)

    return result_list

# # With this line, passing longitude and latitude values
# attributes_list = list(get_details(address, city, state, zip_code).values())[8]
# parcel_details = list(attributes_list[0].values())[0]
# parcel_details.get('FullStreetAddress')

# result_list = []

# for item in attributes_list:
#     parcel_details = list(item.values())
#     result_list.append(parcel_details)
    
# master_list = []
# for item in result_list:
#     master_list.append(item[0])

def get_hazard_numbers(address, city, state, zip_code):
  
    # Call the data transformation function
    result_list = transform_data(address, city, state, zip_code)
  
    fault_zone = 0
    liquefaction_zone = 0
    landslide_zone = 0

    for item in result_list:
        if (
            address.lower().strip() == item[0]['FullStreetAddress'].lower().strip()
            and city.lower().strip() == item[0]['SITE_CITY'].lower().strip()
        ):
            fault_zone = item[0]['FaultZone']
            liquefaction_zone = item[0]['LiquefactionZone']
            landslide_zone = item[0]['LandslideZone']
            print(
                f"Fault Zone: {fault_zone}, Liquefaction Zone: {liquefaction_zone}, Landslide Zone: {landslide_zone}"
            )
            return fault_zone, liquefaction_zone, landslide_zone

def get_hazard_zones(fault_zone, liquefaction_zone, landslide_zone):
    if fault_zone == 1:
        fault_zone_description = 'This parcel is NOT WITHIN an Earthquake Fault Zone.'
    else:
        fault_zone_description = 'All or a portion of this parcel LIES WITHIN an Earthquake Fault Zone.'

    if liquefaction_zone == 1:
        liquefaction_zone_description = 'All or a portion of this parcel LIES WITHIN a Liquefaction Zone.'
    elif liquefaction_zone == 2:
        liquefaction_zone_description = 'This parcel is NOT WITHIN a Liquefaction Zone.'
    elif liquefaction_zone == 3:
        liquefaction_zone_description = 'Not all of this parcel has been evaluated by CGS for liquefaction hazards. See FAQs for more information.'
    else:
        liquefaction_zone_description = 'This parcel has NOT been EVALUATED by CGS for liquefaction hazards.'

    if landslide_zone == 1:
        landslide_zone_description = 'All or a portion of this parcel LIES WITHIN a Landslide Zone.'
    elif landslide_zone == 2:
        landslide_zone_description = 'This parcel is NOT WITHIN a Landslide Zone.'
    elif landslide_zone == 3:
        landslide_zone_description = 'Not all of this parcel has been evaluated by CGS for landslide hazards. See FAQs for more information.'
    else:
        landslide_zone_description = 'This parcel has NOT been EVALUATED by CGS for seismic landslide hazards.'
    
    return fault_zone_description, liquefaction_zone_description, landslide_zone_description
