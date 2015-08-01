# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 14:39:52 2015

@author: Pratheep
"""

from selenium import webdriver
import time
from datetime import datetime , timedelta
import random
import csv
import os
import sys
from Queue import Queue  # use for Thread and send recieve data
#import logging

#os.chdir('Desktop\customs')
sys.path.append(os.getcwd()) #Add curent to Path it have a selenium runtime

my_q = Queue()

class core_true:
    

    def __init__(self,que):
        self.q =que
            
        
    def test_q(self,que): #for test only
        
        import random
        self.test_g = '5807a'+str(random.randrange(1111111,9999999))

        self.q = que
        print 'From core_true and will send to Q to update gui'
        
        self.test_send_nomal = {'status':  'nomal'  , 'good': self.test_g ,'text' : 'update compleate'  , 'v' : [   ]}
        self.test_send_error_nogood = {'status':  'error_nogood'  , 'good':self.test_g ,'text' : 'update compleate'  , 'v' : [   ]}
        self.test_send_error_port = {'status':  'nomal'  , 'good':self.test_g ,'text' : 'update compleate'  , 'v' : [   ]}        
        self.test_send_error_notfound ={'status':  'error_notfound'  , 'good':self.test_g ,'text' : 'update compleate'  , 'v' : [   ]} 
        self.test_send_error_cnum = {'status':  'error_cnum'  , 'good':self.test_g ,'text' : 'update compleate'  , 'v' : [   ]}        
        self.test_send_warning = {'status':  'warnning'  , 'good':self.test_g ,'text' : 'update compleate'  , 'v' : [   ]}
        self.test_send_check = {'status':  'check'  , 'good':self.test_g ,'text' : 'update compleate'  , 'v' : [   ]}        
        signal = random.choice([self.test_send_check,self.test_send_error_cnum,self.test_send_error_nogood,self.test_send_error_notfound,self.test_send_error_port,self.test_send_nomal,self.test_send_warning])
        self.q.put(signal)
        


    
    def opendriver(self):
        self.driver = webdriver.Ie() # set defult zoom to 100 manual #and then go to export by manual..... at first tab
        return self.driver

    ########################################################
    #    other function  it will use in class  #
    def ck_checked(self,driver):
        el = ele() ## set var from anather class ... it use in def..
        
        """ check status of Checked or Loaded"""
        for i in el.req(driver):
            if "checked" in str(i.text).lower() or "loaded" in str(i.text).lower():
                return True
        return False
      
   


    def ck_port(self,driver,p):
        el = ele() ## set var from anather class ... it use in def..
        
        pdata = el.port(driver).get_attribute('value')
        if str(p) == str(pdata) :
                return True , str(pdata)
        else:
                return False , str(pdata)
    
    
    def ck_cont(self,driver,n):
        el = ele() ## set var from anather class ... it use in def..
        
        cont = el.contnum(driver).get_attribute('value')
       # print cont,n
        if str(n).lower() == str(cont).lower():
                return True , str(cont)
        else:
                return False , str(cont)
                    
    
    def date_c(self,d,t):
        #el = ele() ## set var from anather class ... it use in def..
        
        eir_datetime = datetime.strptime(str(d)+' '+str(t),'%d/%m/%Y %H:%M:%S')
        upto = timedelta(seconds = random.randrange(300,421)) # random time delay
        usetime = upto + eir_datetime
        return usetime
            
    
    def csv_2_dict(self,f): # file name in same folder
        #el = ele() ## set var from anather class ... it use in def..
        
        csv_file = csv.DictReader(open(f, 'rb'), delimiter=',', quotechar='"')
        result = {}
        for i in csv_file:
                result[i['good']] = {'container':i['container'],'size':i['size'],'date':i['date'],'time':i['time'],'ter':i['ter']}
        return result
    
    def ch_weight(self,z):
        if z == '20':
                return '20000'
        else:
                return '30000'
           
    
    
    def popup(self,driver): #popup and event handel like goos not found
        el = ele() ## set var from anather class ... it use in def..
        
        try:
            weight_t = el.weight(driver)
            weight_test = weight_t.get_attribute("value")
            if weight_test == "0.000" and self.ck_checked(driver):
                return "checked"
        except:
            pass
        try:
            weight_t = el.weight(driver)
            weight_test = weight_t.get_attribute("value")
            if weight_test == "0.000":
                return None
        except:
            pass
        try:
            if self.ck_checked(driver) is True:
                return "checked"
        except:
            pass
        try:
            if el.notf(driver) is True:
                return "good transition not found!"
        except:
            pass
        
        try:
            alert = driver.switch_to_alert()
            txt = str(alert.text)
            return txt
            alert.accept()

        except:
            return None
            
    def pop_out(self,driver):
        try:
            exi = driver.find_element_by_xpath("//*[contains(text(), 'Already Exist')]")
            return exi.text
        except:
            pass

 ########################################################################   
    
    
    
    # edit hear !!!!!!!!!!!
    # funtion how to run in step 
    def doit1(self,driver,g,z,p,cn,d,t): 
        el = ele() ## set var from anather class ... it use in def..        
        

        # Auto
        """g = goods transition Number. , z = size, p = Port
        cn = Container Number , d = Date , t = Time  """


        el.clr(driver).click() #clear screen
        el.gnum(driver).send_keys(g) #input goods transition no... 5806a....
        el.inq(driver).click() #click inquery button
        
        pop = self.popup(driver)
        if pop == None: # Run nomal
            el.weight(driver).clear()
            el.weight(driver).send_keys(self.ch_weight(z)) # input weight
            
            #date and time
            usetime = self.date_c(d,t)
            el.date(driver).clear() #clear box and key
            el.date(driver).send_keys(usetime.strftime('%d-%m-%Y')) 
            el.time(driver).clear() #clear box and key
            el.time(driver).send_keys(usetime.strftime('%H:%M:%S'))
            
            
            ck_p = self.ck_port(driver,p) #check port
            if ck_p[0] is False:
                if ck_p[1] != '0251':
                                    
                    # Re turn to Q for thead and send recive data
                    signal = {'status':  'error_port','good':g,'text' :'can not change port from : ' , 'v' : [ck_p[1]] }
                    self.q.put(signal)
                    ##
                    
                     #logging.info("Port can not change from %s to %s goods : %s"%(ck_p[1],p,g))
                    return 'Can not change Port.....' #end
                    
                else:
                    el.port(driver).clear() # clear port in put
                    el.port(driver).send_keys(p) # change port
    
    
            container = self.ck_cont(driver,cn) #check container number
            if container[0] is False:
                   
                # Re turn to Q for thead and send recive data
                signal = {'status':  'error_cnum' ,'good':g, 'text' : 'container number not match'  , 'v' :[ g ]}
                self.q.put(signal)
                ##
            
                #logging.info("Container does not match goods : %s %s insystem ---> %s"%(g,cn,container[1]))
                #print "Container number is not match\t",g #confirm and continue or end
                return "Container number is not match\t",g #confirm and continue or end

            time.sleep(0.5)
            
            #update
            el.upd(driver).click()
            
            try:
                alert = driver.switch_to_alert()
                #txt = str(alert.text)
                alert.accept()
                upd_comp = driver.find_element_by_xpath("//*[contains(text(), 'Update Complete')]")
                #print "%s %s"%(g,upd_comp.text)
                
                
                # Re turn to Q for thead and send recive data
                signal = {'status':  'nomal'  , 'good':g ,'text' : 'update compleate'  , 'v' : [   ]}
                self.q.put(signal)
                ##

                return "%s %s"%(g,upd_comp.text)
                
                
                # For x-ray popup  ..!! it must fix
                    
                try:
                    alert = driver.switch_to_alert()
                    alert.accept()
                    #logging.info("%s  -- X-ray"%(g))
                except:
                    pass
            except:
                    
                popout = self.pop_out(driver)
                if popout == None:
                    pass
                else:
                    #logging.info("%s --> %s"%(g,popout))
                    #print popout
                    # Re turn to Q for thead and send recive data
                    signal = {'status': 'warnning','good':g,'text': 'good transition exit' , 'v' : [ popout  ]}
                    self.q.put(signal)
                    
                    ##
                
                    return popout
                        
            #Try for xray
            try:
                alert = driver.switch_to_alert()
                alert.accept()
                #logging.info("%s  -- X-ray"%(g))
    
            except:
                pass
            
        elif "found" in pop: #'good transition not found!'
            # Re turn to Q for thead and send recive data
            signal = {'status': 'error_notfound'   , 'good':g, 'text' : 'good transition not found' , 'v' : [ g ]}
            self.q.put(signal)
             #
            return pop
        
        elif "Must Be Enter" in pop:
            # Re turn to Q for thead and send recive data
            signal = {'status': 'error_nogood'   , 'good':g,  'text' : 'good transition must be enter'  , 'v' : [ g ]}
            self.q.put(signal)
             ##
            return pop
        
        elif "checked" in pop:
            # Re turn to Q for thead and send recive data
            signal = {'status':  'check'  ,'good':g, 'text' : 'good transition is' , 'v' : [ g , pop  ]}
            self.q.put(signal)
             ##
            return pop


    
    
    
    
    
    ## funtion to run
    def run(self,driver): # funtion automatic This run from itself CMD.
        

        
        counter = 1
        
        print os.getcwd()
        file_name = raw_input("please input file name! ")     
        data = self.csv_2_dict(file_name)
        for i in data:
            g = i
            z = data[i]['size']
            p = data[i]['ter']
            cn = data[i]['container']
            d = data[i]['date']
            t = data[i]['time']
            
            print "%s . #\t%s\t%s\t%s\t%s\t%s\t%s"%(counter,g,z,p,cn,d,t)
            print self.doit1(driver,g,z,p,cn,d,t)
          
            
            # for out put to gui set it to guiprogram



            counter += 1
    
#test
    
    
class elee:
    def __init__(self):
        print 'This is Class of element . test'
    def se(self,driver):
        """ serch google """
        return driver.find_element_by_name("q")    
    
    
class ele:
    def __init__(self):
        #print 'This is Class of element . it must be use element funtion manual   .send_keys(....) or anather'
        pass
    
    def gnum(self,driver):
        """ goods control No. 5806a.... """
        return driver.find_element_by_name("gdsCtrNum")
    def weight(self,driver):
        """ weight kgm."""
        return driver.find_element_by_name("wgtGrt")
    def port(self,driver):
        """ port """
        return driver.find_element_by_name("potRea")
    def contnum(self,driver):
        """ container Number """
        return driver.find_element_by_name("ctrNum")
    def date(self,driver):
        """ date """
        return driver.find_element_by_name("dteChk")
    def time(self,driver):
        """ time """
        return driver.find_element_by_name("tmeChk")
    
    #button
    def conse(self,driver):
        """Container Search"""
        return driver.find_element_by_name("Container Search")
    def inq(self,driver):
        """ Button inquiry """
        return driver.find_element_by_name("INQ")
    def upd(self,driver):
        """ Button Update """
        return driver.find_element_by_name("UPD")
    def clr(self,driver):
        """  Button Clear """
        return driver.find_element_by_name("CLR")
        
    #element check
    def req(self,driver):
        """ get all elements ... it find for Checked """
        return driver.find_elements_by_class_name('Required') # get all elements ... it find element.text for 'Checked'
    def notf(self,driver):
        """ find good transection notfound.. if true return True"""
        try:
            #notf = driver.find_element_by_xpath("//*[contains(text(), 'EXP-0544')]")
            return True
        except:
            return False




class main_run:
    def __init__(self):
        self.run = core_true(my_q)
        self.web = self.run.opendriver()
        raw_input("please go to manualpage and press enter to continue")       
        self.web.switch_to_frame("frameset")
        
        counter = 1
            
        print os.getcwd()
        file_name = raw_input("please input file name! ")     
        data = self.run.csv_2_dict(file_name)
        for i in data:
            g = i
            z = data[i]['size']
            p = data[i]['ter']
            cn = data[i]['container']
            d = data[i]['date']
            t = data[i]['time']
            
            print "%s . #\t%s\t%s\t%s\t%s\t%s\t%s"%(counter,g,z,p,cn,d,t)
            print self.run.doit1(self.web,g,z,p,cn,d,t)
            counter += 1
###

            
            # for out put to gui set it to guiprogram



            


if __name__ == "__main__":
    main_run()


