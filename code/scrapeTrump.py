from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def scroll_inifint_page(driver):
    # open website
    driver.get("https://www.thetrumparchive.com/")
    time.sleep(3)

    # get page height
    prev_height = driver.execute_script('return document.body.scrollHeight')

    while True:
    # for i in range(0, 2):
        # scroll down
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(3)

        # get new page height
        new_height = driver.execute_script('return document.body.scrollHeight')

        # if there is nowhere to go its means that we got to the end of the page
        if new_height == prev_height:
            break

def get_from_page(driver):

    # init df list
    data_list = []

    # get the number of tweets
    tweet_num_elem = driver.find_elements_by_class_name("results___1pfEc")
    tweet_num = tweet_num_elem[0].text

    # get all tweets by elemnt class name
    elem = driver.find_elements_by_class_name("tweet___2xXtA")

    # insert all the tweets to the dataframe
    for i in range(0, tweet_num):
        rv_data = elem[i].text.split('\n')
        dict = {
            'date' : rv_data[0].split('.')[1],
            'retweets': rv_data[1],
            'likes': rv_data[2],
            'isDeletedTweet': False if  rv_data[3] == 'Show' else True,
            'text': rv_data[4]
        }
        data_list.append(dict)

    df = pd.DataFrame(data_list)
    return df

driver = webdriver.Chrome('chromedriver.exe')
scroll_inifint_page(driver)
data_farme = get_from_page(driver)
driver.close()

data_farme.to_csv('trumpTweets.csv', mode='a', index=False, header=True)

# print message
print("Data appended successfully.")

## TODO: change code from debug to prod =>
# change get_from_page func to number for tweets + for loop 
# change scroll_inifint_page func to while True