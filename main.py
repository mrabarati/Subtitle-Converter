
from PyQt6.QtWidgets import (QApplication,QPushButton,QCheckBox,
                            QStackedWidget,QMainWindow,QFileDialog)

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QFont,QIcon
from PyQt6 import QtCore
import sys

from mindProject import mind_main,convert_one_file,finish
from asyncio import run as run_method
from threading import Thread
from os import getlogin


#run Thread
run = lambda  x :run_method(x)


class data:
    def __init__(self):
        #parametr one is translate tow lang
        #parametr two is shudown auto after work
        self.data ={'check_box_two':False,"shutter":False}
        
    @property    
    def get_data(self):
        return self.data
    
    @get_data.setter
    def set_data_check_box_two(self, data):
        self.data['check_box_two'] = data
    
    @get_data.setter
    def set_data_shutter(self, data):
        self.data['shutter'] = data


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        
        self.choseFile   = QPushButton('انتخاب فایل',self)
        self.choseFolder = QPushButton('انتخاب پوشه',self)
        self.startButton = QPushButton('شروع',self)    
        self.confButton  = QPushButton('تنظیمات',self)
        self.exitButton  = QPushButton('خروج',self)

        self.configButtons()

        self.file_choiced = None
        self.folder_choiced = None

    def configButtons(self):
        
        self.choseFile.setGeometry(55,25,200,25)
        self.choseFolder.setGeometry(55,50,200,25)
        self.startButton.setGeometry(55,75,200,25)
        self.confButton.setGeometry(55,100,200,25)
        self.exitButton.setGeometry(55,125,200,25)

        
        #clicked configs
        self.choseFile.clicked.connect(self.selectFile)
        self.choseFolder.clicked.connect(self.selectFolder)
        self.startButton.clicked.connect(self.start)
        self.confButton.clicked.connect(self.gotoConfigWindow)
        self.exitButton.clicked.connect(self.exitProgram)



        #color
        self.choseFile.setStyleSheet('color:blue;background-color:white')
        self.choseFolder.setStyleSheet('color:blue;background-color:#4af3d9')
        self.startButton.setStyleSheet('color:blue;background-color:#f7cd31')
        self.confButton.setStyleSheet('color:blue;background-color:#b98af1')
        self.exitButton.setStyleSheet('color:blue;background-color:#f73131')

        
    def exitProgram(self):
        widget.hide()
        finish()
        exit()
        #widget.hide()
    def selectFile(self):
        Desktop = f"C:\\users\\{getlogin()}\\Desktop"

        self.file = QFileDialog.getOpenFileName(self,str("انتخاب فایل"),Desktop,
            ("Files (*.vtt *.srt)\
            ;;Text files (*.txt)"))

        if self.file[0] =='':
            pass
        else:
            self.file_choiced = self.file[0]
            self.show_warning(title="انتخاب فایل",text="فایل با موفقیت انتخاب شد")
        

    def selectFolder(self):

        self.directory = QFileDialog.getExistingDirectory(self,"انتخاب پوشه")

        if self.directory:
            self.folder_choiced = self.directory
            self.show_warning(title="انتخاب پوشه",text="پوشه با موفقیت انتخاب شد")


    def start(self):
        if self.file_choiced is None and self.folder_choiced is None:
            self.show_warning(title="عملیات ناموفق",text='لطفااول فایل یا پوشه ای انتخاب کنید')


        elif self.file_choiced and self.folder_choiced:
            self.show_warning(title='برو بریم',text='فرایند فایل و پوشه به ترتیب در حال اجرا هستن')
            par1,par2 = self.file_choiced,self.folder_choiced
            
            self.file_choiced, self.folder_choiced = False, False
            Thread(target=run,args=(convert_one_file(par1,loaded_object.get_data),)).start() 
            Thread(target = run,args =(mind_main(par2,loaded_object.get_data),)).start()

            
        elif self.file_choiced:
            self.show_warning(title='برو بریم',text='فرایند تبدیل فایل شروع شد')
            par = self.file_choiced
            self.file_choiced = None
            Thread(target=run,args=(convert_one_file(par,loaded_object.get_data),)).start()
            
            


        else:
            self.show_warning(title='برو بریم',text='پوشه در حال اسکن  برای شروع است')
            par = self.folder_choiced
            self.folder_choiced =None
            Thread(target = run,args =(mind_main(par,loaded_object.get_data),)).start()
            
            

    def show_warning(self,title,text):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(text)
        dlg.exec()


    def gotoConfigWindow(self):
        confWindowObject = windowConfig()
        widget.addWidget(confWindowObject)
        widget.setWindowTitle('تنظیمات')
        widget.setWindowIcon(QIcon("\\picturs\\python.png"))
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedWidth(300)
        widget.setFixedHeight(300)
        widget.setStyleSheet('background-color:#edff55')

class windowConfig(QMainWindow):
    def __init__(self):
        super(windowConfig,self).__init__()

        #checkBox for the configurations
        self.langSubtitleText = QCheckBox(self)
        self.shutDownSystem = QCheckBox(self)
    
        self.langSubtitleText.toggled.connect(lambda :self.check_box_function(1))
        self.shutDownSystem.toggled.connect(lambda :self.check_box_function(2))


        #button return to main page
        self.returnButton  = QPushButton(self)
       

        self.config_Qwidgets()
    

    
    #set config
    def config_Qwidgets(self):
        '''Config buttons,checkBoxs....'''
        #checkBoxs lang
        self.langSubtitleText.setFont(QFont('Times',12))
        self.langSubtitleText.setGeometry(20,15,250,20)
        self.langSubtitleText.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.langSubtitleText.setChecked(loaded_object.get_data['check_box_two'])
        
        #checkBox shutdown
        self.shutDownSystem.setFont(QFont('Times',12))
        self.shutDownSystem.setGeometry(20,40,250,20)
        self.shutDownSystem.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.shutDownSystem.setChecked(loaded_object.get_data['shutter'])


        #buttons -> return to main page
        self.returnButton.setGeometry(20,250,250,25)
        self.returnButton.clicked.connect(self.goMainWindow)
        self.returnButton.setStyleSheet('color:blue;background-color:#78f02f')
        
        #goto set lang function
        self.set_languge_fa_for_widgets()
        
    
    #set languge_fa
    def set_languge_fa_for_widgets(self):
        '''Set Language farsi to any thing'''
        self.langSubtitleText.setText('زیرنویس دو زبانه باشد(زبان مبدا و فارسی)')
        self.shutDownSystem.setText('سیستم پس از انجام عملیات خاموش شود')
        self.returnButton.setText('بازگشت به منو')
        

    def set_languge_En_for_widgets(self):
        '''This option coming soon'''
        pass
    
    def check_box_function(self,index):
        global loaded_object
        
        if index == 1 :  
            loaded_object.set_data_check_box_two = self.langSubtitleText.isChecked()

        else: 
            loaded_object.set_data_shutter = self.shutDownSystem.isChecked()

  
        #write update config
        file_to_store = open("stored_object.pickle", "wb")
        pickle.dump(loaded_object, file_to_store)
        file_to_store.close()


        
    #go to back data
    def goMainWindow(self):
        
        widget.setWindowTitle('صفحه اصلی')
        widget.setCurrentIndex(widget.currentIndex()-1) 
        widget.setFixedWidth(320)
        widget.setFixedHeight(200)
        widget.setStyleSheet('background-color:#94e944')



if __name__ =='__main__':

    def config_widget():
            
        widget.addWidget(window)
        widget.setCurrentIndex(widget.currentIndex())
        widget.setWindowTitle('صفحه اصلی')
        widget.setFixedWidth(320)
        widget.setFixedHeight(200)
        widget.setWindowIcon(QIcon('python.png'))
        widget.setStyleSheet('background-color:#94e944')
    
    try:
        import pickle
        file_to_read = open("stored_object.pickle", "rb")
        loaded_object = pickle.load(file_to_read)
        
        #run program
        app = QApplication(sys.argv)
        window = MainWindow()
        widget = QStackedWidget()
        config_widget()
        widget.show()

        sys.exit(app.exec())
    except:
        loaded_object = data()
        #run program
        app = QApplication(sys.argv)
        window = MainWindow()
        widget = QStackedWidget()
        config_widget()
        widget.show()
    
        file_to_store = open("stored_object.pickle", "wb")
        pickle.dump(loaded_object, file_to_store)
        file_to_store.close()
        sys.exit(app.exec())

