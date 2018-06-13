from datetime import datetime, time


def dateDiffInSeconds(date1, date2):
    timedelta = date2 - date1
    return timedelta.days * 24 * 3600 + timedelta.seconds

def daysHoursMinutesSecondsFromSeconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (days, hours, minutes, seconds)

leaving_date = datetime.strptime('2021-01-20 10:00:00', '%Y-%m-%d %H:%M:%S')
now = datetime.now()

print("%d days, %d hours, %d minutes, %d seconds" % daysHoursMinutesSecondsFromSeconds(dateDiffInSeconds(now, leaving_date)))




#
# from tkinter import *
# from tkinter import ttk
# from tkinter import font
# import time
# import datetime
#
# global endTime
#
#
# def quit(*args):
#     root.destroy()
#
#
# def show_time():
#     # Get the time remaining until the event
#     remainder = endTime - datetime.datetime.now()
#     # remove the microseconds part
#     remainder = remainder - datetime.timedelta(microseconds=remainder.microseconds)
#     # Show the time left
#     txt.set(remainder)
#     # Trigger the countdown after 1000ms
#     root.after(1000, show_time)
#
#
# # Use tkinter lib for showing the clock
# root = Tk()
# root.attributes("-fullscreen", True)
# root.configure(background='black')
# root.bind("x", quit)
# root.after(1000, show_time)
#
# # Set the end date and time for the countdown
# endTime = datetime.datetime(2021, 1, 20, 0, 0, 0)
#
# fnt = font.Font(family='Helvetica', size=60, weight='bold')
# txt = StringVar()
# lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="blue", background="black")
# lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
#
# root.mainloop()