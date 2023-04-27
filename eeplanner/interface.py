import gi
import threading
import datetime
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from eeplanner.model import EventPlanner
from eeplanner.checkers import check_autologin, check_hour_format, check_activity_format
import sys
import os

import pathlib

import yawaei

DAYS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
FORMAT_ERROR_MESSAGE = """
Format authorized :
    - https://<intranet-link>/<autologin-token>
    - <intranet-link>/<autologin-token>
    - <autologin-token>
http is replaced by https
"""

class Handler:
    """GTK event handler class connected to builder signal
    """
    def __init__(self, app):
        self.application = app

    def onDestroy(self, *args):
        Gtk.main_quit()

    def button_error_handling(self):
        if not self.application.get_planning_hours() or len(self.application.get_planning_hours()) <= 0:
            self.application.hours.forall(self.onAddWidget)
        if not self.application.intra_autologin.get_text():
            self.application.error_dialog_window(
                "Error : no Epitech intranet autologin token provided.",
                "Find it under the administration tab on the Epitech intranet !"
            )
            return
        token = check_autologin(self.application.intra_autologin.get_text())
        if not token:
            self.application.error_dialog_window(
                "Error : invalid Epitech intranet autologin token format.",
                FORMAT_ERROR_MESSAGE
            )
            return
        self.application.set_activity_url(self.application.activity_input.get_text())
        if not self.application.get_activity_url() or not check_activity_format(self.application.get_activity_url()):
            self.application.error_dialog_window(
                "Error : no activity recognized selected, please provide an activity url.",
                "format : /module/<year>/<module-code>/<session>/<activity-code>"
            )
            return
        self.application.thrower.set_token(token)

    def onSendForm(self, button):
        self.button_error_handling()
        if self.application.progress.get_fraction() == 0.0:
            thread = threading.Thread(target=self.application.planify_and_register)
            thread.daemon = True
            thread.start()
        else:
            self.application.error_dialog_window("Error : cannot start job, another one is already running.")
            return

    def onPlanify(self, button):
        self.button_error_handling()
        if self.application.progress.get_fraction() == 0.0:
            thread = threading.Thread(target=self.application.planify)
            thread.daemon = True
            thread.start()
        else:
            self.application.error_dialog_window("Error : cannot start job, another one is already running.")
            return
    
    def onRegister(self, button):
        self.button_error_handling()
        if len(self.application.planned) == 0 and self.application.specific_session_active.get_active() == False:
            self.application.error_dialog_window(
                "Error : you must planify sessions before student registration",
            )
            return
        if self.application.progress.get_fraction() == 0.0:
            thread = threading.Thread(target=self.application.register)
            thread.daemon = True
            thread.start()
        else:
            self.application.error_dialog_window("Error : cannot start job, another one is already running.")
            return

    def onAddWidget(self, widget):
        if widget.get_active():
            self.application.planning_hours.append(widget.get_label())

    def onAddHour(self, button):
        new_label = self.application.new_hour_label.get_text()
        if not check_hour_format(new_label):
            self.application.error_dialog_window('Error : entry must be a correct hour format')
            return
        new_checkbox = Gtk.CheckButton(label=self.application.new_hour_label.get_text())
        self.application.set_planning_hours([])
        self.application.hours.add(new_checkbox)
        new_checkbox.show()
    
    def onDateSwitch(self, button):
        if button.get_label() == 'gtk-go-back':
            self.application.set_dates(self.application.selected_date + datetime.timedelta(days=-7))
        elif button.get_label() == 'gtk-go-forward':
            self.application.set_dates(self.application.selected_date + datetime.timedelta(days=7))
        elif button.get_label() == 'gtk-refresh':
            self.application.set_dates(datetime.date.today())

class Application:
    """
    Class Application for GTK window using Glade
    """
    def __init__(self):
        self.builder = Gtk.Builder()
        print(os.path.abspath(os.path.dirname(__file__)))
        self.builder.add_from_file(f'{pathlib.Path.home()}/.local/lib/eeplanner/Application2.glade')
        self.builder.connect_signals(Handler(self))

        self.window = self.builder.get_object("Window")
        self.window.show_all()
        
        self.progress = self.builder.get_object('Bar')
        self.intra_autologin = self.builder.get_object('IntraInput')

        self.thrower = yawaei.intranet.AutologinIntranet()
        self.intra = EventPlanner(self.thrower)

        self.planned = {}

        self.current_year = self.thrower.get_current_scholar_year()
        self.YEARS = [str(int(self.current_year) - 1), self.current_year]

        self.enabled_promotions = {
            day: { year: {
                'wac1': self.builder.get_object(f'{day}Wac1_year{"-1" if year == min(self.YEARS) else ""}'),
                'wac2': self.builder.get_object(f'{day}Wac2_year{"-1" if year == min(self.YEARS) else ""}'),
                'msc1': self.builder.get_object(f'{day}Msc1_year{"-1" if year == min(self.YEARS) else ""}'),
                'msc2': self.builder.get_object(f'{day}Msc2_year{"-1" if year == min(self.YEARS) else ""}'),
                'premsc': self.builder.get_object(f'{day}PreMsc_year{"-1" if year == min(self.YEARS) else ""}'),
                'tek1': self.builder.get_object(f'{day}Tek1_year{"-1" if year == min(self.YEARS) else ""}'),
                'tek2': self.builder.get_object(f'{day}Tek2_year{"-1" if year == min(self.YEARS) else ""}'),
                'tek3': self.builder.get_object(f'{day}Tek3_year{"-1" if year == min(self.YEARS) else ""}'),
            } for year in self.YEARS} for day in DAYS
        }

        self.specific_session = { year: {
            'wac1': self.builder.get_object(f'SessionWac1_year{"-1" if year == min(self.YEARS) else ""}'),
            'wac2': self.builder.get_object(f'SessionWac2_year{"-1" if year == min(self.YEARS) else ""}'),
            'msc1': self.builder.get_object(f'SessionMsc1_year{"-1" if year == min(self.YEARS) else ""}'),
            'msc2': self.builder.get_object(f'SessionMsc2_year{"-1" if year == min(self.YEARS) else ""}'),
            'premsc': self.builder.get_object(f'SessionPreMsc_year{"-1" if year == min(self.YEARS) else ""}'),
            'tek1': self.builder.get_object(f'SessionTek1_year{"-1" if year == min(self.YEARS) else ""}'),
            'tek2': self.builder.get_object(f'SessionTek2_year{"-1" if year == min(self.YEARS) else ""}'),    
        } for year in self.YEARS }

        self.specific_session_active = self.builder.get_object('SessionActive')

        self.specific_session_event = self.builder.get_object('SessionID')

        self.active_days = {
            day: self.builder.get_object(f'{day}Active') for day in DAYS
        }

        for i in range(0, 11):
            year = self.builder.get_object(f'year{i}')
            if i % 2 == 0:
                year.set_text(min(self.YEARS))
            else:
                year.set_text(max(self.YEARS))

        self.selected_date = datetime.date.today()
        self.set_dates(self.selected_date)

        self.hours = self.builder.get_object('hours_selector')
        self.new_hour_label = self.builder.get_object('InputHour')
        self.activity_input = self.builder.get_object('ActivityInput')
        
        self.activity_url = ""
        self.planning_hours = []

    def set_activity_url(self, url):
        """Setter for Activity url

        :param url: Activity Url (format must match check_activity_format)
        :type url: str
        """
        self.activity_url = url

    def get_activity_url(self):
        """Getter for Activity url

        :returns: The saved activity url
        :rtype: str
        """
        return self.activity_url

    def set_planning_hours(self, hours):
        """Setter for planning hours

        :param hours: hours to add to planning (format '%HH-%MM-%SS')
        :type hours: list[str]
        """
        self.planning_hours = hours

    def get_planning_hours(self):
        """Getter for planning hours

        :returns: The planned hours
        :rtype: list[str]
        """
        return self.planning_hours

    def set_dates(self, current_day):
        """Set current week by giving a day, the week will start at the closest monday  

        :param current_day: current day
        :type current_day: <class 'datetime.date'>
        """
        while current_day.weekday() != 0:
            current_day = current_day + datetime.timedelta(days=1)
        next_monday = current_day
        self.selected_date = next_monday
        self.dates = {
            'Lundi':next_monday.strftime("%Y-%m-%d"),
            'Mardi':(next_monday + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            'Mercredi':(next_monday + datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
            'Jeudi':(next_monday + datetime.timedelta(days=3)).strftime("%Y-%m-%d"),
            'Vendredi':(next_monday + datetime.timedelta(days=4)).strftime("%Y-%m-%d"),
        }

        self.builder.get_object("LundiDate").set_label(self.dates['Lundi'])
        self.builder.get_object("MardiDate").set_label(self.dates['Mardi'])
        self.builder.get_object("MercrediDate").set_label(self.dates['Mercredi'])
        self.builder.get_object("JeudiDate").set_label(self.dates['Jeudi'])
        self.builder.get_object("VendrediDate").set_label(self.dates['Vendredi'])

    def error_dialog_window(self, error_msg, secondary=None):
        """Display a dialog with a custom message and optional secondary message

        :param error_msg: Message to display as title
        :type error_msg: str
        :param secondary: Message to display as description
        :type secondary: str
        """
        md = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=error_msg
        )
        if secondary:
            md.format_secondary_text(
                secondary
            )
        md.run()
        md.destroy()

    def update_progress(self, i):
        """Update progress bar

        :param i: progression (between 1 and 5)
        :type i: int
        """
        self.progress.pulse()
        self.progress.set_fraction(0.2 * i)
        return False

    def reset_progress(self):
        """Reset progress bar
        """
        self.progress.set_fraction(0)

    def planify_and_register(self):
        """Call model method to planify and register students to the planified sessions
        """
        ...
        self.planify()
        self.register()
        GLib.idle_add(self.reset_progress)

    def planify(self):
        """Planify all active sessions in the notebook
        """
        GLib.idle_add(self.error_dialog_window, 'Starting planification')
        count = 1
        for day in DAYS:
            GLib.idle_add(self.update_progress, count)
            count += 1
            if self.active_days[day].get_active() == True:
                self.planned[day] = self.intra.planify_sessions(self.get_activity_url(), [self.dates[day]], self.get_planning_hours())
        self.reset_progress()
        GLib.idle_add(self.reset_progress)
        GLib.idle_add(self.error_dialog_window, 'Planification finished, you can now register students')

    def register(self):
        """Register all promotions to the planified events
        """
        GLib.idle_add(self.error_dialog_window, 'Starting registration')
        count = 1
        # TODO: Look for generic function
        if self.specific_session_active.get_active():
            clean = self.specific_session_event.get_text().replace(' ', '')
            specific_sessions = clean.split(',')
            for session in specific_sessions:
                for y in self.YEARS:
                    for promo in self.specific_session[y].items():
                        if promo[1].get_active():
                            self.intra.students_registration(self.get_activity_url() + session, promo[0], y)

        selected = {day: [] for day in DAYS}
        for day in DAYS:
            GLib.idle_add(self.update_progress, count)
            count += 1
            for y in self.YEARS:
                for promo in self.enabled_promotions[day][y].items():
                    if promo[1].get_active():
                        selected[day].append((y, promo[0]))
            if self.planned.get(day) != None:
                for session in self.planned[day]:
                    for sel in selected[day]:
                        self.intra.students_registration(self.get_activity_url() + session, sel[1], sel[0])

        self.planned = {}
        GLib.idle_add(self.reset_progress)
        GLib.idle_add(self.error_dialog_window, 'Registration finished')

def start():
    App = Application()
    Gtk.main()    

if __name__ == "__main__":
    start()