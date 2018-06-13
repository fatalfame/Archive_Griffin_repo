import markovify

# Get raw text as string.
with open("..//markov/depechedad.txt") as f:
    text = f.read()

roth_list = ['hillary', 'cassie', 'oliver', 'christian', 'karl', 'beth', 'bethany', 'frances', 'hayden', 'hannah',
             'lonny', 'jon', 'shannon', 'daryl', 'jimmer', 'Jimmer', 'mom']


# Build the model.
text_model = markovify.Text(text)

# Print five randomly-generated sentences
#for i in range(5):
#    print(text_model.make_sentence())

# Print three randomly-generated sentences of no more than 140 characters
for i in range(100):
    if (buzzword in (text_model.make_short_sentence(125)) for buzzword in roth_list):
        print((text_model.make_short_sentence(125)))
