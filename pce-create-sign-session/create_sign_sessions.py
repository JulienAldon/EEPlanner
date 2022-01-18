import browser_cookie3
import requests
import csv
import os
import argparse
import sys
import datetime

activity_url = f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/'
promotions = {
    'codac': 'CODAC.csv',
    'msc1': 'MSC1.csv',
    'msc2': 'MSC2.csv',
    'premsc': 'PreMSC.csv',
    'wac1': 'WAC1.csv',
    'wac2': 'WAC2.csv'
}
planification_hours = [
    '9:00:00',
    '12:00:00',
    '13:30:00',
    '17:00:00'
]
if os.getenv('INTRANET_AUTOLOGIN'):
    cj = user=os.getenv('INTRANET_AUTOLOGIN')
else:
    print("Error, no autologin link please create a INTRANET_AUTOLOGIN environment variable")

def register_students(selected_list, event):
    students = []
    for selected in selected_list:
        try:
            with open('Promotions/'+promotions[selected], newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=' ')
                tmp = [','.join(row) for row in reader]
                students += tmp[1:]
        except Exception as e:
            print("An error occured : ", e)
            return None
    data = {f'items[{index}][login]': row for index, row in enumerate(students)}
    req = requests.post(cj+activity_url + event + '/updateregistered?format=json', data)
    return (req.status_code, req.json())

def planify_sessions(dates, hours):
    for date in dates:
        for hour in hours:
            acti_data = {
                'start': date + ' ' + hour,
            }
            req = requests.post(cj+activity_url+'planify?format=json', acti_data)
    activities = requests.get(cj+activity_url+'?format=json')
    activities_json = activities.json()
    #gestion erreur si l'intra dit non
    a = [i['code'] for i in activities_json['events'] if i['begin'][:10] in dates]
    if len(a) <= 0:
        print("An error occured : No session created")
        return None
    return a

def valid_date(s):
    try:
        return str(datetime.datetime.strptime(s, "%Y-%m-%d"))[:10]
    except ValueError:
        msg = "Not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)

def valid_event(s):
    try:
        a = s.split('-')
        if a[0] == 'event' and a[1].isnumeric():
            return s
        else:
            raise ValueError("Event format is invalid, must be `event-<numbers>`")
    except ValueError:
        msg = "Not a valid event format"
        raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser(description='Select promotions and dates')
parser.add_argument('--promotion', '-p', metavar="promotion", type=str, required=True, action='append', choices=promotions.keys())
parser.add_argument('dates', metavar="dates in %Y-%m-%d", type=valid_date, nargs='*', default=[])
parser.add_argument('--events', metavar="events", type=valid_event, nargs='*', default=[])
promotion_arg = parser.parse_args(sys.argv[1:])
selected_formations = promotion_arg.promotion
selected_dates = promotion_arg.dates
selected_event = promotion_arg.events

print("dates", selected_dates)
print("event", selected_event)
print("formations", selected_formations)

if len(selected_event) > 0:
    planified_sessions = selected_event
else:
    print(selected_dates)
    planified_sessions = planify_sessions(selected_dates, planification_hours)

if planified_sessions:
    sessions = []
    for session in planified_sessions:
        sessions.append(session)
        register_students(selected_formations, session)
    print(*sessions, sep=" ")
else:
    print("No session planified please make sure you are logged in or Set the env variable INTRANET_AUTOLOGIN")