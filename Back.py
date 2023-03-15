
from selenium import webdriver

from time import *

from re import *

from PIL import Image

from pytesseract import pytesseract

import random

import os

import schedule

import threading

todayCodes = []

PROXY = '37.32.12.86:17280'

chDrURL = '/Users/MeT/Code/Telegram Bot/Beheshti Self/chromedriver'

pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.3.0_1/bin/tesseract'

class Code:
    
    def __init__(self,num,seller,buyer,meal,room,food,completed,checked,used):
        
        self.num = num
        
        self.seller = seller
        
        self.buyer = buyer
        
        self.meal = meal # ناهار شام
        
        self.room = room # MKL
        
        self.food = food # Persian from Dining
        
        self.completed = completed # True False
        
        self.checked = checked
        
        self.used = used
        
    def checkCode(self):
        
        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_argument(f'--proxy-server={PROXY}')
        
        driver = webdriver.Chrome(chDrURL , chrome_options=chrome_options)
        
        driver.get('https://dining.sbu.ac.ir/index.rose')
        
        driver.find_element('id' , 'username').send_keys(self.seller.studentId)
        
        driver.find_element('id' , 'password').send_keys(self.seller.idNumber)
        
        driver.find_element('id' , 'login_btn_submit').click()
        
        sleep(1)
        
        if len(driver.find_elements('xpath' , '//*[@id="login"]/div[3]/div[1]/div')) > 0:
            
            driver.close()
            
            return False
        
        driver.get('https://dining.sbu.ac.ir/student/forgetCard/getCode/list.rose')
        
        sleep(1)
        
        reserves = driver.find_elements('xpath' , '//*[@id="reserve"]/tbody/tr')
        
        for i in range(1,len(reserves)+1):
            
            if driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[6]').text == self.meal:
                
                if driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[12]/input').is_selected() == True:
                    
                    return False
                
                else:
                    
                    self.checked = True
                    
                    return True
        
class Seller:
    
    def __init__(self,code,studentId,idNumber,meal,checked,payedTo,chatId):
        
        self.code = code
        
        self.studentId = studentId
        
        self.idNumber = idNumber
        
        self.checked = checked
        
        self.payedTo = payedTo
        
        self.chatId = chatId
        
        self.meal = meal
        
    def findCode(self):
        
        chrome_options = webdriver.ChromeOptions()
        
        chrome_options.add_argument(f'--proxy-server={PROXY}')
        
        driver = webdriver.Chrome(chDrURL,chrome_options=chrome_options)
        
        driver.get('https://dining.sbu.ac.ir/index.rose')
        
        driver.find_element('id' , 'username').send_keys(self.studentId)
        
        driver.find_element('id' , 'password').send_keys(self.idNumber)
        
        driver.find_element('id' , 'login_btn_submit').click()
        
        sleep(1)
        
        if len(driver.find_elements('xpath' , '//*[@id="login"]/div[3]/div[1]/div')) > 0:
            
            driver.close()
            
            return False
        
        driver.get('https://dining.sbu.ac.ir/student/forgetCard/getCode/list.rose')
        
        sleep(1)
        
        reserves = driver.find_elements('xpath' , '//*[@id="reserve"]/tbody/tr')
        
        for i in range(1,len(reserves)+1):
            
            if driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[6]').text == self.meal:
            
                if driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[12]/input').is_selected() == False:
            
                    room = driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[5]').text
    
                    if room == '33-شهید بهشتی-رستوران مکمل دانشجویی':
                    
                        room = 'MKL'
    
                    elif room == '01-شهید بهشتی-سلف مرکزی برادران':
                    
                        room = 'BMB'
    
                    elif room == '03-شهید بهشتی : خوابگاه کوی پسران':
                    
                        room = 'BDB'
    
                    elif room == '05-شهید عباسپور : سلف دانشجویی پسران':
                    
                        room = 'AMB'
    
                    elif room == '08-شهید عباسپور : خوابگاه کوی پسران':
                    
                        room = 'ADB'
    
                    elif room == '02-شهید بهشتی-سلف مرکزی خواهران':
                    
                        room = 'BMG'
    
                    elif room == '04-شهید بهشتی : خوابگاه کوی دختران':
                    
                        room = 'BDG'
    
                    elif room == '06-شهید عباسپور : سلف دانشجویی دختران':
                    
                        room = 'AMG'
    
                    elif room == '09-شهید عباسپور : خوابگاه کوی دختران':
                    
                        room = 'ADG'
    
                    completed = driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[7]').text
    
                    if completed.find('نیم پرس'):
                    
                        completed = False
    
                    else:
                    
                        completed = True
    
                    food = driver.find_element('xpath' , f'//*[@id="reserve"]/tbody/tr[{i}]/td[8]').text
    
                    driver.find_element('xpath' , f'//*[@id="print-{i}"]').click()
    
                    sleep(1)
    
                    codeText = driver.find_element('xpath' , '//*[@id="printResult"]/tr[1]/td').text
    
                    driver.close()
    
                    num = int(findall('[0-9]+' , codeText)[0])
    
                    for c in todayCodes:
                    
                        if c.num == num:
                        
                            return False
    
                    code = Code(num=num, seller=self, buyer=None, meal=self.meal, room=room, food=food, completed=completed, checked=False, used=False)
    
                    self.code = code
    
                    self.checked = True
    
                    todayCodes.append(code)
    
                    return True
            
        driver.close()
        
        return False
    
    def payment(self):
        
        cost = 0
        
        if self.code.room == 'MKL':
            
            cost = 60000
            
        elif self.code.completed == False:
            
            cost = 30000
            
        else:
            
            cost = 60000
        
        chrome_options = webdriver.ChromeOptions()
    
        chrome_options.add_argument(f'--proxy-server={PROXY}')
        
        driver = webdriver.Chrome(chDrURL , chrome_options=chrome_options)
    
        driver.get('https://dining.sbu.ac.ir/index.rose')
    
        driver.find_element('id' , 'username').send_keys(400243043)
    
        driver.find_element('id' , 'password').send_keys(4610913976)
    
        driver.find_element('id' , 'login_btn_submit').click()
    
        sleep(1)
        
        driver.get('https://dining.sbu.ac.ir/nurture/user/credit/inputTransferCreditInfo.rose')
        
        sleep(1)
        
        driver.find_element('id' , 'studentNumberInput').send_keys(self.studentId)
        
        driver.find_element('id' , 'transferAmount').send_keys(cost)
    
        c = driver.find_element('id' , 'captcha_img')
    
        imgName = random.randrange(1,1001)
    
        imgName = str(imgName)
    
        c.screenshot(f'{imgName}.png')
    
        sleep(1)
    
        img = Image.open(f'{imgName}.png')
        
        captcha = pytesseract.image_to_string(img)
    
        driver.find_element('id' , 'captcha_input').send_keys(captcha)
    
        sleep(2)
    
        driver.find_element('xpath' , '/html/body/div[2]/div[4]/div[1]/div/div/div[2]/form/table/tbody/tr/td[1]/input').click()
    
        sleep(1)
        
        driver.close()
        
        os.remove(f'{imgName}.png')
        
        self.payedTo = True
        
    def clearList():
        
        todayCodes.clear()
        
class Buyer:
    
    def __init__(self , code , studentId , idNumber , meal , room , isPayed , chatId):
        
        self.code = code
        
        self.studentId = studentId
        
        self.idNumber = idNumber
        
        self.isPayed = isPayed
        
        self.chatId = chatId
        
        self.room = room
        
        self.meal = meal
        
    def findCodesList(self):
        
        codes = []
        
        for code in todayCodes:
            
            if code.room == self.room:
                
                if code.meal == self.meal:
                    
                    if len(codes) < 1:
                        
                        codes.append(code)
                    
                    for idx in range(len(codes)):
                        
                        if code.food == codes[idx].food and code.completed == codes[idx].completed:
                            
                            break
                        
                        elif idx == len(codes) - 1:
                            
                            codes.append(code)
                            
        return codes
    
    def findCode(self,food,completed):
        
        for index in range(len(todayCodes)):
            
            if todayCodes[index].meal == self.meal and todayCodes[index].room == self.room:
                
                if todayCodes[index].food == food and todayCodes[index].completed == self.completed:
                    
                    if todayCodes[index].used == False:
                        
                        if Code.checkCode(todayCodes[index]):
                        
                            todayCodes[index].buyer = self
                        
                            todayCodes[index].used = True
                        
                            self.code = todayCodes[index]
                        
                            return True
                        
                        else:
                            
                            del todayCodes[index].seller
                            
                            del todayCodes[index]
                            
                            Buyer.findCode(self, food, completed)
                    
        return False
    
    def payment(self):
        
        cost = 0
        
        if self.room == 'MKL':
            
            cost = 80000
            
        elif self.code.completed == False:
            
            cost = 30000
            
        else:
            
            cost = 60000
            
        chrome_options = webdriver.ChromeOptions()
    
        chrome_options.add_argument(f'--proxy-server={PROXY}')
        
        driver = webdriver.Chrome(chDrURL , chrome_options=chrome_options)
    
        driver.get('https://dining.sbu.ac.ir/index.rose')
    
        driver.find_element('id' , 'username').send_keys(self.studentId)
    
        driver.find_element('id' , 'password').send_keys(self.idNumber)
    
        driver.find_element('id' , 'login_btn_submit').click()
    
        sleep(1)
    
        if len(driver.find_elements('xpath' , '//*[@id="login"]/div[3]/div[1]/div')) > 0:
            
            driver.close()
            
            self.code.used = False
            
            self.code.buyer = None
            
            del self
        
            return False
    
        driver.get('https://dining.sbu.ac.ir/nurture/user/credit/inputTransferCreditInfo.rose')
    
        sleep(1)
        
        priceText = driver.find_element('xpath' , '/html/body/div[2]/div[4]/div[1]/div/div/div[1]/div/div').text
        
        priceText = priceText.partition('\n')[0]
        
        price = findall('[0-9]+', priceText)[0]
        
        price = int(price)
        
        if price < cost:
            
            driver.close()
            
            self.code.used = False
            
            self.code.buyer = None
            
            del self
            
            return False
        
        driver.find_element('id' , 'studentNumberInput').send_keys(400243043)
        
        driver.find_element('id' , 'transferAmount').send_keys(cost)
        
        c = driver.find_element('id' , 'captcha_img')
        
        imgName = random.randrange(1,1001)
        
        imgName = str(imgName)
        
        c.screenshot(f'{imgName}.png')
        
        sleep(1)
        
        img = Image.open(f'{imgName}.png')
        
        captcha = pytesseract.image_to_string(img)
        
        driver.find_element('id' , 'captcha_input').send_keys(captcha)
        
        sleep(2)
        
        driver.find_element('xpath' , '/html/body/div[2]/div[4]/div[1]/div/div/div[2]/form/table/tbody/tr/td[1]/input').click()
        
        sleep(1)
            
        driver.close()
            
        os.remove(f'{imgName}.png')
        
        self.isPayed = True
        
        return True
    