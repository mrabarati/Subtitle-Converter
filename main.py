import tkinter as tk
from threading import Thread
from tkinter.messagebox import showinfo,showwarning
from tkinter import filedialog as fd
from tkinter import font as tkfont
from mindProject import mind_main,convert_one_file
from asyncio import run as run_method


#variables
file_choiced = None
folder_choiced = None
run = lambda  x :run_method(x)

class data:
    def __init__(self):
        #parametr one is translate tow lang
        #parametr two is shudown auto after work
        self.data ={'check_box_two':1,"shutter":0}
        
    @property    
    def get_data(self):
        return self.data
    
    @get_data.setter
    def set_data_check_box_two(self, data):
        self.data['check_box_two'] = data
    
    @get_data.setter
    def set_data_shutter(self, data):
        self.data['shutter'] = data

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["main"] = main(parent=container, controller=self)
        self.frames["Config"] = Config(parent=container, controller=self)
        
        self.frames["main"].grid(row=0, column=0, sticky="nsew")
        self.frames["Config"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("main")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



class main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #config controller
        self.controller = controller
        self.controller.title('صفحه اصلی')
        self.controller.configure(background='#A8B4AF')
        self.controller.geometry('320x195')
        self.controller.resizable(False, False)
        #buttons
        ##############btns########################
        self.open_button = tk.Button(self,text='انتخاب فایل',command=self.select_file)
        self.open_button_folder  = tk.Button(self,text = 'انتخاب پوشه',command = self.select_folder)
        self.submit = tk.Button(self,text = 'شروع',command = self.start)
        self.conf_window = tk.Button(self,text = 'تنظیمات',command = self.change_frame)
        self.quit_btn = tk.Button(self,text = 'خروج',command = lambda :self.controller.destroy())
        self.config_btns()
    def on_enter_file(self,e):
        e['background'] = '#dcefee'
    
    def on_leave_file(self,e):
        e['background'] = '#84F3C5'
    def config_btns(self):
        
        #config buttons
        self.open_button_folder.pack(expand=True)
        self.open_button.pack(expand=True)
        self.submit.pack(expand=True)
        self.conf_window.pack(expand=True)
        self.quit_btn.pack(expand=True)
        #folder btn
        self.open_button_folder.place(x=70, y=21)
        self.open_button_folder.configure(width=26)
        self.open_button_folder.configure(background='#84F3C5')
        self.open_button_folder.bind("<Enter>", lambda x: self.on_enter_file(self.open_button_folder))
        self.open_button_folder.bind("<Leave>",lambda x: self.on_leave_file(self.open_button_folder))
        #file btn
        self.open_button.place(x=70, y=50)
        self.open_button.configure(width=26)
        self.open_button.configure(background='#84F3C5')
        self.open_button.bind("<Enter>", lambda x: self.on_enter_file(self.open_button))
        self.open_button.bind("<Leave>",lambda x: self.on_leave_file(self.open_button))

        #submit btn
        self.submit.configure(width=26 , background='#84F3C5')
        self.submit.place(x=70, y=79)
        self.submit.bind("<Enter>", lambda x: self.on_enter_file(self.submit))
        self.submit.bind("<Leave>",lambda x: self.on_leave_file(self.submit))
        # #conf btn
        self.conf_window.configure(width=26 , background='#84F3C5')
        self.conf_window.place(x=70, y=107)
        self.conf_window.bind("<Enter>", lambda x: self.on_enter_file(self.conf_window))
        self.conf_window.bind("<Leave>",lambda x: self.on_leave_file(self.conf_window))
        #quit btn
        self.quit_btn.configure(width=26 , background='#84F3C5')
        self.quit_btn.place(x=70, y=134)
        self.quit_btn.bind("<Enter>", lambda x: self.on_enter_file(self.quit_btn))
        self.quit_btn.bind("<Leave>",lambda x:self.on_leave_file(self.quit_btn))
    
    def start(self):
        global root,folder_choiced,file_choiced
        if file_choiced == None and folder_choiced == None:
            showwarning('انتخاب کنید','لطفا فایل یا پوشه ای انتخاب کنید')
        
        elif file_choiced and folder_choiced:
            showwarning('برو بریم','فرایند فایل و پوشه به ترتیب در حال اجرا هستن')
            
            par1,par2 = file_choiced,folder_choiced
            file_choiced = folder_choiced= False
            Thread(target=run,args=(convert_one_file(par1,loaded_object.get_data),)).start() 
            Thread(target = run,args =(mind_main(par2,loaded_object.get_data),)).start()

        elif file_choiced :
            showwarning('برو بریم','فرایند تبدیل فایل شروع شد')
            par = file_choiced
            file_choiced = None
            Thread(target=run,args=(convert_one_file(par,loaded_object.get_data),)).start()
            
        else:
            showwarning('برو بریم','پوشه در حال اسکن  برای شروع است')
            # root.destroy()
            par = folder_choiced
            folder_choiced =None
            Thread(target = run,args =(mind_main(par,loaded_object.get_data),)).start()
    
    def select_file(self):  
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
    def select_folder(self):
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
    def change_frame(self):
        
        self.controller.geometry('300x300')
        self.controller.resizable(False, False)
        self.controller.title('تنظیمات')
        self.controller.show_frame("Config")

		


# second window frame page1
class Config(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #config controller
        self.controller = controller
        self.back_main =tk.Button(self,text = 'بازگشت به منو اصلی',command = lambda :self.show_frame("main"))
        
        

        #check button translate 1
        self.text_ = 'زیرنویس دوزبانه باشد(زبان مبدا و مقصد)'
        self.status_check_button = tk.IntVar(self,value=loaded_object.get_data['check_box_two'])
        self.bt_check = tk.Checkbutton(self, text=self.text_, variable=self.status_check_button)
        
        #check button translate 1
        self._text_ = 'سیستم پس از انجام عملیات خاموش شود'
        self.status_check_two = tk.IntVar(self,value=loaded_object.get_data['shutter'])
        self.bt_check_two = tk.Checkbutton(self, text=self._text_, variable=self.status_check_two)
        self.config_btns()
    
    def config_btns(self):
        #config back to main 
        self.back_main.pack(expand=True)        
        self.back_main.configure(background='#A8B4AF',width=40)
        self.back_main.place(x=5,y=260)
        
        
        #config check btn
        self.bt_check.place(x=25, y=10)
        self.bt_check.configure(background='#A8B4AF',width=30)
        
        #config check btn two

        self.bt_check_two.place(x=25,y=40)
        self.bt_check_two.configure(background='#A8B4AF',width=30)


    def show_frame(self, page_name):
        loaded_object.set_data_check_box_two = self.status_check_button.get()
        loaded_object.set_data_shutter = self.status_check_two.get()
        self.controller.geometry('320x195')
        self.controller.resizable(False, False)
        self.controller.title('صفحه اصلی')
        self.controller.show_frame("main")
    

if __name__ == '__main__':
    try:
        import pickle
        file_to_read = open("stored_object.pickle", "rb")
        loaded_object = pickle.load(file_to_read)

        app = tkinterApp()
        app.mainloop()

        file_to_store = open("stored_object.pickle", "wb")
        pickle.dump(loaded_object, file_to_store)
        
        file_to_store.close()
        file_to_read.close()
    except Exception as e:
        loaded_object = data()

        app = tkinterApp()
        app.mainloop()

        file_to_store = open("stored_object.pickle", "wb")
        pickle.dump(loaded_object, file_to_store)
        file_to_store.close()
    

