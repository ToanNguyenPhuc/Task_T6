from selenium import webdriver
# selenium-wire
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
import re
import csv
import time
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# EXE_PATH = "D:\Workspace/VisLab_Learn/Task_T6/task_crawl_data/chromedriver.exe"
# service = ChromeService(executable_path=EXE_PATH)
# driver = webdriver.Chrome(service=service)
website = 'https://www.xetra.com/xetra-de/instrumente/aktien/primaermarktstatistik-neue-unternehmen/5424!search?state=H4sIAAAAAAAAADWOsQoCMRBEf0WmvuKaU0wtVhYHio1YhGRPAzHR3Q1yHPfvBiHlY94Ms8BbpSPnF0wqMXZ_vuRGk3WkArNA2SZ5W6bkZpgb9sN21_e4r1UKLHoiVeLWewaVkXi0D4IZ-g4huVg8nYOSNCmnOI9-gplsFOrwKcR1G-jAJCXqNdC3yZJZayaH-m_jSRzWH1_t3gO9AAAA&hitsPerPage=50&pageNum=0'
# website = 'https://www.xetra.com/xetra-de/instrumente/aktien/liste-der-handelbaren-aktien/xetra/3002!search?state=H4sIAAAAAAAAADWKsQoCMRAFf0W2TqFtPsDKIuBhH5IXDawJ7m6Q47h_9xDSzTCzUY6Gq_Q3-TaY3d-XPq3EBFPy235wFbUbzCAzv6ppgIT4BPnL2VFtiUfGvRp0Tr3xGnIhXyIrHH0GZCVP5Eigg-1R8Z2zdrGj6VKNcYqaaP8BsKzzjqQAAAA&sort=sTitle+asc&hitsPerPage=50'
output_file = 'delisting_infor.csv'
driver.get(website)
def handleOnePage():
    list_li_container = driver.find_element(By.CLASS_NAME,'list.search-results')
    list_li = list_li_container.find_elements(By.TAG_NAME,'li')
    company_paths  = []
    a_elements = list_li_container.find_elements(By.TAG_NAME,'a')
    for a_ele in a_elements:
        company_paths.append(a_ele.get_attribute('href'))
    ls_surface_infor = []
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
        ls_surface_infor.append(list_save_to_file)
    return ls_surface_infor,company_paths
def handleCompanyPage():
    ls_element = driver.find_element(By.CLASS_NAME,'list.list-tradable-details')
    dt_elements = ls_element.find_elements(By.TAG_NAME,'dt')
    dd_elements = ls_element.find_elements(By.TAG_NAME,'dd')
    ls_return = ['None'] * 32
    ls_save_infor = []
    for dt_ele,dd_ele in zip(dt_elements,dd_elements):
        ls_save_infor.append(f'{dt_ele.text}{dd_ele.text}')
    # ls_save_infor = [cp_atr for cp_atr in ls_save_infor if  'ISIN' not in cp_atr and 'CCP-Abwicklung' not in cp_atr and 'Market Identifier Code'not in cp_atr ]
    for ii,infor in enumerate(ls_save_infor):
        if 'Bezeichnung' in infor:
            ls_return[0] = infor.split(':')[1]
        elif 'Konsortium' in infor:
                ls_return[14] = infor.split(':',1)[1]
        elif 'Segment bei Erstnotierung' in infor:
                ls_return[1] = infor.split(':')[1]
        elif 'Art der Transaktion' in infor:
                ls_return[2] = infor.split(':')[1]
        elif 'Supersektor' in infor:
                ls_return[3] = infor.split(':')[1]
        elif 'Subsektor' in infor:
                ls_return[4] = infor.split(':')[1]
        elif 'Land' in infor:
                ls_return[5] = infor.split(':')[1]
        elif 'Börsenkürzel' in infor:
                ls_return[6] = infor.split(':')[1]
        elif 'Instrumentenart (Gattung)' in infor:
                ls_return[7] = infor.split(':')[1]
        elif 'Zeichnungsfrist' in infor:
                ls_return[8] = infor.split(':')[1]
        elif 'Emissionsverfahren' in infor:
                ls_return[9] = infor.split(':')[1]
        elif 'Bookbuildingspanne' in infor:
                ls_return[10] = infor.split(':')[1]
        elif 'Emissionspreis' in infor:
                ls_return[11] = infor.split(':')[1]
        elif 'Erster Preis geg. Emiss.preis' in infor:
                ls_return[29] = infor.split(':')[1]
        elif 'Erster Preis' in infor:
                ls_return[12] = infor.split(':')[1]
        elif 'Konsortialführer' in infor:
                ls_return[13] = infor.split(':')[1]
        elif 'Platzierungsvolumen exkl. Greenshoe' in infor:
                ls_return[15] = infor.split(':')[1]
        elif 'Platzierungsvolumen in Stück exkl. Greenshoe' in infor:
                ls_return[16] = infor.split(':')[1]
        elif 'Platzierungsvolumen inkl. Greenshoe' in infor:
                ls_return[17] = infor.split(':')[1]
        elif 'Platzierungsvolumen ausgeübter Greenshoe' in infor:
                ls_return[18] = infor.split(':')[1]
        elif 'Platzierungsvolumen (Aktien) aus Kapitalerhöhung' in infor:
                ls_return[19] = infor.split(':')[1]
        elif 'Platzierungsvolumen (Aktien) aus Umplatzierung' in infor:
                ls_return[20] = infor.split(':')[1]
        elif 'Verfügbarer Greenshoe in Stück' in infor:
                ls_return[21] = infor.split(':')[1]
        elif 'Ausgeübter Greenshoe in Stück' in infor:
                ls_return[22] = infor.split(':')[1]
        elif 'Bevorzugte Zuteilung' in infor:
                ls_return[23] = infor.split(':')[1]
        elif 'Zuteilung friends & family' in infor:
                ls_return[24] = infor.split(':')[1]
        elif 'Grundkapital in Stück bei Erstnotierung' in infor:
                ls_return[25] = infor.split(':')[1]
        elif 'Marktkapitalisierung gesamt bei Erstnotierung' in infor:
                ls_return[26] = infor.split(':')[1]
        elif 'Marktkapitalisierung Freefloat bei Erstnotierung' in infor:
                ls_return[27] = infor.split(':')[1]
        elif 'Freefloat bei Erstnotierung' in infor:
                ls_return[28] = infor.split(':')[1]
        elif 'Ergänzende Erläuterungen' in infor:
                ls_return[30] = infor.split(':')[1]
        elif 'ISIN' in infor:
                ls_return[31] = infor.split(':')[1]
    for ii,ele in enumerate(ls_return):
        ls_return[ii] = ele.replace('\n','')
    return ls_return
while driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div/div/form[2]/ul/li[9]/button'):
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
    change_page = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/div/div/form[2]/ul/li[9]/button')
    change_page.click()
    time.sleep(0.1)