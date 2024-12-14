# coding: utf-8

from ksupk import singleton_decorator, restore_json, save_json
import importlib.resources
import os


@singleton_decorator
class SettingsHandler:

    def __init__(self, json_path: str):
        self.__json_setting_path = json_path
        if not os.path.isfile(json_path) and not os.path.isdir(json_path):
            self.create_new()
        self.__d = restore_json(json_path)

    def d(self) -> dict:
        return self.__d.copy()

    def tele_token(self) -> str:
        return self.__d["telegram-config"]["token"]

    def tele_password(self) -> str:
        return self.__d["telegram-config"]["password"]

    def create_new(self):
        print("There are not config file. Attempt to create new...")
        d = {"telegram-config": {"token": "YOUR_TOKEN_HERE", "password": "YOUR_PASSWORD_HERE"}}
        save_json(self.__json_setting_path, d)
        print("Created, fill it, and run again. Exiting...")
        exit()


@singleton_decorator
class ResourceManager:

    def __init__(self):
        self.package_name = "lockdown_protocol_extra_bot"
        self.package_assets_folder = "assets"

    def file_path(self, file_path) -> str or None:
        res = None
        with importlib.resources.path(f"{self.package_name}.{self.package_assets_folder}", file_path) as tmp_file_path:
            res = str(tmp_file_path)
        return res

    def challenges_path(self) -> str:
        return self.file_path("challenges.json")
