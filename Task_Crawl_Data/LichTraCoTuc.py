from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re
import csv
import time
EXE_PATH = "D:/Workspace/VisLab_Learn/Task_T6/task_crawl_data/chromedriver.exe"
service = ChromeService(executable_path=EXE_PATH)
driver = webdriver.Chrome(service=service)
website = 'https://s.cafef.vn/Lich-su-giao-dich-FRT-1.chn'
output_file = 'LichSuGia.csv'
driver.get(website)
# numb_range = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
numb_range = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22']

def handleOnePage():
    for i in range(0,20):
        if i % 2 == 0:

            id_ = f'ContentPlaceHolder1_ctl03_rptData2_itemTR_{i}'
        else:
            id_ =    f'ContentPlaceHolder1_ctl03_rptData2_altitemTR_{i}'
        div_container = driver.find_element(By.ID,id_)
        text_ = div_container.text
        # test_ = re.search(r"-?\d+\.\d+\s%",text_).group(1)
        # print(test_)
        # pattern = r"\(-?\d+ \. \d+\s %\)"
        # print(text_)
        # text_ = re.sub(pattern, '', text_)
        # print(text_)
        text_arr = re.split(r'(\s+)',text_)

        text_arr = [ele for ele in text_arr if ' ' not in ele and '(' not in ele and ')' not in ele and ele]
        with open(output_file, 'a', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows([text_arr])
while True:
        table_container_page_change = driver.find_element(By.CLASS_NAME,'CafeF_Paging')
        td_eles = table_container_page_change.find_elements(By.TAG_NAME,'td')
        for td_ele in td_eles:
             if td_ele:
                print(td_ele.text)
        for ii,td_ele in enumerate(td_eles):
            
            if td_ele.text in numb_range:
                numb_range.pop(0)
                for i in range(0,20):
                    if i % 2 == 0:

                        id_ = f'ContentPlaceHolder1_ctl03_rptData2_itemTR_{i}'
                    else:
                        id_ = f'ContentPlaceHolder1_ctl03_rptData2_altitemTR_{i}'
                    div_container = driver.find_element(By.ID,id_)
                    text_ = div_container.text
                    # test_ = re.search(r"-?\d+\.\d+\s%",text_).group(1)
                    # print(test_)
                    # pattern = r"\(-?\d+ \. \d+\s %\)"
                    # print(text_)
                    # text_ = re.sub(pattern, '', text_)
                    # print(text_)
                    text_arr = re.split(r'(\s+)',text_)

                    text_arr = [ele for ele in text_arr if ' ' not in ele and '(' not in ele and ')' not in ele and ele]
                    with open(output_file, 'a', newline='',encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerows([text_arr])

                # actions = ActionChains(driver)
                # actions.click(td_ele).perform()
                element = driver.find_element(By.XPATH,f'//*[@id="ContentPlaceHolder1_ctl03_divHO"]/div/div/table/tbody/tr/td[{ii+1}]')
                element.click()
                time.sleep(0.5)
                break
     
                
