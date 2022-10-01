import csv
import json
from datetime import date, datetime, time, timedelta

start_date = date.fromisoformat('2022-10-03')
start_date -= timedelta(days = start_date.weekday())
def load(path):
    with open(path, encoding='utf-8') as f:
        r = csv.reader(f, delimiter='\t')
        return [*r]
    
cml = load('classmap.txt')
tt = load('timetable.txt')

cm = {key: c for c in cml for key in c[0:2]}
    
def parse_weeks(w):
    tokens = w.split(',')
    ws = []
    for token in tokens:
        if '-' in token:
            ts = token.split('-')
            for i in range(int(ts[0]), int(ts[1]) + 1):
                ws.append(i)
        else:
            ws.append(int(token))
    return ws


def parse_evt(row):
    name = cm[row[4]][2]
    time = row[1].split('-')
    time_from = time[0]
    time_to = time[1]
    weeks = parse_weeks(row[2])
    dates = [start_date + timedelta(days = (int(row[0]) - 2) + (week - 1) * 7) for week in weeks]
    return [{'name': name, 'from': time_from, 'to': time_to, 'date': d.isoformat()} for d in dates]

with open('output.json', 'w', encoding='utf-8') as out:
    evts = [evt for row in tt for evt in parse_evt(row)]
    evts.sort(key = lambda e: datetime.combine(date.fromisoformat(e['date']), time.fromisoformat(e['from'])))
    json.dump(evts, out, ensure_ascii=False)