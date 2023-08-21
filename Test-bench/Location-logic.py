import geohash2
import boto3
import json
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')

# Get current location

#Somewhere in East Coast
# current_location = (1.309467552015505, 103.93787515190861)

# 464A Clementi Avenue 1
current_location = (1.3112533293915378, 103.76847867934113)

## Hash current location
current_location_hash = geohash2.encode(current_location[0], current_location[1], precision=5)
print(current_location_hash)

## Look for food places near current location
food_nearby = table.query(
    TableName='Locations',
    KeyConditionExpression='Geohash = :geohash_value',
    ExpressionAttributeValues={
        ':geohash_value': current_location_hash
    }
)

food_nearby = food_nearby['Items']
food_nearby_list = []
for i in food_nearby:
    food_nearby_list.append(i['Name'])

print(food_nearby_list)


