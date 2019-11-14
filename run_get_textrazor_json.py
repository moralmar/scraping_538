import config
import utils
import time
import re
import json
import logging
import pandas as pd
import textrazor

now_str = time.strftime('%Y%m%d_%H%M%S')
FILENAME_lOG = 'log/' + now_str + 'get_textrazor_json.txt'
utils.start_logging(FILENAME_lOG)
NUMBER_OF_RECORDS = 20

logging.info('*'*30 + '\nGET Text_Razor JSON - START\n' + '*'*30)

# get data
conn = utils.create_connection('scraping538.db')
query = "SELECT * FROM ARTICLES_538 LIMIT {a}".format(a=NUMBER_OF_RECORDS)
articles_all = pd.read_sql(query, con=conn)
logging.info('Number of records (for which to get the JSON): {a}'.format(a=articles_all.shape[0]))
# text razor config
textrazor.api_key = config.TEXT_RAZOR_API_KEY
client = textrazor.TextRazor(extractors=['entailments', 'relations', 'dependency-trees', "entities", "topics", "words","phrases"])
client.set_classifiers(["textrazor_newscodes"])

logging.info('Starting Iteration')
for rec in range(articles_all.shape[0]):
    # text to analyze
    analyze_this = articles_all['article_text_without_children'][rec]
    analyze_this_PK = articles_all['PK_ID'][rec]
    analyze_this_PK_clean = articles_all['PK_ID_CLEAN'][rec]
    logging.info('>> PK of text to analyze: {a}'.format(a=analyze_this_PK))
    # get JSON
    # response = client.analyze(analyze_this)
    # json_response = response.json

    # temp
    json_response = "{'test': 'ABCDEF...XYZ'}"

    # write data
    # analyze_this_PK_clean = ''.join(e for e in analyze_this_PK if e.isalnum())
    # better:
    FILE_NAME = 'db_razor_json/' + analyze_this_PK_clean + '_' + now_str + '.txt'

    with open(FILE_NAME, 'w') as outfile:
        json.dump(json_response, outfile)

