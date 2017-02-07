import requests
from requests.exceptions import ConnectionError as CE
import lxml.html
import string
import itertools
import csv
import re
from requests.exceptions import ChunkedEncodingError as CH


fieldnames = ['Player', 'Season', 'Age', 'Team', 'Points', 'Rebounds', 'Assists', 'Mins', 'FTA', 'Blocks',
              'Fouls', '3p%', 'FGA', '2p%', 'ft%', 'Steals', 'Turnovers', 'Games', 'Games Started', 'FGM', '3pa',
              '3pm', 'ftm', 'orb', 'drb', 'FG%', 'EFG%', 'TS%']
writer = csv.DictWriter(open('cbb_player_statst-z.csv', 'wb'), fieldnames=fieldnames, lineterminator='\n')
writer.writeheader()


def main():
    for a in itertools.product(string.ascii_lowercase[19:]):
        try:
            r = requests.get('http://www.sports-reference.com/cbb/players/' + str(a[0] + '-index.html'))
        except CE:
            continue
        tree = lxml.html.fromstring(r.content)
        players = tree.xpath(".//*[@id='content']/div/p")
        for p in players:
            try:
                y = requests.get('http://www.sports-reference.com/' + str(p.xpath('.//a/@href')[0]))
            except CE:
                try:
                    y = requests.get('http://www.sports-reference.com/' + str(p.xpath('.//a/@href')[0]))
                except CH:
                    continue
            player = p.xpath(".//a/text()")[0]
            print player
            s = p.xpath(".//small/text()")[0]
            seasons = re.sub(r"\(|-.*", "", s)
            z = lxml.html.fromstring(y.content)
            stats = z.xpath(".//*[@id='players_per_game']/tfoot/tr[1]")
            for row in stats:
                mpg = convert(row.xpath(".//td[4]/text()"))
                fgm = convert(row.xpath(".//td[5]/text()"))
                fga = convert(row.xpath(".//td[6]/text()"))
                fgp = convert(row.xpath(".//td[7]/text()"))
                twos = convert(row.xpath(".//td[8]/text()"))
                twoa = convert(row.xpath(".//td[9]/text()"))
                twop = convert(row.xpath(".//td[10]/text()"))
                tpm = convert(row.xpath(".//td[11]/text()"))
                tpa = convert(row.xpath(".//td[12]/text()"))
                tpp = convert(row.xpath(".//td[13]/text()"))
                ftm = convert(row.xpath(".//td[14]/text()"))
                fta = convert(row.xpath(".//td[15]/text()"))
                ftp = convert(row.xpath(".//td[16]/text()"))
                trb = convert(row.xpath(".//td[17]/text()"))
                ast = convert(row.xpath(".//td[18]/text()"))
                stl = convert(row.xpath(".//td[19]/text()"))
                blk = convert(row.xpath(".//td[20]/text()"))
                tov = convert(row.xpath(".//td[21]/text()"))
                pf = convert(row.xpath(".//td[22]/text()"))
                ppg = convert(row.xpath(".//td[23]/text()"))
                # if row.get('class') != 'thead':
                writer.writerow({'Player': player, 'Season': seasons, 'Points': ppg,
                                 'Rebounds': trb, 'Assists': ast, 'Mins': mpg, 'FTA': fta, 'Blocks': blk,
                                 'Fouls': pf, '3p%': tpp, 'FGA': fga, '2p%': twos, 'ft%': ftp, 'Steals': stl,
                                 'Turnovers': tov, 'FGM': fgm, '3pa': tpa,
                                 '3pm': tpm, 'ftm': ftm, 'FG%': fgp})


def convert(val):
    if val:
        x = val[0]
        return x
    else:
        val = float(0)
    return val


def value(val):
    if val:
        x = val[0]
        y = float(x)
        return y
    else:
        val = float(0)
    return val


if __name__ == '__main__':
    main()
