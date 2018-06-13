import requests
from lxml import html
import csv


fieldnames = ['Season', 'Team', 'Points Per Game', 'Opponent Points Per Game', 'Point Differential', 'Own FG%',
              'Opponent FG%', 'Own 3p%', 'Opponent 3p%', 'FT%', 'Offensive Rebounds', 'Defensive Rebounds',
              'Rebounding %', 'Own Turnovers', 'Opponent Turnovers', 'Offensive adjusted field goal %', 'Offensive ppg',
              'Offensive FGM', 'Offensive FGA', 'Offensive 3pm', 'Offensive 3pa', 'Offensive FTA', 'Offensive FTM',
              'Offensive PPS', 'Opponent adjusted field goal %', 'Opponent ppg', 'Opponent FGM', 'Opponent FGA',
              'Opponent 3pm', 'Opponent 3pa', 'Opponent FTA', 'Opponent FTM', 'Opponent PPS', 'Opponent APG',
              'Team APG', 'Team SPG', 'Opponent SPG', 'Team BPG', 'Opponent BPG', 'Team TPG', 'Opponent TPG',
              'Team ATO', 'Team Techs']

teamdict = {'CHI': 'Chicago', 'MEM': 'Memphis', 'PHO': 'Phoenix', 'MIA': 'Miami', 'SAC': 'Sacramento', 'ATL': 'Atlanta',
            'BKN': 'Brooklyn', 'BOS': 'Boston', 'CHO': 'Charlotte', 'CLE': 'Cleveland', 'DAL': 'Dallas',
            'DEN': 'Denver', 'DET': 'Detroit', 'GSW': 'Golden State', 'HOU': 'Houston', 'IND': 'Indiana', 'LAC': 'LA',
            'LA': 'LA Lakers', 'MIL': 'Milwaukee', 'NO': 'New Orleans', 'NYK': 'New York', 'OKC': 'Oklahoma City',
            'ORL': 'Orlando', 'PHI': 'Philadelphia', 'POR': 'Portland', 'SAS': 'San Antonio', 'TOR': 'Toronto', 'UTA':
            'Utah', 'WAS': 'Washington', 'MIN': 'Minnesota', 'VAN': 'Memphis', 'SEA': 'Oklahoma City', 'TOT': 'Toronto',
            'CHH': 'Charlotte', 'NJN': 'Brooklyn', 'LAL': 'LA Lakers', 'BRK': 'Brooklyn', 'NOP': 'New Orleans',
            'NOH': 'New Orleans', 'NOK': 'New Orleans', 'CHA': 'Charlotte'}

playerfields = ['Season', 'Player', 'Team', 'Games Played', 'Minutes per Game', 'Age', 'Games Started',
                'Minutes per Game', 'Player Per Game Field Goals Made', 'Player Per Game Field Goals Attempted',
                'Player Per Game Field Goal Percentage', 'Player Per Game 3 Pointers Made',
                'Player Per Game 3 Pointers Attempted',
                'Player Per Game Two Pointers Made', 'Player Per Game Two Pointers Attempted',
                'Player Per Game Two Pointers Percentage',
                'Player Per Game Effective Field Goal Percentage', 'Player Per Game Free Throws Made',
                'Player Per Game Free Throws Attempted',
                'Player Per Game Free Throw Percentage', 'Player Per Game Offensive Rebounds',
                'Player Per Game Defensive Rebounds',
                'Player Per Game Total Rebounds', 'Player Per Game Assists', 'Player Per Game Steals',
                'Player Per Game Blocks', 'Player Per Game Turnovers',
                'Player Per Game Personal Fouls', 'Player Per Game Points Per Game',
                'Player Per Game 3 Pointers Percentage', 'Position']


writer = csv.DictWriter(open('team_ratings.csv', 'w'), fieldnames=fieldnames)
writer.writeheader()

player_writer = csv.DictWriter(open('player_ratings.csv', 'w'), fieldnames=playerfields)
player_writer.writeheader()


link_1 = 'http://www.espn.com/nba/statistics/team/_/stat/team-comparison-per-game/year/'
link_2 = 'http://www.espn.com/nba/statistics/team/_/stat/offense-per-game/year/'
link_3 = 'http://www.espn.com/nba/statistics/team/_/stat/defense-per-game/year/'
link_4 = 'http://www.espn.com/nba/statistics/team/_/stat/miscellaneous-per-game/year/'


def main():
    #scrape team comparison stats per game
    data = {}
    for year in range(2001, 2018):
        year = str(year)
        r = requests.get(link_1 + year)
        details = html.fromstring(r.content)
        tree = details.xpath(".//*[@id='my-teams-table']/div/div[2]/table/tr")
        for row in tree:
            if len(row.xpath(".//td[2]/a/text()")) > 0:
                team = select(row.xpath(".//td[2]/a/text()")) #team name
                pown = select(row.xpath(".//td[3]/text()")) #team points per game
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
                data[team] = {
                    'Season': year, 'Team': team, 'Points Per Game': pown,
                    'Opponent Points Per Game': popp, 'Point Differential': pdiff,
                    'Own FG%': fgown, 'Opponent FG%': fgopp, 'Own 3p%': town,
                    'Opponent 3p%': topp, 'FT%': free, 'Offensive Rebounds': roff,
                    'Defensive Rebounds': rdef, 'Rebounding %': trp,
                    'Own Turnovers': turno, 'Opponent Turnovers': turnp}
        #scrape team offense stats:
        r = requests.get(link_2 + year)
        details = html.fromstring(r.content)
        tree = details.xpath(".//*[@id='my-teams-table']/div/div[2]/table/tr")
        for row in tree:
            if len(row.xpath(".//td[2]/a/text()")) > 0:
                team = select(row.xpath(".//td[2]/a/text()")) #team name
                off_pts = select(row.xpath(".//td[3]/text()")) #offensive points per game (off efficiency)
                off_fgm = select(row.xpath(".//td[4]/text()")) #field goals made
                off_fga = select(row.xpath(".//td[5]/text()")) #field goals attempted
                off_3pm = select(row.xpath(".//td[7]/text()")) #3 pointers made
                off_3pa = select(row.xpath(".//td[8]/text()")) #3 pointers attempted
                off_ftm = select(row.xpath(".//td[10]/text()")) #free throws made
                off_fta = select(row.xpath(".//td[11]/text()")) #free throws attempted
                off_pps = select(row.xpath(".//td[13]/text()")) #offense points per shot
                off_afg = select(row.xpath(".//td[14]/text()")) #offense adjusted field goal %
                data[team].update(
                    {'Season': year, 'Team': team, 'Offensive adjusted field goal %': off_afg,
                     'Offensive ppg': off_pts, 'Offensive FGM': off_fgm, 'Offensive FGA': off_fga,
                     'Offensive 3pm': off_3pm, 'Offensive 3pa': off_3pa, 'Offensive FTA': off_fta,
                     'Offensive FTM': off_ftm, 'Offensive PPS': off_pps})
        #scrape defensive stats:
        r = requests.get(link_3 + year)
        details = html.fromstring(r.content)
        tree = details.xpath(".//*[@id='my-teams-table']/div/div[2]/table/tr")
        for row in tree:
            if len(row.xpath(".//td[2]/a/text()")) > 0:
                team = select(row.xpath(".//td[2]/a/text()")) #team name
                opp_pts = select(row.xpath(".//td[3]/text()")) #opponent points per game (def efficiency)
                opp_fgm = select(row.xpath(".//td[4]/text()")) #opponent field goals made
                opp_fga = select(row.xpath(".//td[5]/text()")) #opponent field goals attempted
                opp_3pm = select(row.xpath(".//td[7]/text()")) #opponent 3 pointers made
                opp_3pa = select(row.xpath(".//td[8]/text()")) #opponent 3 pointers attempted
                opp_ftm = select(row.xpath(".//td[10]/text()")) #opponent free throws made
                opp_fta = select(row.xpath(".//td[11]/text()")) #opponent free throws attempted
                opp_pps = select(row.xpath(".//td[13]/text()")) #opponent offense points per shot
                opp_afg = select(row.xpath(".//td[14]/text()")) #opponent offense adjusted field goal %
                data[team].update(
                    {'Season': year, 'Team': team, 'Opponent adjusted field goal %': opp_afg,
                     'Opponent ppg': opp_pts, 'Opponent FGM': opp_fgm, 'Opponent FGA': opp_fga,
                     'Opponent 3pm': opp_3pm, 'Opponent 3pa': opp_3pa, 'Opponent FTA': opp_fta,
                     'Opponent FTM': opp_ftm, 'Opponent PPS': opp_pps})
        #scrape misc stats:
        r = requests.get(link_4 + year)
        details = html.fromstring(r.content)
        tree = details.xpath(".//*[@id='my-teams-table']/div/div[2]/table/tr")
        for row in tree:
            if len(row.xpath(".//td[2]/a/text()")) > 0:
                team = select(row.xpath(".//td[2]/a/text()")) #team name
                own_asst = select(row.xpath(".//td[3]/text()")) #team assists per game
                opp_asst = select(row.xpath(".//td[4]/text()")) #opponent assists per game
                own_stl = select(row.xpath(".//td[5]/text()")) #team steals per game
                opp_stl = select(row.xpath(".//td[6]/text()")) #opponent steals per game
                own_blk = select(row.xpath(".//td[7]/text()")) #team blocks per game
                opp_blk = select(row.xpath(".//td[8]/text()")) #opponent blocks per game
                own_trn = select(row.xpath(".//td[9]/text()")) #team turnovers per game
                opp_trn = select(row.xpath(".//td[10]/text()")) #opponent turnovers per game
                team_ato = select(row.xpath(".//td[12]/text()")) #team assist to turnover ratio
                team_tch = select(row.xpath(".//td[13]/text()")) #team technical fouls per season
                data[team].update(
                    {'Season': year, 'Team': team, 'Team APG': own_asst,
                     'Opponent APG': opp_asst, 'Team SPG': own_stl, 'Opponent SPG': opp_stl,
                     'Team BPG': own_blk, 'Opponent BPG': opp_blk, 'Team TPG': own_trn,
                     'Opponent TPG': opp_trn, 'Team ATO': team_ato, 'Team Techs': team_tch})
        writer.writerows(data.values())

    #scrape player stats
    data_two = {}
    for year in range(2001, 2018):
        r = requests.get('http://www.basketball-reference.com/leagues/NBA_' + str(year) + '_per_game.html')
        details = html.fromstring(r.content)
        stats = details.xpath(".//*[@id='per_game_stats']/tbody/tr")
        for row in stats:
            if select(row.xpath(".//td[1]/a[@href]/text()")) is not None:
                player = select(row.xpath(".//td[1]/a[@href]/text()"))
                year = year
                position = select(row.xpath(".//td[2]/text()"))
                age = select(row.xpath(".//td[3]/text()"))
                team = team_convert(select(row.xpath(".//td[4]/a[@href]/text()")))
                games = select(row.xpath(".//td[5]/text()"))
                games_started = select(row.xpath(".//td[6]/text()"))
                mpg = select(row.xpath(".//td[7]/text()"))
                pfgm = select(row.xpath(".//td[8]/text()"))
                pfga = select(row.xpath(".//td[9]/text()"))
                pfgp = select(row.xpath(".//td[10]/text()"))
                ptpm = select(row.xpath(".//td[11]/text()"))
                ptpa = select(row.xpath(".//td[12]/text()"))
                ptpp = select(row.xpath(".//td[13]/text()"))
                ptwo = select(row.xpath(".//td[14]/text()"))
                ptwoa = select(row.xpath(".//td[15]/text()"))
                ptwop = select(row.xpath(".//td[16]/text()"))
                pefg = select(row.xpath(".//td[17]/text()"))
                pft = select(row.xpath(".//td[18]/text()"))
                pfta = select(row.xpath(".//td[19]/text()"))
                pftp = select(row.xpath(".//td[20]/text()"))
                porb = select(row.xpath(".//td[21]/text()"))
                pdrb = select(row.xpath(".//td[22]/text()"))
                ptrb = select(row.xpath(".//td[23]/text()"))
                past = select(row.xpath(".//td[24]/text()"))
                pstl = select(row.xpath(".//td[25]/text()"))
                pblk = select(row.xpath(".//td[26]/text()"))
                ptov = select(row.xpath(".//td[27]/text()"))
                ppf = select(row.xpath(".//td[28]/text()"))
                pppg = select(row.xpath(".//td[29]/text()"))
                data_two[player] = {
                    'Season': year, 'Player': player, 'Team': team, 'Games Played': games, 'Minutes per Game': mpg,
                    'Age': age, 'Games Started': games_started, 'Player Per Game Field Goals Made': pfgm,
                    'Player Per Game Field Goals Attempted': pfga, 'Player Per Game Field Goal Percentage': pfgp,
                    'Player Per Game 3 Pointers Made': ptpm, 'Player Per Game 3 Pointers Attempted': ptpa,
                    'Player Per Game Two Pointers Made': ptwo, 'Player Per Game Two Pointers Attempted': ptwoa,
                    'Player Per Game Two Pointers Percentage': ptwop,
                    'Player Per Game Effective Field Goal Percentage': pefg,
                    'Player Per Game Free Throws Made': pft, 'Player Per Game Free Throws Attempted': pfta,
                    'Player Per Game Free Throw Percentage': pftp, 'Player Per Game Offensive Rebounds': porb,
                    'Player Per Game Defensive Rebounds': pdrb, 'Player Per Game Total Rebounds': ptrb,
                    'Player Per Game Assists': past,
                    'Player Per Game Steals': pstl, 'Player Per Game Blocks': pblk, 'Player Per Game Turnovers': ptov,
                    'Player Per Game Personal Fouls': ppf, 'Player Per Game Points Per Game': pppg,
                    'Player Per Game 3 Pointers Percentage': ptpp,
                    'Position': position}

        player_writer.writerows(data_two.values())


def select(item):
    if item is not None:
        for value in item:
            return value


def team_convert(team):
    try:
        teamdict[team]
    except KeyError:
        return team
    return teamdict[team]


if __name__ == '__main__':
    main()
