import requests
import sqlite3
import re
from urllib.request import urlopen
from sqlite3 import Error
from bs4 import BeautifulSoup
from helper import url_to_domain


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
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
    sql = ''' INSERT OR IGNORE INTO sources(source_title,href,link,bias_label,factual_rating,bias_desc,source_desc)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, source)
    return cur.lastrowid


def main():
    database = "./db/sources.db"
    url = "https://mediabiasfactcheck.com/"
    biases = ["left", "leftcenter", "center", "right-center",
              "right", "pro-science", "conspiracy", "fake-news", "satire"]

    conn = create_connection(database)
    with conn:
        for bias in biases:
            i = 1
            r_bias = requests.get(url + bias)

            bias_soup = BeautifulSoup(r_bias.content, 'html.parser')

            for a in bias_soup.select('.entry p a'):
                # get source title from sources list
                source_title = a.text.strip()
                # href is link to full info page on source
                href = a['href']

                # stops specific trouble children from crashing scanner
                if (not "mediabiasfactcheck" in href) or ("strategic-culture-foundation" in href):
                    print("Bad Source")
                    continue

                # if 404, skip to next link
                try:
                    page = urlopen(href)
                except:
                    continue

                r_source = requests.get(href)
                source_soup = BeautifulSoup(r_source.content, 'html.parser')

                # link is link to news site
                pattern = re.compile(r"(?:^|\W)Source:(?:$|\W)")
                if pattern.search(source_soup.text):
                    index = pattern.search(source_soup.text).start()
                    link = source_soup.text[index+9:index+100]
                    link = link[:link.find('\n')]
                    print(link)
                    link = url_to_domain(link)

                else:
                    link = "Error"

                html = source_soup.select_one('.entry-header > h1')
                bias_label = html.text.strip() if html else "Error"

                # grabs factual reporting tag
                pattern = re.compile(r"(?:^|\W)Reporting:(?:$|\W)")
                if pattern.search(source_soup.text):
                    index = pattern.search(source_soup.text).start()
                    factual_rating = source_soup.text[index+12:index+20]
                    factual_rating = factual_rating[:factual_rating.find('\n')]
                else:
                    factual_rating = "Error"

                html = source_soup.select_one('.entry-content p:nth-child(1)')
                bias_desc = html.text.strip().replace(u'\xa0', u' ') if html else "Error"

                html = source_soup.select_one('.entry-content p:nth-child(3)')
                source_desc = html.text.strip().replace(u'\xa0', u' ') if html else "Error"

                source = (source_title, href, link, bias_label,
                          factual_rating, bias_desc, source_desc)
                create_source(conn, source)
                print("Added " + bias + " source " +
                      str(i) + " " + href + " " + link)
                i += 1


if __name__ == '__main__':
    main()
