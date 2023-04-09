import requests

url = 'http://localhost:5000/recommend'
ingredients = 'chicken tomato onion garlic ginger'

response = requests.post(url, json={'ingredients': ingredients})

# {"ingredients":"beef cauliflower","amt":"1 pound","exclude":"gluten milk","substitue":"gluten free rice "}

print(response.json())
