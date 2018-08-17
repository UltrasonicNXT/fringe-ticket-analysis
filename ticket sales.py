import glob, csv, copy, os, datetime
import matplotlib.pyplot as plt
import numpy as np
#import plotly.plotly as py
import matplotlib.ticker as ticker

prices = [
    'Price band 1 - Full Price',
    'Price band 1 - Papering Comp',
    'Price band 1 - Company Comp',
    'Price band 1 - Standby Comp',
    'Price band 1 - Press Comp',
    'Price band 1 - Student',
    'Price band 1 - Under 18',
    'Price band 1 - Fringe Industry Comp',
    'Price band 1 - Senior Citizen',
    'Price band 1 - FotF',
    'Price band 1 - 2for1',
    'Price band 1 - Advance Comp',
    'Price band 1 - Unwaged',
    'Price band 1 - Venue Comp',
]

price_dict = {}
for price in prices:
    price_dict[price] = 0

empty = {
    '2018-08-01 16:35':copy.copy(price_dict), # pass the value, not a reference
    '2018-08-02 16:35':copy.copy(price_dict),
    '2018-08-03 16:35':copy.copy(price_dict),
    '2018-08-04 16:35':copy.copy(price_dict),
    '2018-08-05 16:35':copy.copy(price_dict),
    '2018-08-06 16:35':copy.copy(price_dict),
    '2018-08-07 16:35':copy.copy(price_dict),
    '2018-08-08 16:35':copy.copy(price_dict),
    '2018-08-09 16:35':copy.copy(price_dict),
    '2018-08-10 16:35':copy.copy(price_dict),
    '2018-08-11 16:35':copy.copy(price_dict),
    '2018-08-12 16:35':copy.copy(price_dict),
    '2018-08-13 16:35':copy.copy(price_dict),
    '2018-08-14 16:35':copy.copy(price_dict),
    '2018-08-15 16:35':copy.copy(price_dict),
    '2018-08-16 16:35':copy.copy(price_dict),
    '2018-08-17 16:35':copy.copy(price_dict),
    '2018-08-18 16:35':copy.copy(price_dict),
    '2018-08-19 16:35':copy.copy(price_dict),
    '2018-08-20 16:35':copy.copy(price_dict),
    '2018-08-21 16:35':copy.copy(price_dict),
    '2018-08-22 16:35':copy.copy(price_dict),
    '2018-08-23 16:35':copy.copy(price_dict),
    '2018-08-24 16:35':copy.copy(price_dict),
    '2018-08-25 16:35':copy.copy(price_dict),
    '2018-08-26 16:35':copy.copy(price_dict),
    '2018-08-27 16:35':copy.copy(price_dict)
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
                if date not in new_tix:
                    new_tix[date] = {}
                new_tix[date][price] = new[date][price] - old[date][price]
    return new_tix

old = copy.deepcopy(empty)

sold = [] # just pure numbers. list of ints
sold_days = {} # divided by which show they're buying for. dict of list of ints

first = datetime.datetime(2018, 8, 14, 20, 21)
half_hour = datetime.timedelta(minutes=30)
times = []

def get_day_ahead(purchase_date, perf_date):
    perf_datetime = datetime.datetime.fromisoformat(perf_date)
    return (perf_datetime - current_time).days

for filename in sorted(glob.glob('*.csv'), key=os.path.getmtime):

    with open(filename) as csv_file:
        next(csv_file) # skip header row

        new_reader = csv.reader(csv_file)

        new = process_data(new_reader)

        new_tix = compare(new, old)

        # just number
        numbers = sum([sum(new_tix[d].values()) for d in new_tix])
        sold.append(numbers)

        
        # divided by days in advance
        current_time = first + len(times)*half_hour
        times.append(current_time)

        for i in range(0, 30):
            if i not in sold_days:
                sold_days[i] = []
            numbers = sum([sum(new_tix[perf_date].values()) for perf_date in new_tix if get_day_ahead(current_time, perf_date) == i])
            sold_days[i].append(numbers)

        """
        days = {}
        
        for perf_date in new_tix:
            #get datetime from perf_date
            perf_datetime = datetime.datetime.fromisoformat(perf_date)
            days_ahead = (perf_datetime - current_time).days
            if days_ahead not in sold_days:
                sold_days[days_ahead] = []
            sold_days[days_ahead].append(sum(new_tix[perf_date].values()))
            print(new_tix[perf_date])"""
            
        # footer
        old = new

        #0=venue 1=venue_title 2=subvenue 3=subvenue_title 4=event 5=event_title
        #6=perf_date 7=performance 8=status 9=ticket_price 10=fringe_sold_count
        #11=sold_count 12=fringe_sold_value 13=sold_value 14=concession_code

#first time (0) was Tue Aug 14 20:21:29
        
sold[0] = 0 # ignore first one
for key in sold_days:
    sold_days[key][0] = 0

y = sold

x = range(0,len(y))

fig, ax = plt.subplots()

start, end = ax.get_xlim()

#ax.bar(times,y, width=0.018)
previous = sold_days[29] # any empty array
for day_ahead in sold_days:
    sales = sold_days[day_ahead]
    if sum(sales):
        ax.bar(times, sales, width=0.018, bottom=previous, label=str(day_ahead))
        previous = sales

print(sold_days)

ax.xaxis_date()
plt.xticks(rotation=45)

ax.xaxis.set_major_locator(ticker.MultipleLocator(1/12))
plt.legend()
plt.show()

