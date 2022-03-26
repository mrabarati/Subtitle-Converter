import asyncio
import os
from tkinter.messagebox import showinfo
from methods import *
async def convert_one_file(filename):
    pass
async def mind_main(folder):
    type_sub = ['.srt','.vtt']
    os.chdir(folder)

    files = [i for i in os.listdir('.') if type_sub[0] in i or type_sub[1] in i]#to do list all subtitles
    folders = [i for i in os.listdir('.') if os.path.isdir(i)]#to do list all folders
    
    #creat folders for new subtitles
    try:
        await creat_folders(folders) 
    except FileExistsError:
        pass
    
    direction = os.getcwd()
    for index,filename in enumerate(files):
        data = open(filename).readlines()
        await write_srt_data(data,filename,index,direction)\
            if '.srt' in filename else write_vtt_data()
        await log(index,filename,direction)
    
    await log_seprator() #sepreted last logs
    for index,folder_name in enumerate(folders):
        print(colored(f"Scaning {folder_name}...",'green'))
        scaned = [i for i in os.listdir(f'{folder_name}\\') if type_sub[0] in i or type_sub[1] in i]
        start = time.time()
        for index_,filename in enumerate(scaned):
            data = open(f'{folder_name}\\{filename}' , encoding='utf8').readlines()

            await write_srt_data(data,filename,index_,folder_name)\
                 if '.srt' in filename else write_vtt_data()
            await log(index_,filename,folder_name)
            
        end = time.time()
        print(colored(f'finished {folder_name} folder at >>{await calc_time(int(end-start))} ','green'))
        await log_seprator() #sepreted last logs

