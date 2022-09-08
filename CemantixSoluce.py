from gensim.models import KeyedVectors
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
import random
import numpy as np

model=KeyedVectors.load_word2vec_format("ModeleDoc2Vec/modeleCemantix.bin", binary=True, unicode_errors="ignore")
WORD_to_FIND=""

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
    for i in range(100):
        rd=random.randint(1,100000)
        max_score.append(send_word(driver,model.index_to_key[rd]))
        max_mot.append(model.index_to_key[rd])
    return max_mot[np.argmax(max_score)]


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
            
print("Le mot du jour à trouver est : ",WORD_to_FIND)