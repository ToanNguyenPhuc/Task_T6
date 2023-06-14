from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re
import csv
EXE_PATH = "LichTraCoTuc.csv"
service = ChromeService(executable_path=EXE_PATH)
driver = webdriver.Chrome(service=service)
website = 'https://s.cafef.vn/hose/FRT-cong-ty-co-phan-ban-le-ky-thuat-so-fpt.chn'
driver.get(website)

parent_element_ = driver.find_element(By.CLASS_NAME,'view-more-btn')
# Find the element to hover over


# Create an instance of ActionChains
actions = ActionChains(driver)

# Perform the hover action
actions.move_to_element(parent_element_).perform()
output_file = 'LichTraCoTuc.csv'
with open(output_file, 'a', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows([['Time', 'Bằng Cổ Phiếu','Bằng Tiền']])
child_contain = parent_element_.find_element(By.CLASS_NAME,'middle')
contents = child_contain.text
contents_arr = contents.split('-')
for i in range(len(contents_arr)):
        save_ls = ['None'] * 3  
        content = contents_arr[i]
        # # remove useless element 
        if not content or ' Cổ tức bằng Cổ phiếu' not in content and ' Cổ tức bằng Tiền' not in content:
            continue
        content_arr = content.split(':',1)
        save_ls[0] = content_arr[0]
    # if 'Cổ tức bằng Cổ phiếu' in content and ' Cổ tức bằng Tiền' in content:
        DIVIDEND = re.search(r'(\d+:\d+)',content_arr[1])
        if DIVIDEND:
            save_ls[1] = DIVIDEND.group(1)
               
        MONEY = re.search(r'(\d+%)',content_arr[1])
        if MONEY:
            save_ls[2] = MONEY.group(1)
        print(save_ls)
        with open(output_file, 'a', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows([save_ls])

