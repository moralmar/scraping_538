import logging
import sqlite3


def start_logging(filename_log):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - -%(levelname)s - %(message)s',
                        filename=filename_log,
                        filemode='w')

    logging.handlers = []
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


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
