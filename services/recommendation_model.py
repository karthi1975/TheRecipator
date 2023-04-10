import mysql.connector
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer

# Establish a connection with the MySQL server
cnx = mysql.connector.connect(
    user='recipator',
    password='Banana@Bread',
    host='recipatornew.mysql.database.azure.com',
    port=3306,
    database='recipator_db',
    ssl_ca='DigiCertGlobalRootCA.crt.pem'
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

print(recipe_df.columns)

# JULIO
# recipe_df column names:
# Index(['RECIPE_ID', 'URL', 'TITLE', 'IMAGE', 'INGREDIENTS', 'DIRECTIONS',
#        'SUBMITTER', 'DESCRIPTION', 'CATEGORIES', 'NUM_RATINGS', 'NUM_STARS',
#        'PREP_TIME', 'READY_IN', 'NUM_SERVINGS', 'NUTRITIONAL_FACTS',
#        'TITLE_DESC'],
#       dtype='object')


# JULIO
# Get substitute df

subsquery = 'SELECT * FROM ingredient_substitutions'
subs_df = pd.read_sql(subsquery, con=cnx)

# ingredient_substitutions
# Index(['Ingredient', 'Amount', 'Substitution1', 'Substitution2',
#        'Substitution3', 'Substitution4', 'Substitution5', 'Substitution6'],
#       dtype='object')
