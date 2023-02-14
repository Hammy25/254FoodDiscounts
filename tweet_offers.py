# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 10:41:58 2023

@author: mhmwawuda
"""

import tweepy
import os
import logging
import pyshorteners
import pandas as pd

# Initialize URL shortener
url_shortener = pyshorteners.Shortener()


def setup_logger():
    """
    Setting up logger
    """
    logger = logging.getLogger("tweepy")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename="tweepy.log")
    logger.addHandler(handler)
    return logger


def get_images_folder(app_name):
    """
    Get folder with screenshoots

    Parameters
    ----------
    app_name : App the offers are from.

    Returns
    -------
    folder : Folder with the images.

    """
    # Paths
    # project_folder = "C:/Users/mhmwawuda/Desktop/projects/254FoodDiscounts"
    project_folder = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(project_folder, app_name)
    return folder


def get_offers_dataframe(app_name):
    """
    Get Dataframe of the offers
    
    Parameters
    ----------
    app_name : App the offers are from.

    Returns
    -------
    Offers: DataFrame of offers.

    """
    project_folder = os.path.abspath(os.path.dirname(__file__))
    folder = os.path.join(project_folder, app_name)
    offers_file = os.path.join(folder, "offers.csv")
    offers = pd.read_csv(offers_file)
    offers = offers.reset_index()
    return offers


def tweet_thread(api, offers):
    """
    Tweet the offers as a thread.
    
    Parameters
    ----------
    api : Authenticated Twitter API
    offers: Dataframe of offers

    Returns
    -------
    None.

    """
    count = 0
    for index, offer in offers.iterrows():
        store = offer["Store"]
        off_type = offer["Offer Type"]
        try:
            url = url_shortener.tinyurl.short(offer["Offer Link"])
        except Exception as e:
            print("Ignoring URL shortener beacause of error.")
            url = offer["Offer Link"]
        # print(offer["Screenshot Path"])
        tweet = "Store: " + store + "\nOffer Type: " + off_type + "\nStore Link: " + url
        try:
            if count == 0:
                tweeted = api.update_status_with_media(tweet, offer["Screenshot Path"])
            else:
                tweeted = api.update_status_with_media(tweet, offer["Screenshot Path"], in_reply_to_status_id = tweeted.id)
        except FileNotFoundError:
            pass
        count += 1


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
    api = tweepy.API(auth)  
    return api

def main():
    """
    Main function

    Returns
    -------
    None.

    """
    setup_logger()
    api = twitter_authentication()
    # images_folder = get_images_folder("Ubereats")
    df = get_offers_dataframe("Ubereats")
    tweet_thread(api, df)
    

if __name__ == "__main__":
    main()
    
    
    


    

    
    

