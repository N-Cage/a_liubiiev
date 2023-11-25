import gspread as gs
import pandas as pd
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


search_link = 'https://filmfreeway.com/submissions?utf8=%E2%9C%93&has_query=&sort=created_at&sort_dir=desc&season=101950&q=&ga_search_category=Submissions&date_range=&judge=&advanced_filters=1&project_type=&project_category%5B%5D=&project_category%5B%5D=&project_category%5B%5D=&genres=&synopsis=&runtime_from=&runtime_to=&completion_date_mode=After&completion_date=&language_mode=1&language=&country_of_origin_mode=1&country_of_origin=&region_of_origin_mode=1&region_of_origin=&country_of_filming_mode=1&country_of_filming=&shooting_format_mode=1&shooting_format=&aspect_ratio_mode=1&aspect_ratio=&film_color_mode=1&film_color=&student_project=true&custom_field_field=&custom_fields_contains=&tracking=&download_permission=&discount_code=&discount_code_presence=&first_time_filmmaker=&age_from=&age_to=&gender=&biography=&statement=&cover_letter=&rating_from=&rating_to=&judging_field_field=&judging_field_contains=&ratings=&ratings_count_from=&ratings_count_to=&rated_by_me=&notified=&assigned_judges=&filter_ratings=&budget_mode=gte&budget=&budget_currency=USD&entry_fee_from=&entry_fee_to=&screened_mode=true&screened_country=&awards=&distribution_country_mode=available&distribution_country=&distribution_rights=&per_page=50'


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(), options=options)

# reaching out to the current list of submissions on the website

driver.get(search_link) 

ff_login = driver.find_element(By.ID, "user_account_email")
ff_login.clear()
ff_login.send_keys('dascha.levchenko@gmail.com')

ff_pswd = driver.find_element(By.ID, "user_account_password") 
ff_pswd.clear()
ff_pswd.send_keys('#')

time.sleep(40)

# locating and clicking the first button

button1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-dropdown="#dropdown-export-content"]'))) 

button1.click()

# idling until the page is updated

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-submission-export-dropdown]'))) 

# clicking the second button

button2 = driver.find_element(By.CSS_SELECTOR, "[data-submission-export-dropdown]")

button2.click()

# idling until the page is updated

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn btn-success btn-thin'))) 


# extracting the sheet download link

sheet_download_link = driver.find_element(By.CLASS_NAME, "btn btn-success btn-thin").get_attribute("href") 

print(sheet_download_link)

# credentials = {
#     "installed":{
#         "client_id":"594963415722-dlldd9sqrpacpdnn5g8qfke9vl7ned1i.apps.googleusercontent.com",
#         "project_id":"list-for-film-festival-dascha",
#         "auth_uri":"https://accounts.google.com/o/oauth2/auth",
#         "token_uri":"https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
#         "client_secret":"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",


        
#         "redirect_uris":["http://localhost"]
#         }
#     }

# gc, authorized_user = gs.oauth_from_dict(credentials)


# https://filmfreeway-production-storage-01.s3.us-west-2.amazonaws.com/system_export_files/files/003/290/323/original/FilmFreeway-Submissions-2023-07-26-01-09-42.csv?response-content-disposition=attachment%3B&X-Amz-Expires=3600&X-Amz-Date=20230726T080955Z&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2CLUDU3Q532SSOBJ/20230726/us-west-2/s3/aws4_request&X-Amz-SignedHeaders=host&X-Amz-Signature=6193142a8b7e102c2b1f0e755410ac2b68a7d890d1bb9bbb48493cc73fe2a7b2

# https://filmfreeway-production-storage-01.s3.us-west-2.amazonaws.com/system_export_files/files/003/290/332/original/FilmFreeway-Submissions-2023-07-26-01-28-38.csv?response-content-disposition=attachment%3B&X-Amz-Expires=3600&X-Amz-Date=20230726T082840Z&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2CLUDU3Q532SSOBJ/20230726/us-west-2/s3/aws4_request&X-Amz-SignedHeaders=host&X-Amz-Signature=171eeb41046b5d4f22a0832286311902443a833dee94d7d217ded37c26dc0ea9

# https://filmfreeway-production-storage-01.s3.us-west-2.amazonaws.com/system_export_files/files/003/297/415/original/FilmFreeway-Submissions-2023-08-26-02-31-57.csv?response-content-disposition=attachment%3B&X-Amz-Expires=3600&X-Amz-Date=20230826T093215Z&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA2CLUDU3Q532SSOBJ/20230826/us-west-2/s3/aws4_request&X-Amz-SignedHeaders=host&X-Amz-Signature=6f3c8fd8c0ae80c7b16133590c40b7abd71687f4d30a313fe1b78efcfae5e7e2

#sh = gc.create('New spreadsheet test2')


# sheet_id = '1Q9Fid086R439wuYHmxsCAg8iuX9VKvaDgubddUdMnQQ'

# df_export = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# print(df_export.head())