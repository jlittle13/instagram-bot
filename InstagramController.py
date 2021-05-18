from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options


import random
import json


with open('config.json', 'r') as f:
    config = json.load(f)


class InstagramController:
    def __init__(self):
        # create selenium chrome driver
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome("./lib/chromedriver", chrome_options=options)
        self.actions = ActionChains(self.driver)
        self.login()

    def login(self):
        sleep(2)
        self.driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        sleep(3)

        username = self.driver.find_element_by_name('username')
        username.send_keys(config["instagram"]["username"])
        password = self.driver.find_element_by_name('password')
        password.send_keys(config["instagram"]["password"])

        button_login = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]')
        button_login.click()
        sleep(5)

    def follow(self):
        user_list = config["instagram"]["user_list"]

        self.driver.get('https://www.instagram.com/' + random.choice(user_list))
        sleep(3)

        # find the "users following" button
        view_followers_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/'
                                                                'main/div/header/section/ul/li[2]/a')
        view_followers_btn.click()
        sleep(3)

        # get list of all followers
        followers_list = self.driver.find_elements_by_xpath("//button[(contains(text(), 'Follow') and not(contains(text(),'Following')))]")

        # skip over first el in the case that we are not following
        # the user whose friends list we are looking at
        for i in range(1, len(followers_list)):
            # pick random follower from the list
            follower = followers_list[i]
            try:
                # scroll to the follower
                self.actions.move_to_element(follower).perform();
                sleep(1)
                follower.click()
                sleep(random.uniform(2.0, 3.1))
            except:
                print("ran into issue")
                continue

            print("followed a user: " + str(i))

        print("pausing...")


ic = InstagramController()
while True:
    ic.follow()
    sleep(config["instagram"]["follow_interval"])
