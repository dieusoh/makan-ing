# data = [
#     {"name": "John", "age": 30, "gender": "Male"},
#     {"name": "Alice", "age": 25},
#     {"name": "Bob", "age": 35, "gender": "Male"}
# ]

# # Using a loop to format dictionaries as strings with numbers
# formatted_data = []
# for i, item in enumerate(data, 1):
#     formatted_item = f"{i}. Name: {item['name']}\n Age: {item['age']}"
#     if 'gender' in item:
#         formatted_item += f"\n Gender: {item['gender']}"
#     formatted_data.append(formatted_item)

# # Joining the formatted strings with newline characters
# result_string = "\n".join(formatted_data)

# print(result_string)

output_list = [
    {"Name": "IKURA Japanese (West Coast Plaza)", "Address": "154 West Coast Road #B1-48 West Coast Plaza Singapore 127371"},
    {"Name": "Artea (Galaxis)", "Address": "1 Fusionopolis Place #01-27 Galaxis Singapore 138522"},
    {"Name": "CRAVE Nasi Lemak (The Star Vista)", "Address": "1 Vista Exchange Green #B1-42 The Star Vista Singapore 138617"},
    {"Name": "The Soup Spoon Union (The Metropolis)", "Address": "9 North Buona Vista Drive #01-05 The Metropolis Singapore 138588", "Price": "~$15/pax"},
    {"Name": "iSTEAKS Diner (The Star Vista)", "Address": "1 Vista Exchange Green #01-42/K3 The Star Vista Singapore 138617", "Price": "~$25/pax"}
]
formatted_data = ""
for i, restaurant in enumerate(output_list, 1):
    formatted_data += f"{i}.{restaurant['Name']}\n"
    formatted_data += f"Address: {restaurant['Address']}\n"
    if 'Price' in restaurant:
        formatted_data += f"Price: {restaurant['Price']}\n"
    formatted_data += "\n"  # Add a blank line between restaurants
print(formatted_data)