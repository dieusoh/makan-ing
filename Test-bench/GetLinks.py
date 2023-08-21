import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urljoin

url="https://www.burpple.com/search/sg?q=Cafes+%26+Coffee"
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
more_options = [link for link in links if link.startswith("https://www.burpple.com/search")]
                
print (more_options)

# Filter links to remove nonburpple links
filtered_links = [link for link in links if link.startswith("https://www.burpple.com")]

# Filter links to remove useless subdomains starting with "beyond" and "categories"
filtered_links = [link for link in links if not link.startswith("https://www.burpple.com/neighbourhoods") and not link.startswith("https://www.burpple.com/categories") if not link.startswith("https://www.burpple.com/list/") if not link.startswith("https://www.burpple.com/f/") if not link.startswith("https://www.burpple.com/@") if not link.startswith("https://www.burpple.com/about-us") if not link.startswith("https://www.burpple.com/newsroom")  if not link.startswith("https://www.burpple.com/careers") if not link.startswith("https://www.burpple.com/terms") if not link.startswith("https://www.burpple.com/search") if not link.startswith("https://www.burpple.com/features") if not link.startswith("https://www.burpple.com/sg/mobile") if not link.startswith("https://www.burpple.com/sg/beyond") if not link.startswith("https://www.burpple.com/sg/advertise") if not link.startswith("https://www.bites.burpple.com")]

unique_links = list(set(filtered_links))

print("All Links:")
for link in unique_links:
    print(link)