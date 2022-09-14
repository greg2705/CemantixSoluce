from flask import Flask, flash, request,render_template
import webbrowser
from threading import Timer
import os
from gensim.models import KeyedVectors
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
import random
import numpy as np
import warnings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
warnings.filterwarnings("ignore")



def initialisation_driver():
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver= webdriver.Chrome(executable_path="ChromeDriver/chromedriver",options=options)
    driver.get("https://cemantix.herokuapp.com/") 
    element=driver.find_element(By.ID,"dialog-close")
    element.click()
    return driver

def send_word(driver,mot):
    
    element = driver.find_element(By.ID,"cemantix-guess")
    element.send_keys(mot)
    element = driver.find_element(By.ID,"cemantix-guess-btn")
    element.click()
    
    if(driver.find_element(By.ID,"cemantix-error").text !=""):
        return -1000
    
    time.sleep(0.2)
    a=driver.find_element(By.ID,"cemantix-guesses")
    b=a.find_elements(By.TAG_NAME,"tr")[0]
    c=b.find_elements(By.TAG_NAME,"td")[2]
    
    if(c.text==''):
        time.sleep(1)
        a=driver.find_element(By.ID,"cemantix-guesses")
        b=a.find_elements(By.TAG_NAME,"tr")[0]
        c=b.find_elements(By.TAG_NAME,"td")[2]
    
    res=float(c.text.replace(",","."))
    if(res==100.0):
        global WORD_to_FIND
        WORD_to_FIND=mot
        return 100.0
    return res

def best_start(model,driver):
    max_score=[send_word(driver,"faire")]
    max_mot=["faire"]
    for i in range(50):
        rd=random.randint(1,100000)
        max_score.append(send_word(driver,model.index_to_key[rd]))
        max_mot.append(model.index_to_key[rd])
    return max_mot[np.argmax(max_score)]

def res():
    
    model=KeyedVectors.load_word2vec_format("ModeleDoc2Vec/modeleCemantix.bin", binary=True, unicode_errors="ignore")
    global WORD_to_FIND
    dico_word={}
    lst_mot=[]
    driver=initialisation_driver()
    
    mot=best_start(model,driver)
    dico_word[mot]=send_word(driver,mot)
    lst_mot=lst_mot+[i[0] for i in model.most_similar(mot,topn=50)][::-1]
    
    while(WORD_to_FIND==""):
        
        if(lst_mot==[]):
            mot=best_start(model,driver)
            dico_word[mot]=send_word(driver,mot)
            lst_mot=lst_mot+[i[0] for i in model.most_similar(mot,topn=50)][::-1]
            
        mot_test=lst_mot[-1]
        lst_mot.pop(-1)
        if(mot_test not in dico_word.keys()):
            dico_word[mot_test]=send_word(driver,mot_test)
            if(dico_word[mot_test]>dico_word[mot]):
            
                mot=mot_test
                lst_mot=lst_mot+[i[0] for i in model.most_similar(mot,topn=50)][::-1]
    driver.close()            
    return WORD_to_FIND








i=0
WORD_to_FIND=""
mot=""



app = Flask(__name__)

@app.route('/')
def acceuil():
        return render_template('index.html')



@app.route('/index',methods=['GET', 'POST'])
def index():
    global i
    i+=1
    if(i%2==0):
        return render_template('index.html')
    return render_template('index.html',mot=mot)   

    
def open_browser(): #Pour les tests à  enlever après 
      webbrowser.open_new('http://127.0.0.1:5000/')
      
      
def job_function():
    global mot
    mot=res()
    
    
    
sched = BackgroundScheduler()
trigger = CronTrigger(year="*", month="*", day="*", hour="0",minute="2", second="0")
sched.add_job(job_function,trigger=trigger)
sched.start()


if __name__ == "__main__":

    Timer(1,open_browser()).start
    app.run(use_reloader=False)
    
