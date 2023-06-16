
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

output_file = '_.csv'
# numb_range = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
# website = 'https://finance.yahoo.com/screener/unsaved/408095ee-5b3e-4421-bb55-6a31d04a4bf0'
# driver.get(website)
def handleOnePage():
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

for offset in range(1900,73600,100):
    website = f'https://finance.yahoo.com/screener/unsaved/408095ee-5b3e-4421-bb55-6a31d04a4bf0?count=100&offset={offset}'
    driver.get(website)
    time.sleep(0.3)
    handleOnePage()
    # blocking_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'td[aria-label="52 Week Range"]')))
    offset += 25
    
# //*[@id="scr-res-table"]/div[1]/table/tbody/tr[7]/td[10]/canvas

# Handle canvas_element


    # canvas_element = driver.find_element(By.XPATH,'//*[@id="scr-res-table"]/div[1]/table/tbody/tr[7]/td[10]/canvas')
    # image_data = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas_element)
    # # print(image_data)
    # image_data = base64.b64decode(image_data)
    # with open("canvas_image.png", "wb") as file:
    #     file.write(image_data)
    # image = Image.open("canvas_image.png")
    # image.show()
    # print(pytesseract.image_to_string(image))
    
    #  (r'\\n|(\s+)(?=\S)