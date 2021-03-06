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
    def __init__(self, api, track):
        self.api = api
        self.track = [t.lower() for t in track]

    def on_status(self, tweet):
        if tweet.retweeted or tweet.text.startswith('RT @'):
            return
        content = tweet.text.lower()
        if not any(t in content for t in self.track):
            return
        logger.info(
            'https://twitter.com/twitter/statuses/%s @%s: %s',
            tweet.id,
            tweet.user.screen_name,
            tweet.text,
        )
        self.api.update_status(
            f'@{tweet.user.screen_name} Ta gue\u200Bule !',
            in_reply_to_status_id=tweet.id,
        )

    def on_error(self, status):
        logger.error(status)


track = [
    'ça va être tout noir',
    'ça va etre tout noir',
    'ca va être tout noir',
    'ca va etre tout noir',
]
stream = tweepy.Stream(api.auth, StreamListener(api, track))
stream.filter(track=track, languages=['fr'])
