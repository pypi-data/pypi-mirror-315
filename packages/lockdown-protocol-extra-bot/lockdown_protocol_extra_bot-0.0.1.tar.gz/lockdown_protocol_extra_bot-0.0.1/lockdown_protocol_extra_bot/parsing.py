# coding: utf-8

import argparse
import os


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="lockdown_protocol_extra_bot. "
                                                 "Telegram bot for Lockdown Protocol extra challenges.")

    subparsers = parser.add_subparsers(dest='command', required=True)

    # start
    do_logic_parser = subparsers.add_parser('start', help='Perform logic')
    do_logic_parser.add_argument('file_path', type=str, help='Path to the config file. It is json format.')

    return parser.parse_args()

