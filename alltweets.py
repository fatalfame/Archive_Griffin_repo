from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml.html
from lxml import html
import time
import requests
import re


driver = webdriver.Firefox()
RESULTS = '//*/div/div/div[@class="js-tweet-text-container"]/p/text()'
SEARCH_BOX = "/html/body/div[2]/div[2]/div/div/div[1]/form/fieldset[1]/div[3]/label/input"
ACCOUNT = "/html/body/div[2]/div[2]/div/div/div[1]/form/fieldset[2]/div[1]/label/input"
BUTTON = "/html/body/div[2]/div[2]/div/div/div[1]/form/button"
word_list = ['Trump', 'The White House', 'The President']
reps = {'Trump': 'Obama', 'Donald': 'Barack', 'The White House': 'The Obama White House', 'Melania': 'Michelle',
        'Ivanka': 'Malia', 'Barron': 'Sasha', 'Eric': 'Malia', 'The President': 'President Obama'}
file = open('quotes3.xls', 'w')


def main():
    driver.get('https://twitter.com/search-advanced?lang=en&lang=en&lang=en&lang=en&lang=en')
    # driver.find_element_by_xpath(SEARCH_BOX).send_keys("Trump, Donald, White")
    driver.find_element_by_xpath(ACCOUNT).send_keys("cnnbrk")
    driver.find_element_by_xpath(BUTTON).click()
    while True:
        page_root = lxml.html.fromstring(driver.page_source)
        table_rows = page_root.xpath(RESULTS)
        for row in table_rows:
            if any(word in row for word in word_list) and len(row) > 10:
                tweet = replace_all(row, reps)
                file.write(tweet)
                file.write('\n')
                # print(tweet)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(1.5)


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

if __name__ == '__main__':
    main()