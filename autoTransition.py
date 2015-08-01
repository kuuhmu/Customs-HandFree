# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 23:07:16 2015

@author: Pratheep
"""

from PySide import QtGui , QtCore # Import the PySide module we'll need  Not Pyqt4
import sys # We need sys so that we can pass argv to QApplication


from qt import autoUi # import from sub folder that include __init__.py in subfolder
# This file holds our MainWindow and all design related things
# it also keeps events etc that we defined in Qt Designer

from qt import core
from Queue import Queue   # use Q for return varailble
import time





### gui start ####

class auto_app(QtGui.QMainWindow,autoUi.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in .py file automatically
            
        #set event menu bar
        self.actionExit.activated.connect(self.close) #when click toexit or use -> self.close() in anather way
        self.actionOpen.activated.connect(self.open_file)
        
        
        
        # when click run start() and it start thread 
        self.button_start.clicked.connect(self.start)  # note cl or module not have a () ex: cl() use: cl
        self.button_open.clicked.connect(self.open_file)
        
        #set file chooser
        self.dialog = QtGui.QFileDialog()
        self.dialog.setFileMode(self.dialog.ExistingFile)
        self.filters = '*.csv' # filter
        self.dialog.setFilters(self.filters) #set fillter to .csv and *
    
        #set varialble
        self.file_path = None # for startup
        self.q = Queue() # for Queue
        
        
        self.count_sum = 0
        self.count_me = 0
        self.count_check = 0
        self.count_error = 0
        
        #  set instant of thread ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #if set in __init__ it will send arg before update it....
        #self.start_t = start_th(self,self.file_path)  # it sende var befor update


        
    #catch event Try to exit program . running itself     
    def closeEvent(self, event): ##### Close event !!!!
        try:
            thread_run_is = self.start_t.isRunning()
            if thread_run_is is True:
                force_quit = QtGui.QMessageBox.warning(self, 'Force Quit','Are you sure to exit? \n\nHave a process is running in background\n', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if  force_quit == QtGui.QMessageBox.Yes:
                    try:   # Try to close web and thread before exit program             
                        self.start_t.open_browser('exit')    # quit opened Browser             
                        self.start_t.quit() # quit Thread
                        print 'thread is running will quite .and exit program.'
                        event.accept() #close program wiht confirmation
                    except:
                        event.accept()
                else:
                    event.ignore()
            else:
                event.accept()
        except:
            event.accept()
        
    
    
    
    
    # function for interactive with gui #
    def start(self): #run  class start_t  .. start thread
        
        #  set instant of thread ## onthis use var update!
        self.start_t = start_th(self,self.file_path,self.q)  #!!!!!!! connect My Q pass from *arg

        if self.file_path is None or self.file_path == '':
            text_info = 'Can not Start! . You must select file from --> Click Open'
            #self.textBrowser.append(text_info)
            self.statusbar.showMessage(text_info)  #update satusbar
            print 'not select file'
        else:
            self.start_t.open_browser(1)
            print 'break'
            
            customs_url_1 = 'http://portal.customs.net/EXP/SecurityServlet'
            customs_url_2 = 'http://portal.customs.net/EXP/indexFrame.jsp'
            message_to_open_1 = '\
            Please Manual to prompt..\n\
            1. Click new tab To open new tab\n\
            2. Right Click -- > Past to URL box and Enter.\n\
            \n\
               It will open\n\
               http://portal.customs.net/EXP/SecurityServlet\n\n\
            3. After Enter it will load page and wait to finished\n\
            4. Close Tab And  Click OK'
            
            message_to_open_2 = '\
            5. On first tab Right Click -- > Past to URL box and Enter.\n\
            \n\
               It will open\n\
               http://portal.customs.net/EXP/indexFrame.jsp\n\n\
            6. Then select YOUR PORT and Update\n\
            7. Open Manual Matching Goods.. in left panel\n\
            8. Click OK to finished and it will start running Automatic matching\n\
            \n\
            Warning Important You must To Do all Befor click ok to run. \n\
            If not Browser will Close and you must to start again\n\n\
            If you not prompt you can click CANCLE.. IE browser will close.\n\
            You can start it again when you prompt'
                     
            
            cb = QtGui.QClipboard() #instant for clipboard            
            
            #open first guide 
            #set clipboard for first guide
            cb.setText(customs_url_1) #set text to clipboard
            reply1 = QtGui.QMessageBox.warning(self, 'Ok To Continue',message_to_open_1, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if  reply1 == QtGui.QMessageBox.Yes:
                #open second guide
                #set clipboard for second guide
                cb.setText(customs_url_2) #set text to clipboard
                reply2 = QtGui.QMessageBox.warning(self, 'Ok To Continue',message_to_open_2, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply2 == QtGui.QMessageBox.Yes:
                            # this for test if can not switch to frame that mean user not complet step open custom portal....
                    try:
                        self.start_t.web.switch_to_frame("frameset") #test unit
                        self.start_t.start() #start thread
                        self.start_t.sig.connect(self.update_gui)
                        self.button_start.setText('Starting..') #chang buttontext
                        self.button_start.setEnabled(False) # set disable button start   
                        cb.clear() #clear clipboard
                    except:
                        QtGui.QMessageBox.information(self,'You Not Compleate','You Not Compleate Step On Open Customs url.\n\nBrowser will Close!  And You Must Start Again')
                        self.start_t.open_browser('exit')

                else:
                    self.start_t.open_browser('exit') #close browser
            else:
                self.start_t.open_browser('exit')#close browser
                
                
        
    def open_file(self):
      
        
        #open dialog and it retrun of file and filter ,  (file,filter)                
        self.filename = self.dialog.getOpenFileName(caption="Please Choose File", filter=self.filters)
        
        print "Open click\t%s"%str(self.file_path)       
        if self.file_path == '':     
            self.statusbar.showMessage('Pleases Select file')
        else:
            self.file_path = self.filename[0]
            text_info = 'You are select    :  %s    If you promt - > click Start'%self.file_path
            self.textBrowser.append(text_info)
            self.button_start.setEnabled(True)
            print "Open click\t%s"%str(self.file_path)
        
    
    # update gui when recieve signal and get data from Q
    @QtCore.Slot(object)
    def update_gui(self,ob): #recieve signal
        print ob
  
  
        #move to __init__
#        self.count_sum = 0
#        self.count_me = 0
#        self.count_check = 0
#        self.count_error = 0
        
            ##   do display it!! 
        
        #use Queue but it ha ploblem
        #try:            
        q_get = self.q.get_nowait()
        status = q_get['status']
        good = q_get['good']
        text = q_get['text']
        v = q_get['v']
        
        if status == 'nomal':
            status_text = 'GTransition No. %s done. By You'%good
            self.statusbar.showMessage(status_text)
            self.count_sum += 1
            self.lcd_sum.display(self.count_sum)
            self.count_me +=1
            self.lcd_me.display(self.count_me)
            
            
        elif status == 'check':
            status_text = 'GTransition No. %s is CHECKED .'%good
            self.statusbar.showMessage(status_text)
            self.count_sum += 1
            self.lcd_sum.display(self.count_sum)
            self.count_check += 1
            self.lcd_check.display(self.count_check)
            
            
        elif status == 'error_port':
            status_text = 'GTransition No. %s can not chang port %s '%(good,str(v))
            info_text = 'GT : %s   -- can not change port %s'%(good,str(v))                 
            self.textBrowser.append(info_text)
            self.statusbar.showMessage(status_text)
            self.count_error += 1
            self.lcd_error.display(self.count_error)
            #self.log_it('info',info_text)
        
        elif status == 'error_notfound':
            status_text = 'GTransition No. %s NOT FOUND'%(good)
            info_text = 'GT : %s  GOOD TRANSITION NOT FOUND'%(good)                 
            self.textBrowser.append(info_text)
            self.statusbar.showMessage(status_text)
            self.count_error += 1
            self.lcd_error.display(self.count_error)
            #self.log_it('info',info_text)
            
        elif status == 'warnning':
            status_text = 'GTransition No. %s GT EXIT %s'%(good,str(v))
            info_text = 'GT : %s  GOOD TRANSITION EXIT %s'%(good,str(v))                 
            self.textBrowser.append(info_text)
            self.statusbar.showMessage(status_text)
            self.count_error += 1
            self.lcd_error.display(self.count_error)
            #self.log_it('info',info_text)

#        except:
#            print 'can nat get from q'
    
    
### gui end ###




## for main program core.py


class start_th(QtCore.QThread): # start is a thread #and use var form auto_app
    sig = QtCore.Signal(object) #must use object

    def __init__(self, parent=None , *arg ): #recieve file_p 
        QtCore.QThread.__init__(self, parent)
        self.exiting = True  # set thread exit when main windows exit()
        
        print str(arg)

        #arg is tuple
        self.file_path = arg[0]
        self.q = arg[1]
        
        #get instanl of Class
        self.c = core.core_true(self.q)
   
        
    def run_test(self): #for test only .... rename it to run.
        a = 0
        while a != 1000:
            self.c.test_q(self.q)
            self.sig.emit('ok')
            time.sleep(0.03)
            a +=1
        self.web.quit()
            
        
    
    #  QThread will use this funtion to run it ONLY!!!
    def run(self):       
  
        #print self.file_path,'\tfrom class auto_app'
        
     
            
            
        counter = 1 
        file_name = self.file_path
        data = self.c.csv_2_dict(file_name)
        for i in data:
            g = i
            z = data[i]['size']
            p = data[i]['ter']
            cn = data[i]['container']
            d = data[i]['date']
            t = data[i]['time']
            
            #sent to statusbar    "%s . #\t%s\t%s\t%s\t%s\t%s\t%s"%(counter,g,z,p,cn,d,t)
            time.sleep(0.5)
            #textview_debug_add("%s . #\t%s\t%s\t%s\t%s\t%s\t%s"%(counter,g,z,p,cn,d,t))  #gtk
            self.c.doit1(self.web,g,z,p,cn,d,t) # use Q to put and get
            
            self.sig.emit(counter) # send signal out from thread to qt
            counter += 1

        self.web.quit()
        
        
    def open_browser(self,status):

        if status == 'exit':
            self.web.quit()
        else:
            print 'now will open browser'
            #print self.file_path,'\tfrom class auto_app'
            
            self.web = self.c.opendriver() # set hear
            self.web.implicitly_wait(10)
            self.web.get("http://portal.customs.net")
            #log_it('info','Open brower....')
            print 'open browser complete'


  
## end main core.. ##



def main():
    ## This fix A new instance of QApplication
    #RuntimeError: A QApplication instance already exists.

    app=QtGui.QApplication.instance()	# checks if QApplication already exists
    if not app:	# create QApplication if it doesnt exist
        app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
        
    ##### 
    windows = auto_app()                 # We set the form to be our ExampleApp (design)
    windows.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function