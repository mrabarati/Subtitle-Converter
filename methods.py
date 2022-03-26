import os
from googletrans import Translator
from termcolor import colored
import time
import asyncio

FileSubtitle = 'conver'
logFile = open(f'C:\\Users\\{os.getlogin()}\\Desktop\\log.text', mode = 'w')
logFile.close()

#first section creat new folder subtitles
async def creat_folders(folders):
    try:
        global FileSubtitle 
        addr = f'C:\\Users\\{os.getlogin()}\\Desktop\\'
        os.mkdir(f'{addr}{FileSubtitle}')
        
        for folder in folders:
            os.mkdir(f'{addr}\\{FileSubtitle}\\{folder}')
    except :
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

async def write_srt_data(data,filename,index,directory):
    
    addr = f'C:\\Users\{os.getlogin()}\Desktop\\'
    for d in os.listdir(f'{addr}\\{FileSubtitle}\\{directory}\\'):
        if filename in d:
            print(colored(f'file was in directory>>{directory}>>{filename}' , 'red'))
            return


    new_data  = [i.replace('\n','')  for i in data if i.replace('\n','').strip() !='']
    out_put = ''
    # pprint.pprint(new_data)

    
    try:
        
        if directory =='root':
            for subtitle in range(0,len(new_data),3):
                out_put += new_data[subtitle]+"\n"
                out_put += new_data[subtitle+1]+"\n"
                out_put += new_data[subtitle+2]+"\n"
                convert = await translate(new_data[subtitle+2])
                out_put += convert+"\n\n"
                print(convert)
                
            f = open(f'{filename}','w+' , encoding='utf-8')
            f.write(u'{}'.format(out_put))
            f.close()
            
        else:
            
            for subtitle in range(0,len(new_data),3):
                out_put += new_data[subtitle]+"\n" #Time
                out_put += new_data[subtitle+1]+"\n" #subtitle En
                out_put += new_data[subtitle+2]+"\n"
                convert = await translate(new_data[subtitle+2])
                out_put += convert+"\n\n"
                print(convert)

            f = open(f'{addr}\\{FileSubtitle}\\{directory}\\{filename}','w+' , encoding='utf-8')
            f.write(u'{}'.format(out_put))
            f.close()
    except Exception as e:
        print(e)
        print(colored("server rejected tour request..",'red'))
        print('try again after 60 sencend')
        for i in range(60,0,-1):
            print(f"",end=f'\r{i}')
            time.sleep(1)
        os.remove(f'{addr}\\{FileSubtitle}\\{directory}\\{filename}') #remove defext file
        await write_srt_data(data,filename,index,directory) #try again lost file
    print(f"Successfully The translate file {filename} from {directory} folder")


async def write_vtt_data():
    pass

