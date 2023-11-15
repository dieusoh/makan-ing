import requests
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import boto3
import geohash2
from decimal import Decimal
import time
import re
from datetime import datetime

## For windows client
session = boto3.Session(profile_name='makaning-2')
ddb = session.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')
als = session.client('location')

## For mac client
# ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
# table = ddb.Table('Locations')
# als = boto3.client('location')

specific_links_to_exclude = [
    "https://www.burpple.com/kl",
    "https://www.burpple.com/jb",
    "https://www.burpple.com/beyond",
    'https://www.burpple.com/sg',
    "https://www.burpple.com/mn",
    "https://www.burpple.com/guides/sg",
    "https://www.burpple.com/advertise"
]

def get_links(url):
    url=url
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()

    webpage = web_byte.decode('utf-8')
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(webpage, 'html.parser')

    # Find all anchor tags (<a>) in the page
    anchor_tags = soup.find_all('a')

    # Extract and store the links in a list
    base_url = url 
    links = [urljoin(base_url, link.get('href')) for link in anchor_tags]

    # Filter out None values (links without href attribute)
    links = [link for link in links if link is not None]
    # print (links)

    # Link for the next page
    more_options = [link for link in links if link.startswith("https://www.burpple.com/search/sg?offset")]

    # Filter links to remove non-Burpple links
    filtered_links = [link for link in links if link.startswith("https://www.burpple.com")]

    # Filter links to remove useless subdomains starting with "beyond" and "categories"
    filtered_links = [link for link in filtered_links 
                      if not link.startswith("https://www.burpple.com/neighbourhoods") and not link.startswith("https://www.burpple.com/categories") if not link.startswith("https://www.burpple.com/list/") if not link.startswith("https://www.burpple.com/f/") if not link.startswith("https://www.burpple.com/@") if not link.startswith("https://www.burpple.com/about-us") if not link.startswith("https://www.burpple.com/newsroom")  if not link.startswith("https://www.burpple.com/careers") if not link.startswith("https://www.burpple.com/terms") if not link.startswith("https://www.burpple.com/search") if not link.startswith("https://www.burpple.com/features") if not link.startswith("https://www.burpple.com/sg/mobile") if not link.startswith("https://www.burpple.com/sg/beyond") if not link.startswith("https://www.burpple.com/sg/advertise") if not link.startswith("https://www.bites.burpple.com")
                      ]
    
    filtered_links = [
        link for link in filtered_links if link not in specific_links_to_exclude]
    # print (filtered_links)
    unique_links = list(set(filtered_links))
    return more_options, unique_links


def get_restaurant_info(url):
    # print (soup)
    try: 
        url=url
        print ("getting info for " + url)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        web_byte = urlopen(req).read()

        webpage = web_byte.decode('utf-8')

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(webpage, 'html.parser')
        # Get restaurant name 
        name = soup.find('h1')
        name = name.text
        name = name.replace('\n', '')
        # print (name)

        # Get neighbourhood
        neighbourhood = soup.find('div', class_='venue-area')
        neighbourhood = neighbourhood.a.text.strip()
        # print (neighbourhood)

        # Get address
        address = soup.find('div', attrs={'data-venue-address': True})
        address = address.get('data-venue-address')
        # print (address)

        # Get price (if available)
        try:
            pricetag = soup.find('div', class_='venue-price')
        except:
            pricetag = 'Unknown'
        # Extract the text from the element
        price = pricetag.get_text(strip=True)
        # print (price)

        # Get categories
        tags = soup.find('div', class_='venue-tags')
        # print (tags)
        categories = []
        for tag in tags:
            tag = tag.get_text()
            tag = tag.strip()
            if tag != '':
                if 'Burpple' not in tag: 
                    categories.append(tag)
        # print (categories)

        # Get geocode address
        Coordinates = als.search_place_index_for_text(
            FilterCountries=[
                'SGP',
            ],
            IndexName='explore.place.Esri',
            Text=address
        )

        Coordinates = Coordinates['Results'][0]['Place']['Geometry']['Point']
        ## Geohash Coordinates
        GeohashBroad = geohash2.encode(Coordinates[1], Coordinates[0],precision = 5)
        GeohashPrecise = geohash2.encode(Coordinates[1], Coordinates[0], precision = 6)

        # Get opening hours
        opening_hours_dict = {}
        try: 
            opening_hours_section = soup.find('div', class_='venue-details__item--opening')
            opening_hours_header = opening_hours_section.find('div', class_='venueInfo-details-header-item-header--openingHours')
            hidden_div = opening_hours_section.find('div', id='venueInfo-details-header-item-body-hidden-openingHours')
            # Extract the opening hours from all days
            days_and_hours = re.findall(r'(\w+):\s*((?:\d{1,2}:\d{2}[apm]+\s*-\s*\d{1,2}:\d{2}[apm]+\s*)+|Closed)', hidden_div.get_text())
            # Extract the current day's opening hours
            current_day_opening_hours = opening_hours_section.find('p').get_text()
            current_day_match = re.search(r'0?(\w+):\s*((?:\d{1,2}:\d{2}[apm]+\s*-\s*\d{1,2}:\d{2}[apm]+\s*)+|Closed)', current_day_opening_hours)
            # Initialize an empty dictionary to store the opening hours for each day
            # Display the results
            if current_day_match:
                current_day, current_day_hours = current_day_match.groups()
                if current_day_hours == 'Closed':
                    opening_hours_dict[current_day] = 'Closed'

                else:
                    time_slots = re.findall(r'\d{1,2}:\d{2}[apmAPM]{2}\s*-\s*\d{1,2}:\d{2}[apmAPM]{2}', current_day_hours)
                    formatted_time_slots = []
                    for time_slot in time_slots:
                        start_time_str, end_time_str = time_slot.split(' - ')
                        start_time = datetime.strptime(start_time_str, "%I:%M%p")
                        end_time = datetime.strptime(end_time_str, "%I:%M%p")

                        formatted_start_time = start_time.strftime('%I:%M%p').lstrip('0').replace(':00', '')
                        formatted_end_time = end_time.strftime('%I:%M%p').lstrip('0').replace(':00', '')

                        formatted_time_slots.append(f"{formatted_start_time} - {formatted_end_time}")

                        # Join the formatted time slots into a single string
                        formatted_current_day_hours  = ' | '.join(formatted_time_slots)
                            
                    opening_hours_dict[current_day] = formatted_current_day_hours

            for day, opening_hours in days_and_hours:
                if opening_hours == 'Closed':
                    formatted_hours = 'Closed'
                    opening_hours_dict[day] = 'Closed'
                else:
                    # Split the string into individual time ranges
                    time_slots = re.findall(r'\d{1,2}:\d{2}[apmAPM]{2}\s*-\s*\d{1,2}:\d{2}[apmAPM]{2}', opening_hours)
                    formatted_time_slots = []
                    for time_slot in time_slots:
                        start_time_str, end_time_str = time_slot.split(' - ')
                        start_time = datetime.strptime(start_time_str, "%I:%M%p")
                        end_time = datetime.strptime(end_time_str, "%I:%M%p")

                        formatted_start_time = start_time.strftime('%I:%M%p').lstrip('0').replace(':00', '')
                        formatted_end_time = end_time.strftime('%I:%M%p').lstrip('0').replace(':00', '')

                        formatted_time_slots.append(f"{formatted_start_time} - {formatted_end_time}")

                        # Join the formatted time slots into a single string
                        formatted_current_day_hours  = ' | '.join(formatted_time_slots)

                    opening_hours_dict[day] = formatted_current_day_hours
        except:
            opening_hours_dict['Monday'] = 'Unknown'
            opening_hours_dict['Tuesday'] = 'Unknown'
            opening_hours_dict['Wednesday'] = 'Unknown'
            opening_hours_dict['Thursday'] = 'Unknown'
            opening_hours_dict['Friday'] = 'Unknown'
            opening_hours_dict['Saturday'] = 'Unknown'
            opening_hours_dict['Sunday'] = 'Unknown'
        
        print(opening_hours_dict)

        # Write to DynamoDB
        table.put_item(
            Item={
                'Geohash': GeohashBroad,
                'Name': name,
                'Address': address,
                'GeohashPrecise': GeohashPrecise,
                'Neighbourhood': neighbourhood,
                'Price': price,
                'Categories': categories,
                'Latitude': str(Coordinates[1]),
                'Longitude': str(Coordinates[0]),
                'Monday': opening_hours_dict['Monday'],
                'Tuesday': opening_hours_dict['Tuesday'],
                'Wednesday': opening_hours_dict['Wednesday'],
                'Thursday': opening_hours_dict['Thursday'],
                'Friday': opening_hours_dict['Friday'],
                'Saturday': opening_hours_dict['Saturday'],
                'Sunday': opening_hours_dict['Sunday']
                }
        )
        print ('Wrote to table')
    except Exception as error:
        print(f"Error occurred writing to dynamoDB table")
        print (error)
        return []

def main(category):
    base_url = 'https://www.burpple.com/search/sg?offset='
    category = category
    offset = 0
    limit = 7000
    print(category)

    while offset < limit:
        url = f'{base_url}{offset}&open_now=false&price_from=0&price_to=90&q={category}'
        while True:
            try:
                print ("Getting links for page " + str(url))
                Links = get_links(url)
                # url = Links[0]
                # print ("Next page = " + str(url))
                Restaurants = Links[1]
                for restaurant in Restaurants:
                    get_restaurant_info(restaurant)
                offset += 10  # Increment the offset value by 10 for the next page
                print (offset)
                break

            except:
                print("Error occurred")
                time.sleep(2)
                print ("Waited two seconds, retrying")

Categories = ["Burgers", "Cafes+%26+Coffee", "Chinese", "French", "Halal", "Hawker-fare", "Indian", "Italian", "Japanese", "Korean", "Malay", "Mediterranean", "Mexican", "Pasta", "Pizza", "Ramen", "Salads", "Spanish"]
for category in Categories:
    main(category)

# link = 'https://www.burpple.com/yoons-social-kitchen-by-yoons-traditional-teochew-kueh'
# get_restaurant_info(link)