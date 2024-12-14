# coding: utf-8

from threading import Thread
from ksupk import get_time_str
import time
import os

from lockdown_protocol_extra_bot.parsing import get_args
from lockdown_protocol_extra_bot.settings_handler import SettingsHandler
from lockdown_protocol_extra_bot.telegram_bot import start_telegram_bot


def main():
    args = get_args()
    if args.command == 'start':
        sh = SettingsHandler(args.file_path)

        t = Thread(target=start_telegram_bot)
        t.start()
    else:
        print("Failed successfully (main). ")


if __name__ == "__main__":
    main()
