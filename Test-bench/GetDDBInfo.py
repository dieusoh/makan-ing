import boto3
import csv
import os

## For windows client
# session = boto3.Session(profile_name='makaning')

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='ap-southeast-1')

# Initialize the S3 client
s3 = boto3.client('s3', region_name='ap-southeast-1')

# Define your DynamoDB table name
table_name = 'Locations'

# Define your S3 bucket name and CSV file name
csv_file_name = 'YourExportedFile.csv'
current_directory = os.getcwd()
csv_file_path = os.path.join(current_directory, csv_file_name)

# Define the specific category you want to filter for
desired_category = 'Chinese'  # Change this to your desired category


# Query DynamoDB and retrieve all items
response = dynamodb.scan(TableName=table_name)

# Extract the items from the response
items = response['Items']

# Define the CSV field names based on the DynamoDB item keys
field_names = []
for item in items:
    for key in item.keys():
        if key not in field_names:
            field_names.append(key)
    # print (item)

# Prepare the CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
    csv_writer.writeheader()

    # Write items to the CSV file for the "Cafes & Coffee" category
    for item in items:
        categories = [c['S'] for c in item.get('Categories', {}).get('L', [])]  # Extract categories as a list of strings
        if desired_category in categories:
            csv_writer.writerow({field: item.get(field, '') for field in field_names})
print(f'Data exported to local CSV file for category: {desired_category}')