import geohash2
import boto3
ddb = boto3.resource('dynamodb', region_name='ap-southeast-1')
table = ddb.Table('Locations')


current_location = geohash2.encode(1.3112533293915378, 103.76847867934113, precision = 6)

RoastMeat = geohash2.encode(1.3095710525476265, 103.76842114765549, precision = 5)

EastCoastLagoon = geohash2.encode(1.3069658396726995, 103.93497117830118, precision = 5)

ChickBoySingapore = geohash2.encode(1.3100134832743762, 103.76890353686379, precision = 5)

IpohOldStreetBanMian = geohash2.encode(1.3095267895332008, 103.76837111837516, precision = 5)

food_places = {"East Coast Lagoon Food Village": EastCoastLagoon, "Ipoh Old Street Roast Meat": RoastMeat, "Chick Boy Singapore": ChickBoySingapore, "Ipoh Old Street Ban Mian": IpohOldStreetBanMian}

# print ("464A is " + str(current_location))
# print ("RoastMeat is " + str(RoastMeat))
# print ("EastCoastLagoon is " + str(EastCoastLagoon))

for i in food_places:
    table.put_item(
        Item={
            'Geohash': food_places[i],
            'Name': i
        }
    )