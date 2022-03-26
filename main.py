import asyncio
from tkinter import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo,showwarning
from mindProject import mind_main

file_choiced = folder_choiced = None

# create the root window
root = Tk()
root.title('زیر نویس ساز')
root.resizable(False, False)
root.geometry('320x150')
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
run = lambda  :asyncio.run(mind_main(folder_choiced))
def start():
    global root
    if file_choiced == None and folder_choiced == None:
        showwarning('انتخاب کنید','لطفا فایل یا پوشه ای انتخاب کنید')
    elif file_choiced and folder_choiced:
        showwarning('برو بریم','فرایند فایل و پوشه به ترتیب در حال اجرا هستن')
    elif file_choiced :
        showwarning('برو بریم','فرایند تبدیل فایل شروع شد')
        
    else:
        showwarning('برو بریم','پوشه در حال اسکن  برای شروع است')
        root.destroy()
        run()
        
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


#config buttons
open_button_folder.pack(expand=True)
open_button.pack(expand=True)
submit.pack(expand=True)

#folder btn
open_button_folder.place(x=70, y=21)
open_button_folder.configure(width=26)
open_button_folder.configure(background='#84F3C5')
#file btn
open_button.place(x=70, y=50)
open_button.configure(width=26)
open_button.configure(background='#84F3C5')
#submit btn
submit.configure(width=26 , background='#84F3C5')
submit.place(x=70, y=79)


############## end btns #########################
root.mainloop()
