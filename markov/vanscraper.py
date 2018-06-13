import requests
import lxml.html


def main():
    r = requests.get('http://www.lyricsfreak.com/v/van+halen/')
    link_list = []
    page_root = lxml.html.fromstring(r.content)
    # page_rows = page_root.xpath("//*[@id='cmn_wrap']/div[5]/div[2]/div[2]/table/tbody/tr/td/a")
    page_rows = page_root.xpath("//*[@id='cmn_wrap']/div[5]/div[2]/div[2]/table/tbody/tr[1]/td[1]/a")
    for thing in page_rows:
        try:
            link_list.append('http://www.lyricsfreak.com/v/van+halen/'+thing.xpath(".//@href")[0][2:])
        except IndexError:
            continue
    for link in link_list:
        print(link)
        rr = requests.get(link)
        root = lxml.html.fromstring(rr.content)
        rows = root.xpath("//*[@id='content']")
        print('rows')
        print(rows)
        for row in rows:
            print(row)
            song = row.xpath(".//text()")
            for line in set(song):
                if '(Guitar Solo)' not in line:
                    print(line)


if __name__ == '__main__':
    main()