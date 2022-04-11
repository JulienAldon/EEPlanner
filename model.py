from constants import ACTIVITY_URL

class EventPlanner():
    def __init__(self, intranet):
        self.intranet = intranet

    def students_registration(self, event, promotions):
        """Register promotion

        :param event: Complete event URL
        :type event: str
        :param promotions: promotions to register ('described in Constants file')
        :type promotions: list[str]
        :returns: Registered students or false otherwise
        :rtype: typing.Optional(list[str])
        """
        if not promotions or len(promotions) == 0:
            return None
        students = self.intranet.getStudents(promotions)
        if not students:
            return None
        return self.intranet.registerStudents(event, students)
    
    def planify_sessions(self, dates, hours):
        """Create pce sign event given a list of dates and list of hours

        :param dates: All dates to planify
        :type dates: list[str]
        :param hours: Hours to planify
        :type hours: list[str]
        :rtype: list[dict]
        """
        if not dates or not hours or len(dates) == 0 or len(hours) == 0:
            return None
        res = [self.intranet.createEvent(ACTIVITY_URL, date, hour) for date in dates for hour in hours]
        return self.intranet.getEvents(ACTIVITY_URL, dates[0])
        
