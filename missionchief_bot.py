from splinter import Browser
from configparser import ConfigParser
import time
import platform
import random
import os
operatingsystem = platform.system()
hrefs= []
path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()

# Get config values
config.read('config.ini')
baseurl = config.get('Settings', 'URL')
username = config.get('Settings', 'Username')
password = config.get('Settings', 'Password')
Min_Sleeptime = config.getint('Settings', 'Min_Sleeptime')
Max_Sleeptime = config.getint('Settings', 'Max_Sleeptime')

class MissonChiefBot:
 def init(self):
    logged_in = login(username,password)
    if logged_in:
     while True:
      hrefs.clear()
      getMissions()
      timer = random.randint(Min_Sleeptime,Max_Sleeptime)
      print('Sleeping for',timer,'seconds...')
      time.sleep(timer)
    else:
     print("Couldn't log in...")
def login(username,password):
    print("Logging in")
    # Visit URL
    url = baseurl+"/users/sign_in"
    browser.visit(url)
    # Filling in login information
    browser.fill("user[email]",username)
    browser.fill("user[password]",password)
    # Submitting login
    browser.find_by_name('commit').click()
    try :
     # check we are logged in- by grabbing a random tag only visible on log in.
     alliance = browser.find_by_id('alliance_li')
     print("Logged in")
     if alliance['class']=="dropdown":
      return True
     else:
      return False
    except Exception:
     return False

def getMissions():
    print("Getting missions")
    url = baseurl
    browser.visit(url)
    # Finding links for missions
    try:
        links = browser.find_link_by_partial_href('/missions/')
        print(str(len(links)) + " missons found")
        for link in links:
         hrefs.append(link['href'])
        doMissions()
        return True;
    except:
        time.sleep(1)

def doMissions():
 count = 0
 for href in hrefs:
  time.sleep(5)
  count+=1
  mission_str = str(count)
  try:
   print("MISSION " + mission_str +":" + " VISITING MISSION")
   browser.visit(href)
  except:
   print("MISSION " + mission_str +":" + " COULDN'T GET LINK")
  try:
   print("MISSION " + mission_str +":" + " SELECTING UNIT TO DESPATCH")
   checkbox=browser.find_by_css('input[class="vehicle_checkbox"]')
   for check in checkbox:
    check.check()
  except:
   print("MISSION " + mission_str +":" + " NO UNITS TO DESPATCH")
  try:
   browser.find_by_name('commit').click()
   print("MISSION " + mission_str +":" + " ATTEMPTED TO DESPATCH.")
  except:
   print("MISSION " + mission_str +":" + "CAN NOT DESPATCH A UNIT, OR UNIT ALREADY DESPATCHED")

# Setting up browser
if operatingsystem == "Windows":
 executable_path = {'executable_path': path +'/chromedriver.exe'}
elif operatingsystem == "Linux":
  executable_path = {'executable_path': path +'/linux/chromedriver'}

elif operatingsystem == "Darwin":
  executable_path = {'executable_path': path+'/mac/chromedriver'}

browser = Browser('chrome', **executable_path)

def begin():
 MissonChiefBot().init()

if __name__ == '__main__':
 begin()
