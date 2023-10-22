import boto3

als = boto3.client('location')

## function that is given the user's curreent coordinates and the restaurant's coordinates and is calculates the time taken to walk between them. 

def food_distance (user_lat, user_long, restaurant_lat, restaurant_long):
    response = als.calculate_route(
        CalculatorName = 'GrabCalculator',
        DeparturePosition=[user_long, user_lat],
        DestinationPosition=[restaurant_long, restaurant_lat],
        TravelMode='Walking'
    )
    print (response)
    Distance = response['Summary']['Distance']
    Duration = response['Summary']['DurationSeconds']
    return [Duration, Distance]

user_lat = 1.3137922364061911
user_long = 103.76257464133185
restaurant_lat = 1.3122856851787625
restaurant_long = 103.76777670497655
print (food_distance(user_lat, user_long, restaurant_lat, restaurant_long))