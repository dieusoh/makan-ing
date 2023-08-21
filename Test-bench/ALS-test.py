import boto3

als = boto3.client('location')

response = als.search_place_index_for_text(
    BiasPosition=[
        1.312090, 103.768012
        ],
    FilterCategories=[
        'Restaurant',
    ],
    IndexName='kevin-test-index',
    Language='en',
    MaxResults=5,
    Text='Singapore'

    )
 
print (response)