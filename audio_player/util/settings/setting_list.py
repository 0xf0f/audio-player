from .setting import Setting
from typing import Any, Dict


class SettingList:
    def __init__(self):
        self.settings: Dict[str, Setting] = {}

    def add_setting(self, name, default=None) -> Setting:
        setting = Setting(name, default)
        self.settings[name] = setting

        return setting

    # def add_settings(self, settings: Dict[str, Any]):
    #     for name, default in settings.items():
    #         setting = Setting()

    def __getitem__(self, item):
        return self.settings[item]

    def __iter__(self):
        yield from self.settings.values()
