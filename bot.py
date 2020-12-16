import logging
from os import environ

import tweepy


logging.basicConfig(
    level='INFO',
    style='{',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='{asctime} [{levelname}]: {message}',
)
logger = logging.getLogger()


auth = tweepy.OAuthHandler(
    environ['CONSUMER_KEY'],
    environ['CONSUMER_SECRET'],
)
auth.set_access_token(
    environ['ACCESS_TOKEN'],
    environ['ACCESS_TOKEN_SECRET'],
)

api = tweepy.API(auth)
api.verify_credentials()


class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api

    def on_status(self, tweet):
        if tweet.retweeted or tweet.text.startswith('RT @'):
            return
        logger.info(
            'https://twitter.com/twitter/statuses/%s @%s: %s',
            tweet.id,
            tweet.user.screen_name,
            tweet.text,
        )
        self.api.update_status('Ta gueule.', in_reply_to_status_id=tweet.id)

    def on_error(self, status):
        logger.error(status)


stream = tweepy.Stream(api.auth, StreamListener(api))
track = [
    'ça va être tout noir',
    'ça va etre tout noir',
    'ca va être tout noir',
    'ca va etre tout noir',
]
stream.filter(track=track, languages=['fr'])
