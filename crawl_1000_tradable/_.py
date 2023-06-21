from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
import re
import csv
import time

EXE_PATH = "D:\Workspace/VisLab_Learn/Task_T6/task_crawl_data/chromedriver.exe"
service = ChromeService(executable_path=EXE_PATH)
driver = webdriver.Chrome(service=service)
website = 'https://www.xetra.com/xetra-de/instrumente/aktien/liste-der-handelbaren-aktien/xetra/3002!search?state=H4sIAAAAAAAAADWKsQoCMRAFf0W2TqFtPsDKIuBhH5IXDawJ7m6Q47h_9xDSzTCzUY6Gq_Q3-TaY3d-XPq3EBFPy235wFbUbzCAzv6ppgIT4BPnL2VFtiUfGvRp0Tr3xGnIhXyIrHH0GZCVP5Eigg-1R8Z2zdrGj6VKNcYqaaP8BsKzzjqQAAAA&sort=sTitle+asc&hitsPerPage=50'
output_file = '_.csv'
driver.get(website)
def handleOnePage():
    list_li = driver.find_element(By.CLASS_NAME,'search-results')
    a_elements = list_li.find_elements(By.CSS_SELECTOR,'a')
    companys_path = []
    for ele in a_elements:
        href = ele.get_attribute('href')
        companys_path.append(href)
    list_li_arr = re.split(r'Aktien',list_li.text)
    # filter useless element
    list_li_arr = [re.split(r'\n',list_li) for list_li in list_li_arr if list_li]
    save_ls_big = []
    
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
        save_ls_big.append(save_ls)
    return save_ls_big,companys_path
def handleCompanyPage():
    ls_element = driver.find_element(By.CLASS_NAME,'list.list-tradable-instruments')
    dt_elements = ls_element.find_elements(By.TAG_NAME,'dt')
    dd_elements = ls_element.find_elements(By.TAG_NAME,'dd')
    ls_return = ['None'] * 9
    ls_save_infor = []
    for dt_ele,dd_ele in zip(dt_elements,dd_elements):
        ls_save_infor.append(f'{dt_ele.text}{dd_ele.text}')
    ls_save_infor = [cp_atr for cp_atr in ls_save_infor if  'ISIN' not in cp_atr and 'CCP-Abwicklung' not in cp_atr and 'Market Identifier Code'not in cp_atr ]
    for ii,infor in enumerate(ls_save_infor):
        if 'WKN' in infor:
            ls_return[0] = infor.split(':')[1]
        elif 'Kürzel' in infor:
                ls_return[1] = infor.split(':')[1]
        elif 'Währung' in infor:
                ls_return[2] = infor.split(':')[1]
        elif 'Instrumententyp' in infor:
                ls_return[3] = infor.split(':')[1]
        elif 'Designated Sponsor(s)' in infor:
                ls_return[4] = infor.split(':')[1]
        elif 'Market Maker' in infor:
                ls_return[5] = infor.split(':')[1]
        elif 'Handelsmodell' in infor:
                ls_return[6] = infor.split(':')[1]
        elif 'Maximale Spanne' in infor:
                ls_return[7] = infor.split(':')[1]
        elif 'Minimales Quotierungsvolumen' in infor:
                ls_return[8] = infor.split(':')[1]
    return ls_return
while driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div/div[2]/form[2]/ul/li[9]/button'):
    current_website = driver.current_url
    infor,company_path = handleOnePage()
    for ii,path in enumerate(company_path):
        driver.get(path)
        company_infor = handleCompanyPage()
        infor[ii] = infor[ii] + (company_infor)
        with open(output_file, 'a', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows([infor[ii]])
    driver.get(current_website)
    change_page = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div/div[2]/form[2]/ul/li[9]/button')
    change_page.click()
    time.sleep(0.3)