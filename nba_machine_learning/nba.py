from selenium import webdriver
import lxml.html
import time
import csv


fieldnames = ['Player', 'Season', 'Age', 'Team', 'Points', 'Rebounds', 'Assists', 'Mins', 'FTA', 'Blocks',
              'Fouls', '3p%', 'FGA', '2p%', 'ft%', 'Steals', 'Turnovers', 'Games', 'Games Started', 'FGM', '3pa',
              '3pm', 'ftm', 'orb', 'drb', 'FG%', 'EFG%', 'TS%']
writer = csv.DictWriter(open('..//nba_machine_learning/outputs/2017-18.csv', 'w'), lineterminator='\n',
                        fieldnames=fieldnames)
writer.writeheader()

driver = webdriver.Firefox()
START_URL = 'http://www.basketball-reference.com/play-index/psl_finder.cgi'
PER_GAME = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[1]/div[1]/div[2]/div[2]/label/div[1]/input"
ACTIVE = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[1]/div[6]/div[2]/div[1]/label/div[1]/input"
FROM = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[1]/div[10]/div[5]/button[4]"
SC_ERA = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[1]/div[10]/div[5]/button[3]"
TO = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[1]/div[10]/div[4]/div/select/option[72]"
STAR = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[1]/div[17]/div[2]/div[1]/label/div[1]/input"
NON_STAR = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[1]/div[17]/div[2]/div[2]/label/div[1]/input"
OPTION = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[2]/div[5]/div[2]/div/label/div[1]/input"
SORT = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[2]/div[4]/div[3]/select/option[2]"
SEARCH = "/html/body/div[2]/div[2]/div[1]/form/div[2]/div[2]/div[6]/div/input"
RESULTS = "/html/body/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/table/tbody/tr"
# RESULTS = ".//*[@id='stats']/tbody/tr and not(contains(@class, 'thead'))"
NEXT = '/html/body/div[2]/div[2]/div[1]/div[3]/p/a[contains(text(),"Next page")]'

def main(driver):
    driver.implicitly_wait(10)
    driver.get(START_URL)
    driver.find_element_by_xpath(PER_GAME).click()
    driver.find_element_by_xpath(ACTIVE).click()
    driver.find_element_by_xpath(FROM).click()
    # driver.find_element_by_xpath(SC_ERA).click()
    driver.find_element_by_xpath(TO).click()
    # driver.find_element_by_xpath(STAR).click()
    # driver.find_element_by_xpath(NON_STAR).click()
    driver.find_element_by_xpath(OPTION).click()
    driver.find_element_by_xpath(SORT).click()
    driver.find_element_by_xpath(SEARCH).click()
    while True:
        page_root = lxml.html.fromstring(driver.page_source)
        table_rows = page_root.xpath(RESULTS)
        for row in table_rows:
            try:
                if row.xpath('.//td[1]/a/text()'):
                    player = value(row.xpath('.//td[1]/a/text()'))
                    print(player)
            except IndexError:
                continue
            season = value(row.xpath('.//td[5]/text()'))
            team = value(row.xpath('.//td[3]/a/text()'))
            games = num(row.xpath('.//td[6]/text()'))
            tpa = num(row.xpath('.//td[14]/text()'))
            tpm = num(row.xpath('.//td[13]/text()'))
            gs = num(row.xpath('.//td[7]/text()'))
            age = num(row.xpath('.//td[2]/text()'))
            mins = num(row.xpath('.//td[8]/text()'))
            rebs = num(row.xpath('.//td[19]/text()'))
            ftm = num(row.xpath('.//td[15]/text()'))
            asst = num(row.xpath('.//td[20]/text()'))
            pts = num(row.xpath('.//td[25]/text()'))
            fgm = num(row.xpath('.//td[9]/text()'))
            fga = num(row.xpath('.//td[10]/text()'))
            fta = num(row.xpath('.//td[16]/text()'))
            orb = num(row.xpath('.//td[17]/text()'))
            drb = num(row.xpath('.//td[18]/text()'))
            steals = num(row.xpath('.//td[21]/text()'))
            blk = num(row.xpath('.//td[22]/text()'))
            tov = num(row.xpath('.//td[23]/text()'))
            pf = num(row.xpath('.//td[24]/text()'))
            fgp = num(row.xpath('.//td[26]/text()'))
            twos = num(row.xpath('.//td[27]/text()'))
            three = num(row.xpath('.//td[28]/text()'))
            efg = num(row.xpath('.//td[29]/text()'))
            free = num(row.xpath('.//td[30]/text()'))
            ts = num(row.xpath('.//td[31]/text()'))
            if age:
                writer.writerow({'Player': player, 'Season': season, 'Age': age, 'Team': team, 'Points': pts,
                                 'Rebounds': rebs, 'Assists': asst, 'Mins': mins, 'FTA': fta, 'Blocks': blk,
                                 'Fouls': pf, '3p%': three, 'FGA': fga, '2p%': twos, 'ft%': free, 'Steals': steals,
                                 'Turnovers': tov, 'Games': games, 'Games Started': gs, 'FGM': fgm, '3pa': tpa,
                                 '3pm': tpm, 'ftm': ftm, 'orb': orb, 'drb': drb, 'FG%': fgp, 'EFG%': efg, 'TS%': ts})
        for n in range(0, 2):
            time.sleep(3)
        driver.find_element_by_xpath(NEXT).click()


def num(item):
    try:
        if item:
            item = item[0]
            return float(item)
    except IndexError:
        pass

        
def value(item):
    try:
        if item:
            item = item[0]
            return item
    except IndexError:
        pass


if __name__ == '__main__':
    main(driver)


