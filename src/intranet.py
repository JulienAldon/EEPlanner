import requests

from time import sleep
from abc import ABC, abstractmethod
from checkers import check_autologin

from constants import PROMOTIONS

class Intranet(ABC):
    """Interface of the communication between model and intranet

    :param token: Must be set before anything
    :type token: str
    """
    @abstractmethod
    async def getStudents(self, promotions):
        """Get list of students of the given promotions

        :param promotions: Promotions code ('msc1', 'msc2', 'wac1', 'wac2', 'premsc')
        :type promotions: list[str]
        :returns: Students or None in case of error
        :rtype: typing.Optional[list[str]]
        """
        ...

    @abstractmethod
    async def registerStudents(self, event, students):
        """Register students to given event

        :param event: Epitech intranet url (format: 'event-xxxxxx')
        :type event: str
        :param students: Students to register.
        :type students: list[str]
        :returns: None on failure, the list of students registered on success
        :rtype: typing.Optional(list[str])
        """
        ...

    @abstractmethod
    async def createEvent(self, activity, date, hour):
        """Create event at a given date for a given activity

        :param activity: Activity url under which to create event
        :type activity: str
        :param date: Date of the event to create (format 'YYYY-MM-DD')
        :type date: str
        :param hour: hour of the start of the event to create (format 'HH-MM-SS')
        :type hour: str
        :returns: A code of the created event
        :rtype: str
        """
        ...

    @abstractmethod
    async def getEvents(self, activity, date=None):
        """Get All events for a given activity
        
        :param activity: Activity url
        :type activity: str
        :param date: date of event to get 
        :type date: typing.Optional(str)
        :returns: Events code of the activity
        :rtype: list
        """
        ...

    @abstractmethod
    async def getRegisteredStudents(self, event):
        """Get All students registered to the given event
        
        :param event: Event url
        :type event: str
        :returns: Registered students
        :rtye: list[dict]
        """
        ...

class Intra(Intranet):
    def __init__(self, token=""):
        self.token = check_autologin(token)

    def set_token(self, token):
        self.token = check_autologin(token)

    def getStudents(self, promotions, year):
        results, nb_items, total = [], 0, 1
        promo = '|'.join(list(map(PROMOTIONS.get, promotions)))
        while nb_items < total:
            try:
                #TODO: Add year in args
                req = requests.get(
                    self.token + f'/user/filter/user?format=json&location=FR/LYN&year={year}&active=true&promo={promo}&offset={nb_items}')
            except Exception as e:
                print(f'[getStudents] An error occured while asking intra : {e}')
                return None
            results += [elem['login'] for elem in req.json()['items']]
            total = req.json()['total']
            nb_items += len(req.json()['items'])
        return results
    
    def registerStudents(self, event, students):
        if not students:
            return None
        data = {
            f'items[{index}][login]' : row
            for index, row in enumerate(students)
        }
        try:
            req = requests.post(
                self.token + event + '/updateregistered?format=json', data)
        except Exception as e:
            print(f'[registerStudents] An error occured while asking intra : {e}')
            return None
        sleep(0.2) # HACK: avoid intra rate limit
        return students

    def createEvent(self, activity, date, hour):
        acti_data = {'start': date + ' ' + hour}
        try:
            req = requests.post(
                self.token + activity + 'planify?format=json', acti_data)
        except Exception as e:
            print(f'An error occured while asking intra : {e}')
            return None
        sleep(0.2) # HACK: avoid intra rate limit
        return req.json()

    def getEvents(self, activity, date=None):
        try:
            activities = requests.get(
                self.token + activity+'?format=json')
        except Exception as e:
            print(f'An error occured while asking intra : {e}')
            return None
        activities_json = activities.json()
        events = activities_json.get('events', None)
        if events == None:
            error_message = activities_json.get('message', None)
            print(error_message)
            print('An error occured with the request : unable to get correct content')
            return None
        if date:
            today_event = [
                a['code'] 
                for a in events
                if a['begin'][:10] == date
            ]
            return today_event
        return events

    def getRegisteredStudents(self, event):
        students = requests.get(
            self.token + event +'/registered?format=json')
        presence = {
            a['login'] : a['present']
            for a in students.json()
        }
        return presence