import json
import os
import random
import re
import sys
import time
import urllib
from datetime import datetime
import pydub
import requests
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

web=webdriver.Chrome() #opens chome 
web.get('https://safebrowsing.google.com/safebrowsing/report_phish/') #fetches this url

time.sleep(2) # for page to completely render 

phish_url="http://facebook[dot]com.accounts.login.userid.504393.hoob2.pw/win/fbm/" # key to be filled
phish=web.find_element(By.XPATH,"//*[@id='url']")
phish.send_keys(phish_url) # sends the key in the given xpath

time.sleep(3)
frames = web.find_elements(By.TAG_NAME,"iframe")
recaptcha_control_frame = None
recaptcha_challenge_frame = None
for index, frame in enumerate(frames): # enumerate stores index and frame or elements
    if re.search('reCAPTCHA', frame.get_attribute("title")):
        recaptcha_control_frame = frame
                    
    if re.search('recaptcha challenge', frame.get_attribute("title")):
        recaptcha_challenge_frame = frame
 # captured two frames

frames = web.find_elements(By.TAG_NAME,"iframe")
web.switch_to.frame(recaptcha_control_frame)
web.find_element(By.CLASS_NAME,"recaptcha-checkbox-border").click() # recaptcha checkbox is clicked 

web.switch_to.default_content()
frames = web.find_elements(By.TAG_NAME,"iframe")
web.switch_to.frame(recaptcha_challenge_frame) #frame switched to challenge frame

time.sleep(10)
web.find_element(By.ID,"recaptcha-audio-button").click() #click audio button

web.switch_to.default_content()
frames = web.find_elements(By.TAG_NAME,"iframe")
web.switch_to.frame(recaptcha_challenge_frame)


WebDriverWait(web, 10).until(EC.presence_of_element_located((By.ID, "audio-source")))
src = web.find_element(By.ID,'audio-source').get_attribute('src')
path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav")) #gets audio in mp3 

urllib.request.urlretrieve(src, path_to_mp3)

sound = pydub.AudioSegment.from_mp3(path_to_mp3)
sound.export(path_to_wav, format="wav")
sample_audio = sr.AudioFile(path_to_wav) # audio converted to wav

r = sr.Recognizer() #speech_recognition object is created
with sample_audio as source:
    audio = r.record(source)
key = r.recognize_google(audio) # google recognises speech cstores in key

web.find_element(By.ID,"audio-response").send_keys(key.lower()) #fills audio response as text in input
web.find_element(By.ID,"audio-response").send_keys(Keys.ENTER)
time.sleep(5)
web.switch_to.default_content()
time.sleep(5)
web.find_element(By.ID,"recaptcha-demo-submit").click() #submits recaptcha 

time.sleep(3)

web.find_element(By.XPATH,"//*[@id='formprincipal']/div[4]/input").click() #submit button is clicked

time.sleep(5)
