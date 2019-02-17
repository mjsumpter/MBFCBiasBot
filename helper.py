import sqlite3


def url_to_domain(urlstring):

    domain = urlstring

    str_to_remove = "http://"

    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[index + len(str_to_remove):]

    str_to_remove = "https://"
    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[index + len(str_to_remove):]

    str_to_remove = "www."
    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[index + len(str_to_remove):]

    str_to_remove = "m."
    index = domain.find(str_to_remove)
    if index != -1 and index < 2:
        domain = domain[index + len(str_to_remove):]

    str_to_remove = '/'
    index = domain.find(str_to_remove)
    if index != -1:
        domain = domain[:index]

    return domain


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    database = "./db/sources.db"

    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)

    return None


def create_source(conn, source):
    """
    Create a new source into the sources table
    :param conn:
    :param source:
    :return: source id
    """
    sql = ''' INSERT OR UPDATE INTO sources(source_title,href,link,bias_label,factual_rating,bias_desc,source_desc)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, source)
    return cur.lastrowid
