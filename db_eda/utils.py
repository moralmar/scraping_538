import sqlite3
import os
import json
from pandas.io.json import json_normalize
import pandas as pd


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


def get_topic_df(path, modus):
    """"""
    # list of files
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    if modus=='SUBSET':
        onlyfiles = onlyfiles[0:100]
            
    data = pd.DataFrame()
    for file in onlyfiles:
        with open(os.path.join(path, file)) as json_file:
            datatemp = json.load(json_file)
        datanorm = json_normalize(datatemp['response']['topics'])
        datanorm['file_name'] = file
        datanorm['PK_ID_CLEAN'] = file.split('_')[0]
        data = data.append(datanorm)
    return data