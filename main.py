import asyncio
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo,showwarning
from mindProject import mind_main,convert_one_file
from threading import Thread


file_choiced = folder_choiced = None
data_config_window = dict()

# create the root window
root = Tk()
root.title('زیر نویس ساز')
root.resizable(False, False)
root.geometry('320x175')
root.configure(background='#A8B4AF')
#buttons
##############btns########################


def select_file():  
    global file_choiced 
    filetypes = (
        ('subtitle', '*.srt'),
        ('subtitle','*.vtt')
        
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    if filename =='':
        pass
    else:
        file_choiced = filename
        showinfo(
            title='فایل انتخاب شده',
            message=filename
        )
#btutton for select folder
def select_folder():
    global folder_choiced
    folder_selected = fd.askdirectory()
    if folder_selected == '':
        pass
    else:
        folder_choiced = folder_selected
        showinfo(
                title='پوشه انتخاب شد',
                message=folder_selected
            )
run = lambda  x :asyncio.run(x)
def start():
    global root,folder_choiced,file_choiced
    if file_choiced == None and folder_choiced == None:
        showwarning('انتخاب کنید','لطفا فایل یا پوشه ای انتخاب کنید')
    
    elif file_choiced and folder_choiced:
        showwarning('برو بریم','فرایند فایل و پوشه به ترتیب در حال اجرا هستن')
        
        par1,par2 = file_choiced,folder_choiced
        file_choiced = folder_choiced= False
        Thread(target=run,args=(convert_one_file(par1),)).start()
        
        Thread(target = run,args =(mind_main(par2),)).start()

    elif file_choiced :
        showwarning('برو بریم','فرایند تبدیل فایل شروع شد')
        par = file_choiced
        file_choiced = False
        Thread(target=run,args=(convert_one_file(par),)).start()
        
    else:
        showwarning('برو بریم','پوشه در حال اسکن  برای شروع است')
        # root.destroy()
        par = folder_choiced
        folder_choiced =False
        Thread(target = run,args =(mind_main(par),)).start()
        
def exit_top():
    global root
    root.destroy()

def config_button():
    
    
    config_window = Toplevel(root)
    config_window.title('تنظیمات')
    config_window.resizable(False, False)
    config_window.geometry('600x600')
    config_window.configure(background='#A8B4AF')
    

    #functions
    def go_back_function():
        config_window.destroy()
    
    #btns    
    back_main =Button(
        config_window,
        text = 'بازگشت به منو اصلی',
        command = go_back_function
    )
    back_main.pack(expand=True)        
    back_main.configure(background='#A8B4AF')
    conf_window.mainloop()
    
# button fo select file
open_button = Button(
    root,
    text='انتخاب فایل',
    command=select_file
)

open_button_folder  = Button(
    root,
    text = 'انتخاب پوشه',
    command = select_folder
)
submit = Button(
    root,
    text = 'شروع',
    command = start
)

conf_window = Button(
    root,
    text = 'تنظیمات',
    command = config_button
)

quit_btn = Button(
    root,
    text = 'خروج',
    command = lambda :root.destroy()
)
def on_enter_file(e):
    e['background'] = '#dcefee'
    
def on_leave_file(e):
    e['background'] = '#84F3C5'
    
#config buttons
open_button_folder.pack(expand=True)
open_button.pack(expand=True)
submit.pack(expand=True)
conf_window.pack(expand=True)
quit_btn.pack(expand=True)
#folder btn
open_button_folder.place(x=70, y=21)
open_button_folder.configure(width=26)
open_button_folder.configure(background='#84F3C5')
open_button_folder.bind("<Enter>", lambda x: on_enter_file(open_button_folder))
open_button_folder.bind("<Leave>",lambda x: on_leave_file(open_button_folder))
#file btn
open_button.place(x=70, y=50)
open_button.configure(width=26)
open_button.configure(background='#84F3C5')
open_button.bind("<Enter>", lambda x: on_enter_file(open_button))
open_button.bind("<Leave>",lambda x: on_leave_file(open_button))

#submit btn
submit.configure(width=26 , background='#84F3C5')
submit.place(x=70, y=79)
submit.bind("<Enter>", lambda x: on_enter_file(submit))
submit.bind("<Leave>",lambda x: on_leave_file(submit))
#conf btn
conf_window.configure(width=26 , background='#84F3C5')
conf_window.place(x=70, y=107)
conf_window.bind("<Enter>", lambda x: on_enter_file(conf_window))
conf_window.bind("<Leave>",lambda x: on_leave_file(conf_window))
#quit btn
quit_btn.configure(width=26 , background='#84F3C5')
quit_btn.place(x=70, y=134)
quit_btn.bind("<Enter>", lambda x: on_enter_file(quit_btn))
quit_btn.bind("<Leave>",lambda x: on_leave_file(quit_btn))
############## end btns #########################
root.mainloop()
