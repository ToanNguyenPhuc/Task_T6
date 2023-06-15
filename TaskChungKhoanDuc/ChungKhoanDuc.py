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
website = 'https://www.xetra.com/xetra-de/instrumente/aktien/liste-der-handelbaren-aktien'
output_file = '_.csv'
driver.get(website)
def handleOnePage():
    list_li = driver.find_element(By.CLASS_NAME,'search-results')
    list_li_arr = re.split(r'Aktien',list_li.text)
    # filter useless element
    list_li_arr = [re.split(r'\n',list_li) for list_li in list_li_arr if list_li]
    for li in list_li_arr:
        save_ls = [None] * 4
        li = [column for column in li if column]
        if 'CCP-fähig' in li:
            save_ls[2] = 'Yes' 
        else: 
            save_ls[2] = 'No'
        save_ls[0] = li[0]
        save_ls[1] = li[1].split(':')[1]
        save_ls[3] = li[3].split(':')[1]
        with open(output_file, 'a', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows([save_ls])
while driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div/div[2]/form[2]/ul/li[9]/button'):
    change_page = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div/div[2]/form[2]/ul/li[9]/button')
    handleOnePage()
    change_page.click()
    time.sleep(0.5)    
