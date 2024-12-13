from pathlib import Path
from typing import List, Tuple, Dict, Union

from breeze_chms_api import breeze
from configured_mail_sender import known_domains
from datetime import date, timedelta

import logging
import configured_mail_sender
import argparse
import sys
import os
import platformdirs


def _list_domains(args):
    domains = known_domains(overrides=args.email_servers)
    print("Known email domains:")
    for domain, text in domains.items():
        print(f'   {domain}: {text}')


def parse_arguments(parser: argparse.ArgumentParser,
                    application_name: str,
                    to_add: List[Tuple[List[str], Dict[str, str]]]=[]) -> argparse.Namespace:
    """
    Fill in argument parser with special debug options
    :param parser: The parser
    :param application_name: Name of application
    :param to_add: List of argument specs for additional parameters
    :return: None
    """

    logfile = os.path.join(platformdirs.user_log_dir(), f'{application_name}.log')

    parser.add_argument('--list_directories',
                        default=False,
                        action='store_true',
                        help='list data and configuration directories and exit')
    parser.add_argument('--list_domains',
                        default=False,
                        action='store_true',
                        help='Print known email domains and exit')
    parser.add_argument('--logfile',
                        default=logfile,
                        metavar='Log file',
                        help='File for application logs')
    parser.add_argument('--log_level',
                        default='info',
                        metavar='Log level',
                        help='Logging level, default=info')

    for parm in to_add:
        parser.add_argument(*parm[0], **parm[1])

    args = parser.parse_args()

    if args.logfile == 'stdout':
        out = {'stream': sys.stdout}
    elif args.logfile == 'stderr':
        out = {'stream': sys.stderr}
    else:
        out = {'filename': args.logfile}
        directory, file = os.path.split(args.logfile)
        Path(directory).mkdir(exist_ok=True, parents=True)

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=getattr(logging, args.log_level.upper()),
        **out
    )
    logging.info(f'Running {" ".join(sys.argv)}')

    if args.list_domains:
        _list_domains(args)
        sys.exit(0)

    if args.list_directories:
        # Making it easy to note where users should look for files on this platform.
        mailsender_configs = configured_mail_sender.config_file_list()
        print('configured_mail_sender configuration files:')
        for f in mailsender_configs:
            print(f'\t{f}')
        breeze_config = breeze.config_file_list(overrides=args.breeze_creds)
        print('breeze_chms_api configuration files:')
        for f in breeze_config:
            print(f'\t{f}')
        if hasattr(args, 'data'):
            print(f'{application_name} data directory:\n\t{args.data}')
        print(f'log output\n\t{args.logfile}')
        sys.exit(0)

    return args


def check_date(dt: str) -> Union[str, None]:
    """
    Check for correctly formatted date and convert to date object
    Exit with error if date format is bad.
    :param dt:
    :return: Date as date object, or None if none.
    """
    try:
        return date.fromisoformat(dt) if dt else None
    except ValueError as e:
        # There was a problem with the date
        sys.exit(f'"{dt}" is not a valid date. Needs to be YYYY-MM-DD')
