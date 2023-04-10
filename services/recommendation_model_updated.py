import time
import pickle
import os
import random
import networkx as nx
import community as community_louvain
import pandas as pd
import numpy as np
import mysql.connector

random.seed(101)

def get_recipe_recommendations(edges_pickle, desired_ingredients, excluded_ingredients):


    # parse strings from user
    ui = desired_ingredients.split(' ')
    bad_list = excluded_ingredients.split(' ')
    print('inclusions:', ui, ' vs. exclusions:', bad_list)

    # match ui to indices of edges aka nodes
    edges_matching_ui = []

    # get the full set of recipes and remove recipes with bad ingredients
    for n in range(len(ui)):
        match_one = [k for k, v in edges_pickle.items() if v == ui[0] and v not in bad_list]
        if len(ui) < 2:
            edges_matching_ui = match_one
        else:
            match_more = [k for k, v in edges_pickle.items() if v == ui[n] and v not in bad_list]
            new_matches = (list(set(match_one).intersection(match_more)))
            edges_matching_ui.extend(new_matches)

    # time the execution
    start_time = time.time()

    G = nx.Graph()
    G.add_edges_from(edges_matching_ui)

    # return partition type = dict
    partition = community_louvain.best_partition(G)

    # Get recipe ids
    recipe_ids = []
    for n in set(partition.values()):
        matching_recipes = [k for k, v in partition.items() if v == n]
        recipe_ids.append(random.choice(matching_recipes))

    #print("Recipe Ids :",recipe_ids)
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
    cursor = cnx.cursor()

    if not recipe_ids:
        print("No recipe IDs found. Exiting.")
        return []



    recipe_ids_str = ', '.join([str(recipe_id) for recipe_id in recipe_ids])
    query = f'SELECT * FROM recipator_db.base_table_clean WHERE RECIPE_ID IN ({recipe_ids_str});'
    print("Query:", query)
    cursor.execute(query)

    # Load results into a Pandas DataFrame
    colnames = cursor.column_names
    rows = cursor.fetchall()
    recipe_df = pd.DataFrame(rows, columns=colnames)

    # Close MySQL connection
    cursor.close()
    cnx.close()

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
    return recommended_recipes
# # import the matrix pickle files
# with open(os.getcwd()+'/offline/edges.pickle', 'rb') as handle:
#     edges_pickle = pickle.load(handle)
# ## Example usage
# user_ing = input('Enter desired ingredients: ')
# remove = input('Recipe cannot include: ')
# get_recipe_recommendations(edges_pickle,user_ing, remove)
