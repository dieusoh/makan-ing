import boto3
import geohash2
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')
als = boto3.client('location')
from boto3.dynamodb.conditions import Key
import random

# For windows client
session = boto3.Session(profile_name='makaning')
ddb = session.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')
als = session.client('location')

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
            try:
                same_category_list.append(restaurant)
            except:
                print ("Restaurant does not match user's food choice")

    else:
        for restaurant in restaurant_list:
            try:
                if category in restaurant['Categories']:
                    same_category_list.append(restaurant)
            except:
                print ("Restaurant does not match user's food choice")
    
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
            'Address': restaurant.get('Address')
        }
        if price is not None:
            restaurant_info['Price'] = price
        
        restaurant_info_list.append(restaurant_info)
    return restaurant_info_list


# A function that splits up the list into manageable sections that 
def split_list(list_to_split, current_index):
    sublist_size = 5
    current_index = current_index
    start = current_index * sublist_size
    end = (current_index + 1) * sublist_size
    return list_to_split[start:end]


# Simple flow that demonstrates the above

def find_food(geohash, category):
    # Get all the restaurants in the general area
    restaurant_list = get_category_list(geohash, category)
    # print(restaurant_list)

    # Take a list of the restaurants nearby and put them into a list. If the list is empty, it uses the less precise geohash. 
    # nearby_list = get_nearby_list(precise_geohash, restaurant_list)
    # nearby_list = get_restaurant_info(nearby_list)
    # random.shuffle(nearby_list)
    # output_list = split_list(nearby_list,0)

    # if not output_list:
    #     print ("no restaurants in precise geohash")
    #     restaurant_list = get_restaurant_info(restaurant_list)
    #     random.shuffle(restaurant_list)
    #     output_list = split_list(restaurant_list,0)

    restaurant_list = get_restaurant_info(restaurant_list)
    random.shuffle(restaurant_list)
    output_list = split_list(restaurant_list,0)

    for i  in output_list:
        print (i)
        print ('________')

# geohash = "w21zg"
# precise_geohash = 'w21zg9'
# category = 'IDK, surprise me!'
# find_food(geohash, category)