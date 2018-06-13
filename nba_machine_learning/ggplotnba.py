import ggplot
import pandas
import seaborn as sns; sns.set(color_codes=True)
import numpy as np


# More rows plz!
players = pandas.read_csv('..//NBA_machine_learning/outputs/all_star_probability.csv')
# young = players[players["Age"] > 30]
# players = players[players["Seas"] >= 2016]
# What counties are all the people under 50 from?
# a = ggplot(players, aes(x="X", y="Prob", color="Y")) + geom_point()
# print(a)
# d = ggplot(players, aes(x="Points", y="Salary")) + geom_point() + geom_abline(intercept=20)
# print(d)
# print b
players = players.dropna(axis=0)
ax = sns.regplot(x="Points", y="All Star", data=players, logistic=True)
ax.set(xlabel="Points per game", ylabel="Probability of prediction")
ax.set_title('NBA All Star Classifications')
sns.plt.show()
# ag = sns.regplot(x="Season", y="Salary Cap", data=players, ci=None)
# ag.set_title('NBA Salary Cap On the Rise')
# sns.plt.ylim(0,)
# sns.plt.show()
# ag = sns.lmplot(x="Points", y="Assists", hue="All Star", data=players, palette="Set1", ci=70)
# sns.plt.show()
# Let's add some color!
# c = ggplot(young, aes(x="OperatingRoomMinuteQTY", y="PatientAge", color="GenderDSC")) + geom_point()
# print c
# I like different colors better. I'm going to access those from the qualitative palette.
# (http://docs.ggplot2.org/current/scale_brewer.html)
# d = ggplot(young, aes(x="OperatingRoomMinuteQTY", y="PatientAge", color="GenderDSC")) \
#     + geom_point() + scale_color_brewer(type="qual", palette="Set1")
# print d
# Or from the diverging palette
# e = ggplot(young, aes(x="OperatingRoomMinuteQTY", y="PatientAge", color="GenderDSC")) \
    # + geom_point() + scale_color_brewer(type="div", palette="Spectral")
# print e
# This doesn't work at all for my data I'm analyzing.
# f = ggplot(young, aes(x="OperatingRoomMinuteQTY", y="PatientAge", color="GenderDSC")) \
#     + geom_point() + scale_color_brewer(type="seq", palette="Greens")
# print f
# # I'm just going to reset with a quick plot. How religious is everyone?
# g = qplot(x="ReligionCD", y="PatientAge", data=young)
# print g
# # You can color qplots really easy!
# h = qplot(x="ReligionCD", y="PatientAge", data=young, color="GenderCD")
# print h


