import unittest
from model import EventPlanner
from mock_intranet import MockIntranet
from mock_data import events, students

class TestModelIntranet(unittest.TestCase):
    def test_event_planner_registration_good(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', ['wac1', 'wac2', 'msc1', 'msc2', 'premsc'])
        self.assertEqual(te, students)

    def test_event_planner_registration_error(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', None)
        self.assertEqual(te, None)

    def test_event_planner_registration_error2(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.students_registration(f'/module/2021/W-ADM-007/LYN-0-1/acti-505014/', [])
        self.assertEqual(te, None)

    def test_event_planify_session_good(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions(['2022-04-04'], ['10:10:10'])
        self.assertEqual(te, events)

    def test_event_planify_session_error_date(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions([], ['10:10:10'])
        self.assertEqual(te, None)

    def test_event_planify_session_error_hour(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions(['2022-04-04'], [])
        self.assertEqual(te, None)

    def test_event_planify_session_errors(self):
        intra = MockIntranet("")
        e = EventPlanner(intra)
        te = e.planify_sessions(None, None)
        self.assertEqual(te, None)


if __name__ == '__main__':
    unittest.main()