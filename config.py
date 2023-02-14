import os
import tweepy
import logging

logger = logging.getLogger()


def twitter_authentication():
    """
    Authenticate into Twitter.

    Returns
    -------
    api : Twitter API authentication model

    """
    consumer_key = os.getenv("FoodDealsAPIKey")
    consumer_secret = os.getenv("FoodDealsAPIKeySecret")
    access_token = os.getenv("FoodDealsAccessToken")
    access_secret = os.getenv("FoodDealsAccessTokenSecret")


    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
