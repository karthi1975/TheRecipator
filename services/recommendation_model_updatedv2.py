import time
import pickle
import os
import random
import networkx as nx
import community as community_louvain
import pandas as pd
import numpy as np
import mysql.connector
from concurrent.futures import ThreadPoolExecutor

random.seed(101)

def get_mysql_data(recipe_ids):
    # Connect to MySQL database
    cnx = mysql.connector.connect(
        user='recipator',
        password='Banana@Bread',
        host='recipatornew.mysql.database.azure.com',
        port=3306,
        database='recipator_db',
        ssl_ca='DigiCertGlobalRootCA.crt.pem'
    )

    # Get recipe details
    cursor = cnx.cursor(prepared=True)
    recipe_ids_str = ', '.join([str(recipe_id) for recipe_id in recipe_ids])
    query = f'SELECT * FROM recipator_db.base_table_clean WHERE RECIPE_ID IN ({recipe_ids_str});'
    cursor.execute(query)

    # Load results into a Pandas DataFrame
    colnames = cursor.column_names
    rows = cursor.fetchall()
    recipe_df = pd.DataFrame(rows, columns=colnames)

    # Close MySQL connection
    cursor.close()
    cnx.close()

    return recipe_df

def get_recipe_recommendations(edges_pickle, desired_ingredients, excluded_ingredients):
    # parse strings from user
    ui = desired_ingredients.split(' ')
    bad_list = excluded_ingredients.split(' ')
    print('inclusions:', ui, ' vs. exclusions:', bad_list)

    # Find matching edges and build the graph
    G = nx.Graph()
    for edge, ingredient in edges_pickle.items():
        if ingredient in ui and ingredient not in bad_list:
            G.add_edge(*edge)

    # time the execution
    start_time = time.time()

    # return partition type = dict
    partition = community_louvain.best_partition(G)

    # Get recipe ids
    recipe_ids = []
    for n in set(partition.values()):
        matching_recipes = [k for k, v in partition.items() if v == n]
        recipe_ids.append(random.choice(matching_recipes))

    # Parallelize MySQL query
    with ThreadPoolExecutor(max_workers=1) as executor:
        recipe_df_future = executor.submit(get_mysql_data, recipe_ids)
        recipe_df = recipe_df_future.result()

    # Filter and format recommendations
    recommended_recipes = []
    for recipe_id in recipe_ids:
        filtered_recipe_df = recipe_df.loc[recipe_df['RECIPE_ID'] == recipe_id]
        if not filtered_recipe_df.empty:
            recipe = filtered_recipe_df.iloc[0]
            if not any(excluded.lower() in recipe['INGREDIENTS'].lower() for excluded in excluded_ingredients.split()):
                recommended_recipes.append({
                    'title': recipe['TITLE'],
                    'description': recipe['DESCRIPTION'],
                    'ingredients': recipe['INGREDIENTS'],
                    'directions': recipe['DIRECTIONS'],
                    'image': recipe['URL']
                })

    # Shuffle the recommended_recipes list
    random.shuffle(recommended_recipes)

    # Return only the first 10 recipes
    recommended_recipes = recommended_recipes[:10]


    # Print recommendations and execution time
    print('List of recommended recipes:\n', recommended_recipes)
    print('\nThis function took', round(time.time() - start_time, 2), 'seconds to run.')

# import the matrix pickle files
with open(os.getcwd()+'/offline/edges.pickle', 'rb') as handle:
    edges_pickle = pickle.load(handle)

# Example usage
user_ing = input('Enter desired ingredients: ')
remove = input('Recipe cannot include: ')
get_recipe_recommendations(edges_pickle, user_ing, remove)
