import requests
from lxml import html
import csv
import sys
sys.setdefaultencoding('utf-8')


fieldnames = ['Season', 'Team', 'Points Per Game', 'Opponent Points Per Game', 'Point Differential', 'Own FG%',
              'Opponent FG%', 'Own 3p%', 'Opponent 3p%', 'FT%', 'Offensive Rebounds', 'Defensive Rebounds',
              'Rebounding %', 'Own Turnovers', 'Opponent Turnovers', 'Offensive adjusted field goal %', 'Offensive ppg',
              'Offensive FGM']
writer = csv.DictWriter(open('..//nba_stats/ratings_new.csv', 'wb'),
                        fieldnames=fieldnames)
writer.writeheader()

def main():
    link = 'http://www.espn.com/nba/statistics/team/_/stat/team-comparison-per-game/sort/avgPoints/year/'
    link2 = 'http://www.espn.com/nba/statistics/team/_/stat/offense-per-game/year/'
    for year in range(2000, 2018):
        data = {}
        response = requests.get(link + str(year))
        details = html.fromstring(response.content)
        tree = details.xpath(".//*[@id='my-teams-table']/div/div[2]/table/tr")
        #scrape team comparison stats per game
        for row in tree:
            if len(row.xpath(".//td[2]/a/text()")) > 0:
                data['Season'] = str(year)
                data['Team'] = select(row.xpath(".//td[2]/a/text()")) #team name
                data['Points Per Game'] = select(row.xpath(".//td[3]/text()")) #team points per game
                popp = select(row.xpath(".//td[4]/text()")) #opponent points per game
                pdiff = select(row.xpath(".//td[5]/text()")) #point differential
                fgown = select(row.xpath(".//td[6]/text()")) #team field goal %
                fgopp = select(row.xpath(".//td[7]/text()")) #opponent field goal %
                town = select(row.xpath(".//td[8]/text()")) #team 3pt field goal %
                topp = select(row.xpath(".//td[9]/text()")) #opponent 3pt field goal %
                free = select(row.xpath(".//td[10]/text()")) #team free throw %
                roff = select(row.xpath(".//td[11]/text()")) #team offensive rebound %
                rdef = select(row.xpath(".//td[12]/text()")) #team defensive rebound %
                trp = select(row.xpath(".//td[13]/text()")) #team total rebounding %
                turno = select(row.xpath(".//td[14]/text()")) #team turnovers
                turnp = select(row.xpath(".//td[15]/text()")) #opponent turnovers
                # print data['Season'], data['Team'],data['Points Per Game'],'ONE'
        response2 = requests.get(link2 + str(year))
        details2 = html.fromstring(response2.content)
        tree2 = details2.xpath(".//*[@id='my-teams-table']/div/div[2]/table/tr")
        #scrape team offense stats per game
        for row in tree2:
            if len(row.xpath(".//td[2]/a/text()")) > 0:
                data['Team'] = select(row.xpath(".//td[2]/a/text()")) #team name
                data['Season'] = year
                team = select(row.xpath(".//td[2]/a/text()")) #team name
                data['Offensive ppg'] = select(row.xpath(".//td[3]/text()")) #offensive points per game (off efficiency)
                data['Offensive FGM'] = select(row.xpath(".//td[4]/text()")) #field goals made
                # print data2['Season'], data2['Team'],data2['Offensive FGM'], 'loop 2'
        writer.writerow(data)



            #             team = select(row.xpath(".//td[2]/a/text()")) #team name
            #             off_pts = select(row.xpath(".//td[3]/text()")) #offensive points per game (off efficiency)
            #             off_fgm = select(row.xpath(".//td[4]/text()")) #field goals made
            #             off_fga = select(row.xpath(".//td[5]/text()")) #field goals attempted
            #             off_3pm = select(row.xpath(".//td[7]/text()")) #3 pointers made
            #             off_3pa = select(row.xpath(".//td[8]/text()")) #3 pointers attempted
            #             off_ftm = select(row.xpath(".//td[10]/text()")) #free throws made
            #             off_fta = select(row.xpath(".//td[11]/text()")) #free throws attempted
            #             off_pps = select(row.xpath(".//td[13]/text()")) #offense points per shot
            #             off_afg = select(row.xpath(".//td[14]/text()")) #offense adjusted field goal %
            #             writer.writerow({'Season': season, 'Team': team, 'Offensive adjusted field goal %': off_afg,
            #                              'Offensive ppg': off_pts})



def select(item):
    if len(item) >= 1 and item is not None:
        for value in item:
            return value



if __name__ == '__main__':
    main()
