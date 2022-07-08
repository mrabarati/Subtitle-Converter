import os
from googletrans import Translator
from termcolor import colored
import time
import asyncio
import tqdm
import pprint
FileSubtitle = 'tranlated_data'
logFile = open(f'C:\\Users\\{os.getlogin()}\\Desktop\\log.text', mode = 'w')
logFile.close()

#set new name for FileSubtitle by user
async def set_FileSubtitle(name):
    global FileSubtitle
    FileSubtitle = name

#first section creat new folder subtitles
async def creat_folders(folders):
    print(folders)
    status = False if type(folders) != list else True
    # print(folders,status)
    
    try:
        global FileSubtitle 
        addr = f'C:\\Users\\{os.getlogin()}\\Desktop\\'
        os.mkdir(f'{addr}{FileSubtitle}')
        for folder in folders:
            
            os.mkdir(f'{addr}\\{FileSubtitle}\\{folder}')
    except :
        for folder in folders:
            try:

                os.mkdir(f'{addr}\\{FileSubtitle}\\{folder}')
            except:
                pass
#translate text
async def translate(data):
    translator = Translator()
    result = translator.translate(data ,dest='fa')
    return result.text

#first number of srt files
#last_success is file that was successfully translated
#folder file folder
async def log(index,last_success_file,folder):
    addr = f'C:\\Users\\{os.getlogin()}\\Desktop\\log.text'
    logFile = open(addr, mode = 'a')
    logFile.write(f'{folder} >> {index} >> file name >>{last_success_file}\n')
    logFile.close()

async def log_seprator():
    addr = f'C:\\Users\\{os.getlogin()}\\Desktop\\log.text'
    logFile = open(addr, mode = 'a')
    logFile.write('##################################\n')
    logFile.close()

async def calc_time(secend):
    h = secend//3600
    secend = secend-(h*3600)
    m = secend//60
    secend = secend -m*60
    return f'{h} Hour: {m} min: {secend} secend'

#write and translate subtitle 
async def write_data(data,filename,index,directory):
    addr = f'C:\\Users\\{os.getlogin()}\\Desktop\\'
    if directory!='root':
        for d in os.listdir(f'{addr}{FileSubtitle}\\{directory}\\'):
            if filename in d:
                print(colored(f'file was in directory>>{directory}>>{filename}' , 'red'))
                return
    else:
       for d in os.listdir(f'{addr}{FileSubtitle}\\'):
            if filename in d:
                print(colored(f'file was in directory>>{directory}>>{filename}' , 'red'))
                return 
    #check the string is a number!!
    async def is_digit_(string):
        string = string.strip()
        if string.isdigit():
            return True
        return False

    #check is time subtitle
    async def is_time_subtitle(string):
        string = string.strip()
        if string.count(':')>=2 and "-->" in string:
            return True

    #chck the string is subtitle
    async def is_subtitle(string):
        if len(string)>=3:
            return True

    async def find_first_line(list_data):
        index = 0
        for i in list_data:
            if await is_time_subtitle(i):
                break
            index +=1

        return index
    
    data = data[await find_first_line(data):]
    new_data = []
    index = 1

    try:
        for subtitle in tqdm.tqdm(data,desc=colored('converting..','green')):
            subtitle = subtitle.replace('\n','').strip()
            if await is_time_subtitle(subtitle):
                new_data.append('\n')
                new_data.append(index)
                index +=1
                new_data.append(subtitle)
            elif await is_subtitle(subtitle):
                #convert data to dst lang and append into new_data
                new_data.append(subtitle)
                new_data.append(await translate(subtitle))
        
        #write finally data
        f = open(f'{addr}\\{filename}','w+' , encoding='utf-8') if directory =='root' else \
                open(f'{addr}\\{FileSubtitle}\\{directory}\\{filename}','w+' , encoding='utf-8')
        for i in new_data:
            if i=='\n':
                f.write(u'\n')
            else:
                f.write(u'{}\n'.format(str(i)))
        f.close()

    except Exception as e:
        print(colored("server rejected your request..",'red'))
        print('try again after 60 sencend')
        for i in range(60,0,-1):
            print(f"",end=f'\r{i}')
            time.sleep(1)
        
        await write_data(data,filename,index,directory) #try again lost file
    print(f"Successfully The translate file {filename} from {directory} folder")
