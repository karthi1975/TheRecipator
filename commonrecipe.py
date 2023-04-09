import requests
from bs4 import BeautifulSoup

url = "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"
response = requests.get(url)
html_content = response.content

# Use Beautiful Soup to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the ingredients list elements
ingredients = soup.find_all('li', class_='mntl-structured-ingredients__list-item')

# Extract the quantity, unit, and name of each ingredient
for ingredient in ingredients:
    quantity = ingredient.find('span', {'data-ingredient-quantity': 'true'}).text
    unit = ingredient.find('span', {'data-ingredient-unit': 'true'}).text
    name = ingredient.find('span', {'data-ingredient-name': 'true'}).text
    print(f"{quantity} {unit} {name}")