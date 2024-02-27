import gspread as gs
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


search_link = '#link'


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(), options=options)

# reaching out to the current list of submissions on the website

driver.get(search_link) 

ff_login = driver.find_element(By.ID, "#") # Specified login
ff_login.clear()
ff_login.send_keys('#') # Specified password

ff_pswd = driver.find_element(By.ID, "user_account_password") 
ff_pswd.clear()
ff_pswd.send_keys('ShittyFilmPassword22')

time.sleep(10)

button_login = driver.find_element(By.NAME, 'commit')

button_login.click()

# locating and clicking the first button

button1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-dropdown="#dropdown-export-content"]'))) 

button1.click()

# idling until the page is updated

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-submission-export-dropdown]'))) 

# clicking the second button

button2 = driver.find_element(By.CSS_SELECTOR, "[data-submission-export-dropdown]")

button2.click()

button_exel = driver.find_element(By.XPATH, "//label[@for='excel']")

button_exel.click()


# idling until the page is updated

# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn btn-success btn-thin'))) 


# extracting the sheet download link

sheet_download_link = driver.find_element(By.XPATH, "//button[@class='btn btn-success btn-thin']")

sheet_download_link.click()


time.sleep(30)

# Uploading to G-sheets

# Changing the working directory to the downloaded file location
user_name = os.getlogin()

os.chdir(f'c:\\users\\{user_name}\\downloads')


credentials = {
    ####
    } # Service account credentials


gc, authorized_user = gs.oauth_from_dict(credentials)


sh = gc.open('Film Submissions')


sh.get_worksheet(0).clear()

csv_sheet = open('FilmFreeway-Submissions.xls', 'r').read()

gc.import_csv(sh, csv_sheet)

