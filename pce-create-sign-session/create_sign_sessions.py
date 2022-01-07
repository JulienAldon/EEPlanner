import browser_cookie3
import requests
import csv
import os

activity_url = f'https://intra.epitech.eu/module/2021/W-ADM-007/LYN-0-1/acti-505014/'
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
if os.getenv('INTRANET_TOKEN'):
    cj = dict(user=os.getenv('INTRANET_TOKEN'))    
else:
    cj = browser_cookie3.firefox(domain_name='intra.epitech.eu')

print(a.json(), a.status_code)
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
    req = requests.post(activity_url + event + '/updateregistered?format=json', data, cookies=cj)
    return (req.status_code, req.json())

def planify_sessions(dates, hours):
    for date in dates:
        for hour in hours:
            acti_data = {
                'start': date + ' ' + hour,
            }
            req = requests.post(activity_url+'planify?format=json', acti_data, cookies=cj)
    activities = requests.get(activity_url+'?format=json', cookies=cj)
    activities_json = activities.json()['events']
    a = [i['code'] for i in activities_json if i['begin'][:10] in dates]
    if len(a) <= 0:
        print("An error occured : No session created")
        return None
    return a

#TODO: ask user to select dates
#TODO: ask user to select hours
#TODO: ask user to select promotion
selected_formations = ['codac', 'wac1', 'wac2', 'premsc', 'msc1', 'msc2']
selected_dates = ['2022-01-17']
planified_sessions = planify_sessions(selected_dates, planification_hours)

for session in planified_sessions:
    register_students(selected_formations, session)