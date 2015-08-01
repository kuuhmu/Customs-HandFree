from selenium import webdriver
import time
from datetime import datetime , timedelta
import random
import csv
import re
import os
import logging
from pymouse import PyMouse

mouse = PyMouse()
log = 'log.log'
logging.basicConfig(filename = log,level=logging.INFO)

driver = webdriver.Ie() # set defult zoom to 100 manual
driver.implicitly_wait(10)
driver.get("http://portal.customs.net") #and then go to export by manual..... at first tab


raw_input('Enter to continue win 1')
print "OK"

driver.switch_to_frame("frameset")


# Note .. when page refresh it will find_element again !!

class ele: #sloved
        def __init__(self):
                print 'This is Class of element . it must be use element funtion manual   .send_keys(....) or anather'
        def gnum(self):
                """ goods control No. 5806a.... """
                return driver.find_element_by_name("gdsCtrNum")
        def weight(self):
                """ weight kgm."""
                return driver.find_element_by_name("wgtGrt")
        def port(self):
                """ port """
                return driver.find_element_by_name("potRea")
        def contnum(self):
                """ container Number """
                return driver.find_element_by_name("ctrNum")
        def date(self):
                """ date """
                return driver.find_element_by_name("dteChk")
        def time(self):
                """ time """
                return driver.find_element_by_name("tmeChk")
        
        #button
        def conse(self):
                """Container Search"""
                return driver.find_element_by_name("Container Search")
        def inq(self):
                """ Button inquiry """
                return driver.find_element_by_name("INQ")
        def upd(self):
                """ Button Update """
                return driver.find_element_by_name("UPD")
        def clr(self):
                """  Button Clear """
                return driver.find_element_by_name("CLR")
        
        #element check
        def req(self):
                """ get all elements ... it find for Checked """
                return driver.find_elements_by_class_name('Required') # get all elements ... it find element.text for 'Checked'
        def notf(self):
                """ find good transection notfound.. if true return True"""
                try:
                        notf = driver.find_element_by_xpath("//*[contains(text(), 'EXP-0544')]")
                        return True
                except:
                        return False

el = ele()


# driver.switch_to_alert().accept() is can use of alert when finish update or anather
#test


def ck_checked():
        """ check status of Checked or Loaded"""
        for i in el.req():
                if "checked" in str(i.text).lower() or "loaded" in str(i.text).lower():
                        return True
        return False
      
   


def ck_port(p):
        pdata = el.port().get_attribute('value')
        if str(p) == str(pdata) :
                return True , str(pdata)
        else:
                return False , str(pdata)


def ck_cont(n):
        cont = el.contnum().get_attribute('value')
       # print cont,n
        if str(n).lower() == str(cont).lower():
                return True , str(cont)
        else:
                return False , str(cont)
                

def date_c(d,t):
        eir_datetime = datetime.strptime(str(d)+' '+str(t),'%d/%m/%Y %H:%M:%S')
        upto = timedelta(seconds = random.randrange(300,421)) # random time delay
        usetime = upto + eir_datetime
        return usetime
        

def csv_2_dict(f): # file name in same folder
        csv_file = csv.DictReader(open(f, 'rb'), delimiter=',', quotechar='"')
        result = {}
        for i in csv_file:
                result[i['good']] = {'container':i['container'],'size':i['size'],'date':i['date'],'time':i['time'],'ter':i['ter']}
        return result

def ch_weight(z):
        if z == '20':
                return '20000'
        else:
                return '30000'
       


def popup(): #popup and event handel like goos not found
        try:
                weight_t = el.weight()
                weight_test = weight_t.get_attribute("value")
                if weight_test == "0.000" and ck_checked():
                        return "checked"
        except:
                pass
        try:
                weight_t = el.weight()
                weight_test = weight_t.get_attribute("value")
                if weight_test == "0.000":
                        return None
        except:
                pass
        try:
                if ck_checked() is True:
                        return "checked"
        except:
                pass
        try:
                if el.notf() is True:
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
        
def pop_out():
        try:
                exi = driver.find_element_by_xpath("//*[contains(text(), 'Already Exist')]")
                return exi.text
        except:
                pass



def doit1(g,z,p,cn,d,t):        # deverlop
        """g = goods transition Number. , z = size, p = Port
        cn = Container Number , d = Date , t = Time  """
        

#        try:
        el.clr().click() #clear screen
        el.gnum().send_keys(g) #input goods transition no... 5806a....
        el.inq().click() #click inquery button
        
        pop = popup()
        if pop == None: # Run nomal
                el.weight().clear()
                el.weight().send_keys(ch_weight(z)) # input weight
                
                #date and time
                usetime = date_c(d,t)
                el.date().clear() #clear box and key
                el.date().send_keys(usetime.strftime('%d-%m-%Y')) 
                el.time().clear() #clear box and key
                el.time().send_keys(usetime.strftime('%H:%M:%S'))
                
                
                ck_p = ck_port(p) #check port
                if ck_p[0] is False:
                        if ck_p[1] != '0251':
                                logging.info("Port can not change from %s to %s goods : %s"%(ck_p[1],p,g))
                                return 'Can not change Port.....' #end
                        else:
                                el.port().clear() # clear port in put
                                el.port().send_keys(p) # change port
        
        
                container = ck_cont(cn) #check container number
                if container[0] is False:
                        logging.info("Container does not match goods : %s %s insystem ---> %s"%(g,cn,container[1]))
                        print "Container number is not match\t",g #confirm and continue or end
                

                time.sleep(0.5)
                
                #update
                el.upd().click()
                try:
                        alert = driver.switch_to_alert()
                        txt = str(alert.text)
                        alert.accept()
                        upd_comp = driver.find_element_by_xpath("//*[contains(text(), 'Update Complete')]")
                        print "%s %s"%(g,upd_comp.text)
                        
                        # For x-ray popup  ..!! it must fix
                        
                        try:
                                alert = driver.switch_to_alert()
                                alert.accept()
                                logging.info("%s  -- X-ray"%(g))
                        except:
                                pass
                except:
                        
                        popout = pop_out()
                        if popout == None:
                                pass
                        else:
                                logging.info("%s --> %s"%(g,popout))
                                
                #Try for xray
                try:
                        alert = driver.switch_to_alert()
                        alert.accept()
                        logging.info("%s  -- X-ray"%(g))
        
                except:
                        pass
                
        elif "found" in pop: #'good transition not found!'
                return pop
        elif "Must Be Enter" in pop:
                return pop
        elif "checked" in pop:
                return pop
        
        
def run():       
        counter = 1
        
        print os.getcwd()
        file_name = raw_input("please input file name! ")     
        data = csv_2_dict(file_name)
        for i in data:
                g = i
                z = data[i]['size']
                p = data[i]['ter']
                cn = data[i]['container']
                d = data[i]['date']
                t = data[i]['time']
                print "%s . #\t%s\t%s\t%s\t%s\t%s\t%s"%(counter,g,z,p,cn,d,t)
                print doit1(g,z,p,cn,d,t)
                counter += 1
                
                
        # error when alert box popup
        # error when good transition not found
        # error when not enter  alert box



#run()




# ------------------------------------------------------------- #




driver1 = webdriver.Ie() # set defult zoom to 100 manual
driver1.implicitly_wait(10)
driver1.get("http://portal.customs.net") #and then go to export by manual..... at first tab

# ark for date ..... manual
#s_date_from = raw_input("please input search date from (01/01/2558) --> 01012558 :")
#s_date_to = raw_input("please input search date to (01/02/2558) --> 01022558 :")

raw_input('Enter to continue win 2')
print "OK"

driver1.switch_to_frame("frameset")





#date_between = driver1.find_elements_by_id("stpDteXmt3")
#date_between[0].send_keys(s_date_from)
#date_between[0].send_keys(s_date_to)

def get_tran(container):
        """ return goodstransition num"""
        
        
        
        ctrn = driver1.find_element_by_name("ctrNum")
        ctrn.clear()
        ctrn.send_keys(container)
        srh = driver1.find_element_by_name("SRH")
        srh.click()
        
        try:
                gts = re.search("License\n(.+?)\n",driver1.find_element_by_xpath("//*[contains(text(), digit)]").text).group(1)


        except:
                get_tran(raw_input("container number : "))
                
        gts = re.search("License\n(.+?)\n",driver1.find_element_by_xpath("//*[contains(text(), digit)]").text).group(1)
        #print gts
        return gts



digit = raw_input("please insert 3 digit of P.S. : 2558 insert : 580 : ")

print "in sert between search date manualy : wait 30 sec"
raw_input('Enter to continue Date and Time')


eir_date = raw_input("Eir date : ") # one time

while True:
        mouse.click(1247,323,1)
        container = raw_input(" please inseart container number.")
        if "change" in container:
                mouse.click(1247,323,1)
                eir_date = raw_input("Eir date : ")
        elif "exit" in container:
                break
        else:
                el = ele()
                el.gnum().send_keys(get_tran(container))
                el.inq().click()
                ck = ck_checked()
                if ck is True:
                        el.clr().click()
                        print 'checked or loaded.'
                else:
                        mouse.click(1247,323,1)
                        while True:
                                wei = input("weight : ")
                                if wei > 35000 or wei < 1000:
                                        pass
                                else: 
                                        break
                        

                        
                        el.weight().send_keys(wei)
                        tim = raw_input("Time 015959 : ")
                        el.port().clear()
                        el.port().send_keys("0252")
                        el.date().clear()
                        el.date().send_keys(eir_date)
                        el.time().clear()
                        el.time().send_keys(tim)
                        el.upd().click()
                        try:
                                alert = driver.switch_to_alert()
                                if 'Not' in str(alert.text):
                                        alert.accept()
                                else:
                                        print 'Ploblem'
                        except:
                                print "no alert"
