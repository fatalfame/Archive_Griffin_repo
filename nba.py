from selenium import webdriver
import lxml.html
import time
import csv


fieldnames = ['Player', 'Season', 'Age', 'Points', 'Rebounds', 'Assists', 'Minutes']
writer = csv.DictWriter(open('..//Code/ncaa_machine_learning/outputs/nba_players.csv', 'wb'),
                        fieldnames=fieldnames)
writer.writeheader()


SETTINGS = {'needs_driver': True, }

driver = webdriver.Firefox()
START_URL = 'http://www.basketball-reference.com/play-index/psl_finder.cgi'
PER_GAME = ".//*[@id='psl_finder']/table/tbody/tr[2]/td[1]/div[1]/div/div[2]/input"
ACTIVE = ".//*[@id='psl_finder']/table/tbody/tr[2]/td[3]/div[2]/div/input[1]"
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
            writer.writerow({'Player': player, 'Season': season, 'Age': age, 'Points': pts, 'Rebounds': rebs,
                             'Assists': asst, 'Minutes': mins})
            # print player+'/', season+'/', age+'/', pts+'/', rebs+'/', asst+'/', mins
        for n in xrange(0, 2):
            time.sleep(5)
        driver.find_element_by_xpath(NEXT).click()




if __name__ == '__main__':
    main(driver)


