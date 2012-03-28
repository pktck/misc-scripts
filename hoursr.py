import sys
import csv
import collections
import pprint
import operator

def parse(filename):
    thefile = open(filename)
    csv_contents = csv.reader(thefile)
    dates_and_hours = [{'date': c[4].split(' ')[0], 'hours': c[9]} for c in csv_contents][1:-1] # strip the header row
    hours_by_date = collections.defaultdict(lambda: 0.0)

    for x in dates_and_hours:
        hours_by_date[x['date']] += float(x['hours'])

    for key in hours_by_date:
        hours_by_date[key] = round(hours_by_date[key] * 4) / 4.0

    parsed = hours_by_date.items()

    parsed.sort(key=operator.itemgetter(0))

    return parsed

if __name__ == '__main__':
    parsed = parse(sys.argv[1])
    for day in parsed:
        print day[0] + '\t' + str(day[1])

    print 'TOTAL:', sum([x[1] for x in parsed])
