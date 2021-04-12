from urllib.request import urlopen
from bs4 import BeautifulSoup

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from tqdm import tqdm
import openpyxl
import pandas as pd
import os
import time

from constants import YEAR

class scrapeBasketballRef():

    def scrapeWithSoup(self, YEAR, page_string):

        # specify directory we want the csv files to go into
        os.chdir('../input/{}'.format(page_string))

        for i in tqdm(range(len(YEAR))):

            year = YEAR[i]

            # url of page to scrape data from
            url = "https://www.basketball-reference.com/leagues/NBA_{}_{}.html".format(year, page_string)

            # html from given url
            html = urlopen(url)

            # initialize BeautifulSoup class object
            soup = BeautifulSoup(html, features="html.parser")

            # extract text to get a list of header labels (exclude ranking order from basketball reference)
            headers = [th.getText() for th in soup.findAll('tr')[0].findAll('th')[1:]]

            # extract text to get a list of row values (exclude first header row)
            rows = soup.findAll('tr')[1:]
            player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

            # create pandas dataframe to organize data extracted
            stats = pd.DataFrame(player_stats, columns=headers)
            # print(stats.head(10))

            # gets the path which was changed to the specified folder
            export_path = os.getcwd()
            # saves to csv file labeled by the statistics type and year
            stats.to_csv(export_path+ '\\{}-{}.csv'.format(year, page_string))

    def scrapeWithSelenium(self, YEAR, page_string):

        # specify directory we want the csv files to go into
        os.chdir('../input/{}'.format(page_string))
        export_path = os.getcwd()

        options = webdriver.ChromeOptions()

        preferences = {"download.default_directory": export_path}

        options.add_experimental_option("prefs", preferences)

        chromedriver = 'C:/SeleniumDrivers/chromedriver'
        driver = webdriver.Chrome(chromedriver, options=options)

        driver.maximize_window()

        for i in tqdm(range(len(YEAR))):

            year = YEAR[i]

            # url of page to scrape data from
            url = "https://www.basketball-reference.com/leagues/NBA_{}_{}.html".format(year, page_string)

            # navigate to the page given by the url
            driver.get(url)

            driver.execute_script("window.scrollTo(0, 500)")

            # hover over tooltips bar
            hover_over_element = driver.find_element_by_xpath("//*[@id='expanded_standings_sh']/div/ul/li[1]/span")

            # the button to download a csv file
            click_element = driver.find_element_by_xpath('//*[@id="expanded_standings_sh"]/div/ul/li[1]/div/ul/li[3]/button')

            delay = 200

            try:
                # WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="expanded_standings_sh"]/div/ul/li[1]/div/ul/li[3]/button')))
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'all_expanded_standings')))
            except TimeoutException:
                raise("Loading took too much time!")

            # hover over the tooltip and then click download excel file
            perform_action = ActionChains(driver).move_to_element(hover_over_element).move_to_element(click_element).click()

            # perform the action
            perform_action.perform()

            read_excel_file = pd.read_csv(export_path + "\\sportsref_download.xls")
            read_excel_file.to_csv(export_path+ '\\{}-{}.csv'.format(year, page_string))

            if os.path.exists("sportsref_download.xls"):
                os.remove("sportsref_download.xls")

scrape = scrapeBasketballRef()
scrape.scrapeWithSelenium(YEAR, 'standings')
