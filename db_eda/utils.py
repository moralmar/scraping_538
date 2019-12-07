import sqlite3
import os
import json
from pandas.io.json import json_normalize
import pandas as pd
import networkx as nx
import imageio
import matplotlib.pyplot as plt


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn


def create_folder(foldername):
    """define the name of the directory to be created"""
    try:  
        os.mkdir(foldername)
    except OSError:  
        print ("Creation of the directory %s failed" % foldername)
    else:  
        print ("Successfully created the directory %s " % foldername)

        
def create_gif(folder_name_pngs, folder_name_gif, filenames_pngs, duration):
    """"""
    images = []
    for filename in filenames_pngs:
        images.append(imageio.imread(folder_name_pngs + '/' + filename))
    imageio.mimsave(folder_name_gif + '/seq_movie.gif', images, duration = duration)
    

def get_topic_df(path, modus, subset_records=100):
    """"""
    # list of files
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    if modus=='SUBSET':
        onlyfiles = onlyfiles[0:subset_records]
            
    data = pd.DataFrame()
    for file in onlyfiles:
        with open(os.path.join(path, file)) as json_file:
            datatemp = json.load(json_file)
        datanorm = json_normalize(datatemp['response']['topics'])
        datanorm['file_name'] = file
        datanorm['PK_ID_CLEAN'] = file.split('_')[0]
        data = data.append(datanorm)
    return data


def create_spring_layout(data, club_col, person_col, iteration=50, seed=None, modus='SHOW', folder_name_pngs='', fig_save_name=''):
    """"""
    # Prep
    # -------
    # Make a list of the clubs, we'll use it later
    club_list = list(data[club_col].unique())
    
    # Make a list of the people, we'll use it later
    people_list = list(data[person_col].unique())
    
    # Figure
    # --------
    plt.figure(figsize=(12, 12))
    # 1. Create the graph
    # g = nx.from_pandas_dataframe(data, source=person_col, target=club_col)  << old
    g = nx.from_pandas_edgelist(data, source=person_col, target=club_col)
    # 2. Create a layout for our nodes 
    layout = nx.spring_layout(g, iterations=iteration, seed=seed)
    # 3. Draw the parts we want
    # Edges thin and grey
    # People small and grey
    # Clubs sized according to their number of connections
    # Clubs blue
    # Labels for clubs ONLY
    # People who are highly connected are a highlighted color

    # Go through every club name, ask the graph how many
    # connections it has. Multiply that by 80 to get the circle size
    club_size = [g.degree(club) * 30 for club in club_list]
    nx.draw_networkx_nodes(g, 
                           layout, 
                           nodelist=club_list, 
                           node_size=club_size, # a LIST of sizes, based on g.degree
                           node_color='lightblue', 
                           alpha=0.3)
    # Draw EVERYONE
#     nx.draw_networkx_nodes(g, layout, nodelist=people_list, node_color='#cccccc', node_size=100)
    # Draw POPULAR PEOPLE
    popular_people = [person for person in people_list if g.degree(person) > 1]
    nx.draw_networkx_nodes(g, 
                           layout, 
                           nodelist=popular_people, 
                           node_color='orange', 
                           node_size=100, 
                           alpha=0.8)
    nx.draw_networkx_edges(g, 
                           layout, 
                           width=0.3, 
                           edge_color="#cccccc")
    node_labels = dict(zip(club_list, club_list))
    # nx.draw_networkx_labels(g, layout, labels=node_labels)
    # 4. Turn off the axis because I know you don't want it
    plt.axis('off')
    plt.title("Topic Clustering")
    # 5. Tell matplotlib to show it
    if modus=='SHOW':
        plt.show()
    elif modus=='SAVEPLOT':
        plt.savefig(folder_name_pngs + '/' + str(fig_save_name) + '.png')