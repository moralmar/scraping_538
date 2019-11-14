import logging
import utils
import time
import sqlite3
import pandas as pd

now_str = time.strftime('%Y%m%d_%H%M%S')
FILENAME_lOG = 'log/' + now_str + 'report_integration.txt'
utils.start_logging(FILENAME_lOG)

logging.info('*'*30 + '\nINTEGRATION START\n' + '*'*30)


# INPUTS
TABLE_NAME = 'ARTICLES_538'
STAGING_TABLE = 'S_ARTICLES_538'

# Get data
# ----------------------------------------------------------------
conn = utils.create_connection('scraping538.db')
query = "SELECT * FROM " + STAGING_TABLE + " WHERE PROCESSED = 0"
data = pd.read_sql(query, con=conn)
data.drop("PROCESSED", axis=1, inplace=True)

# Clean data
# ----------------------------------------------------------------
# date
data['date'] = pd.to_datetime(data['date'])
data.rename(columns={"date": "DATE"}, inplace=True)

# date_hour
# (you can have NaT)
data['date_hour'] = data['date_hour'].str.replace('.', '')
data['date_hour'] = pd.to_datetime(data['date_hour'],
                                   format='%b %d, %Y-%I:%M %p',
                                   errors='coerce')
data.rename(columns={"date_hour": "DATE_HOUR"}, inplace=True)

# date_import
data['date_import'] = pd.to_datetime(data['date_import'])
data.rename(columns={"date_import": "DATE_IMPORT"}, inplace=True)

# define PK
data['PK_ID'] = data['DATE'].dt.strftime('%d-%m-%Y_') + data['title']
data['PK_ID_CLEAN'] = data['PK_ID'].str.replace(r'[^A-Za-z0-9]+', '')

# did we save the json from text-razor?
data['TEXTRAZOR_JSON_SAVED'] = 0

# Write data
# ----------------------------------------------------------------
num_rejected = 0
for index in range(data.shape[0]):

    one_rec = data.loc[[index]]

    try:
        one_rec.to_sql(TABLE_NAME, con=conn, if_exists='append', index=False)
        pass
    except sqlite3.IntegrityError as err:
        logging.info('Following Articles were duplicated (due to PK):')
        logging.info('*** IntegrityError  --  {a}'.format(a=one_rec['PK_ID'][index]))
        num_rejected += 1
    finally:
        conn.commit()

conn.execute('UPDATE ' + STAGING_TABLE + ' SET PROCESSED = 1 WHERE PROCESSED = 0;')
conn.commit()
conn.close()

logging.info('# of articles loaded:       {a}'.format(a=data.shape[0]))
logging.info('# of articles "integrated": {a}'.format(a=data.shape[0] - num_rejected))
logging.info('# of articles rejected:     {a}'.format(a=num_rejected))
logging.info('*'*30 + '\nFINISHED\n' + '*'*30)

# TODO: put here: Visual Aid - to be sure that all articles are scraped
