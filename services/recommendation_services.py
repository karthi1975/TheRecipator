from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation_model import knn_ingredients, knn_title_desc, recipe_df, vectorizer
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the list of ingredients from the HTTP request
    # ingredients = request.json['ingredients']
    ingredients = request.json['include']
    excluded_ingredients = request.json['exclude']

    # Vectorize the input ingredients using CountVectorizer
    # input_vector = vectorizer.transform([ingredients])
    #
    # # Convert the input vector to a numpy array
    # input_array = np.asarray(input_vector.todense())

    # Vectorize the input ingredients and excluded ingredients using CountVectorizer
    input_vector = vectorizer.transform([ingredients])
    excluded_vector = vectorizer.transform([excluded_ingredients])

    # Convert the input vector and excluded vector to numpy arrays
    input_array = np.asarray(input_vector.todense())
    excluded_array = np.asarray(excluded_vector.todense())

    # Find the nearest neighbors for the input ingredients using k-NN
    # distances_ingredients, indices_ingredients = knn_ingredients.kneighbors(input_array, n_neighbors=10)
    # distances_title_desc, indices_title_desc = knn_title_desc.kneighbors(input_array, n_neighbors=10)

##

    # Find the nearest neighbors for the input ingredients using k-NN
    # distances_ingredients, indices_ingredients = knn_ingredients.kneighbors(input_array, n_neighbors=10)

    ##

    # # Combine the results from both models and return the recommended recipes
    # recommended_indices = set(indices_ingredients[0]) | set(indices_title_desc[0])
    # recommended_recipes = recipe_df.loc[recommended_indices, 'TITLE'].tolist()
    #
    # return jsonify({'recipes': recommended_recipes})

   # Find the nearest neighbors for the input ingredients using k-NN
    distances_ingredients, indices_ingredients = knn_ingredients.kneighbors(input_array, n_neighbors=10)

    # Combine the results from both models and return the recommended recipes
    recommended_indices = set(indices_ingredients[0])
    recommended_recipes = []
    for index in recommended_indices:
        recipe = recipe_df.iloc[index]
        if not any(excluded in recipe['INGREDIENTS'].lower() for excluded in excluded_ingredients.split()):
            recommended_recipes.append({
                'title': recipe['TITLE'],
                'description': recipe['DESCRIPTION'],
                'ingredients': recipe['INGREDIENTS'],
                'directions': recipe['DIRECTIONS'],
                'image': recipe['IMAGE']
            })

    return jsonify({'recipes': recommended_recipes})



def substitute():
    # Get the substitute ingredient from the HTTP request
    singredient = request.json['subsIngredient']

    recommended_substitutes = recipe_df.loc[singredient, 'Original Ingredient']

    return jsonify({'substitutes': recommended_substitutes})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
    
    print('The app is running on http://localhost:5001/')

