import requests
from time import sleep
import re

INTRA_LINK = r'intra\.epitech\.eu'
activity_url = f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/'

PROMOTIONS = {
    'msc1': 'msc4',
    'msc2': 'msc5',
    'premsc': 'msc3',
    'wac1': 'wac1',
    'wac2': 'wac2'
}
PLANIFICATION_HOURS = [
    '9:00:00',
    '12:00:00',
    '13:30:00',
    '17:00:00'
]

def exec_regex(reg, tstr):
    """return true if reg is found in tstr false otherwise
    """
    matches = re.finditer(reg, tstr, re.MULTILINE)
    for match in matches:
        if match:
            return True
    return False

class Intra:
    """Intra exchange facilities, a token must be set and valid before calling any other methods
    """
    def __init__(self, token="", planification_hours=PLANIFICATION_HOURS):
        self.token = Intra.check_autologin(token)
        self.planification_hours = planification_hours
    
    def set_token(self, token):
        self.token = Intra.check_autologin(token)
        return self.token

    def set_planification_hours(self, hours):
        self.planification_hours = hours

    @staticmethod
    def check_hour_format(hour):
        if not exec_regex(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$', hour):
            return False
        return True

    @staticmethod
    def check_autologin(autologin):
        if exec_regex(r'^http://', autologin):
            autologin = autologin.replace('http', 'https')
        if exec_regex(rf'^{INTRA_LINK}/auth-[0-9a-fA-F]+$', autologin):
            autologin = 'https://' + autologin
            return autologin
        elif exec_regex(r'^auth-[0-9a-fA-F]+$', autologin):
            return f'https://intra.epitech.eu/' + autologin
        elif exec_regex(rf'^https://{INTRA_LINK}/auth-[0-9a-fA-F]+$', autologin):
            return autologin
        return False

    def get_promotions(self, selected_promotions):
        """fetch selected promotions student list
        selected_promotions can be:
            - msc1
            - msc2
            - wac1
            - wac2
            - premsc
        """
        promotions = []
        nb_items = 0
        total = 1
        promo = '|'.join(list(map(PROMOTIONS.get, selected_promotions)))
        while nb_items < total:
            req = requests.get(self.token + f'/user/filter/user?format=json&location=FR/LYN&year=2021&active=true&promo={promo}&offset={nb_items}')
            result = req.json()
            promotions += [elem['login'] for elem in result['items']]
            total = result['total']
            nb_items += len(result['items'])
        return promotions

    def register_students(self, selected_promotions, event):
        """register selected_students to each event given in parameter
        """
        if not self.token:
            print(self.token)
            print('Error : token is not valid')
            return None
        try:
            students = self.get_promotions(selected_promotions)
        except Exception as e:
            print(f'An error occured when retreiving intranet promotions : {e}')
            return None
        if not students:
            return None
        data = {f'items[{index}][login]': row for index, row in enumerate(students)}
        try:
            req = requests.post(self.token+activity_url + event + '/updateregistered?format=json', data)
        except Exception as e:
            print(f'An error occured while asking intra to register students : {e}')
            return None
        sleep(0.2) # HACK: avoid intra rate limit
        return (req.status_code, req.json())

    def planify_sessions(self, dates):
        """create events for each timestamps in the current schedule (dates & self.planification_hours)
        """
        print(self.planification_hours)
        if not self.token:
            print(self.token)
            print("Error : token is not valid")
            return None
        for date in dates:
            for hour in self.planification_hours:
                acti_data = {
                    'start': date + ' ' + hour,
                }
                try:
                    req = requests.post(self.token+activity_url+'planify?format=json', acti_data)
                    sleep(0.2) # HACK: avoid intra rate limit
                except Exception as e:
                    print(f'An error occured while creating activities : {e}')
                    return None
        try:
            activities = requests.get(self.token+activity_url+'?format=json')
            sleep(0.2) # HACK: avoid intra rate limit
        except Exception as e:
            print(f'An error occured while retrieving activities : {e}') 
            return None
        activities_json = activities.json()
        created_activities = [i['code'] for i in activities_json['events'] if i['begin'][:10] in dates]
        if len(created_activities) <= 0:
            print("An error occured : No session created")
            return None
        return created_activities