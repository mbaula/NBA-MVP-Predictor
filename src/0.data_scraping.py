from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import os

from constants import YEAR

class dataScraper():

    def getPerGameStats(self, YEAR):

        # specify directory we want the csv files to go into
        os.chdir('../input/per-game')

        for i in tqdm(range(len(YEAR))):

            year = YEAR[i]

            # url of page to scrape data from
            url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)

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

            export_path = os.getcwd()
            stats.to_csv(export_path+ '\\{}-per-game.csv'.format(year))

    def getAdvancedStats(self, YEAR):

        # specify directory we want the csv files to go into
        os.chdir('../input/advanced')

        for i in tqdm(range(len(YEAR))):
            year = YEAR[i]

            # url of page to scrape data from
            url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(year)

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

            export_path = os.getcwd()
            stats.to_csv(export_path + '\\{}-advanced.csv'.format(year))

scrape = dataScraper()
# scrape.getPerGameStats(YEAR)
scrape.getAdvancedStats(YEAR)