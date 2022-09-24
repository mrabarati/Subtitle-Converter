import os
from os import (listdir,system,chdir,getcwd,path)
from methods import *
import time
import Virtual_thread
Object_pro = Virtual_thread.Thread_()

def finish():
    global Object_pro
    Object_pro.stop()
    
async def convert_one_file(filename,config_):
  
    file = filename.split('/')[-1]

    data = open(filename).readlines()
    await write_data(data,file,0,'root',config_,Object_pro)
    await log(0,filename,'root')
    if config_['shutter']:
        system('shutdown /s /t 1')
async def mind_main(folder,config_):
    type_sub = ('.srt','.vtt')
    chdir(folder)
    

    files = [i for i in listdir('.') if type_sub[0] in i or type_sub[1] in i]#to do list all subtitles
    
    #better way for list files
    #files = [i for i in listdir('.') if i.endswith(type_sub)]
    #files = [filter(sample.endswith, type_sub) for i in listdir('.')]
    folders = [i for i in listdir('.') if path.isdir(i)]#to do list all folders
    
    #creat folders for new subtitles
    
    direction = getcwd().split('\\')[-1]

    # print(direction)
    try:
        await creat_folders([direction,]) 
        await creat_folders(folders) 
    except FileExistsError:
        pass
    
    #############single folder section################
    start = time.time()
    for index,filename in enumerate(files):
        if Object_pro.get_convert() == False:
            return
        data = open(filename).readlines()
        await write_data(data,filename,index,direction,config_,Object_pro)
        await log(index,filename,direction)
    if len(files) != 0:
        end = time.time()
        print(colored(f'finished {direction} folder at >>{await calc_time(int(end-start))} ','green'))
    #############single folder end################

    await log_seprator() #sepreted last logs

    
    for index,folder_name in enumerate(folders):
        print(colored(f"Scaning {folder_name}...",'green'))
        
        scaned = [i for i in listdir(f'{folder_name}\\') if type_sub[0] in i or type_sub[1] in i]
        
            
        start = time.time()
        # print(scaned)
        if len(scaned) ==0:
            print("zero length...")
            continue
        else:
            for index_,filename in enumerate(scaned):
                if Object_pro.get_convert() == False:
                    return
                data = open(f'{folder_name}\\{filename}' , encoding='utf8').readlines()
                
                await write_data(data,filename,index_,folder_name,config_,Object_pro)
                await log(index_,filename,folder_name)
                
            end = time.time()
            print(colored(f'finished {folder_name} folder at >>{await calc_time(int(end-start))} ','green'))
            await log_seprator() #sepreted last logs
    print("finished")
    if config_['shutter']:
        system('shutdown /s /t 1')
    return