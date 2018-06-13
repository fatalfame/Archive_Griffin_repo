from random import choice

EOS = ['.', '?', '!']
roth_list = ['babe', 'woo', 'cool', 'sexy', 'devil', 'mama', '!', 'lady', 'woman', 'yeah', 'don\'t',
             'down', 'hey', 'uh', 'baby', 'little', 'good', 'dream', 'gonna', 'wanna', 'touch', 'ooh',
             'gotta', 'fire', 'whoa', 'money', 'gimme', 'feelin', 'boys', 'girls', 'damn', 'hot', 'dancing',
             'inside', 'sweet', 'honey', 'lookin', 'sucker', 'jump', 'talkin', 'magic', 'spank', 'whoo',
             'gettin', 'women', 'sugar', 'shoobe', 'in\'', 'bar', 'music', 'come on', 'you know', 'hey hey',
             'i think', 'i got', 'ooo', 'oooh', 'life', 'bout', 'rock', 'drink', 'drug', 'smoke', 'car',
             'hamburger', 'money', 'tattoo', 'heat', 'action', 'satisfied', 'gorgeous', 'beauty', 'window',
             'phone', 'dream', 'world', 'nobody', 'crazy', 'fun', 'sweet', 'ass', 'summer', 'face', 'jimmy',
             'mmm', 'hell', 'dead', 'wrong', 'shine', 'hammerhead', 'shake', 'shoes', 'shark', 'dirty', 'beer',
             'buddy', 'amsterdam', 'cabo', 'beach', 'tan', 'squeeze', 'slide', 'job', 'telephone', 'cream',
             'coast', 'doctor', 'shoo', 'soda', 'insane', 'wild', 'kiss', 'taste', 'lipstick', 'dyke', 'daddy',
             'breathin', 'barely', 'ride', 'rhythm', 'fat', 'free', 'bit', 'lovin', 'street', 'heart', 'round',
             'piss', 'pants', 'gun', 'hips', 'her', 'legs', 'face', 'smile', 'teacher', 'boat', 'jesus', 'whiskey',
             'breakfast', 'harder', 'cradle', 'alimony', 'lover', 'girlfriend', 'lord', 'god']


def main():
    maxsentences = 100
    sentencecount = 0
    while sentencecount < maxsentences:
        fname = '..//markov/vanbible.txt'
        with open(fname, "rt") as f:
            text = f.read()
        words = text.split()
        d = build_dict(words)
        sent = generate_sentence(d)
        sentencecount += 1
        # if len(sent) < 150 and len(sent) > 20:
        if (buzzword in sent for buzzword in roth_list) and len(sent) < 150:
            print(sent)


def build_dict(words):
    """
    Build a dictionary from the words.

    (word1, word2) => [w1, w2, ...]  # key: tuple; value: list
    """
    d = {}
    for i, word in enumerate(words):
        try:
            first, second, third = words[i], words[i+1], words[i+2]
        except IndexError:
            break
        key = (first, second)
        if key not in d:
            d[key] = []
        #
        d[key].append(third)

    return d


def generate_sentence(d):
    li = [key for key in d.keys() if key[0][0].isupper()]
    key = choice(li)

    li = []
    first, second = key
    li.append(first)
    li.append(second)
    while True:
        try:
            third = choice(d[key])
        except KeyError:
            break
        li.append(third)
        if third[-1] in EOS:
            break
        key = (second, third)
        first, second = key
    return ' '.join(li)
####################

if __name__ == "__main__":
    main()
