from selenium import webdriver
import lxml.html
import time


def main():
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get('http://www.azlyrics.com/v/vanhalen.html')
    time.sleep(10)
    link_list = []
    page_root = lxml.html.fromstring(driver.page_source)
    page_rows = page_root.xpath(".//*[@id='listAlbum']/a")
    for thing in page_rows:
        try:
            link_list.append('www.azlyrics.com'+thing.xpath(".//@href")[0][2:])
        except IndexError:
            continue
    for link in link_list:
        driver.get(link)
        link_root = lxml.html.fromstring(driver.page_source)
        link_rows = link_root.xpath(".//body/div[3]/div/div[2]/div[6]")
        for row in link_rows:
            song = row.xpath(".//text()")
            for line in set(song):
                if '[' not in line:
                    print line
    driver.quit()

if __name__ == '__main__':
    main()


