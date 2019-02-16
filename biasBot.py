import praw
from helper import url_to_domain


def main():
    reddit = praw.Reddit('bot1')

    subreddit = reddit.subreddit('news+worldnews+politics')
    for submission in subreddit.stream.submissions():
        if submission.num_comments > 1 and submission.num_comments < 150 and not submission.stickied:
            # strip url to base domain
            domain = url_to_domain(submission.url)
            print(domain)


if __name__ == '__main__':
    main()
# in subreddit
# if submission has over 50 but less than 100
# pull domain
# check for domain
# if exists, push data into formatted message
# post
