import boto3
import geohash2
import csv

## For windows client
# session = boto3.Session(profile_name='makaning-2')
# ddb = session.resource('dynamodb', region_name='ap-southeast-1')
# table = ddb.Table('MRT')
# als = session.client('location')

## For mac client
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('MRT')
als = boto3.client('location')

csv_file_path = 'MakanDocker/MRT/mrt_stations.csv'

with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        # Extract data from CSV
        station_name = row['MRT-name']
        latitude = float(row['Latitude'])
        longitude = float(row['Longitude'])

        ## Geohash Coordinates
        Geohash = geohash2.encode(latitude, longitude ,precision = 5)

    # Write data to DynamoDB
        table.put_item(
            Item={
                'MRT-name': station_name,
                'Latitude': str(latitude),
                'Longitude': str(longitude),
                'Geohash' : Geohash
            }
        )
        print ('Added ' + station_name)