import gi
import threading
import datetime
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from model import Intra
import re

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
        self.application.intra.set_planification_hours(self.application.planning_hours)
        if not self.application.intra_autologin.get_text():
            self.application.error_dialog_window(
                "Error : no Epitech intranet autologin token provided.",
                "Find it under the administration tab on the Epitech intranet !"
            )
            return
        token = Intra.check_autologin(self.application.intra_autologin.get_text())
        if not token:
            self.application.error_dialog_window(
                "Error : invalid Epitech intranet autologin token format.",
                FORMAT_ERROR_MESSAGE
            )
            return
        self.application.intra.set_token(token)
        if self.application.progress.get_fraction() == 0.0:
            thread = threading.Thread(target=self.application.planify)
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
        if not Intra.check_hour_format(new_label):
            self.application.error_dialog_window('Error : entry must be a correct hour format')
            return
        new_checkbox = Gtk.CheckButton(label=self.application.new_hour_label.get_text())
        self.application.set_planning_hours([])
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

        self.intra = Intra()

        self.enabled_promotions = {
            day: {
                'wac1': self.builder.get_object(day+'Wac1'),
                'wac2': self.builder.get_object(day+'Wac2'),
                'msc1': self.builder.get_object(day+'Msc1'),
                'msc2': self.builder.get_object(day+'Msc2'),
                'premsc': self.builder.get_object(day+'PreMsc'),
            } for day in DAYS
        }
        Application.set_default_settings(DAYS, self.enabled_promotions)
        self.set_dates(datetime.date.today() + datetime.timedelta(days=7))

        self.hours = self.builder.get_object('hours_selector')
        self.new_hour_label = self.builder.get_object('InputHour')

        self.planning_hours = []

    @staticmethod
    def set_default_settings(days, day):
        """set default settings for checkbox inside the GUI
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

    def set_planning_hours(self, hours):
        self.planning_hours = hours

    def set_dates(self, current_day):
        """Set current week by giving a day, the week will start at the closest monday  
        """
        next_monday = current_day + datetime.timedelta(days=-current_day.weekday(), weeks=1)
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
        return

    def update_progress(self, i):
        self.progress.pulse()
        self.progress.set_fraction(0.2 * i)
        return False

    def reset_progress(self):
        self.progress.set_fraction(0)

    def planify(self):
        count = 1
        for a in DAYS:
            GLib.idle_add(self.update_progress, count)
            count += 1
            selected = []
            for i in self.enabled_promotions[a].items():
                if i[1].get_active():
                    selected.append(i[0])
            planned = self.intra.planify_sessions([self.dates[a]])
            for t in planned:
                self.intra.register_students(selected, t)
        self.reset_progress()
        GLib.idle_add(self.error_dialog_window, 'Job finished ')

if __name__ == "__main__":
    App = Application()
    Gtk.main()