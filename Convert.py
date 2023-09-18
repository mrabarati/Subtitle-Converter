from os import walk, makedirs,listdir, getlogin
from termcolor import colored
from time import time, sleep
from tqdm import tqdm
from googletrans import Translator


class Scan:

    def __init__(self, concat_route):
        self.count_files = 0

        #contain a tuple have two item
        #item1 -> file sub folders
        #item2 -> file name
        self.__folder_file = []
        self.sub_types = ('.srt','.vtt')
        self.path_folder = None
        self.path_folder_translated = None
        self.index_folder_name = None
        self.concat_route = concat_route
    def scan_direcroy(self, directory_address):
        """ scan course folders and files """

        self.path_folder = directory_address
        self.path_folder_translated = self.path_folder.split(self.concat_route)
        self.index_folder_name = len(self.path_folder_translated) - 1
        self.path_folder_translated = [f'new_sub_curse_{self.path_folder_translated[-1]}']

        for root, dir, file in walk(self.path_folder):

            file_path = root.split(self.concat_route)
            file_path[self.index_folder_name] = self.path_folder_translated[0]
            file_path = f'{self.concat_route}'.join(file_path)
            for file_name in file:
                if file_name.endswith(self.sub_types):
                    self.__folder_file.append(dict(source_path = root+self.concat_route,
                                                   dest_path   = file_path+self.concat_route,
                                                   file_name   = file_name))

    def create_folders_for_new_sub(self):
        """ Create new subtitle folders """
        for directory in self.__folder_file:
            try:
                makedirs(directory['dest_path'])
            except FileExistsError:
                # print(f"The directory already exists: {directory}")
                pass
    def get_files(self):
        return self.__folder_file

class ConvertText:

    def __init__(self, sublist: list, stop: object, concat: str, source_lang_with_dest_lang_together:bool):
        self.subtitle_list = sublist
        self.stop = stop
        self.concat_address = concat
        self.s_d_lang = source_lang_with_dest_lang_together

    def start(self):
        check_directory_name = None
        start_folder_convert_time = time()
        message_scan = False
        for index, dictionary_of_data in enumerate(self.subtitle_list, start=1):
            s_path = dictionary_of_data['source_path']
            d_path = dictionary_of_data['dest_path']
            f_name = dictionary_of_data['file_name']

            if not message_scan:
                print(colored(f"Scaning {s_path}", 'green'))
                message_scan = True

            if check_directory_name is None:
                check_directory_name = s_path

            if check_directory_name != s_path:
                check_directory_name = s_path
                end_time = time()
                print(colored(f'finished {s_path} folder at >>{self.calc_time(int(end_time - start_folder_convert_time))} ', 'green'))
                message_scan = False
            try:
                # Check continue for translate or not
                if not self.stop.get_convert():
                    return

                # Checking if the file has already been translated or not
                if self.check_translated(directory= d_path, file_name= f_name):
                    continue

                data_file = open(s_path + f_name, encoding='utf8').readlines()

                self.write(
                    data=data_file,
                    dict_data=
                    {
                        "s_path" :s_path,
                        "d_path" :d_path,
                        "f_name" :f_name,
                    },

                )


            except Exception as e:
                print('Error :(')
                print(e)

    def write(self,
              #list of string for translate
              data: list,
              # Information of file,dir_file, dir_dest after translate
              dict_data: dict,
              # If the program is interrupted during translation, continue from this number
              index: int = 0, translated_data: list = None) -> None:


        # If the program is interrupted during translation continue from lose index
        if index:
            data = data
            new_data = translated_data
            start_index = index
        else:
            data = data[self.find_first_line(data):]
            new_data = []
            start_index = 1

        try:

            for index_converting, subtitle in enumerate(tqdm(data[index:],
                                                             desc=colored('converting..','green'))):
                subtitle = subtitle.replace('\n', '').strip()

                # If user stop program
                if not self.stop.get_convert():
                    return
                if self.is_time_subtitle(subtitle):
                    new_data.extend(['\n', start_index, subtitle])
                    start_index += 1
                elif self.is_digit_(subtitle) == False:
                    # convert data to dst lang and append into new_data

                    if self.s_d_lang:
                        new_data.extend([subtitle, self.translate(subtitle)])
                    else:
                        new_data.append(self.translate(subtitle))
            # write finally data
            _file_path = dict_data['d_path']+dict_data['f_name']
            with open(_file_path, mode= 'w+' , encoding= 'utf-8') as translated_file:
                for _ in new_data:
                    if _ == '\n':
                        translated_file.write(u'\n')
                    else:
                        translated_file.write(u'{}\n'.format(str(_)))



        except Exception as error:
            print(colored("server rejected your request..", 'red'))
            print('try again after 60 sencend')
            for i in range(60, 0, -1):
                print(f"", flush=True, end=f'\r{i}')
                sleep(1)


            self.write(data, dict_data, index=index_converting, translated_data=new_data)
        finally:
            print(f"Successfully The translate file {dict_data['f_name']} from {dict_data['s_path']} folder")




    def check_translated(self, directory: str, file_name: str):
        if file_name in listdir(directory):
            print(colored(f'file was in directory>>{directory}>>{file_name}', 'red'))
            return True
        return False
    def is_digit_(self, string):
        return True if string.strip().isdigit() else False

    def is_time_subtitle(self, string):
        string = string.strip()
        if string.count(':') >= 2 and "-->" in string:
            return True

    def find_first_line(self, list_data):
        index = 0
        for i in list_data:
            if self.is_time_subtitle(i):
                break
            index += 1
        return index

    def calc_time(self, secend: int) -> str:
        h = secend // 3600
        secend = secend - (h * 3600)
        m = secend // 60
        secend = secend - m * 60
        return f'{h} Hour: {m} min: {secend} secend'

    def translate(self, data):
        translator = Translator()
        result = translator.translate(data, dest='fa')
        return result.text
class Log:

    def __init__(self):
        pass

    def log_create_folder(self):
        pass

    def log_success_convert_file(self):
        pass

    def log_failed_convert_file(self):
        pass


def start_convert(course_path: str, config_object: object,  stop_thread:object, single_file: bool = False):
    scan_result = None
    concat_route = config_object.get_concat_route
    if single_file:
        curse = course_path.split(concat_route)
        curse_name = curse.pop()
        curse_path = f'{concat_route}'.join(curse)
        curse_dst = f'/home/{getlogin()}/Desktop/'

        ConvertText(sublist=[{
                'source_path' :curse_path+concat_route,
                'dest_path' :curse_dst+concat_route,
                'file_name':curse_name
            },],
                    stop=stop_thread,
                    concat=concat_route,
                    source_lang_with_dest_lang_together=config_object.get_data['check_box_two'],
                                     ).start()
        
    else:
        # Create object from class Scan
        scan_object = Scan(config_object.get_concat_route)
        # Scan all folders and find subtitle files
        scan_object.scan_direcroy(course_path)
        # Create all folder have subtitle for new subtitle
        scan_object.create_folders_for_new_sub()

        # Get list all_of file contains (source_path, dest_path, file_name)
        scan_result = scan_object.get_files()

        # Create Object from Convert Class
        convert_object = ConvertText(sublist=scan_result,
                                     stop=stop_thread,
                                     concat=config_object.get_concat_route,
                                     source_lang_with_dest_lang_together=config_object.get_data['check_box_two'],
                                     )

        #start convert
        convert_object.start()

    # Shutdown system
    # config_object.shutdown()

    print("translated file" if single_file else "All files translated")



# {'source_path': '/media/ali/51E9-B1A8/down/javaScript/01 - Welcome, Welcome, Welcome_/',
#  'dest_path': '/media/ali/51E9-B1A8/down/new_sub_curse_javaScript/01 - Welcome, Welcome, Welcome_/',
#  'file_name': '001 Course Structure and Projects_Downloadly.ir_en.srt'}
