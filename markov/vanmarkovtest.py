import random;
import string
import sys;
import re;
import markovify


# with open('..//markov/van_halen.txt') as f:

with open('..//markov/vanbible3.txt') as f:
    text_model = markovify.Text(f, retain_original=False)

print(text_model.make_sentence())