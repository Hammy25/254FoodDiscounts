# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 11:01:09 2022

@author: mhmwawuda
"""

import time
import platform
import os.path
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

project_folder = os.path.abspath(os.path.dirname(__file__))
ubereats_folder = os.path.join(project_folder, "Ubereats")
operating_system = platform.system()


def delete_folder_items(n_path):
    """
    Delete items in folder
    """
    if(operating_system == "Windows"):
        os.system("rmdir /S /Q " + n_path)
        os.system("mkdir " + n_path)
    else:
        os.system("rm -f " + n_path + "/*")


def setupDriver():
    """
    Setting up driver
    """
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    return webdriver.Chrome(options = options, service = Service(ChromeDriverManager().install()))


def goToAddress(driver ,address="https://www.ubereats.com/ke"):
    """
    Going to specific address
    """
    driver.get(address)
    time.sleep(5)


def scrollToTheBottom(driver, scroll_factor=18, waitFactor=2):
    """
    Scroll to bottom of page in intervals
    
    Parameters
    ----------
    driver : Web driver
    scroll_factor : Fraction
    
    Returns
    -------
    None.

    """
    for num in range(1, scroll_factor + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight*("+ str(num) + "/" + str(scroll_factor) + "))")
        time.sleep(waitFactor)
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0)")
    
def extractOffersUber(driver, waitFactor=5):
    """
    Parameters
    ----------
    driver : Web driver
    
    Returns
    -------
    Offers Data Frame
    """
    # Data frame for storing Data
    datafrme = pd.DataFrame(columns=["Store", "Offer Type", "Offer Link", "Screenshot Path"])
    # Moving to the offers
    location = driver.find_element(By.XPATH, '//*[@id="location-typeahead-home-input"]')
    location.send_keys("Nairobi")
    time.sleep(waitFactor)
    location.send_keys(Keys.ENTER)
    find_food = WebDriverWait(driver, waitFactor*2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div[1]/div[2]/div/div[1]/button')))
    find_food.click()
    time.sleep(waitFactor*2)
    deals_toggle = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[3]/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div/label[1]/div[2]/div')
    deals_toggle.click()
    time.sleep(waitFactor*2)
    
    # Extracting offers
    base_link = "https://www.ubereats.com"
    soup = BeautifulSoup(driver.page_source, "lxml")
    scrollToTheBottom(driver)
    grid = soup.find("div",{"data-test": "feed-desktop", "data-testid": "feed-desktop"})
    time.sleep(waitFactor*2)

    try:
        offers = grid.children
    except AttributeError as e:
        if(waitFactor > 150):
            print("Error: " + e)
            print("Website might have changed or inaccessible.")
            exit(0)
        print("Could be that the page hasn't loaded!")
        print(e)
        print("....Multiplying wait factor by 2")
        waitFactor = waitFactor*2
        print("...Attempting again")
        goToAddress(driver, address="https://www.ubereats.com/ke")
        extractOffersUber(driver, waitFactor)
    offer_num = 1
    time.sleep(waitFactor*2)
    pictures = []
    scr_num = 1
    while True:
        try:
            picture = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/main/div/div/div[2]/div/div[2]/div["+ str(scr_num) + "]")
        except NoSuchElementException:
            print("All offers collected!")
            break
        scr_num+=1
        pictures.append(picture)
    index = 0
    for offer in offers:
        offer_link = offer.find("a").get("href")
        offer_link = base_link + offer_link
        offer_type = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/main/div/div/div[2]/div/div[2]/div[" + str(index + 1)+"]/div/div/div/div[1]/div[2]/div[1]").text
        store = offer.find("h3").text
        screenshot_name = store + ".png"
        pictures[index].screenshot(os.path.join(ubereats_folder, screenshot_name))
        datafrme.loc[len(datafrme.index)] = [store , offer_type, offer_link, os.path.join(ubereats_folder, screenshot_name)]
        offer_num += 1
        index += 1
    datafrme.to_csv(os.path.join(ubereats_folder,"offers.csv"))

    
def main():
    """
    Main function.
    
    Returns
    -------
    None.
    """
    # exit(0)
    delete_folder_items(ubereats_folder)
    driver = setupDriver()
    goToAddress(driver)
    extractOffersUber(driver)


if __name__ == "__main__":
    main()
