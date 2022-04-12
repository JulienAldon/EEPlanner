import unittest
from intranet import Intranet
from mockData import students, events, registered_students, event

class MockIntranet(Intranet):
    def __init__(self, token):
        pass

    def getStudents(self, promotions):
        return students
    
    def registerStudents(self, _event, _students):
        return students

    def createEvent(self, activity, date, hour):
        return event

    def getEvents(self, activity, date=None):
        return events
    
    def getRegisteredStudents(self, _event):
        return registered_students