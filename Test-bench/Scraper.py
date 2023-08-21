from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import boto3
import geohash2
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')
als = boto3.client('location')

url="https://www.burpple.com/wooshi-dhoby-ghaut-exchange"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

web_byte = urlopen(req).read()

webpage = web_byte.decode('utf-8')

#         # Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')

# print (soup)

# Find Name 
name = soup.find('h1')
name = name.text
name = name.replace('\n', '')
# print (name)

# Get neighbourhood
neighbourhood = soup.find('div', class_='venue-area')
neighbourhood = neighbourhood.a.text.strip()
# print (neighbourhood)

# find address
address = soup.find('div', attrs={'data-venue-address': True})
address = address.get('data-venue-address')
# print (address)

## Geocode address
# Coordinates = als.search_place_index_for_text(
#     FilterCountries=[
#         'SGP',
#     ],
#     IndexName='explore.place.Esri',
#     Text=address
# )

## Find tags
tags = soup.find('div', class_='venue-tags')
# print (tags)
categories = []
for tag in tags:
    tag = tag.get_text()
    tag = tag.strip()
    if tag is not '':
        if 'Burpple' not in tag: 
            categories.append(tag)

print (categories)

# Coordinates = Coordinates['Results'][0]['Place']['Geometry']['Point']
## Geohash Coordinates
# GeohashBroad = geohash2.encode(Coordinates[1], Coordinates[0],precision = 5)
# GeohashPrecise = geohash2.encode(Coordinates[1], Coordinates[0], precision = 6)

# # write to DynamoDB
# table.put_item(
#     Item={
#         'Geohash': GeohashBroad,
#         'Name': name,
#         'Address': address,
#         'GeohashPrecise': GeohashPrecise,
#         'Neighbourhood': neighbourhood
#     }
# )