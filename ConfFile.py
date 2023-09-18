
from platform import system as system_base
from os import system, getlogin
class ConfigProgram :

    def __init__(self):
        # param one is translated tow lang
        # param two is shutdown auto after work
        self.system_os = system_base()

        if self.system_os == 'windows':
            self.__concat_route = '\\'
            self.shut_down_command = 'shutdown /s /t 0'
            self.desktop_route = f"C:\\users\\{getlogin()}\\Desktop"

        else :
            self.__concat_route = '/'
            self.shut_down_command = 'shutdown now'
            self.desktop_route = f"/home/{getlogin()}/Desktop"
        self.data =\
        {
            'check_box_two': False,
            "shutdown": False,
            'system_base': self.system_os,

        }

    @property
    def get_data(self) -> dict:
        return self.data

    @get_data.setter
    def set_data_check_box_two(self, data) -> None:
        self.data['check_box_two'] = data

    @get_data.setter
    def set_data_shutter(self, data) -> None:
        self.data['shutdown'] = data

    @property
    def get_os_name(self) -> str:
        return self.system_os

    @property
    def get_concat_route(self) -> str:
        return self.__concat_route

    def shutdown(self) -> None:
        if self.data['shutdown']:
            system(self.shut_down_command)


    def defult_route(self) -> str:
        return self.desktop_route
