import twitter
import csv

api = twitter.Api(consumer_key='6bOj60mh5DCuTWwTzcf2FEwOY',
  consumer_secret='i5GeQekQpveNEu8UyfqIeYQ8gxvcyW4y1BHD4d300sKRCtYbSD',
    access_token_key='42350266-RkpUEVXwPsSswJjCS5aApGY8Ma3VXF8i82tG18adA',
    access_token_secret='uGaFjImvoqmWqMpQsxGjFC1QCA3O1BI3cCBiKEJn04Xd2')

# writer = csv.DictWriter(open('twitterbot.csv', 'w'), lineterminator='\n')
# writer.writeheader()

tweets = []
# print(api.VerifyCredentials())
musk = api.GetUserTimeline(screen_name='cnnbrk')
tweets.append([m.text for m in musk])
for t in tweets:
  print(t)
# friends = api.GetFriends(screen_name='Christianh3k')
# print([f.name for f in friends])
# followers = api.GetFriends(screen_name='acrookedhand', total_count=10)
# print([f.name for f in followers])