import boto3
import geohash2
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')
als = boto3.client('location')
from boto3.dynamodb.conditions import Key

## A function that receives the longitude and latitude of a location and returns the geohash of the location at precision of 5
def get_geohash(lat, lon):
    return geohash2.encode(lat, lon, precision=5)

## A function that receives the longitude and latitude of a location and returns the geohash of the location at a precision of 6
def get_geohash_precise(lat, lon):
    return geohash2.encode(lat, lon, precision=6)

# ## A function that takes the value from geohash and queries DynamoDB for restaurants with the same geohash
# def get_restaurants(geohash):
#     response = table.query(
#         KeyConditionExpression=Key('Geohash').eq(geohash)
#     )
#     return response['Items']

## a function that takes the geohash, and category and queries DynamoDB for restaurants with the same geohash and returns the list of restaurants'

def get_category_list(geohash, category):
    restaurants = table.query(
        KeyConditionExpression=Key('Geohash').eq(geohash)
    )
    restaurants = restaurants['Items']

    same_category_list = []
    for i in restaurants:
        try:
            if category in i['Categories']:
                same_category_list.append(i)
        except:
            print ('No Categories')
    
    return same_category_list

## a function that filters down to the precise geohash of the location
def get_nearby_list(precise_geohash, restaurant_list):
    nearby_list = []
    for restaurant in restaurant_list:
        if precise_geohash in restaurant['GeohashPrecise']:
            nearby_list.append(restaurant)
    return nearby_list

## a function that takes the list of restaurants and returns their names and addresses

def get_shortened_restaurants(restaurant_list):
    name_and_address_list = []
    for restaurant in restaurant_list:
        name_and_address = {
            'Name': restaurant.get('Name'),
            'Address': restaurant.get('Address')
        }
        name_and_address_list.append(name_and_address)
    return name_and_address_list


## A function that splits up the list into manageable sections that 
def split_list(list_to_split, current_index):
    sublist_size = 5
    current_index = current_index
    start = current_index * sublist_size
    end = (current_index + 1) * sublist_size
    return list_to_split[start:end]


## simple flow that demonstrates the above
geohash = "w21zg"
precise_geohash = 'w21zg9'
category = 'Japanese'

## get all the restaurants in the general area
restaurant_list = get_category_list(geohash, category)

## get a list of the restaurants nearby and put them into a list. If the list is empty, it uses the less precise geohash. 
nearby_list = get_nearby_list(precise_geohash, restaurant_list)
nearby_list = get_shortened_restaurants(nearby_list)
output_list = split_list(nearby_list,0)

if not output_list:
    print ("no restaurants in precise geohash")
    restaurant_list = get_shortened_restaurants(restaurant_list)
    output_list = split_list(restaurant_list,0)


for i  in output_list:
    print (i)
    print ('________')