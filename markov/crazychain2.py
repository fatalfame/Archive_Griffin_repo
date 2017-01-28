from selenium import webdriver
import lxml.html
import time


def main():
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    counter = range(1, 214)
    for i in counter:
        driver.get('http://www.values.com/inspirational-quotes?page=' + str(i))
        page_root = lxml.html.fromstring(driver.page_source)
        page_rows = page_root.xpath(".//*[@id='container']/div/h6")
        for quote in page_rows:
            song = quote.xpath(".//a/text()")
            for word in set(song):
                length = word.count(' ')
                if length < 20:
                    print song
    driver.quit()

if __name__ == '__main__':
    main()


