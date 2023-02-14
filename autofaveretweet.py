import os
import tweepy
import logging
from config import twitter_authentication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FavRetweetListener(tweepy.StreamingClient):

    def __init__(self, bearertoken, api):
        super().__init__(bearertoken)
        self.api = api
        self.id = api.get_user

    def on_tweet(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        status = self.api.get_status(tweet.id)
        if status.in_reply_to_status_id is not None:
            pass
        if not status.favorited:
            # Marked it as liked
            try:
                status.favorite()
            except Exception as e:
                logger.error("Error on fav. ", exc_info=True)
                logger.error(e)
        if not status.retweeted:
            # Retweet
            try:
                status.retweet()
            except Exception as e:
                logger.error("Error on fave and retweet", exc_info=True)
                logger.error(e)

    def on_error(self, status_code):
        if status_code == 420:
            logger.error("Exceeded limit")
        else:
            logger.error(status_code)


def main(keyword):
    api = twitter_authentication()
    stream = FavRetweetListener(os.getenv("FoodDealsBearerToken"), api)
    stream.filter()


if __name__ == "__main__":
    main("@254fooddeals")
