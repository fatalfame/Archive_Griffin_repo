import requests
from lxml import html
import csv


fieldnames = ['School', 'Season', 'Conf', 'W', 'L', 'Percent', 'SRS', 'SOS', 'OFF', 'DEF', 'AP High',
              'AP Final', 'NCAA']
writer = csv.DictWriter(open('team_stats2.csv', 'w'), fieldnames=fieldnames, lineterminator='\n')
writer.writeheader()


def main():
    r = requests.get('http://www.sports-reference.com/cbb/schools/')
    tree = html.fromstring(r.content)
    teams = tree.xpath(".//*[@id='schools']/tbody/tr/td[1]/a")
    link = 'http://www.sports-reference.com'
    for team in teams:
        link_list = []
        school = team.xpath(".//@href")[0]
        school_name = team.xpath('.//text()')[0]
        link_list.append(link + str(school))
        print(school_name)
        for item in link_list:
            d = requests.get(item)
            details = html.fromstring(d.content)
            stats = details.xpath(".//tbody/tr")
            for row in stats:
                # print(row.get('class'))
                if row.get('class') != 'thead':
                    season = convert(row.xpath(".//*[@data-stat='season']/a//text()"))
                    conf = convert(row.xpath(".//*[@data-stat='conf_abbr']/a//text()"))
                    wins = value(row.xpath(".//*[@data-stat='wins']//text()"))
                    loss = value(row.xpath(".//*[@data-stat='losses']//text()"))
                    percent = value(row.xpath(".//*[@data-stat='win_loss_pct']//text()"))
                    srs = value(row.xpath(".//*[@data-stat='srs']//text()"))
                    sos = value(row.xpath(".//*[@data-stat='sos']//text()"))
                    off = value(row.xpath(".//*[@data-stat='pts_per_g']//text()"))
                    defense = value(row.xpath(".//*[@data-stat='opp_pts_per_g']//text()"))
                    ap_high = value(row.xpath(".//*[@data-stat='rank_min']//text()"))
                    ap_final = value(row.xpath(".//*[@data-stat='rank_final']//text()"))
                    ncaa = convert(row.xpath(".//*[@data-stat='round_max']//text()"))
                    if ncaa in ('Lost First Round', 'Lost Opening Round', 'Lost Regional Final', '',
                                'Lost Regional Semifinal','Lost Second Round', 'Lost Third Round', 'Lost First Four'):
                        ncaa = int(0)
                    if ncaa in ('Lost National Final', 'Lost National SemiFinal', 'Lost Regional Final (Final Four)',
                                'Won National Final', 'Lost National Semifinal'):
                        ncaa = int(1)
                    writer.writerow({'School': school_name, 'Season': season, 'Conf': conf, 'W': wins, 'L': loss,
                                     'Percent': percent, 'SRS': srs, 'SOS': sos, 'OFF': off, 'DEF': defense,
                                     'AP High': ap_high, 'AP Final': ap_final, 'NCAA': ncaa})


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
