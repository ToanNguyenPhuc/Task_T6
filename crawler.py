# build up
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import csv
import time
import base64
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
frankfurk_listing = 'BorseFrankFurk.csv'
data = pd.read_csv(frankfurk_listing)
df = pd.DataFrame(data,index=None)
PATH_TEST = 'https://www.boerse-frankfurt.de/aktie/apple-inc'
ISINs = df['ISIN']
names =df['Instrument']
columns_name = ['name',
                'ISIN',
                'Dividende (2022)',
                'Dividendenrendite in %',
                'KGV',
                'Gewinn je Aktie',
                'Anzahl Aktien',
                'Marktkapitalisierung',
                'Segment',
                'Markt',
                'Aktientyp',
                'Aktienform',
                'Land',
                'Branche',
                'Sektor',
                'Subsektor']
with open('ChungKhoanDuc.csv','a',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns_name)
def handleOnePage(name,ISIN):
    first_table = driver.find_element(By.XPATH,'/html/body/app-root/app-wrapper/div/div[2]/app-equity/div[2]/div[4]/div[1]/app-widget-equity-key-data/div/div/div/div/table/tbody')
    second_table = driver.find_element(By.XPATH,'/html/body/app-root/app-wrapper/div/div[2]/app-equity/div[2]/div[5]/div[1]/app-widget-equity-master-data/div/div/table/tbody')
    table_combine = [first_table,second_table]
    dict_save_to_file = {}
    dict_save_to_file['name'] = name
    dict_save_to_file['ISIN'] = ISIN
    for table in table_combine:
        tr_elements = table.find_elements(By.TAG_NAME,'tr')
        for tr in tr_elements:
            td_elements = tr.find_elements(By.TAG_NAME,'td')
            dict_save_to_file[td_elements[0].text] = td_elements[1].text
    with open('BorserFrankfurk_listing.csv','a',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(dict_save_to_file.values())    
for ii,ISIN in enumerate(ISINs):
    path =  f'https://www.boerse-frankfurt.de/aktie/{ISIN}'
    driver.get(path)
    time.sleep(5)
    try: 
       handleOnePage(names[ii],ISIN)
    except:
        with open('error_Xetra.csv','a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ISIN])

            















# for name in names:
#     # input_element = driver.find_element(By.XPATH,'//*[@id="mat-input-0"]')
#     # input_element.send_keys(name)
#     transformed_name = re.sub(r'-',' ',name)
#     transformed_name = re.sub(r"\.(?=[^.]*$)", "", str(transformed_name))
#     transformed_name = re.sub(r'(\s+)','-',transformed_name)
#     transformed_name = transformed_name.lower()
#     time.sleep(0.3)
#     # try :
#     path = f'https://www.boerse-frankfurt.de/aktie/{transformed_name}'
#     driver.get(path)
#     try: 
#         handleOnePage()
    
#     # button_element = driver.find_element(By.XPATH,'//*[@id="global-search"]/form/button')
#         # button_element.click()
#         # _ngcontent-boerse-frankfurt-c116
#     except:
#         with open('error.csv','a',newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([name,transformed_name])
            