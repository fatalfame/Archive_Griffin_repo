import random;
import string
from gtts import gTTS
import pyttsx
import os
import time

quote_file = '..//markov/van_halen.txt'
input_file = open(quote_file, 'r')
engine = pyttsx.init()

for line in input_file:
    myobj = gTTS(text=line, lang='en', slow=False)
    engine.say(line)
    myobj.save("test.mp3")
    os.system("test.mp3")
    time.sleep(2)


#
# for line in input_file:
#     if len(line) > 2:
#         print(line)
#         engine.say(line)
#         engine.runAndWait()