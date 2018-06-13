import textblob
import csv
from aylienapiclient import textapi

def main():

    print('hello')

    # # Initialize a new client of AYLIEN Text API
    client = textapi.Client("2c3e9386", "16df7c1346dca44686403928cf518192")

    with open('van_halen_analysis.csv', 'w', encoding='utf8', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Lyric", "Sentiment"])
        with open("van_halen.txt", 'r') as f:
            for lyrics in f.readlines():
                ## Remove extra spaces or newlines around the text
                lyric = lyrics.strip()
                if len(lyric) == 0:
                    # print('skipped')
                    continue
                ## Make call to AYLIEN Text API
                sentiment = client.Sentiment({'text': lyric})

                ## Write the sentiment result into csv file
                csv_writer.writerow([sentiment['text'], sentiment['polarity']])

if __name__ == '__main__':
    main()


