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


def source_to_dict(source):
    source_dict["title"] = source[0]
    source_dict["href"] = source[1]
    source_dict["link"] = source[2]
    source_dict["bias"] = source[3]
    source_dict["rating"] = source[4]
    source_dict["desc1"] = source[5]
    source_dict["desc2"] = source[6]

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

    return source_to_dict


def build_message(source_dict):
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

    return template.format(**source_dict)
