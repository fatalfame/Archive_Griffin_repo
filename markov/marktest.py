import random;
import string
import sys;
import re;
# from gtts import gTTS;
# import os;
# import time;


stopword = "\n"
stopsentence = (".", "!")  # Cause a "new sentence" if found at the end of a word
sentencesep  = "\n"  #String used to seperate sentences
quote_file = '..//markov/vanbible3.txt'
input_file = open(quote_file, 'r')


# GENERATE TABLE
w1 = stopword
w2 = stopword
table = {}

for line in input_file:
    if len(line) > 2:
        for word in line.split():
            if word[-1] in stopsentence:
                table.setdefault((w1, w2), []).append(word[0:-1])
                w1, w2 = w2, word[0:-1]
                word = word[-1]
            if w1 != '\n' and w2 != '\n':
                table.setdefault((w1, w2), []).append(word)
                w1, w2 = w2, word
# Mark the end of the file
table.setdefault((w1, w2), []).append(stopword)


# GENERATE SENTENCE OUTPUT
maxsentences = 500
w1 = stopword
w2 = stopword
sentencecount = 0
sentence = []
roth_list = set(['babe', 'woo', 'cool', 'sexy', 'mama', '!', 'yeah', 'hey', 'uh', 'gonna', 'wanna', 'ooh',
                 'gotta', 'whoa', 'gimme', 'feelin', 'dancing', 'lookin', 'sucker', 'jump', 'talkin', 'magic', 'spank',
                 'whoo', 'oh', 'tonight', 'pretty', 'money', 'street'
                 'gettin', 'shoobe', 'music', 'come on', 'you know', 'hey hey',
                 'i think', 'i got', 'ooo', 'oooh', 'bout', 'drug', 'car',
                 'hamburger', 'tattoo', 'gorgeous', 'beauty', 'window',
                 'phone', 'crazy', 'fun', 'ass', 'summer', 'jimmy', 'aah',
                 'mmm', 'hammerhead', 'shark', 'beer', 'sweat', 'cookin',
                 'buddy', 'amsterdam', 'cabo', 'beach', 'tan', 'squeeze', 'slide', 'telephone', 'cream',
                 'doctor', 'shoo', 'soda', 'insane', 'wild', 'kiss', 'taste', 'lipstick', 'dyke', 'daddy',
                 'breathin', 'rhythm', 'lovin', 'piss', 'pants', 'gun', 'hips', 'whiskey','alimony', 'lover',
                 'girlfriend', 'booze', 'shot', 'cops', 'guitar'])
bible_list = set(['god', 'holy', 'peace', 'war', 'angry', 'unto', 'thy', 'saith', 'christ', 'jesus',
                  'sea', 'fire', 'hell', 'cast', 'down', 'earth', 'heaven', 'angel', 'angels', 'satan', 'devil',
                  'thee', 'thou', 'gnashing', 'teeth', 'rain', 'rained', 'fowl', 'king', 'jehovah', 'worship', 'idols',
                  'beast', 'deceiver', 'temptation', 'fool', 'lame', 'tongues', 'flood', 'believe', 'faith', 'holy',
                  'wicked', 'burn', 'tempt', 'temptation', 'sick', 'meek', 'steadfast', 'pray', 'creature', 'kill',
                  'spirit', 'faith', 'shall', 'ye', 'israel', 'mankind', 'unclean', 'unholy', 'flesh',
                  'man', 'son', 'hath', 'king', 'people', 'house', 'before', 'children', 'against', 'land', 'shalt',
                  'behold', 'therefore', 'because', 'hast', 'sons', 'david', 'city', 'moses', 'heart', 'steadfast',
                  'forth', 'neither', 'judah', 'jerusalem', 'according', 'took', 'whom', 'offering', 'temple',
                  'lord', 'eat', 'heard', 'called', 'egypt', 'lamb', 'flock', 'shepherd', 'servant', 'fasting',
                  'prosper', 'riches', 'gold', 'silver',
                  'woe', 'prophet', 'horse', 'commandments', 'amen', 'blessed', 'begat',
                  'almighty', 'wine', 'cursed', 'verily', 'sacrifice', 'atonement', 'pure', 'prophet', 'disciple'])
convo_list = set(['said', 'saieth', 'sayest', 'spoke', 'speaking', 'tell', 'asked', 'ask', 'say', 'commanded',
                  'shout', 'command', 'wrote', 'taught', 'teach', 'saying', 'prophecy', 'teaching', 'written',
                  'testify', 'testified', 'pray', 'wrote', 'voice', 'shouted', 'shouting', 'asketh', 'proclaim',
                  'whipser', 'whispered'])


while sentencecount < maxsentences:
    new_word = random.choice(table[(w1, w2)])
    if new_word == stopword:
        sys.exit()
    if new_word in stopsentence:
        tweet = "%s%s%s" % (" ".join(sentence), new_word, sentencesep)
        fixed_tweet = re.sub(r'[0-9]+:[0-9]+', '', tweet, re.IGNORECASE)
        sentence = []
        lcase_words = [x.lower() for x in tweet.split()]
        no_punct = [x.strip(string.punctuation) for x in lcase_words]
        tokens = set(no_punct)
        if roth_list.intersection(tokens) and bible_list.intersection(tokens) and convo_list.intersection(tokens):
            if len(fixed_tweet) > 30 and len(fixed_tweet) < 150:
                print(roth_list.intersection(tokens))
                print(bible_list.intersection(tokens))
                print(convo_list.intersection(tokens))
                print(fixed_tweet)
                # myobj = gTTS(text=fixed_tweet, lang='en', slow=False)
                # myobj.save("test.mp3")
                # os.system("test.mp3")
                # time.sleep(10)
                sentencecount += 1
    else:
        sentence.append(new_word)
    w1, w2 = w2, new_word