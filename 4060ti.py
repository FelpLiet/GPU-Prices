from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('variables.env')
sheetUrl = os.getenv("URL")

# create a new Chrome session
driver = webdriver.Chrome()
driver.implicitly_wait(30)

# navigate to the application home page
driver.get("http://www.google.com")

# wait for the search box to be loaded
wait = WebDriverWait(driver, 10)
search_field = wait.until(EC.presence_of_element_located((By.NAME, "q")))

# clear any pre-populated text in the input field (if it's present)
search_field.clear()

# enter search keyword and submit
search_field.send_keys('GeForce RTX 4060 Ti')
search_field.submit()

time.sleep(2)

# wait for the search results to be loaded
wait = WebDriverWait(driver, 10)
priceElements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "pla-unit-container")))

dataToSheets = {
    "boards" : [],
}

for element in priceElements:
    data = element.text
    
    if (data == '' or 'PC' in data or 'Pc' in data or 'pc' in data or 'Computador' in data or '3060' in data):
        continue
    
    data = data.replace('PROMOÇÃO\n', '') #TODO - adicionar aviso quando for promoção de alguma forma
    
    data_split = data.split('\n')
    if len(data_split) < 3:
        continue

    boardName = data.split('\n')[0]
    boardName = boardName.split(',')[0]
    loja = data.split('\n')[2]
    price = data.rsplit('\n')[1]
    price = price.rpartition(',')[0]

    dataToSheets["boards"].append({
        "boardName": boardName,
        "price": price,
        "loja": loja,
    })

driver.quit()

with open('boards.json', "w") as file:
    json.dump(dataToSheets, file)

response = requests.post(sheetUrl, json=dataToSheets)
print(response.content)

response = requests.get(sheetUrl)
print(response.content)

