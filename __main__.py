import os
import argparse
import sys
import datetime
from constants import PROMOTIONS, ACTIVITY_URL
from model import EventPlanner
from intranet import Intra

planified_hours = ['09:00:00', '17:00:00']

if __name__ == "__main__":
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
    
    if os.getenv('INTRANET_AUTOLOGIN'):
        cj = user=os.getenv('INTRANET_AUTOLOGIN')
    else:
        print("Error, no autologin link please create a INTRANET_AUTOLOGIN environment variable")
    
    parser = argparse.ArgumentParser(description='Select promotions and dates')
    parser.add_argument('--promotion', '-p', metavar="promotion", type=str, required=True, action='append', choices=PROMOTIONS.keys())
    parser.add_argument('dates', metavar="dates in %Y-%m-%d", type=valid_date, nargs='*', default=[])
    parser.add_argument('--events', metavar="events", type=valid_event, nargs='*', default=[])
    promotion_arg = parser.parse_args(sys.argv[1:])

    selected_formations = promotion_arg.promotion
    selected_dates = promotion_arg.dates
    selected_event = promotion_arg.events

    print(f"Dates : {selected_dates}")
    print(f"Event : {selected_event}")
    print(f"Formations : {selected_formations}")

    t = Intra(cj)
    intra = EventPlanner(t)

    if len(selected_event) > 0:
        planified_sessions = selected_event
    else:
        print(selected_dates)
        planified_sessions = intra.planify_sessions(selected_dates, planified_hours)

    if planified_sessions:
        sessions = []
        for session in planified_sessions:
            sessions.append(session)
            intra.register_students(ACTIVITY_URL + session, selected_formations)
        print(*sessions, sep=" ")
    else:
        print("No session planified please make sure you are logged in or Set the env variable INTRANET_AUTOLOGIN")