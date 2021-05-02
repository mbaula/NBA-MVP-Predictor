from urllib.request import urlopen
from bs4 import BeautifulSoup

from tqdm import tqdm
import pandas as pd
import os

from constants import YEAR

class BasketballReferenceScraper():

    def scrapeStats(self, YEAR, page_string):

        # specify directory we want the csv files to go into
        os.chdir('../input/{}'.format(page_string))

        for i in tqdm(range(len(YEAR))):

            # year to scrape
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

            # gets the path which was changed to the specified folder
            export_path = os.getcwd()

            # saves to csv file labeled by the statistics type and year
            stats.to_csv(export_path+ '\\{}-{}.csv'.format(year, page_string))

    def scrapeStandings(self, YEAR):

        # specify directory we want the csv files to go into
        os.chdir('../input/standings')

        for i in tqdm(range(len(YEAR))):

            # year to scrape
            year = YEAR[i]

            # url of page to scrape data from
            url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html".format(year)

            # html from given url
            html = urlopen(url)

            # initialize BeautifulSoup class object
            soup = BeautifulSoup(html, features="html.parser")

            # extract text to get a list of headers
            titles = [th.getText() for th in soup.findAll('tr')[0].findAll('th')[1:]]

            # extract text for only column headers
            headers = titles[0:titles.index("SRS")+1]

            # remove column headers from titles
            titles = titles[titles.index("SRS")+1:]

            # get team names
            try:
                team_names = titles[0:titles.index("Easter Conference")]
            except:
                team_names = titles

            # remove non team names from list
            for i in headers:
                team_names.remove(i)

            #remove W and western conference from team names
            team_names.remove("Western Conference")
            try:
                team_names.remove("W")
            except:
                None

            # list of divisions to remove from team names
            divisions = ["Atlantic Division", "Central Division", "Southeast Division", "Northwest Division",
                         "Pacific Division", "Southwest Division", "Midwest Division"]

            # remove division from list
            for division in divisions:
                try:
                    team_names.remove(division)
                except:
                    None

            # then grab all data from rows except first row
            rows = soup.findAll('tr')[1:]

            # get the team standings
            team_standings = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

            # remove empty elements
            team_standings = [e for e in team_standings if e != []]
            # only keep needed rows
            team_standings = team_standings[0:len(team_names)]

            # add corresponding team name to the respective team standings
            for i in range(0, len(team_standings)):
                team_standings[i].insert(0, team_names[i])

            # add team to headers
            headers.insert(0, "Team")

            # create pandas dataframe
            year_standings = pd.DataFrame(team_standings, columns=headers)

            # delete 'games behind' column
            del year_standings['GB']

            # add a column to dataframe to indicate playoff appearance
            year_standings["Playoffs"] = ["Y" if "*" in ele else "N" for ele in year_standings["Team"]]
            # remove * from team names
            year_standings["Team"] = [ele.replace('*', '') for ele in year_standings["Team"]]
            # add losing season indicator (win % < .5)
            year_standings["Losing_season"] = ["Y" if float(ele) < .5 else "N" for ele in year_standings["W/L%"]]

            # gets the path which was changed to the specified folder
            export_path = os.getcwd()

            # saves to csv file labeled by the statistics type and year
            year_standings.to_csv(export_path + '\\{}-standings.csv'.format(year))

    def scrapeMvp(self, YEAR):

        # specify directory we want the csv files to go into
        os.chdir('../../input/mvp_data')

        for i in tqdm(range(len(YEAR))):

            # year to scrape
            year = YEAR[i]

            # url of page to scrape data from
            url = "https://www.basketball-reference.com/awards/awards_{}.html".format(year)

            # html from given url
            html = urlopen(url)

            # initialize BeautifulSoup class object
            soup = BeautifulSoup(html, features="html.parser")

            # extract text to get a list of header labels
            headers = [th.getText() for th in soup.findAll('tr')[1].findAll('th')[1:]]

            # extract text to get a list of row values
            rows = soup.findAll('tr')[2:]
            player_awards = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

            # remove non-mvp data
            for i in range(len(player_awards)):
                if player_awards[i] == []:
                    player_awards = player_awards[0:i]
                    break

            # create pandas dataframe to organize data extracted
            awards = pd.DataFrame(player_awards, columns=headers)

            # gets the path which was changed to the specified folder
            export_path = os.getcwd()

            # saves to csv file labeled by the statistics type and year
            awards.to_csv(export_path + '\\{}-awards.csv'.format(year))

scrape = BasketballReferenceScraper()
# scrape.scrapeMvp(YEAR)
# scrape.scrapeStandings(YEAR)
# scrape.scrapeStats(YEAR, 'advanced')
scrape.scrapeStats(YEAR, 'per_game')
