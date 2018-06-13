import requests
from lxml import html
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as NE
from selenium.common.exceptions import NoAlertPresentException as NA
import time


fieldnames = ['Player', 'Season', 'Age', 'Team', 'Points', 'Rebounds', 'Assists', 'Mins', 'FTA', 'Blocks',
              'Fouls', '3p%', 'FGA', '2p%', 'ft%', 'Steals', 'Turnovers', 'Games', 'Games Started', 'FGM', '3pa',
              '3pm', 'ftm', 'orb', 'drb', 'FG%', 'EFG%', 'TS%']
writer = csv.DictWriter(open('ncaa_player_stats.csv', 'wb'), fieldnames=fieldnames, lineterminator='\n')
writer.writeheader()
driver = webdriver.Chrome()
START_URL = 'http://www.sports-reference.com/cbb/play-index/psl_finder.cgi'
SEARCH = ".//*[@id='psl_finder']/div[2]/div[2]/div[4]/input"
SEASON = ".//*[@id='psl_finder']/div[2]/div[1]/div[1]/div[2]/button[2]"
NEXT = ".//*[@id='pi']/div[3]/p/a[contains(text(), 'Next page')]"


def main(driver):
    driver.implicitly_wait(10)
    driver.get(START_URL)
    # driver.find_element_by_xpath(SEASON).click()
    driver.find_element_by_xpath(".//*[@id='order_by']/select/option[2]").click()
    driver.find_element_by_xpath(SEARCH).click()
    link = 'http://www.sports-reference.com'
    while True:
        r = requests.get(driver.current_url)
        page = html.fromstring(r.content)
        try:
            driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
            x = driver.find_element_by_xpath(".//*[@id='t402-prompt']/div[2]/div[3]/a[2]")
            if x:
                driver.find_element_by_xpath(".//*[@id='t402-prompt']/div[2]/div[3]/a[2]").click()
        except NE:
            pass
        players = page.xpath(".//*[@id='stats']/tbody/tr/td[1]")
        for p in players:
            plink = p.xpath(".//a/@href")[0]
            g = requests.get(link + str(plink))
            h = html.fromstring(g.content)
            try:
                player = h.xpath(".//*[@id='meta']/div/h1/text()")[0]
                print player
            except IndexError:
                break
            stats = h.xpath(".//*[@id='players_per_game']/tfoot/tr[1]")
            for row in stats:
                mpg = convert(row.xpath(".//td[4]/text()"))
                season = row.xpath(".//td[3]/a/text()")
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
                # print ppg
                # if row.get('class') != 'thead':
                writer.writerow({'Player': player, 'Season': season, 'Points': ppg,
                                 'Rebounds': trb, 'Assists': ast, 'Mins': mpg, 'FTA': fta, 'Blocks': blk,
                                 'Fouls': pf, '3p%': tpp, 'FGA': fga, '2p%': twos, 'ft%': ftp, 'Steals': stl,
                                 'Turnovers': tov, 'FGM': fgm, '3pa': tpa,
                                 '3pm': tpm, 'ftm': ftm, 'FG%': fgp})
        driver.find_element_by_xpath(NEXT).click()


def convert(val):
    if val:
        try:
            x = float(val[0])
        except TypeError:
            x = 0
            pass
        return x
    else:
        val = float(0)
    return val


if __name__ == '__main__':
    main(driver)
