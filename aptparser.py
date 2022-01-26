import requests
import lxml
from bs4 import BeautifulSoup
import csv


csv_file = open('aptscrapper.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Constrction Name', 'Location', 'Construction Company', #'Company Webpage',
 'Price', 'Documaents', 'ЛУН link'])

# urllun = ('https://lun.ua/uk/%D0%BD%D0%BE%D0%B2%D0%BE%D0%B1%D1%83%D0%B4%D0%BE%D0%B2%D0%B8-%D0%BA%D0%B8%D1%94%D0%B2%D0%B0') # All const in Kyiv

urllun = ('https://lun.ua/uk/%D0%BD%D0%BE%D0%B2%D0%BE%D0%B1%D1%83%D0%B4%D0%BE%D0%B2%D0%B8-%D0%BA%D0%B8%D1%94%D0%B2%D0%B0?room_count=2&room_count=1&room_count=3&ready_state=2022&ready_state=2021&ready_state=ready&construction_state=under_construct&construction_state=built&class=2&class=4&class=1&order=popularity&max_area=143') # Filtered(rooms, state of const)
response = requests.get(urllun)
soup = BeautifulSoup(response.text, 'lxml')

results = []

for link in soup.find_all('a'):
    if 'ЖК' in link.text:
        # print('lun.ua' + link.get('href'))
        results.append(link.get('href'))

for result in results:
       

# results = 'https://lun.ua/uk/%D0%B6%D0%BA-great-%D0%BA%D0%B8%D1%97%D0%B2'

        response2 = requests.get(result).text

        rs = BeautifulSoup(response2, 'lxml')
        links = []
        company_name = []
        docs = []
        const_name = rs.find('h1').text.strip()
        price = rs.find('div', class_='BuildingPrices-price hidden').text.strip() # PRICE $ sqr.m 
        company = rs.find('div', class_='BuildingContacts-developer-links')
        # LOCATION
        for i in rs.find_all('a', href=True):
                if 'р-н' in i.text:
                        location = i.text

        # DOCUMENTS
        try:
                doc_response = requests.get(result + '/документи#d-docs').text
                doc_page_soup = BeautifulSoup(doc_response, 'lxml')
                for a in doc_page_soup.find_all('a', href=True):
                        if 'Дивитись документ' in a.text:
                                docs.append(a['href'])
        except Exception as e:
                pass

        try:
                company_links = company.find_all('a')

                [links.append(link.get('href')) for link in company_links]
                [company_name.append(name.text.strip()) for name in company_links]   # COMPANY NAME
        except Exception as e:
                pass
        #COMPANY URL
        for l in links:
                url = f'https://lun.ua{l}'
                url_response = requests.get(url).text
                url_soup = BeautifulSoup(url_response, 'lxml')
                comp_url = url_soup.find('div', class_='UITwoLinerButton-content').text.strip()

        csv_writer.writerow([const_name, location, company_name, #comp_url,
         price, docs, result])

csv_file.close()



