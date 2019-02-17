import praw
import sqlite3
import os
from helper import url_to_domain, create_connection, build_message


def main():
    reddit = praw.Reddit('bot1')

    # create log of posts replied to
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))

    subreddit = reddit.subreddit('news+worldnews+politics')
    conn = create_connection()
    with conn:
        c = conn.cursor()

        for submission in subreddit.stream.submissions():

            if (submission.id not in posts_replied_to) and (submission.num_comments > 1) and (submission.num_comments < 150) and (not submission.stickied):
                # strip url to base domain
                domain = (url_to_domain(submission.url),)

                post = ""

                # find match in database
                for row in c.execute("SELECT * FROM sources WHERE link=?", domain):
                    post = build_message(row)  # parses match into comment text

                if post != "":
                    submission.reply(post)  # post comment
                    print("Replying to: ", submission.title,
                          " http://reddit.com", submission.permalink)
                    posts_replied_to.append(submission.id)  # log to posts
                    with open("posts_replied_to.txt", "w") as f:  # write to file
                        for post_id in posts_replied_to:
                        f.write(post_id + "\n")


if __name__ == '__main__':
    main()
# in subreddit
# if submission has over 50 but less than 100
# pull domain
# check for domain
# if exists, push data into formatted message
# post
