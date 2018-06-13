import pickle
import numpy as np
import os.path

np.random.seed(123)

#filepath to the text form which probabilities were extracted
filepath = '..//markov/depechedad.txt'

#maximal order of the Markov chain probabilities to extract
#order = 1 => looks at 1 previous character
maxorder = 10

exists = [False for i in range(maxorder+1)]
counts_dict = {}
for order in range(1, maxorder+1):

    fname = filepath+"_order_"+str(order)+".pickle"
    if os.path.isfile(fname):
        with open(fname,"rb") as fp:  # Python 3: open(..., 'rb')
            counts_dict[order] = pickle.load(fp)
        fp.close()
        print("Order "+str(order)+" loaded.")
        exists[order] = True
    else:
        print("Order "+str(order)+" *NOT FOUND*!")
        exists[order] = False

#initial text as a prior (user lower case)
text = "griffin " #good for 50 Shades
#text = "prophet " #good for the Bible

text_length = 50 #output sequence length

end_of_sequence = False
for t in range(text_length):

    for order in range(min([maxorder, len(text)]), 0, -1):
        history = text[-1*order:]

        if exists[order] and (tuple(history) in counts_dict[order]):
            counts_local = (counts_dict[order])[tuple(history)]
            break
        elif order == 1:
            print("No available continuation from "+"".join(history))
            end_of_sequence = True
            break

    if end_of_sequence == True:
        break

    #counts for possible continuations given the previous order characters
    list_local = [(k, counts_local[k]) for k in counts_local]

    #probability norm == count sum
    total_local = np.sum([c for (s, c) in list_local ])
    probs = [float(c)/total_local for (s, c) in list_local] #probabilities

    cum_probs = [] #cummulative probabilities
    p_sum = 0.0
    for p in probs:
        p_sum += p
        cum_probs.append(p_sum)

    #choosing an option from a list with probs as probabilities
    p_now = np.random.rand()
    cond = (np.array(cum_probs) > p_now)
    ids = [(i-1) for i,x in enumerate(cond) if x == True]
    choice_id = min(ids)

    next_char = list_local[choice_id][0]

    text = text + next_char
    #print(t,order)

print(text)
