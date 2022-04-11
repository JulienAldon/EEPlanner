import gi
import threading
import datetime
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from model import EventPlanner
from intranet import Intra
from checkers import check_autologin, check_hour_format
import re
from constants import ACTIVITY_URL

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

    def onSendForm(self, button):
        if not self.application.planning_hours or len(self.application.planning_hours) <= 0:
            self.application.hours.forall(self.onAddWidget)
        if not self.application.intra_autologin.get_text():
            self.application.errorDialogWindow(
                "Error : no Epitech intranet autologin token provided.",
                "Find it under the administration tab on the Epitech intranet !"
            )
            return
        token = check_autologin(self.application.intra_autologin.get_text())
        if not token:
            self.application.errorDialogWindow(
                "Error : invalid Epitech intranet autologin token format.",
                FORMAT_ERROR_MESSAGE
            )
            return
        self.application.thrower.set_token(token)
        if self.application.progress.get_fraction() == 0.0:
            thread = threading.Thread(target=self.application.planifyAndRegister)
            thread.daemon = True
            thread.start()
        else:
            self.application.errorDialogWindow("Error : cannot start job, another one is already running.")
            return

    def onAddWidget(self, widget):
        if widget.get_active():
            self.application.planning_hours.append(widget.get_label())

    def onAddHour(self, button):
        new_label = self.application.new_hour_label.get_text()
        if not check_hour_format(new_label):
            self.application.errorDialogWindow('Error : entry must be a correct hour format')
            return
        new_checkbox = Gtk.CheckButton(label=self.application.new_hour_label.get_text())
        self.application.setPlanningHours([])
        self.application.hours.add(new_checkbox)
        new_checkbox.show()

class Application:
    """
    Class Application for GTK window using Glade
    """
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Application.glade")
        self.builder.connect_signals(Handler(self))

        self.window = self.builder.get_object("Window")
        self.window.show_all()
        
        self.progress = self.builder.get_object('Bar')
        self.intra_autologin = self.builder.get_object('IntraInput')

        self.thrower = Intra()
        self.intra = EventPlanner(self.thrower)

        self.enabled_promotions = {
            day: {
                'wac1': self.builder.get_object(day+'Wac1'),
                'wac2': self.builder.get_object(day+'Wac2'),
                'msc1': self.builder.get_object(day+'Msc1'),
                'msc2': self.builder.get_object(day+'Msc2'),
                'premsc': self.builder.get_object(day+'PreMsc'),
            } for day in DAYS
        }
        Application.setDefaultSettings(DAYS, self.enabled_promotions)
        self.setDates(datetime.date.today()) # HACK: change nb days if not correct date

        self.hours = self.builder.get_object('hours_selector')
        self.new_hour_label = self.builder.get_object('InputHour')

        self.planning_hours = []

    @staticmethod
    def setDefaultSettings(days, day):
        """set default settings for checkbox inside the GUI

        :param days: Days of the Week
        :type days: list[str]
        :param day: Checkbuttons sorted by day
        :type day: list[<Gtk.CheckButton object>]
        """
        for a in days:
            day[a]['wac1'].set_active(True)
            if a == 'Lundi':
                day[a]['premsc'].set_active(True)
            if a == 'Mardi':
                day[a]['premsc'].set_active(True)
            if a == 'Jeudi':
                day[a]['msc1'].set_active(True)
                day[a]['msc2'].set_active(True)
            if a == 'Vendredi':
                day[a]['msc1'].set_active(True)
                day[a]['msc2'].set_active(True)

    def setPlanningHours(self, hours):
        """Setter for planning hours

        :param hours: hours to add to planning (format '%HH-%MM-%SS')
        :type hours: list[str]
        """
        self.planning_hours = hours

    def setDates(self, current_day):
        """Set current week by giving a day, the week will start at the closest monday  

        :param current_day: current day
        :type current_day: <class 'datetime.date'>
        """
        # next_monday = current_day + datetime.timedelta(days=-current_day.weekday(), weeks=1)
        while current_day.weekday() != 0:
            current_day = current_day + datetime.timedelta(days=1)
        next_monday = current_day
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

    def errorDialogWindow(self, error_msg, secondary=None):
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

    def updateProgress(self, i):
        """Update progress bar

        :param i: progression (between 1 and 5)
        :type i: int
        """
        self.progress.pulse()
        self.progress.set_fraction(0.2 * i)
        return False

    def resetProgress(self):
        """Reset progress bar
        """
        self.progress.set_fraction(0)

    def planifyAndRegister(self):
        """Call model method to planify and register students to the planified sessions
        """
        count = 1
        for a in DAYS:
            GLib.idle_add(self.updateProgress, count)
            count += 1
            selected = []
            for i in self.enabled_promotions[a].items():
                if i[1].get_active():
                    selected.append(i[0])
            planned = self.intra.planify_sessions([self.dates[a]], self.planning_hours)
            for t in planned:
                print("interface", t)
                self.intra.students_registration(ACTIVITY_URL + t, selected)
        self.resetProgress()
        GLib.idle_add(self.errorDialogWindow, 'Job finished ')

if __name__ == "__main__":
    App = Application()
    Gtk.main()