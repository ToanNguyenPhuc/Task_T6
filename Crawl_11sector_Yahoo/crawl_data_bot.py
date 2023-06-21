
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re
import csv
import time
import base64
import pytesseract 
pytesseract.pytesseract.tesseract_cmd="D:/Tesseract_OCR/tesseract.exe"
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
EXE_PATH = "chromedriver.exe"
service = ChromeService(executable_path=EXE_PATH)
driver = webdriver.Chrome(service=service)
link_arr = [
    'https://finance.yahoo.com/screener/unsaved/5eda440d-9818-406e-9eb7-52fb39c7a6f0?count=100&offset=0',
            'https://finance.yahoo.com/screener/unsaved/7fddfaa8-daea-4832-8c55-04eaddd9af8d?count=100&offset=0',
            'https://finance.yahoo.com/screener/unsaved/4e2fe068-43a5-4439-9a22-2e370a3610be?offset=0&count=100',
            'https://finance.yahoo.com/screener/unsaved/ba577415-d461-432c-9987-f1d4a152d176?offset=0&count=100',
            'https://finance.yahoo.com/screener/unsaved/40a29900-725a-490a-9c8c-f07841eca736?offset=0&count=100',
            'https://finance.yahoo.com/screener/unsaved/10309675-4882-414a-a03c-5222f85cbff2?offset=0&count=100',
            'https://finance.yahoo.com/screener/unsaved/f4346095-8387-4bb9-844a-6f8d50dd6e94?offset=0&count=100',
            'https://finance.yahoo.com/screener/unsaved/23467494-961d-4ac9-bfc1-0e0fe3dd4f6f?offset=0&count=100',
            'https://finance.yahoo.com/screener/unsaved/71691287-e0ee-416a-84f0-9b31606fc1b8?offset=0&count=100',
            'https://finance.yahoo.com/screener/unsaved/7322c3bf-2558-42cd-9896-4eed7171514d?offset=0&count=100'
            ]
Estimated_results_arr_1 = [4788,4611,1909,2364,6006,1282,2568,2300,6565,5543]
Estimated_results_arr = [
    4800,
    4700,
    2000,
    2400,
    6100,
    1300,
    2600,
    2400,
    6600,
    5600
    ]
name_arr = [
            'Consumer_Cyclica.csv',
            'Financial_Services.csv',
            'Real_Estate.csv',
            'Consumer_defensive.csv',
            'Healthcare.csv',
            'Utilites.csv',
            'Communication_Sevice.csv',
            'Energy.csv',
            'Industrials.csv',
            'Technology.csv'
            ]

def handleOnePage(output_file):
    t_body_ele = driver.find_element(By.TAG_NAME,'tbody')
    tr_elements = t_body_ele.find_elements(By.TAG_NAME,'tr')
    for tr_element in tr_elements:
        # infor_arr = re.split(r"\s+(?=\S)",string=tr_element.text)
        
        list_save = ['None'] * 9
        col_elements = tr_element.find_elements(By.TAG_NAME,'td')
        for (ii,col) in enumerate(col_elements):
            if col.text:
                list_save[ii] = col.text
        with open(output_file, 'a', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows([list_save])
# input('')   
for (ii,total_result) in enumerate(Estimated_results_arr):
    for offset in range(0,total_result,100):
        website = link_arr[ii]
        website = re.sub(r'(offset=\d+)',f'offset={offset}',website)
        driver.get(website)
        time.sleep(0.01)
        handleOnePage(name_arr[ii])