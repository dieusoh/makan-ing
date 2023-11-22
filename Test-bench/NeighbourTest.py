import boto3
import geohash2
from boto3.dynamodb.conditions import Key
import random
import logging

# For windows client
# session = boto3.Session(profile_name='makaning-2')
# ddb = session.resource('dynamodb', region_name='ap-southeast-1')
# table = ddb.Table('Locations')
# als = session.client('location')

## For mac client / AWS
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')
SessionTable = ddb.Table('SessionTable')
als = boto3.client('location')

# Enables logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Sets higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# A function that receives the longitude and latitude of a location and returns the geohash of the location at precision of 5
def get_geohash(lat, lon):
    return geohash2.encode(lat, lon, precision=5)

# A function that receives the longitude and latitude of a location and returns the geohash of the location at a precision of 6
def get_geohash_precise(lat, lon):
    return geohash2.encode(lat, lon, precision=6)

# ## A function that takes the value from geohash and queries DynamoDB for restaurants with the same geohash
# def get_restaurants(geohash):
#     response = table.query(
#         KeyConditionExpression=Key('Geohash').eq(geohash)
#     )
#     return response['Items']

# A function that takes the geohash, and category and queries DynamoDB for restaurants with the same geohash and returns the list of restaurants'
def get_category_list(geohash, category):
    restaurant_list = table.query(
        KeyConditionExpression=Key('Geohash').eq(geohash)
    )
    restaurant_list = restaurant_list['Items']
    same_category_list = []
    if category == "IDK, surprise me!":
        for restaurant in restaurant_list:
            same_category_list.append(restaurant)

    else:
        for restaurant in restaurant_list:
            if category in restaurant['Categories']:
                same_category_list.append(restaurant)
    
    return same_category_list

# A function that filters down to the precise geohash of the location
def get_nearby_list(precise_geohash, restaurant_list):
    nearby_list = []
    for restaurant in restaurant_list:
        if precise_geohash in restaurant['GeohashPrecise']:
            nearby_list.append(restaurant)
    return nearby_list

# A function that takes the list of restaurants and returns their names and addresses
def get_restaurant_info(restaurant_list):
    restaurant_info_list = []
    for restaurant in restaurant_list:
        price = restaurant.get('Price', None)  # Use item.get() to handle cases where 'Price' doesn't exist
        restaurant_info = {
            'Name': restaurant.get('Name'),
            'Address': restaurant.get('Address'),
            'Restaurant_lat': restaurant.get('Latitude'),
            'Restaurant_long': restaurant.get('Longitude')
        }

        restaurant_lat = restaurant.get('Latitude')
        restaurant_long = restaurant.get('Longitude')
        address = restaurant.get('Address')
        google_maps_url = f"https://www.google.com/maps?q={restaurant_lat},{restaurant_long}"
        Address_link = f'<a href="{google_maps_url}">{address}</a>'
        restaurant_info['Address_link'] = Address_link

# # Create a Google Maps link using the latitude and longitude
#         if Restaurant_lat is not None and Restaurant_long is not None:
#             google_maps_url = f"https://www.google.com/maps?q={restaurant_lat},{restaurant_long}"
#             address_link = f'<a href="{google_maps_url}">{address}</a>'
#         else:
#             address_link = address

        if price is not None:
            restaurant_info['Price'] = price
        
        restaurant_info_list.append(restaurant_info)
    return restaurant_info_list

# A function that is given the user's curreent coordinates and the restaurant's coordinates and is calculates the time taken to walk between them. 
def food_distance (user_lat, user_long, restaurant_lat, restaurant_long):
    # print ('in food distance')
    response = als.calculate_route(
        CalculatorName = 'GrabCalculator',
        DeparturePosition=[user_long, user_lat],
        DestinationPosition=[restaurant_long, restaurant_lat],
        TravelMode='Walking'
    )
    # print (response)
    Distance = response['Summary']['Distance']
    Duration = response['Summary']['DurationSeconds']
    return [Duration, Distance]


# A function that splits up the list into manageable sections that 
def split_list(list_to_split, current_index):
    sublist_size = 5
    start = current_index * sublist_size
    end = (current_index + 1) * sublist_size
    return list_to_split[start:end]

## A Function that expands the search by searching neighbouring geohashes if there are too few results
def expanded_search(geohash):
    new_geohash = geohash[:-1]
    response = table.query(
        KeyConditionExpression=Key('Geohash').eq(geohash)
    )
    print (response)


# Simple flow that demonstrates the above



def geohash_neighbors(geohash, lat, lon):
    # Define the precision of the GeoHash
    precision = len(geohash)
    
    # Define the maximum error in meters to identify neighbors
    max_error = 10 ** -(precision / 2 )
    
    # Calculate the neighbors
    neighbors = []
    for lat_offset in [-1, 0, 1]:
        for lon_offset in [-1, 0, 1]:
            if lat_offset == 0 and lon_offset == 0:
                continue
            neighbor_lat = lat + lat_offset * max_error
            neighbor_lon = lon + lon_offset * max_error
            neighbor_geohash = geohash2.encode(neighbor_lat, neighbor_lon, 5)
            neighbors.append(neighbor_geohash)
    
    return neighbors

geohash = "w21z2"
lat = 1.318337
lon = 103.753793
print (geohash_neighbors(geohash, lat, lon))
