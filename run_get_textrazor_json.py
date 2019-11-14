import config
import utils
import time
import re
import json
import logging
import pandas as pd
import textrazor


TABLE_NAME = 'ARTICLES_538'
NUMBER_OF_RECORDS = 479

now_str = time.strftime('%Y%m%d_%H%M%S')
filename_log = 'log/' + now_str + 'get_textrazor_json.txt'
utils.start_logging(filename_log)

logging.info('*'*30 + '\nGET Text_Razor JSON - START\n' + '*'*30)

# get data
# ----------------------------------------------------------------
conn = utils.create_connection('scraping538.db')
query = "SELECT * FROM ARTICLES_538 WHERE TEXTRAZOR_JSON_SAVED = 0 LIMIT {a}".format(a=NUMBER_OF_RECORDS)
articles_all = pd.read_sql(query, con=conn)
logging.info('Number of records (for which to get the JSON): {a}'.format(a=articles_all.shape[0]))
# text razor config
textrazor.api_key = config.TEXT_RAZOR_API_KEY
client = textrazor.TextRazor(extractors=['entailments', 'relations', 'dependency-trees',
                                         "entities", "topics", "words", "phrases"])
client.set_classifiers(["textrazor_newscodes"])

# get JSON
# ----------------------------------------------------------------
logging.info('Starting Iteration')
for rec in range(articles_all.shape[0]):
    # text to analyze
    analyze_this = articles_all['article_text_without_children'][rec]
    analyze_this_PK = articles_all['PK_ID'][rec]
    analyze_this_PK_clean = articles_all['PK_ID_CLEAN'][rec]
    logging.info('>> PK of text to analyze: {a}'.format(a=analyze_this_PK))

    # get JSON
    response = client.analyze(analyze_this)
    json_response = response.json

    # write data
    file_name = 'db_razor_json/' + analyze_this_PK_clean + '_' + now_str + '.txt'
    with open(file_name, 'w') as outfile:
        json.dump(json_response, outfile)

    # update individual record
    conn.execute('UPDATE ' + TABLE_NAME +
                 ' SET TEXTRAZOR_JSON_SAVED = 1 WHERE PK_ID_CLEAN = "{PK_CLEAN}";'.format(PK_CLEAN=analyze_this_PK_clean))
    conn.commit()

# finally:
# ----------------------------------------------------------------
conn.close()
logging.info('*'*30 + '\nFINISHED\n' + '*'*30)
