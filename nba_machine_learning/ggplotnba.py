from ggplot import *
import pandas


# More rows plz!
players = pandas.read_csv('..//NBA_machine_learning/2016-17_players.csv')
young = players[players["Age"] > 30]
# What counties are all the people under 50 from?
a = ggplot(players, aes(x="Age", y="PS/G", label="Player")) + geom_point() + geom_text()
# print a
d = ggplot(players, aes(x="Age", y="PS/G", color="AST")) + geom_point()
print d
# print b
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


