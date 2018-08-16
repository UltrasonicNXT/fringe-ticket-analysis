import glob, csv, copy, os, datetime
import matplotlib.pyplot as plt
import numpy as np
#import plotly.plotly as py
import matplotlib.ticker as ticker

prices = {
    'Price band 1 - Full Price':0,
    'Price band 1 - Papering Comp':0,
    'Price band 1 - Company Comp':0,
    'Price band 1 - Standby Comp':0,
    'Price band 1 - Press Comp':0,
    'Price band 1 - Student':0,
    'Price band 1 - Under 18':0,
    'Price band 1 - Fringe Industry Comp':0,
    'Price band 1 - Senior Citizen':0,
    'Price band 1 - FotF':0,
    'Price band 1 - 2for1':0,
    'Price band 1 - Advance Comp':0,
    'Price band 1 - Unwaged':0,
    'Price band 1 - Venue Comp':0,
}

empty = {
    '2018-08-01 16:35':copy.copy(prices), # pass the value, not a reference
    '2018-08-02 16:35':copy.copy(prices),
    '2018-08-03 16:35':copy.copy(prices),
    '2018-08-04 16:35':copy.copy(prices),
    '2018-08-05 16:35':copy.copy(prices),
    '2018-08-06 16:35':copy.copy(prices),
    '2018-08-07 16:35':copy.copy(prices),
    '2018-08-08 16:35':copy.copy(prices),
    '2018-08-09 16:35':copy.copy(prices),
    '2018-08-10 16:35':copy.copy(prices),
    '2018-08-11 16:35':copy.copy(prices),
    '2018-08-12 16:35':copy.copy(prices),
    '2018-08-13 16:35':copy.copy(prices),
    '2018-08-14 16:35':copy.copy(prices),
    '2018-08-15 16:35':copy.copy(prices),
    '2018-08-16 16:35':copy.copy(prices),
    '2018-08-17 16:35':copy.copy(prices),
    '2018-08-18 16:35':copy.copy(prices),
    '2018-08-19 16:35':copy.copy(prices),
    '2018-08-20 16:35':copy.copy(prices),
    '2018-08-21 16:35':copy.copy(prices),
    '2018-08-22 16:35':copy.copy(prices),
    '2018-08-23 16:35':copy.copy(prices),
    '2018-08-24 16:35':copy.copy(prices),
    '2018-08-25 16:35':copy.copy(prices),
    '2018-08-26 16:35':copy.copy(prices),
    '2018-08-27 16:35':copy.copy(prices)
}

def process_data(csv_data):
    data = copy.deepcopy(empty) # is this nessacary? probably
    for line in csv_data:
        data[line[6]][line[14]] += int(line[10]) + int(line[11])
    return data

def compare(new, old):
    new_tix = {}
    for date in old:
        for price in old[date]:
            if new[date][price] > old[date][price]:
                new_tix[date] = {}
                new_tix[date][price] = new[date][price] - old[date][price]
    return new_tix

old = copy.deepcopy(empty)

sold = []

for filename in sorted(glob.glob('*.csv'), key=os.path.getmtime):

    with open(filename) as csv_file:
        next(csv_file) # skip header row

        new_reader = csv.reader(csv_file)

        new = process_data(new_reader)

        new_tix = compare(new, old)

        numbers = sum([sum(new_tix[d].values()) for d in new_tix])

        sold.append(numbers)

        old = new

        #0=venue 1=venue_title 2=subvenue 3=subvenue_title 4=event 5=event_title
        #6=perf_date 7=performance 8=status 9=ticket_price 10=fringe_sold_count
        #11=sold_count 12=fringe_sold_value 13=sold_value 14=concession_code

#first time (0) was Tue Aug 14 20:21:29
        
sold[0] = 0 # ignore first one

y = sold

x = range(0,len(y))

first = datetime.datetime(2018, 8, 14, 20, 21)
half_hour = datetime.timedelta(minutes=30)

times = [first + x*half_hour for x in range(0, len(y))]

fig, ax = plt.subplots()

start, end = ax.get_xlim()

print(start,end)
#ax.xaxis.set_ticks(range(0, len(x), 12))

ax.bar(times,y, width=0.015)
ax.xaxis_date()
plt.xticks(rotation=45)

ax.xaxis.set_major_locator(ticker.MultipleLocator(1/12))

plt.show()
