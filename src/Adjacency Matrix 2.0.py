#!/usr/bin/env python
# coding: utf-8

# # Adjacency Matrix 1.1

# In[1]:


from collections import defaultdict
from getpass import getpass
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import pandas as pd
import pickle
from PIL import Image
import pymysql
import regex as re
import seaborn as sb
from sklearn.cluster import KMeans
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# ## Run these imports to skip the data import connector and pre-processing sections
# Uncomment as needed

# In[2]:


## to save time and not re-run the established portions of this notebook

## import saved csv
# ingredients = pd.read_csv('C://Users//KAA//Documents//offline//ingredients.csv')
# ingredients.head()
# ingredients_to_rids_df = pd.read_csv('C://Users//KAA//Documents//offline//ingredients_to_rids.csv',converters={'RECIPE_ID': pd.eval})
# display(ingredients_to_rids_df.head())
# rids_clean_ingredients_df = pd.read_csv('C://Users//KAA//Documents//offline//rids_clean_ingredients.csv')
# display(rids_clean_ingredients_df.head())

## import the pickle files
ingredients_to_rids_df = pd.read_pickle('C://Users//KAA//Documents//offline//ingredients_to_rids.pkl')
display(ingredients_to_rids_df.head())
rids_clean_ingredients_df = pd.read_pickle('C://Users//KAA//Documents//offline//rids_clean_ingredients.pkl')
display(rids_clean_ingredients_df.head())


# ## Connect to database for data import

# In[2]:


## get login info
u = input("Enter username: ")
p = getpass("Enter password: ")


# In[3]:


## Function to import each table
def retrieveTable(query):
    db_conn = pymysql.connect(
        user = u,
        password = p,
        host = "recipatornew.mysql.database.azure.com",
        port = 3306,
        db = "recipator_db",
        ssl_ca = "C://Users//KAA//austinka//GT//CSE6242 DVA//Project//DigiCertGlobalRootCA.crt.pem",
        ssl_disabled = False)
    table = pd.read_sql(query,db_conn)
    db_conn.close() # ALWAYS close the connection
    return table


# In[4]:


## import ingredients table
import_ingr = '''
    SELECT *
    FROM recipator_db.model_ingredients
'''

ingredients = retrieveTable(import_ingr)

# ingredients = pd.DataFrame(results)
display(ingredients.head())
ingredients.info()


# ## Save files for OFFLINE WORK
# Uncomment as needed

# In[6]:


## save to csv for working offline
# main.to_csv('C://Users//KAA//Documents//offline//main.csv', index=False)
# ingredients.to_csv('C://Users//KAA//Documents//offline//ingredients.csv', index=False)
# subs.to_csv('C://Users//KAA//Documents//offline//subs.csv', index=False)


# ## Clean and count the ingredients

# In[5]:


## make a custom stopwords list
## removing status of ingredient words, example (frozen, diced)
## removing adjectives, example (color, dry)
## only put in words that are 3 or more characters, as the code
## removes smaller words (2 chars or less) later
custom_stopwords = ['chopped','and','fresh','ground','white',
                    'sliced','minced','dried','optional','table',
                    'green','diced','shredded','red','drained',
                    'into','peeled','cut','brown','black',
                    'large','softened','frozen','grated','dry',
                    'house','firmly','skim','whole','all-purpose',
                    'dry','mix','melted','beaten','finely','yellow',
                    'cubed','cooked','medium','small','sauce',
                    'crushed','divided','thinly','boneless',
                    'bell','thawed','pieces','cubes','crust',
                    'light','save','follows','hearty','layered',
                    'pan-frying','good-quality','express','skinless',
                    'inch','heirloom','1/2"','rectangular','solid-pack',
                    'fiber','julienne-cut','2-1/2','colossal','tsp',
                    'equivalent','teaspoons','tub-style','southwest',
                    'flanken','outer','least','secret','yields',
                    'well-beaten','dente','','multi-colored','major',
                    'mrs','simply','racks','aisle','working',
                    'untrimmed','excuding','packed','circles','pick',
                    'carb','parboiled','pfs','pad','family-sized',
                    'lbs','meet','digestion','tbsp','leaves',
                    'bdg','national','arm','fairly','microwaved',
                    'diluted','starbucks','mist','lots','full-bodied',
                    'shape','shred','-in','shape','corkscrew','sun-dried',
                    'grate','-inch','per','washing','mist','toothpick',
                    'colour','canister','grillers','kerrygold','wish-bone',
                    'unripe','tempura','pre-packaged','tasting','hugs',
                    'except','fast-rising','length-wise','delightfulls',
                    'handfull','frying','<sup>&reg<sup>otel<sup>&reg<sup>','loose-pack',
                    'young', 'table', 'whites', 'halved', 'tenderloin', # PL start
                    'seedless', 'toasted', 'lean', 'self-rising', 'plain',
                    'sifted', 'skinned', 'unsalted', 'pre-washed', 'box',
                    'boxes', 'squares', 'unsweetened', 'irish', 'flavored',
                    'pink', 'ripe', 'pureed', 'spears', 'bottle', 'colored',
                    'bone-less', 'bob', 'evans®', 'removed', 'tops', 'and', 'squeezed',
                    'italian', 'zesty', 'hot', 'canadian', 'slightly', 'taste',
                    'meat', 'prepared', 'candy-coated', 'slices', 'firm', 'smooth',
                    'flank', 'thinly', 'aged', 'chunks', 'dice', 'trimmed', 'dark',
                    'crumbs', 'pitted', 'room', 'temperature', 'deveined', 'portobello',
                    'caps', 'pre-baked', 'such', 'boboli', 'low-sodium', 'instant', 'active',
                    'dry', 'bittersweet', 'rolled', 'semisweet', 'chips', 'canned', 'make',
                    'ahead', 'mix', 'jigger', 'split', 'roast', 'thick', 'chops', 'center',
                    'loin', 'cutlets', 'about', 'butt', 'bone-in', 'freshly', 'picked',
                    'gluten-free', 'vanilla-flavored', 'buckwheat', 'kraft', 'uncooked',
                    'russet', 'rinsed', 'serving', 'style', 'cans', 'halves', 'jumbo',
                    'confectioners', 'seeded', 'chuck', 'sweetened', 'casings', 'crumbled',
                    'quartered', 'soft', 'very', 'coarsely', 'cooled', 'pounded',
                    'even', 'thickness', 'whole-grain', 'head', 'broken', 'loosely',
                    'reduced-sodium', 'cored', 'florets', 'tails', 'containers',
                    'refrigerated', 'non-fat', 'cloves', 'hulled', 'salted', 'strips',
                    'shelled', 'shoulder', 'korean', 'chinese', 'gluten', 'free', 'round',
                    'raw', 'sirloin', 'asian', 'fillets', 'filet', 'basmati', 'warm', 'tips',
                    'liquid', 'picnic', 'belly', 'stale', 'skewers', 'pressed', 'crispy',
                    'quick', 'quick-cooking', 'torn', 'bite', 'size', 'bite-size', 'washed',
                    'blanched'
                   ]

for w in custom_stopwords:
    STOPWORDS.add(w)
print('There are',len(STOPWORDS),'stopwords.')


# In[6]:


## strip the phrases and parse the words
words_sets = ingredients["INGREDIENT"].str.split(' ').apply(lambda x: [re.sub('[,™()®;\*:.!?\'0-9#\/]','',n.strip().lower()) for n in x]).tolist()
nwords = len(words_sets)
print('Sample of word sets:\n',words_sets[:5])


# In[7]:


## make a set of cleaned words and count frequency
## full file count is millions of words before checking for duplicates
words = []
frequency = {}
word_count = 0
supressed = 0
for n in words_sets:
    for w in n:
        word_count +=1
        if w not in words and w not in STOPWORDS and len(w) > 2:
            words.append(w)
            frequency[w] = 1
        elif w in STOPWORDS or len(w) <= 2:
            supressed +=1
            pass
        elif w in words:
            frequency[w] +=1
        else:
            supressed +=1

print('There are',nwords,'ingredients listed having a total of',word_count,'words.')
print(len(words), 'unique words and', supressed, 'words supressed. That is', round(100*(supressed)/word_count,2),'% reduction!')


# In[8]:


## sort the list by frequency and remove words with extremely low frequency
minfreq = 10

freq_df = pd.DataFrame(frequency,index=[0]).transpose().sort_values(0,ascending=False)
freq_df = freq_df.drop(freq_df[freq_df[0] <= minfreq].index)
freq_df.rename({0:'frequency'},axis=1,inplace=True)

print('There are',len(freq_df), 'words with at least', minfreq+1, 'connections, which is an overall', round(100*(nwords-len(freq_df))/nwords,2),'% reduction')
print('\n\ntop of df\n',freq_df.head(5))
print('\nbottom of df\n',freq_df.tail(5))


# In[71]:


## map the ingredients to sets of recipes that use them
ingredients_to_rids = {}

for i in freq_df.index:
    rids = []
    for row in ingredients.itertuples(index=False):
        if i in row[2]: # 'INGREDIENTS'
            rids.append(row[0]) # 'RECIPE_ID'
    ingredients_to_rids[i] = rids
ingredients_to_rids_df = pd.DataFrame(ingredients_to_rids.items(),columns=['INGREDIENT','RECIPE_ID'])
    
print('length of ingredients_to_rids',len(ingredients_to_rids))
print('example of this data: number of recipes that include cumin',len(ingredients_to_rids['cumin']))
display(ingredients_to_rids_df.head())


# In[74]:


## set the ingredient as the index for future iteration
ingredients_to_rids_df.set_index('INGREDIENT', inplace=True)
# ingredients_to_rids_df.drop('Unnamed: 0',axis=1,inplace=True)
display(ingredients_to_rids_df.head())


# In[9]:


## find the recipes that contain these new cleaned words
rids_clean_ingredients = {}
# rid_clean_ingredients = pd.DataFrame(ingredients["RECIPE_ID"].tolist(),columns=['RECIPE_ID',freq_df.index.tolist()])

for row in ingredients.itertuples(index=False):
    ings = []
    for i in freq_df.index:
        if i in row[2]: # 'INGREDIENTS'
            # if using the df above, write code to put a 1 in the df at rid for the row and ingredient creating a sparse matrix
            ings.append(i) # this is for the dictionary method
    rids_clean_ingredients[row[0]] = ings
rids_clean_ingredients_df = pd.DataFrame(rids_clean_ingredients.items(),columns=['RECIPE_ID','INGREDIENT'])
    
print('length of rids_clean_ingredients',len(rids_clean_ingredients))
display(rids_clean_ingredients_df.head())


# In[76]:


## set the recipe_id as the index for future iteration
rids_clean_ingredients_df.set_index('RECIPE_ID', inplace=True)
# rids_clean_ingredients_df.drop('Unnamed: 0',axis=1,inplace=True)
display(rids_clean_ingredients_df.head())


# ## Save files for OFFLINE WORK
# Uncomment as needed

# In[77]:


## save to csv for offline access or quick import without rebuild
# ingredients_to_rids_df.to_csv('C://Users//KAA//Documents//offline//ingredients_to_rids.csv', index=True)
# rids_clean_ingredients_df.to_csv('C://Users//KAA//Documents//offline//rids_clean_ingredients.csv', index=True)

## save to pickle so that the list saves as list, not string
# ingredients_to_rids_df.to_pickle('C://Users//KAA//Documents//offline//ingredients_to_rids.pkl')
# rids_clean_ingredients_df.to_pickle('C://Users//KAA//Documents//offline//rids_clean_ingredients.pkl')


# ## Matrix build 2.0
# build from the ingredients to rids map

# In[86]:


# from ast import literal_eval

ing = ingredients_to_rids_df.iloc[:1,:]["RECIPE_ID"][0]#.tolist()
print(len(ing),ing[0])


# In[ ]:


## build the edges
edges = {}
weights = {}

for ingr,list_of_rids in ingredients_to_rids_df.iterrows():
    list_of_rids = list_of_rids[0]
    n = len(list_of_rids)-1 # minus one to correct for indexing beginning at 0
    #print(ingr,':',n,':',type(list_of_rids))
    #if n > 10000:
    #    print(ingr,':',n)
    while n > 1:
        n_minus_1 = n-1
        if (list_of_rids[n],list_of_rids[n_minus_1]) in edges.keys():
            weights[(list_of_rids[n],list_of_rids[n_minus_1])] += 1
        elif (list_of_rids[n_minus_1],list_of_rids[n]) in edges.keys():
            weights[(list_of_rids[n_minus_1],list_of_rids[n])] += 1
        else:
            edges[(list_of_rids[n],list_of_rids[n_minus_1])] = ingr
            weights[(list_of_rids[n],list_of_rids[n_minus_1])] = 1


# Error message:
# IOPub data rate exceeded.
# The notebook server will temporarily stop sending output
# to the client in order to avoid crashing it.
# To change this limit, set the config variable
# `--NotebookApp.iopub_data_rate_limit`.
# 
# Current values:
# NotebookApp.iopub_data_rate_limit=1000000.0 (bytes/sec)
# NotebookApp.rate_limit_window=3.0 (secs)

# In[ ]:


## save to pickle files because why not have it be food related? :)

with open('edges.pickle', 'wb') as handle:
    pickle.dump(edges, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('weights.pickle', 'wb') as handle:
    pickle.dump(weights, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('edges.pickle', 'rb') as handle:
    edges_pickle = pickle.load(handle)
with open('weights.pickle', 'rb') as handle:
    weights_pickle = pickle.load(handle)

print(edges == edges_pickle, weights == weights_pickle)


# In[ ]:





# In[ ]:





# ## Build the matrix from the method in DVA HW1

# In[28]:


## Define the Graph for the adjacency matrix

## using technique from HW1Q1 and
## https://algodaily.com/lessons/implementing-graphs-edge-list-adjacency-list-adjacency-matrix/python

class Graph:
    def __init__(self, edges, nodes):
        self.edges = []
        self.nodes = []
    def add_node(self, rid, ingredient) -> None:
        if (rid, ingredient) not in self.nodes:
            self.nodes.append((rid,ingredient))
        else:
            pass
        return
    
    def add_edge(self, source, target) -> None:
        if target == source:
            pass
        elif (source,target) not in self.edges and (target,source) not in self.edges:
            degree[(source, target)] = 1
            self.edges.append((source,target))
        else:
            try:
                d = degree[(source, target)]
                d += 1
                degree[(source, target)] = d
            except KeyError:
                d = degree[(target,source)]
                d+=1
                degree[(target,source)] = d
        return
    
    def total_nodes(self) -> int:
        return len(self.nodes)

    def total_edges(self) -> int:
        return len(self.edges)
    
    def write_edges_file(self, path="edges.csv")->None:
        edges_path = 'C://Users//KAA//Documents//offline//edges.csv'
        edges_file = open(edges_path, 'w', encoding='utf-8')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")

    def write_nodes_file(self, path="nodes.csv")->None:
        nodes_path = 'C://Users//KAA//Documents//offline//nodes.csv'
        nodes_file = open(nodes_path, 'w', encoding='utf-8')

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")


# In[58]:


## build graph from cleaned, unique ingredients list
## use freq_df words and find pairs of these words
## among the recipe ids in the ingredients df
## use ingredients_to_rids
graph = Graph(len(rids_clean_ingredients_df),len(rids_clean_ingredients_df))


def build_graph(ingredient, rid):
    ings = rids_clean_ingredients_df.loc[rids_clean_ingredients_df["RECIPE_ID"] == rid].tolist()
#     print(ings, rid)
    n = 0
    for index in len(ings):
        # get next ingredient
        ingredient = ings[n:n+1]
        # pair the ingredient with everything else in the recipe
        for i in ings:
            n+=1
            if i == ingredient:
                pass
            if (rid,i) not in graph.nodes: ### note to self: if 'i' only gets the first recipe for each ingredient
                graph.add_node(rid,i)
            if ((ingredient,i) not in graph.edges or (i,ingredient) not in graph.edges):
                graph.add_edge((ingredient, i))


# In[59]:


## test that elements are accessible correctly

n = '9999'
l = rids_clean_ingredients_df.loc[rids_clean_ingredients_df["RECIPE_ID"] == n]["INGREDIENT"].values.tolist()#.split#
l = [x for x in l[0]]
print(l[:2])


# In[60]:


subset = rids_clean_ingredients_df.head(10000)


# In[65]:


## this takes a looonngg time to run (like 30-60 minutes) on the full dataset
loops = 0
failures = []

subset = rids_clean_ingredients_df.head(10000)

while loops < 1:
    for n in rids_clean_ingredients_df["RECIPE_ID"]:
        try:
            i = subset.loc[subset["RECIPE_ID"] == n]["INGREDIENT"].values.tolist()
            i = [x for x in i[0]]
            if len(i) > 1:
#                 print('first ingredient of recipe number',n,'is',i[:1])
                for x in i:
                    build_graph(x,n)
        except:
            failures.append(n)
            pass
        
    loops += 1
print(len(failures), 'count of failed recipes')

print('graph has',graph.total_nodes(), 'nodes and', graph.total_edges(),'edges')


# In[63]:


## save the adjacency matrix!
graph.write_edges_file()
graph.write_nodes_file()


# In[64]:


print('graph has',graph.total_nodes(), 'nodes and', graph.total_edges(),'edges')


# ## THE MODEL

# In[ ]:


# kmeans = KMeans(n_clusters = 10)
# kmeans.fit(rids_clean_ingredients)


# In[ ]:


## technique from https://towardsdatascience.com/recommendation-system-in-python-lightfm-61c85010ce17

user_book_interaction = pd.pivot_table(interactions_selected, index='user_id', columns='book_id', values='rating')
# fill missing values with 0
user_book_interaction = user_book_interaction.fillna(0)
user_id = list(user_book_interaction.index)
user_dict = {}
counter = 0 
for i in user_id:
    user_dict[i] = counter
    counter += 1
# convert to csr matrix
user_book_interaction_csr = csr_matrix(user_book_interaction.values)
user_book_interaction_csr


# In[ ]:


## technique from https://towardsdatascience.com/recommendation-system-in-python-lightfm-61c85010ce17

model = LightFM(loss='warp',
                random_state=2016,
                learning_rate=0.90,
                no_components=150,
                user_alpha=0.000005)
model = model.fit(user_book_interaction_csr,
                  epochs=100,
                  num_threads=16, verbose=False)


# In[ ]:


## technique from https://towardsdatascience.com/recommendation-system-in-python-lightfm-61c85010ce17

def sample_recommendation_user(model, interactions, user_id, user_dict, 
                               item_dict,threshold = 0,nrec_items = 5, show = True):
    
    n_users, n_items = interactions.shape
    user_x = user_dict[user_id]
    scores = pd.Series(model.predict(user_x,np.arange(n_items), item_features=books_metadata_csr))
    scores.index = interactions.columns
    scores = list(pd.Series(scores.sort_values(ascending=False).index))
    
    known_items = list(pd.Series(interactions.loc[user_id,:]                                  [interactions.loc[user_id,:] > threshold].index).sort_values(ascending=False))
    
    scores = [x for x in scores if x not in known_items]
    return_score_list = scores[0:nrec_items]
    known_items = list(pd.Series(known_items).apply(lambda x: item_dict[x]))
    scores = list(pd.Series(return_score_list).apply(lambda x: item_dict[x]))
    if show == True:
        print ("User: " + str(user_id))
        print("Known Likes:")
        counter = 1
        for i in known_items:
            print(str(counter) + '- ' + i)
            counter+=1
print("\n Recommended Items:")
        counter = 1
        for i in scores:
            print(str(counter) + '- ' + i)
            counter+=1


# In[ ]:





# In[ ]:





# In[ ]:





# ## Word clouds for fun

# In[ ]:


## ref: https://towardsdatascience.com/generate-meaningful-word-clouds-in-python-5b85f5668eeb


# In[ ]:


STOPWORDS.add('white')
STOPWORDS.add('purpose')
STOPWORDS.add('chopped')

text = []
for i in ingredients["INGREDIENT"]:
    text.append(i)

text = ' '.join(text).lower()

wordcloud = WordCloud(stopwords = STOPWORDS, collocations = True).generate(text)

plt.imshow(wordcloud, interpolation='bilInear')
plt.axis('off')
plt.figure(figsize=(12,10))
plt.show()


# In[ ]:


text = []
for i in rids_clean_ingredients_df["INGREDIENT"]:
    text.append(i)

text = ' '.join(text).lower()

wordcloud = WordCloud(stopwords = STOPWORDS, collocations = True).generate(text)

plt.imshow(wordcloud, interpolation='bilInear')
plt.axis('off')
plt.figure(figsize=(12,10))
plt.show()

