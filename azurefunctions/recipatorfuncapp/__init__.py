import azure.functions as func
import logging
import mysql.connector
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Establish a connection with the MySQL server
cnx = mysql.connector.connect(
    user='recipator',
    password='Banana@Bread',
    host='recipatornew.mysql.database.azure.com',
    port=3306,
    database='recipator_db'
)

# Load the recipe data from the MySQL database using the connection object
query = 'SELECT * FROM recipes_main'
recipe_df = pd.read_sql(query, con=cnx)

# Remove any rows with missing values in the ingredients column
recipe_df = recipe_df.dropna(subset=['INGREDIENTS'])

# Convert data types of numerical columns
recipe_df['NUM_RATINGS'] = pd.to_numeric(recipe_df['NUM_RATINGS'], errors='coerce')
recipe_df['NUM_STARS'] = pd.to_numeric(recipe_df['NUM_STARS'], errors='coerce')
recipe_df['PREP_TIME'] = pd.to_numeric(recipe_df['PREP_TIME'], errors='coerce')
recipe_df['READY_IN'] = pd.to_numeric(recipe_df['READY_IN'], errors='coerce')
recipe_df['NUM_SERVINGS'] = pd.to_numeric(recipe_df['NUM_SERVINGS'], errors='coerce')

# Create a new feature by combining the recipe title and description
recipe_df['TITLE_DESC'] = recipe_df['TITLE'] + ' ' + recipe_df['DESCRIPTION']

# Vectorize the recipe ingredients and directions using CountVectorizer
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(recipe_df['INGREDIENTS'] + ' ' + recipe_df['TITLE_DESC'])

# Train k-NN models for both ingredients and title+description
knn_ingredients = NearestNeighbors(metric='cosine', algorithm='brute')
knn_ingredients.fit(X)

knn_title_desc = NearestNeighbors(metric='cosine', algorithm='brute')
knn_title_desc.fit(X)


@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the list of ingredients from the HTTP request
    ingredients = request.json['ingredients']

    # Vectorize the input ingredients using CountVectorizer
    input_vector = vectorizer.transform([ingredients])

    # Convert the input vector to a numpy array
    input_array = np.asarray(input_vector.todense())

    # Find the nearest neighbors for the input ingredients using k-NN
    distances_ingredients, indices_ingredients = knn_ingredients.kneighbors(input_array, n_neighbors=10)
    distances_title_desc, indices_title_desc = knn_title_desc.kneighbors(input_array, n_neighbors=10)

    # Combine the results from both models and return the recommended recipes
    recommended_indices = set(indices_ingredients[0]) | set(indices_title_desc[0])
    recommended_recipes = recipe_df.loc[recommended_indices, 'TITLE'].tolist()

    return jsonify({'recipes': recommended_recipes})


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return app(req.environ['REQUEST_METHOD'], req)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    print('The app is running on http://localhost:5000/')
