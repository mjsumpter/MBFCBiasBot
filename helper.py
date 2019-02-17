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

    source_dict = {}

    if source[0] and source[0] != "Error":
        source_dict["title"] = source[0]
    else:
        source_dict["title"] = ""
    if source[1] and source[1] != "Error":
        source_dict["href"] = source[1]
    else:
        source_dict["href"] = ""
    if source[2] and source[2] != "Error":
        source_dict["link"] = source[2]
    else:
        source_dict["link"] = ""
    if source[3] and source[3] != "Error":
        source_dict["bias"] = source[3]
    else:
        source_dict["bias"] = ""
    if source[4] and source[4] != "Error":
        source_dict["rating"] = source[4]
    else:
        source_dict["rating"] = ""
    if source[5] and source[5] != "Error":
        source_dict["desc1"] = source[5]
    else:
        source_dict["desc1"] = ""
    if source[6] and source[6] != "Error":
        source_dict["desc2"] = source[6]
    else:
        source_dict["desc2"] = ""

    if source_dict["bias"] == "LEFT BIAS":
        source_dict["bias_arrow"] = "<==O == == == == == == =|= == == == == == == ==>\n\n"
    elif source_dict["bias"] == "LEFT-CENTER BIAS":
        source_dict["bias_arrow"] = "<== == == == ==O == == =|= == == == == == == ==>\n\n"
    elif source_dict["bias"] == "LEAST BIASED":
        source_dict["bias_arrow"] = "<== == == == == == == =(|)= == == == == == == ==>\n\n"
    elif source_dict["bias"] == "RIGHT-CENTER BIAS":
        source_dict["bias_arrow"] = "<== == == == == == == =|= == == O== == == == ==>\n\n"
    elif source_dict["bias"] == "RIGHT BIAS":
        source_dict["bias_arrow"] = "<== == == == == == == =|= == == == == == == O==>\n\n"
    elif source_dict["bias"] == "PRO-SCIENCE":
        source_dict["bias_arrow"] = "<11 00 11 11 00 01 00 =|= 11 00 10 01 00 00 10>\n\n"
    elif source_dict["bias"] == "CONSPIRACY-PSEUDOSCIENCE":
        source_dict["bias_arrow"] = "< o_O o_O o_O o_O o_O =|= o_O o_O o_O o_O o_O >\n\n"
    elif source_dict["bias"] == "QUESTIONABLE SOURCE":
        source_dict["bias_arrow"] = "<(>_<)(>_<)(>_<)(>_<)=|=(>_<)(>_<)(>_<)(>_<)(>_<)>\n\n"
    elif source_dict["bias"] == "SATIRE":
        source_dict["bias_arrow"] = "<(⌒▽⌒）(⌒▽⌒）(⌒▽⌒）(⌒▽⌒）=|=(⌒▽⌒）(⌒▽⌒）(⌒▽⌒）(⌒▽⌒）>\n\n"
    else:
        source_dict["bias_arrow"] = ""

    template = (
        "**{bias}**\n\n"
        "{bias_arrow}"
        "Factual Reporting: {rating}\n\n"
        "{desc1}\n\n"
        "{desc2}\n\n"
        "[Learn More]({href})\n\n"
        "- -------------------------------------------------------------------------\n\n"
        "[MediaBiasFactCheck](https: // mediabiasfactcheck.com/about/) | [Code/Docs](https: // github.com/mjsumpter/MBFCBiasBot) | [Feedback](http: // np.reddit.com/message/compose /?to=MBFCBiasBot & subject=Feedback)\n"
        "- -- | ---- | ----"
    )

    return template.format(**source_dict)
