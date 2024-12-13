from io import StringIO
from typing import List, Tuple, Dict, Union

from configured_mail_sender import create_sender, MailSender
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from breeze_chms_api import breeze
from breeze_chms_api.profile_helper import ProfileHelper
from datetime import date, timedelta
from breeze_email_reports.table_format import ColSpec, _HTMLFormatter

import sys
import argparse
import os
import platformdirs
from breeze_email_reports._common import parse_arguments, check_date

APPLICATION_NAME = 'email_giver_report'
DEFAULT_LOG_FILE = os.path.join(platformdirs.user_log_dir(), APPLICATION_NAME + '.log')


def _field_name_to_id(helper: ProfileHelper) -> Dict[str, str]:
    """
    The Breeze profile data structure is way complex. Fields are generally identified
    by an id, but usually we just want a field by name.
    :param field_spec: Field specification from Breeze
    :param helper: Profile helper
    :return:
    """
    id_to_name = helper.get_field_id_to_name()
    return {v.split(':')[1] if ':' in v else v: k for (k,v) in id_to_name.items()}


def _get_date_range(begin: Union[str, None],
                    end: Union[str, None],
                    today: date = date.today()) -> Tuple[str, str]:
    """
    Generate date range from input parameters
    :param begin: Start date from command invocation
    :param end: End date from command invocation
    :param today: For testing purposes only, use as current day.
    :return: Interpreted beginning and ending dates
    All input and output dates are in the form YYYY-MM-DD.

    The logic is like this:
    if both dates given:
        Return dates as given
    else if end date (and only end date) given:
        return (beginning of hear from end date, end date)
    else if start date given:
        return (start date, end of start date month)
    else (neither was given)
        return first and last days of PREVIOUS month.
    """
    start_date = check_date(begin)
    end_date = check_date(end)

    # If neither start nor end given, use previous month
    if end_date:
        if not start_date:
            start_date = date(year=end_date.year, month=1, day=1)
        elif start_date > end_date:
            # Both given, but make sure it makes sense
            sys.exit("Start date can't be after end date")
        return start_date.isoformat(), end_date.isoformat()

    if start_date:
        # Start date given but no end
        if start_date > today:
            sys.exit("Start date can't be in the future")
        return start_date.isoformat(), today.isoformat()

    # If no dates given use beginning and end of the previous month.
    yr = today.year
    mo = today.month

    if mo == 1:
        start_date = date(yr - 1, 12, 1)
        end_date = date(yr - 1, 12, 31)
    else:
        start_date = date(yr, mo - 1, 1)
        end_date = (date(yr, mo, 1) - timedelta(days=1))
    return start_date.isoformat(), end_date.isoformat()


def get_contributions(breeze_api: breeze,
                      start_date: str,
                      end_date: str,
                      funds: List[str]) -> Tuple[Dict[str,
                                                      List[Tuple[str, float, str]]],
                                                 bool]:
    """
    Generate a contribution report:
    :param breeze_api: Breeze API to get contribution information
    :param start_date: Start of contribution range (YYY-MM-DD)
    :param end_date: End of contribution range
    :param funds: List of funds to include in report
    :return: (Dict profile's contributions, boolean True if there was any note.)
            Key in the dict is the profile id.
            Value for each profile is a list of contributions, each with:
                Date of contribution:
                Amount of contribution.
                The note.
    """

    all_funds = breeze_api.list_funds()
    name_to_id = {f['name']: f['id'] for f in all_funds}
    id_set = []
    for fn in funds:
        fid = name_to_id.get(fn)
        if not fid:
            sys.exit(f'Fund "{fn}" not found')
        id_set.append(fid)

    contributions = breeze_api.list_contributions(fund_ids=id_set,
                                                  start=start_date,
                                                  end=end_date)

    person_gifts = {}
    had_notes = False
    for contrib in contributions:
        amt = 0.0
        # Sum all contributions to requested funds within this contribution
        for fund in contrib['funds']:
            amt += float(fund['amount'])
        if amt > 0:     # Just checking, not sure how it could be otherwise
            paid_on = contrib['paid_on'][0:10]  # Just YYYY-MM-DD part
            pid = contrib.get('person_id')
            prv = person_gifts.get(pid, [])
            note = contrib.get('note')
            prv.append([paid_on, amt, note])
            if note:
                had_notes = True
            # Note: None is fine as a key. It will be interpreted as anonymous later.
            # person_gifts[pid] = prv
            person_gifts[pid] = prv

    ret_gifts = {pid: sorted(gifts, key=lambda x: x[0])
                 for pid, gifts in person_gifts.items()}

    return ret_gifts, had_notes


def main(breeze_api: breeze.BreezeApi = None,
         email_sender: MailSender = None):
    """
    Email a report of Breeze giving
    :param breeze_api: (For testing) pre-made Breeze API
    :param email_sender: (For testing) email sender
    :return: None
    """
    parser = argparse.ArgumentParser(APPLICATION_NAME)
    parser.add_argument('--from',
                        '-f',
                        dest='sender',
                        metavar='sender',
                        help='sending email address (required in most cases)')
    parser.add_argument('-s',
                        '--start',
                        metavar='StartDate',
                        help='Starting date as YYYY-MM-DD')
    parser.add_argument('-e',
                        '--end',
                        metavar='EndDate',
                        help='Ending date as YYYY-MM-D.')
    parser.add_argument('-t',
                        '--to',
                        metavar='Recipient(s)',
                        help='Public recipients')
    parser.add_argument('--cc',
                        metavar='CopyRecipients',
                        help='Copy recipients')
    parser.add_argument('--bcc',
                        metavar='BlindRecipients',
                        help='Blind recipients')
    parser.add_argument('--totals',
                        default=False,
                        action='store_const',
                        const=True,
                        help='Include total for each giver')
    parser.add_argument('--summary',
                        default=False,
                        action='store_const',
                        const=True,
                        help='Show only total'
                        )
    parser.add_argument('--breeze_creds',
                        metavar='<Breeze credential file>',
                        help='file with Breeze credentials if not standard',
                        default=None)
    parser.add_argument('--email_creds',
                        metavar='<email credential file>',
                        help='file with email passwords if not standard')
    parser.add_argument('--email_servers',
                        metavar='<email domain specification file>',
                        help='file with email domain configuration if not standard')

    args = parse_arguments(parser, APPLICATION_NAME,
                           [(['funds'],
                             {'nargs': '*',
                              'metavar': 'Fund(s)',
                              'help': 'Fund(s) to include'})])

    if not args.sender:
        sys.exit('--from is required')
    if not (args.to or args.cc or args.bcc):
        sys.exit('At least one of --to, --cc or --bcc is required')

    if args.summary:
        args.total = False

    if not args.funds:
        sys.exit('One or more funds is required')

    start_date, end_date = _get_date_range(args.start, args.end)

    if not breeze_api:
        # Normal case not testing
        breeze_api = breeze.breeze_api(overrides=args.breeze_creds)

    contributions, have_notes = get_contributions(breeze_api,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  funds=args.funds)

    profile_fields = breeze_api.get_profile_fields()
    profile_helper = ProfileHelper(profile_fields)
    field_name_to_id = _field_name_to_id(profile_helper)
    name_id = field_name_to_id.get("Name")
    address_id = field_name_to_id.get("Address")
    phone_id = field_name_to_id.get("Phone")
    email_id = field_name_to_id.get("Email")
    id_fields = [name_id, address_id, phone_id, email_id]

    needed_profile_ids = [id for id in contributions.keys() if id]
    # Note: I'd use json_filter here to just get the interesting ids, but
    # there's no documentation on how to do that. And doing separate calls
    # for each profile would risk getting throttled. So we'll just
    # get everything and pick the ones we want.
    # Instead, if there are only a few profiles, pull them individually.
    # Otherwise, just get the whole lot in one request to avoid throttling.
    if len(needed_profile_ids) > 10:
        # too many people so get all at once
        profiles = breeze_api.list_people(details=True)
        profiles = [p for p in profiles if p['id'] in needed_profile_ids]
    else:
        # Just get the few we need
        profiles = [breeze_api.get_person_details(id) for id in needed_profile_ids]

    processed = {p['id']: profile_helper.process_member_profile(p)
                 for p in profiles if p['id'] in needed_profile_ids}

    toformat = []
    grand_total = 0.0
    for id, p in contributions.items():
        if id:
            details = processed.get(id)
            id_data = []
            for fld in id_fields:
                dat = details.get(fld)
                if dat:
                    if isinstance(dat, List):
                        dat = '\n'.join(dat)
                    dat = dat.replace(';', '\n')
                    id_data.append(dat)
        else:
            id_data = ['Anonymous']
        # Fix numeric values and get total.
        total = 0.0
        for row in p:
            amt = row[1]
            total += amt
            row[1] = f'{amt:,.2f}'
        col1 = '\n'.join(id_data)
        grand_total += total
        if args.summary:
            toformat.append([col1, [[f'{total:,.2f}']]])
        else:
            if len(p) > 1 and args.totals:
                p.append(['Total', f'{total:,.2f}', ''])
            toformat.append([col1, [list(v) for v in p]])

    # So toformat now is a list of all givers. Each item in the list
    # is a list (why not a Tuple?) where the first entry is the info
    # about the giver (name, address...) as newline-separated string,
    # and following is a list with all the contribution items, the
    # interesting bits being date, amount, notes.

    # sort by giver name (last, first)
    toformat = sorted(toformat, key=lambda x: x[0])
    if grand_total > 0:
        if args.summary:
            toformat.append(['Grand Total', [[f'{grand_total:,.2f}']]])
        else:
            toformat.append(['Grand Total', [['All', f'{grand_total:,.2f}', '']]])

    # Now, let's set up columns.
    # Columns will be:
    #   Donor
    #   Date (unless only totals selected)
    #   Amount
    #   Notes (if there are notes)
    columns = [ColSpec('Donor', width=15, header_attrs={'text-align': 'start'})]
    # args.summary means we only want total for each giver, so no dates.
    if not args.summary:
        columns.append(ColSpec('Date', width=10,
                               header_attrs={'text-align': 'center'}))
    columns.append(ColSpec('Amount', width=7, header_attrs={'text-align': 'end'}))
    # Only create a Notes column if there actually are notes.
    if not args.summary and have_notes:
        columns.append(ColSpec('Note'))

    msg = MIMEMultipart()
    fnames = ', '.join(args.funds)
    subject = f'Contributions to fund(s)\n{fnames}\nfrom {start_date} to {end_date}'
    msg['Subject'] = subject.replace('\n', ' ')
    if args.to:
        msg['to'] = args.to
    if args.bcc:
        msg['bcc'] = args.bcc
    if args.cc:
        msg['cc'] = args.cc
    if toformat:
        # msg.attach(MIMEText(f'{subject}\n\n'))
        # As of now, only HTML format is supported. Maybe a future version.
        formatter = _HTMLFormatter(column_specs=columns, id_top=False, caption=subject)
        output = StringIO()
        formatter.format_table(toformat, output)
        output.seek(0)
        txt = output.read()
        # with open('test.html', 'w') as f:
        #     f.write(txt)
        msg.attach(MIMEText(txt, 'html'))
    else:
        msg.attach(MIMEText(f'No contributions found'))

    sender = email_sender if email_sender else \
        create_sender(args.sender,
                      creds_file=args.email_creds,
                      overrides=args.email_servers)
    sender.send_message(msg)


if __name__ == "__main__":
    main()
