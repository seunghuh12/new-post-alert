import praw
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

reddit = praw.Reddit(
    client_id = config['DEFAULT']['client_id'],
    client_secret = config['DEFAULT']['client_secret'],
    user_agent = 'testing_alert'
)

def subreddit_post_fork(name, num):
    return reddit.subreddit(name).new(limit = num)