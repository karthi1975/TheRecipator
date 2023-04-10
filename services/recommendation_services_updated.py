from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation_model_updated import get_recipe_recommendations
import os
import pickle

app = Flask(__name__)
CORS(app)

# Load edges pickle at the start of the Flask server
with open(os.getcwd() + '/offline/edges.pickle', 'rb') as handle:
    edges_pickle = pickle.load(handle)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the list of ingredients and excluded ingredients from the HTTP request
    ingredients = request.json['include']
    excluded_ingredients = request.json['exclude']

    # Call the get_recipe_recommendations function
    recommended_recipes = get_recipe_recommendations(edges_pickle, ingredients, excluded_ingredients)
    print("Result : ",jsonify({'recipes': recommended_recipes}))
    return jsonify({'recipes': recommended_recipes})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
    print('The app is running on http://localhost:5001/')
