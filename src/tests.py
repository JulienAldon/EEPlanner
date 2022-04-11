import unittest
from model import EventPlanner
from mock_intranet import MockIntranet
from mock_data import events, students
from checkers import check_autologin, check_hour_format, exec_regex

class TestCheckersFunctions(unittest.TestCase):
    def test_exec_regex_error(self):
        self.assertFalse(exec_regex(r'azeasqd', 'https://localhost:8000'))

    def test_exec_regex_good(self):
        self.assertEqual(exec_regex(r'https', 'https://localhost:8000'), True)

    def test_check_autologin_good_short(self):
        self.assertEqual(check_autologin('auth-abcdef123456789abcdef'), 'https://intra.epitech.eu/auth-abcdef123456789abcdef')

    def test_check_autologin_good_medium(self):
        self.assertEqual(check_autologin('http://intra.epitech.eu/auth-abcdef123456789abcdef'), 'https://intra.epitech.eu/auth-abcdef123456789abcdef')

    def test_check_autologin_good_long(self):
        self.assertEqual(check_autologin('intra.epitech.eu/auth-abcdef123456789abcdef'), 'https://intra.epitech.eu/auth-abcdef123456789abcdef')

    def test_check_autologin_error_hexa(self):
        self.assertFalse(check_autologin('auth-abcdefg123456789abcdef'))

    def test_check_autologin_error_format(self):
        self.assertFalse(check_autologin('-abcdef123456789abcdef'))

    def test_check_hour_format_good(self):
        self.assertEqual(check_hour_format('10:00:00'), True)

    def test_check_hour_format_error_seconds(self):
        self.assertFalse(check_hour_format('10:00:70'))
    
    def test_check_hour_format_error_minutes(self):
        self.assertFalse(check_hour_format('10:70:10'))

    def test_check_hour_format_error_hour(self):
        self.assertFalse(check_hour_format('70:00:00'))

    def test_check_hour_format_error_format(self):
        self.assertFalse(check_hour_format('abcd'))
        self.assertFalse(check_hour_format('10'))
        self.assertFalse(check_hour_format('10:20'))
        self.assertFalse(check_hour_format(':20:20'))
        self.assertFalse(check_hour_format(':::'))
        self.assertFalse(check_hour_format('"1"2"3"2"3"'))

class TestModelIntranet(unittest.TestCase):
    def test_registration_good(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', ['wac1', 'wac2', 'msc1', 'msc2', 'premsc'])
        self.assertEqual(te, students)

    def test_registration_error_promotion_none(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', None)
        self.assertEqual(te, None)

    def test_registration_error_promotion_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', [])
        self.assertEqual(te, None)

    def test_registration_error_event_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration('', ['wac1', 'wac2'])
        self.assertEqual(te, None)
    
    def test_registration_error_event_none(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(None, ['wac1', 'wac2'])
        self.assertEqual(te, None)

    def test_planify_session_good(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions(['2022-04-04'], ['10:10:10'])
        self.assertEqual(te, events)

    def test_planify_session_error_date_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions([], ['10:10:10'])
        self.assertEqual(te, None)

    def test_planify_session_error_hour_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions(['2022-04-04'], [])
        self.assertEqual(te, None)

    def test_planify_session_errors_none(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions(None, None)
        self.assertEqual(te, None)

    def test_planify_session_errors_empty(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions([], [])
        self.assertEqual(te, None)


if __name__ == '__main__':
    unittest.main()