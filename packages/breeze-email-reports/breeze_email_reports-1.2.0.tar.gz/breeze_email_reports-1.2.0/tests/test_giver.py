import json
import os
import unittest
import tempfile
from datetime import date
from typing import Tuple, List, Union
from breeze_email_reports._common import check_date
import sys
from breeze_email_reports.EmailGiverReport import main, _get_date_range

"""
Some notes on the test data...
Profiles from CurrentDataBreeze.json:
    13701083: Firstname1 Alast
    13711803: Firstname2 Blast
    19870634: NewFirst Bonzo
    13857066: Firstname3 Blast

Funds in funds.json:
    1816906: Budget (was 2024 budget)
    1816907: Budget (Non Exempt) (Was 2024...)
    1901063: Memorial (Was Anne Cook Memorial)
    1520829: Rents
"""

# TODO: Verify Breeze API calls. In particular requested funds and dates
# TODO: Test logged output (stdout and stdin?)

TEST_FILES_DIR = os.path.join(os.path.split(__file__)[0], 'test_files')


# Returned by Breeze for "current" profile data
CURRENT_DATA_BREEZE = os.path.join(TEST_FILES_DIR, 'CurrentDataBreeze.json')
FUNDS = os.path.join(TEST_FILES_DIR, 'GivingFunds.json')
GIFTS = os.path.join(TEST_FILES_DIR, 'Gifts.json')
EXTRA_GIFTS = os.path.join(TEST_FILES_DIR, 'GiftsExtra.json')
EXTRA_PROFILES = os.path.join(TEST_FILES_DIR, 'ExtraProfiles.json')

# Expected results in email
EXPECTED_HTML = os.path.join(TEST_FILES_DIR, 'GiversExpectedHTML.html')
EXPECTED_HTML_MORE = os.path.join(TEST_FILES_DIR, 'GiversExpectedHTML.more.html')
EXPECTED_SUMMARY = os.path.join(TEST_FILES_DIR, 'GiversExpectedSummary.html')

TO_ADDRESS = 'to@test.com'
BCC_ADDRESS = 'bcc1@bcc.com, bcc2@bcc.com'
CC_ADDRESS = 'cc@cc.com'


class MockBreezeAPI:
    def __init__(self, fields: str,
                 profiles: str,
                 funds: List[str] = [], contributions: List[str] = []):
        self.fields = fields
        self.profiles = profiles
        self.funds = funds
        self.contributions = contributions
        self.funds_requested = None
        self.start_requested = None
        self.end_requested = None
        self.profile_map = None
        self.list_people_requests = []
        self.person_detail_requests = []

    def list_people(self, **kwargs):
        self.list_people_requests.append(kwargs)
        return self.profiles

    def get_profile_fields(self):
        return self.fields

    def get_person_details(self, person_id):
        if not self.profile_map:
            self.profile_map = {p.get("id"): p for p in self.profiles}
        self.person_detail_requests.append(person_id)
        return self.profile_map.get(person_id)

    def list_funds(self):
        ret = []
        for fundfile in self.funds:
            with open(fundfile, 'r') as f:
                ret += json.loads(f.read())
        return ret

    def list_contributions(self,
                           fund_ids: List[str] = [],
                           start: str = None,
                           end: str = None):
        self.funds_requested = fund_ids
        self.start_requested = start
        self.end_requested = end
        ret = []
        for contributions in self.contributions:
            with open(contributions, 'r') as f:
                ret += json.loads(f.read())
        return ret


class MockSender:
    def __init__(self):
        self.result = None

    def send_message(self, msg):
        self.result = msg


class TestGiverSender(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.mock_sender = MockSender()
        self.saved_argv = sys.argv
        self.saved_stdout = None
        self.mock_api = None

    def make_api(self, fields=[], profiles=[], funds=[FUNDS], contributions=[]):
        self.mock_api = MockBreezeAPI(fields, profiles, funds=funds,
                                      contributions=contributions)

    def runTest(self,
                # report_format: str = 'text',
                contributions: List[str] = [GIFTS],
                extra_profiles: List[str] = [],
                start_date: str = '2024-10-01',
                end_date: str = '2024-10-31',
                extra_params: List[str] = []) -> Tuple[str, int]:
        """
        Run BreezeProfile report. Return emitted event.
        :param contributions: file with contributions to return
        :param extra_profiles: More profiles to load
        :param start_date: first date
        :param end_date: end date
        :param extra_params:
        :return:
        :raises: ParamException, IOException
        """

        with open(CURRENT_DATA_BREEZE, 'r') as f:
            fields, profiles = json.loads(f.read())

        for extra in extra_profiles:
            with open(extra, 'r') as f:
                profiles += (json.loads(f.read()))

        self.make_api(fields=fields, profiles=profiles, funds=[FUNDS],
                      contributions=contributions)

        sys.argv = ['test', '-f', 'from@test.com', '--to', TO_ADDRESS,
                    '--bcc', BCC_ADDRESS,
                    '--cc', CC_ADDRESS,
                    # '--data', self.test_dir.name,
                    '--log_level=critical',
                    f'--logfile={os.path.join(self.test_dir.name, "test.log")}']
        # Including format TBD
        if start_date:
            sys.argv += ['--start', start_date]
        if end_date:
            sys.argv += ['--end', end_date]

        sys.argv += extra_params

        ret = main(breeze_api=self.mock_api, email_sender=self.mock_sender)
        self.assertEqual(None, ret)

    def test_basic(self):
        self.runTest(extra_params=['--totals', 'Budget'])
        sent_message = self.mock_sender.result
        # self.assertEqual('Breeze profile change report',
        #                      str(sent_message.get('Subject')))
        self.assertEqual(TO_ADDRESS, sent_message.get('to'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('bcc'))
        self.assertEqual(CC_ADDRESS, sent_message.get('cc'))

        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        # pl1 = payloads[1]
        # self.assertEqual(pl0.get_content_subtype(), 'plain')
        # Contributions to fund(s)
        # Budget
        # from 2024-10-01 to 2024-10-31
        # self.assertTrue(str(pl0.get_payload()).
        #                 startswith('Breeze changes for Unknown thru'))
        self.assertEqual(pl0.get_content_subtype(), 'html')
        got = str(pl0.get_payload())
        # with open(EXPECTED_HTML, 'w') as f:
        #     f.write(got)
        with open(EXPECTED_HTML, 'r') as f:
            self.assertEqual(got, f.read())

    def test_summary(self):
        self.runTest(extra_params=['--summary', 'Budget'])
        sent_message = self.mock_sender.result
        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        got = str(pl0.get_payload())
        # with open(EXPECTED_SUMMARY, 'w') as f:
        #     f.write(got)
        with open(EXPECTED_SUMMARY, 'r') as f:
            self.assertEqual(got, f.read())

    def test_more(self):
        self.runTest(extra_params=['Budget'],
                     contributions=[GIFTS, EXTRA_GIFTS],
                     extra_profiles=[EXTRA_PROFILES])
        sent_message = self.mock_sender.result
        # self.assertEqual('Breeze profile change report',
        #                      str(sent_message.get('Subject')))
        self.assertEqual(TO_ADDRESS, sent_message.get('to'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('bcc'))
        self.assertEqual(CC_ADDRESS, sent_message.get('cc'))

        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        # self.assertEqual(pl0.get_content_subtype(), 'plain')
        self.assertEqual(pl0.get_content_subtype(), 'html')
        got = str(pl0.get_payload())
        # with open(EXPECTED_HTML_MORE, 'w') as f:
        #     f.write(got)
        with open(EXPECTED_HTML_MORE, 'r') as f:
            self.assertEqual(f.read(), got)
        # Contributions to fund(s) (pl0.get_payload())
        # Budget
        # from 2024-10-01 to 2024-10-31
        # self.assertTrue(str(pl0.get_payload()).
        #                 startswith('Breeze changes for Unknown thru'))

    def test_no_data(self):
        self.runTest(extra_params=['Budget'],
                     contributions=[])
        sent_message = self.mock_sender.result
        payloads = sent_message.get_payload()
        self.assertEqual("No contributions found", payloads[0].get_payload())

    def test_no_funds(self):
        sys.argv = ['test', '--bcc', 'foo@bar', '-f', 'foo']
        self.make_api()
        with self.assertRaises(SystemExit) as se:
            main(breeze_api=self.mock_api, email_sender=self.mock_sender)
        self.assertEqual('One or more funds is required', se.exception.code)

    def test_bad_fund(self):
        self.make_api()
        badfund = 'nofund'
        sys.argv = ['test', '--bcc', 'foo@bar', '--from', 'test@foo.com', badfund]
        with self.assertRaises(SystemExit) as se:
            main(breeze_api=self.mock_api, email_sender=self.mock_sender)
        self.assertEqual(f'Fund "{badfund}" not found', se.exception.code)

    def test_no_sender(self):
        self.make_api()
        sys.argv = ['test', '--bcc', 'foo@bar', 'afund']
        with self.assertRaises(SystemExit) as se:
            main(breeze_api=self.mock_api, email_sender=self.mock_sender)
        self.assertEqual('--from is required', se.exception.code)

    def test_no_receiver(self):
        self.make_api()
        sys.argv = ['test', '--from', 'too@bar', 'afund']
        with self.assertRaises(SystemExit) as se:
            main(breeze_api=self.mock_api, email_sender=self.mock_sender)
        self.assertEqual('At least one of --to, --cc or --bcc is required',
                         se.exception.code)

    def test_no_contributions(self):
        self.make_api()
        start_date = '2024-10-01'
        end_date = '2024-11-15'
        self.runTest(extra_params=[
                                   '--start', start_date,
                                   '--end', end_date,
                                   'Budget'],
                     contributions=[],
                     extra_profiles=[EXTRA_PROFILES])
        # Note: The start and end dates don't actually impact the returned
        # data in the test. "We assume Breeze filters correctly given the
        # supplied parameters. We do make sure that the tool sends the
        # appropriate query.
        sent_message = self.mock_sender.result

        self.assertEqual(TO_ADDRESS, sent_message.get('to'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('bcc'))
        self.assertEqual(CC_ADDRESS, sent_message.get('cc'))

        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        self.assertEqual(pl0.get_content_subtype(), 'plain')
        self.assertEqual(pl0.get_payload(), 'No contributions found')

    def test_list_dir(self):
        sys.argv = ['test', '--list_directories']
        with self.assertRaises(SystemExit) as se:
            main(breeze_api=self.mock_api, email_sender=self.mock_sender)
        self.assertEqual(se.exception.code, 0)

    def date_range(self,
                   begin: Union[None, str],
                   end: Union[None, str],
                   expect_start: str,
                   expect_end: str,
                   today: str = '2024-11-09'):
        """
        Use case for testing date ranges, All dates are in form YYYY-MM-DD
        :param begin: Testing begin date
        :param end: Testing end date
        :param expect_start: Expected output start
        :param expect_end: Expected output end
        :param today: Use as "today" for testing purposes
        :return: None
        """
        result_start, result_end = _get_date_range(begin, end,
                                                   today=date.fromisoformat(today))
        self.assertEqual(expect_start, result_start)
        self.assertEqual(expect_end, result_end)

    def test_date_range(self):
        # Bad date causes exit.
        bad = '2024-02-30'
        with self.assertRaises(SystemExit) as e:
            check_date(bad)
        self.assertEqual(f'"{bad}" is not a valid date. Needs to be YYYY-MM-DD',
                         e.exception.code)

        # If no dates, return previous month. (Leap year.)
        self.date_range(None,
                        None,
                        '2024-02-01',
                        '2024-02-29',
                        '2024-03-15')

        # If no dates, return previous month. (Previous year.)
        self.date_range(None,
                        None,
                        '2023-12-01',
                        '2023-12-31',
                        '2024-01-15')

        # Only begin date, return begin date until today
        self.date_range('2023-12-01',
                        None,
                        '2023-12-01',
                        '2024-01-15',
                        '2024-01-15')

        # Only end date, return start of year until end date
        self.date_range(None,
                        '2023-12-05',
                        '2023-01-01',
                        '2023-12-05',
                        '2024-01-15')

        # Explicit beginning and end return same
        self.date_range('2023-09-23',
                        '2023-12-05',
                        '2023-09-23',
                        '2023-12-05',
                        '2024-01-15')

        # Explicit dates inconsistent exits with error
        with self.assertRaises(SystemExit) as e:
            self.date_range('2023-12-23',
                            '2023-01-05',
                            '2023-09-23',
                            '2023-12-05',
                            '2024-01-15')
        self.assertEqual("Start date can't be after end date", e.exception.code)

        # Start date in future
        with self.assertRaises(SystemExit) as e:
            self.date_range('2025-01-01',
                            None,
                            '',
                            '',
                            '2024-01-01')
        self.assertEqual("Start date can't be in the future", e.exception.code)

    def tearDown(self):
        if self.saved_stdout:
            sys.stdout = self.saved_stdout
        self.test_dir.cleanup()
        sys.argv = self.saved_argv
