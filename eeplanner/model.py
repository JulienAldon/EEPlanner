class EventPlanner():
    def __init__(self, intranet):
        self.intranet = intranet

    def students_registration(self, event, promotion, year):
        """Register promotion

        :param event: Complete event URL
        :type event: str
        :param promotion: promotion to register ('described in Constants file')
        :type promotion: list[str]
        :returns: Registered students or false otherwise
        :rtype: typing.Optional(list[str])
        """
        if not promotion or len(promotion) == 0 or not event or len(event) == 0 or not year:
            return None
        students = []
        students += self.intranet.get_students(promotion, year)
        if not students:
            return None
        return self.intranet.register_students(event, students)
    
    def planify_sessions(self, activity, dates, hours):
        """Create pce sign event given a list of dates and list of hours

        :param activity: Activity url where to create events
        :type activity: str
        :param dates: All dates to planify
        :type dates: list[str]
        :param hours: Hours to planify
        :type hours: list[str]
        :rtype: list[dict]
        """
        if not dates or not hours or len(dates) == 0 or len(hours) == 0:
            print("no date or hours")
            return None
        res = [self.intranet.create_event(activity, date, hour) for date in dates for hour in hours]
        print(activity)
        return self.intranet.get_events(activity, date=dates[0])
        
