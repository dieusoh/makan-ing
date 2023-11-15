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

url="https://www.burpple.com/baste"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
web_byte = urlopen(req).read()

webpage = web_byte.decode('utf-8')
# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(webpage, 'html.parser')


# Find the opening hours section
opening_hours_section = soup.find('div', class_='venue-details__item--opening')

# Find the opening hours header
opening_hours_header = opening_hours_section.find('div', class_='venueInfo-details-header-item-header--openingHours')

# Find the hidden div containing all days' opening hours
hidden_div = opening_hours_section.find('div', id='venueInfo-details-header-item-body-hidden-openingHours')

# Extract the opening hours from all days
days_and_hours = re.findall(r'(\w+):\s*((?:\d{1,2}:\d{2}[apm]+\s*-\s*\d{1,2}:\d{2}[apm]+\s*)+|Closed)', hidden_div.get_text())
# print (days_and_hours)


# Extract the current day's opening hours
current_day_opening_hours = opening_hours_section.find('p').get_text()
current_day_match = re.search(r'0?(\w+):\s*((?:\d{1,2}:\d{2}[apm]+\s*-\s*\d{1,2}:\d{2}[apm]+\s*)+|Closed)', current_day_opening_hours)

# Initialize an empty dictionary to store the opening hours for each day
opening_hours_dict = {}

# Display the results
if current_day_match:
    current_day, current_day_hours = current_day_match.groups()
    if current_day_hours == 'Closed':
        print(f"{current_day}: Closed")
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
                
        print(f"{current_day}: {formatted_current_day_hours.replace('<br/>', ' | ')}")
        opening_hours_dict[current_day] = formatted_current_day_hours

for day, opening_hours in days_and_hours:
    if opening_hours == 'Closed':
        formatted_hours = 'Closed'
        print(f"{day}: {formatted_hours}")
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
                
        print(f"{day}: {formatted_current_day_hours.replace('<br/>', ' | ')}")
        opening_hours_dict[day] = formatted_current_day_hours

print (opening_hours_dict)
