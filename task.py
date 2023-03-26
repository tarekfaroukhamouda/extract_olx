
#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver  
import time  
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.common.keys import Keys 
import pymongo
from datetime import date
from flask import Response

def extract_olx(link,current_page,already_data,driver,search_for):
    driver.get(link)  
    time.sleep(5)
    if current_page ==1:
        myDiv = driver.find_element(By.XPATH, '//input[@type="search"]').send_keys(search_for) 
        driver.find_element(By.XPATH, '//button[@aria-label="Search"]').send_keys(Keys.ENTER)
        time.sleep(5)
    wait = WebDriverWait(driver, 20)
    ad_title = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@aria-label='Title']")))
    ad_price=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//span[@class='_95eae7db']")))
    ad_location=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//span[@aria-label='Location']")))
    ad_image=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//img[@role='presentation']")))
    time.sleep(5)
    for title,price,location,prictur in zip(ad_title,ad_price,ad_location,ad_image):
        already_data.append({'search_for':search_for,"date":str(date.today()),'title':title.text,'price':price.text,'location':location.text,"picture":prictur.get_attribute("src")})
        query = new_table.insert_one({'search_for':search_for,"date":str(date.today()),'title':title.text,'price':price.text,'location':location.text,"picture":prictur.get_attribute("src")})
    if len(already_data)< 300:
        try:
            current_page+=1
            if current_page==2:
                extract_olx(driver.current_url+'?page='+str(current_page),current_page,already_data,driver,search_for)
            else:
                new_url=driver.current_url.split('=')
                extract_olx(new_url[0]+"="+str(current_page),current_page,already_data,driver,search_for)
                
            time.sleep(5) 
        except:
             return json.dumps(already_data)

    return json.dumps(already_data)


app = Flask(__name__)
connection_url = Your mongodb connection

db = MongoEngine()
db.init_app(app)
client = pymongo.MongoClient(connection_url)
Database = client.get_database('olx_search')
new_table=Database.new_table

@app.route('/<search_for>', methods=['GET'])
def create_search(search_for):
    all_data=[]
    queryObject = {
        "date": str(date.today()),
        "search_for":search_for
        }
    query = new_table.find(queryObject)

    for x in query[:200]:
        x.pop('_id')
        all_data.append(x)
    if len(all_data)>0:
        return all_data

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    data=extract_olx('https://www.olx.com.eg/en/',1,all_data,driver,search_for)    
    return create_search(search_for)

 
if __name__ == '__main__':
    app.run(debug=True)

