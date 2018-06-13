import pandas as pd
import random

df = pd.read_excel('..//markov/word_lists.xlsx', sheet_name=0)
column1 = df.values.T[0].tolist()
column2 = df.values.T[1].tolist()
column3 = df.values.T[2].tolist()

for c in column1:
    print(random.choice(column1), random.choice(column2), random.choice(column3))
