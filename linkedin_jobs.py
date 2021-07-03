# library imports 
import getpass # for hidden password


from selenium import webdriver
import time 
import logging
# to send input 
from selenium.webdriver.common.keys import Keys
import os

import tkinter as tk

# getting screen size to resize browser window
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()


# initialize browser and go to target page

browser = webdriver.Chrome('./drivers/chromedriver')
browser.set_window_size(width,height)
# get the login page
browser.get('https://www.linkedin.com/login')


time.sleep(3) # wait for the page to load


# login info
user_name = input("Email: ")
password = getpass.getpass("Password: ")

# search terms and location
KEYWORDS = input("Enter desired job title: ")
LOCATION = input("Location: ")

browser.find_element_by_id('username').send_keys(user_name)
browser.find_element_by_id('password').send_keys(password)
browser.find_element_by_id('password').send_keys(Keys.RETURN)


# get to the job search page 
browser.get('https://www.linkedin.com/jobs/')
time.sleep(3)


# get the search bars for job & location



search_bars = browser.find_elements_by_class_name('jobs-search-box__text-input')
search_keywords = search_bars[0]
search_keywords.send_keys(KEYWORDS)

# location was number 3 in the list of search bars elements
search_location =search_bars[3]
search_location.send_keys(LOCATION)
search_keywords.send_keys(Keys.RETURN)

# getting the list of jobs 




def get_jobs(browser=browser):
    # get a list of all the listings elements's in the side bar
    list_items = browser.find_elements_by_class_name("occludable-update")
    # scrolls a single page:
    for job in list_items:
        # executes JavaScript to scroll the div into view
        browser.execute_script("arguments[0].scrollIntoView();", job)
        job.click()
        time.sleep(3)
        # get info:
        [position, company, location] = job.text.split('\n')[:3]
        details = browser.find_element_by_id("job-details").text
        position = position.replace("/", "").strip()
        # writing job info into a text file titles by position_company
        with open(f'./data/{position}_{company}.txt', mode='w+') as f:
            f.write(f"{position}\n{company}\n{location}\n{details}")




if __name__=="__main__":
    time.sleep(5) # give time for the page to load

    get_jobs()