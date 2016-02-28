import pandas


dataframe = pandas.read_csv('outputs/all_players.csv')

print 'the columns in the csv are:'
print dataframe.columns
print

print 'the data types of the columns are:'
print dataframe.dtypes
print 'some columns have objects, some have floats, some have ints'
print 'all columns are dense which means every row has a value in the column'
print 'a columns can be "dense" or "sparse", sparse columns can help with'
print 'memory efficiency'
print

print 'here are 5 random rows:'
print dataframe.sample(5)
print

print 'who scores the most?'
top_five_scorers = dataframe.sort('Points', ascending=False)[:5]
print top_five_scorers[['Player', 'Season', 'Points']]
print

print 'who scores the most? lets try a better way'
print (dataframe
       .groupby('Player')['Points']
       .mean()
       .sort_values(ascending=False)[:5])
print

print 'who are the best scorers of recent years?'
recent_seasons = dataframe[dataframe['Season'].str.startswith('201')]
print (recent_seasons
       .groupby('Player')['Points']
       .mean()
       .sort_values(ascending=False)[:5])
print
