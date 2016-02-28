from selenium import webdriver
import lxml.html
from selenium.common.exceptions import ElementNotVisibleException as Ne
import csv


fieldnames = ['Card Name', 'Description', 'Race', 'Card Class', 'Cost', 'Attack', 'Health', 'Card Pack',
              'Card Type', 'Popularity']
writer = csv.DictWriter(open('..//Code/Griffin_repo/hearthstone/card_database.csv', 'wb'),
                        fieldnames=fieldnames)
writer.writeheader()

SETTINGS = {'needs_driver': True, }
driver = webdriver.Firefox()
NEXT = ".//*[@id='tab-text']/div[1]/div[1]/a[3]"
RESULTS = ".//*[@id='tab-text']/div[2]/table/tbody/tr"


def main(driver):
    driver.implicitly_wait(10)
    driver.get('http://www.hearthhead.com/cards#text')
    driver.find_element_by_xpath(".//*[@id='card-listview-tabs']/div[2]/div/div/div/div[2]/div/a").click()
    while True:
        page_root = lxml.html.fromstring(driver.page_source)
        table_rows = page_root.xpath(RESULTS)
        for item in table_rows:
            card_name = convert(item.xpath('.//td[2]/div/a/text()'))
            description = convert(item.xpath(".//td[2]/div/div[2]/text()"))
            if description is None:
                description = convert(item.xpath(".//td[2]/div/div/text()"))
            race = convert(item.xpath(".//td[4]/a/text()"))
            card_class = convert(item.xpath(".//td[4]/a/text()"))
            cost = value(item.xpath(".//td[6]/span/text()"))
            attack = value(item.xpath(".//td[7]/span/text()"))
            health = value(item.xpath(".//td[8]/span/text()"))
            card_pack = convert(item.xpath(".//td[9]/a[1]/text()"))
            card_type = convert(item.xpath(".//td[9]/a[2]/text()"))
            popularity = value(item.xpath(".//td[11]/text()"))
            writer.writerow({'Card Name': card_name, 'Description': description, 'Race': race,'Card Class': card_class,
                             'Cost': cost, 'Attack': attack, 'Health': health, 'Card Pack': card_pack,
                             'Card Type': card_type, 'Popularity': popularity})
        try:
            driver.find_element_by_xpath(NEXT).click()
        except Ne:
            break


def convert(val):
    if val:
        x = val[0].strip()
        return x.encode('utf-8')
    else:
        return None


def value(val):
    if val:
        x = val[0].strip()
        y = float(x)
        return y
    else:
        return None


if __name__ == '__main__':
    main(driver)
