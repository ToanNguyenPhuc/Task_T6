from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re
import csv
import time
EXE_PATH = "D:\Workspace/VisLab_Learn/Task_T6/task_crawl_data/chromedriver.exe"
service = ChromeService(executable_path=EXE_PATH)
driver = webdriver.Chrome(service=service)
website = 'https://www.xetra.com/xetra-de/instrumente/aktien/primaermarktstatistik-neue-unternehmen'
output_file = '_.csv'
driver.get(website)
def handleOnePage():
    list_li_container = driver.find_element(By.CLASS_NAME,'list.search-results')
    list_li = list_li_container.find_elements(By.TAG_NAME,'li')
    for li in list_li:
        list_save_to_file = ['None'] * 8  
        infor_arr = li.text.split('\n')
        list_save_to_file[0] = infor_arr[0]
        list_save_to_file[1] = infor_arr[1]
        list_save_to_file[2] = infor_arr[2]
        list_save_to_file[3] = infor_arr[3].split(':')[1]
        emiss = 0
        erster = 0
        for (ii,ele) in enumerate(infor_arr):
            if 'Emiss. Preis' in ele:
                # print('emiss',infor_arr[ii])
                emiss = ii
            if 'Erster Preis' in  ele:
                # print('erster',infor_arr[ii])
                erster = ii
        if emiss:
            ipo_value = infor_arr[ii].split(':')[1]
            list_save_to_file[4] = ipo_value.split('/')[0]
            list_save_to_file[5] = ipo_value.split('/')[1]
        if erster:
            trading_value = infor_arr[ii].split(':')[1]
            list_save_to_file[6] = trading_value.split('/')[0]
            list_save_to_file[7] = trading_value.split('/')[1]
        with open(output_file, 'a', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows([list_save_to_file])

while driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div/div[2]/form[2]/ul/li[9]/button'):
    change_page = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div/div[2]/form[2]/ul/li[9]/button')
    handleOnePage()
    change_page.click()
    time.sleep(0.5)    
