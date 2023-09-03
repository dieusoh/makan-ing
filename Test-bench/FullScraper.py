import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urljoin
import boto3
import geohash2
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')
als = boto3.client('location')

Categories = ["Japanese", "Chinese", "Desserts", "French", "Western", "Malay", "Breakfast+%26+Brunch"]

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

    # link for the next page
    more_options = [link for link in links if link.startswith("https://www.burpple.com/search/sg?offset")]

    # Filter links to remove nonburpple links
    filtered_links = [link for link in links if link.startswith("https://www.burpple.com")]

    # Filter links to remove useless subdomains starting with "beyond" and "categories"
    filtered_links = [link for link in filtered_links if not link.startswith("https://www.burpple.com/neighbourhoods") and not link.startswith("https://www.burpple.com/categories") if not link.startswith("https://www.burpple.com/list/") if not link.startswith("https://www.burpple.com/f/") if not link.startswith("https://www.burpple.com/@") if not link.startswith("https://www.burpple.com/about-us") if not link.startswith("https://www.burpple.com/newsroom")  if not link.startswith("https://www.burpple.com/careers") if not link.startswith("https://www.burpple.com/terms") if not link.startswith("https://www.burpple.com/search") if not link.startswith("https://www.burpple.com/features") if not link.startswith("https://www.burpple.com/sg/mobile") if not link.startswith("https://www.burpple.com/sg/beyond") if not link.startswith("https://www.burpple.com/sg/advertise") if not link.startswith("https://www.bites.burpple.com")]

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

        #         # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(webpage, 'html.parser')
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

        ## Find categories
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

        ## Geocode address
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

        # write to DynamoDB
        table.put_item(
            Item={
                'Geohash': GeohashBroad,
                'Name': name,
                'Address': address,
                'GeohashPrecise': GeohashPrecise,
                'Neighbourhood': neighbourhood,
                'Categories': categories,
                'Primary category': 'French'
            }
        )
    except:
        print(f"Error occurred")
        return []


## Main function

# url = "https://www.burpple.com/search/sg?q=Breakfast+%26+Brunch"
base_url = 'https://www.burpple.com/search/sg?offset='
category = 'Breakfast+%26+Brunch'
offset = 0
limit = 2500  # Set the limit of results you want to scrape

while offset < limit:
    url = f'{base_url}{offset}&open_now=false&price_from=0&price_to=90&q={category}'
    try:
        print ("Getting links for page " + str(url))
        Links = get_links(url)
        # url = Links[0]
        # print ("Next page = " + str(url))
        Restaurants = Links[1]
        for restaurant in Restaurants:
            get_restaurant_info(restaurant)
        offset += 12  # Increment the offset value by 12 for the next page
        print (offset)

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        break
