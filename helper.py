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


def build_message(source):
    template = (
        "**{bias}**\n\n"
        "{arrow}<==O == == == == == == |= == == == == == == == >\n\n"
        "{reporting}Factual Reporting: MIXED\n\n"
        "{desc}These media sources are moderately to strongly biased toward liberal causes through story selection and/or political affiliation.  They may utilize strong loaded words(wording that attempts to influence an audience by using appeal to emotion or stereotypes), publish misleading reports and omit reporting of information that may damage liberal causes. Some sources in this category may be untrustworthy.\n\n"
        "[Learn More]({href}https: // mediabiasfactcheck.com/al-hayat/)\n\n"
        "- -------------------------------------------------------------------------\n\n"
        "[MediaBiasFactCheck](https: // mediabiasfactcheck.com/about/) | [Code/Docs](https: // github.com/mjsumpter/MBFCBiasBot) | [Feedback](http: // np.reddit.com/message/compose /?to=MBFCBiasBot & subject=Feedback)\n"
        "- -- | ---- | ----"
    )
