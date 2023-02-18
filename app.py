from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
from datetime import datetime
from dotenv import load_dotenv
import requests, uuid, os

load_dotenv()
base_url = 'https://api.onegov.nsw.gov.au'
access_key = os.getenv('ACCESS_KEY')
auth_header = os.getenv('AUTH_HEADER')
api_key = os.getenv('API_KEY')

app = Flask(__name__, static_folder='fuel-app/build', static_url_path='')
CORS(app)

@app.route('/api/', methods=['POST'])
@cross_origin()
def find_fuel():
    data = request.get_json()
    location = data['location']
    fuel = data['fuel']
    distance = data['distance']
    
    if location == '' or distance == 0:
        return {'result':[]}
    
    lat, lon = get_coordinates(location)
    
    if lat == lon == None:
        return {'result':[]}
    else:
        result = search_by_radius(lat, lon, fuel, distance, location) 
        
    return {
        'result': result
    }

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

def get_coordinates(location):
    base = 'http://api.positionstack.com/v1/forward'
    region = 'New South Wales'
    url = f'{base}?access_key={access_key}&query={location}&region={region}'
    try:
        response = requests.get(url)
        data = response.json()['data'][0]
        lat, lon = data['latitude'], data['longitude']
        return lat, lon
    except:
        return None, None

def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime('%d/%m/%Y %I:%M:%S %p')
    return timestamp

def format_last_updated(time_str):
    time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    today = datetime.today()
    if today.year == time_obj.year and today.month == time_obj.month:
        days_passed = today.date().day - time_obj.date().day
    else:
        days_passed = (today - time_obj).days
        
    if 0 <= days_passed < 1:
        return datetime.strftime(time_obj, '%l:%M%p Today')
    elif days_passed == 1:
        return datetime.strftime(time_obj, '%l:%M%p Yesterday')
    else:
        return f'{days_passed} days ago'
    
def get_auth_token():
    url = base_url + '/oauth/client_credential/accesstoken'
    payload = {'grant_type':'client_credentials'}
    headers = {
        'content-type': 'application/json',
        'authorization': auth_header
    }
    response = requests.get(url, headers=headers, params=payload)
    token = response.json()['access_token']
    return token

def search_by_radius(lat, lon, fuel_type, distance, location):
    endpoint = '/FuelPriceCheck/v1/fuel/prices/nearby'
    url = base_url + endpoint
    payload_dict = {
        'fueltype': fuel_type,
        'brand': [],
        'namedlocation': location,
        'latitude': lat,
        'longitude': lon,
        'radius': distance,
        'sortby': 'price',
        'sortascending': 'true'
    }
    payload = str(payload_dict)

    headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer ' + get_auth_token(),
        'apikey': api_key,
        'transactionid': str(uuid.uuid4()),
        'requesttimestamp': get_timestamp(),
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        return []
    return parse_response(response)

def parse_response(response):
    result = response.json()
    stations = result['stations']
    stations.sort(key=lambda x: x['code'])
    prices = result['prices']
    table = []

    for station, price in zip(stations, prices):
        brand = station['brand']
        name = station['name']
        address = station['address']
        distance = round(station['location']['distance'], 5)
        fuel_price = price['price']
        last_updated = format_last_updated(price['lastupdated'])

        row = {
            'brand': brand,
            'name': name,
            'address': address,
            'distance': distance,
            'price': fuel_price,
            'last_updated': last_updated
        }
        table.append(row)

    table.sort(key=lambda x: x['price'])
    return table

