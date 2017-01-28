import markovify

# Get raw text as string.
with open("..//Griffin_repo/markov/vanbible4.txt") as f:
    text = f.read()

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


# Build the model.
text_model = markovify.Text(text)

# Print five randomly-generated sentences
#for i in range(5):
#    print(text_model.make_sentence())

# Print three randomly-generated sentences of no more than 140 characters
for i in range(100):
    if (buzzword in (text_model.make_short_sentence(125)) for buzzword in roth_list):
        print'======',(text_model.make_short_sentence(125))