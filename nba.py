from selenium import webdriver
import lxml.html
import time
import csv


fieldnames = ['Player', 'Season', 'Age', 'Points', 'Rebounds', 'Assists', 'Minutes', 'FTA', 'Blocks', 'Fouls', '3p%',
              'FGA', '2p%', 'FG', 'ft%', 'Steals', 'Turnovers']
writer = csv.DictWriter(open('..//Code/nba_machine_learning/outputs/2015-16_roster.csv', 'wb'),
                        fieldnames=fieldnames)
writer.writeheader()


SETTINGS = {'needs_driver': True, }

driver = webdriver.Firefox()
START_URL = 'http://www.basketball-reference.com/play-index/psl_finder.cgi'
PER_GAME = ".//*[@id='psl_finder']/table/tbody/tr[2]/td[1]/div[1]/div/div[2]/input"
ACTIVE = ".//*[@id='psl_finder']/table/tbody/tr[2]/td[3]/div[2]/div/input[1]"
FROM = ".//*[@id='year_min']/option[71]"
TO = ".//*[@id='year_min']/option[70]"
# STAR = ".//*[@id='as_single']/div/div/input[1]"
OPTION = ".//*[@id='order_by']/option[1]"
SORT = ".//*[@id='psl_finder']/table/tbody/tr[2]/td[4]/div[3]/div[3]/input"
SEARCH = ".//*[@id='psl_finder']/table/tbody/tr[2]/td[4]/div[3]/div[4]/input"
RESULTS = ".//*[@id='stats']/tbody/tr"
NEXT = './/div[3]/p[2]/a[contains(text(),"Next page")]'


def main(driver):
    driver.implicitly_wait(10)
    driver.get(START_URL)
    driver.find_element_by_xpath(PER_GAME).click()
    driver.find_element_by_xpath(ACTIVE).click()
    driver.find_element_by_xpath(FROM).click()
    driver.find_element_by_xpath(TO).click()
    # driver.find_element_by_xpath(STAR).click()
    driver.find_element_by_xpath(OPTION).click()
    driver.find_element_by_xpath(SORT).click()
    driver.find_element_by_xpath(SEARCH).click()
    while True:
        page_root = lxml.html.fromstring(driver.page_source)
        table_rows = page_root.xpath(RESULTS)
        for row in table_rows:
            try:
                if row.xpath('.//td[2]/a')[0].text:
                    player = row.xpath('.//td[2]/a')[0].text
            except IndexError:
                continue
            season = row.xpath('.//td[3]')[0].text
            age = row.xpath('.//td[4]')[0].text
            mins = row.xpath('.//td[9]')[0].text
            rebs = row.xpath('.//td[20]')[0].text
            asst = row.xpath('.//td[21]')[0].text
            pts = row.xpath('.//td[26]')[0].text
            fg = row.xpath('.//td[10]')[0].text
            fga = row.xpath('.//td[11]')[0].text
            fta = row.xpath('.//td[17]')[0].text
            steals = row.xpath('.//td[22]')[0].text
            blk = row.xpath('.//td[23]')[0].text
            tov = row.xpath('.//td[24]')[0].text
            pf = row.xpath('.//td[25]')[0].text
            twos = row.xpath('.//td[28]')[0].text
            three = row.xpath('.//td[29]')[0].text
            free = row.xpath('.//td[31]')[0].text
            writer.writerow({'Player': player, 'Season': season, 'Age': age, 'Points': pts, 'Rebounds': rebs,
                             'Assists': asst, 'Minutes': mins, 'FG': fg, 'FGA': fga, 'FTA': fta, 'Steals': steals,
                             'Blocks': blk, 'Turnovers': tov, 'Fouls': pf, '2p%': twos, '3p%': three, 'ft%': free})
        for n in xrange(0, 2):
            time.sleep(3)
        driver.find_element_by_xpath(NEXT).click()


if __name__ == '__main__':
    main(driver)


