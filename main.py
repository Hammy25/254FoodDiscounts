#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  30 13:51:58 2023

@author: mhmwawuda
"""
import os
import uber_eats
import tweet_offers

project_folder = os.path.abspath(os.path.dirname(__file__))
ubereats_folder = os.path.join(project_folder, "Ubereats")


def main():
    uber_eats.delete_folder_items(ubereats_folder)
    driver = uber_eats.setupDriver()
    uber_eats.goToAddress(driver)
    uber_eats.extractOffersUber(driver)
    tweet_offers.setup_logger()
    api = tweet_offers.twitter_authentication()
    df = tweet_offers.get_offers_dataframe("Ubereats")
    tweet_offers.tweet_thread(api, df)


if __name__ == "__main__":
    main()
