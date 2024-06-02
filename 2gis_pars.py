import time
import csv
import bs4
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# # chrome_options.headless = True

print('Напишите интересующую вас услугу, например: астосервисы, рестораны, аптеки и т.п.')
usluga = input()
print('Введите название файла на английском')
file_name = input()
count = 1
while count <= 20:
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options) as driver:  # Открываем хром
        driver.get(f"https://2gis.ru/samara/search/{usluga}/page/{count}")  # Открываем страницу
        time.sleep(5)  # Время на прогрузку страницы
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        heads = soup.find_all('div', class_='_zjunba')
        print(len(heads))
        for i in heads:
            w = i.find_next('a').get('href')
            # print('https://2gis.ru' + w)
            get_url = ('https://2gis.ru' + w)

            with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=chrome_options) as peeker:  # Открываем хром

                peeker.get(get_url)  # Открываем страницу
                time.sleep(5)  # Время на прогрузку страницы
                loop = bs4.BeautifulSoup(peeker.page_source, 'html.parser')
                name = loop.find('h1', class_='_tvxwjf')
                print(name.text.strip())
                head = (name.text.strip())
                try:
                    teep = loop.find('div', class_='_1idnaau').find('span')
                    print(teep.text.strip())
                    teeping = (teep.text.strip())
                except:
                    teeping = ''
                try:
                    reiting = loop.find('div', class_='_y10azs')
                    print(reiting.text.strip())
                    rait = (reiting.text.strip())
                except:
                    rait = ''
                try:
                    addr_1 = loop.find('div', class_='_13eh3hvq').find('span', class_='_14quei').find('span',
                                                                                                      class_='_er2xx9')
                    print(addr_1.text.strip())
                    place_1 = (addr_1.text.strip())
                except:
                    place_1 = ''
                try:
                    addr_2 = loop.find('div', class_='_13eh3hvq').find('div', class_='_1p8iqzw')
                    print(addr_2.text.strip())
                    place_2 = (addr_2.text.strip())
                except:
                    place_2 = ''
                try:
                    tel = loop.find('div', class_='_b0ke8').find('a', href=True)
                    print(tel['href'].replace('tel:', ''))
                    phone = (tel['href'].replace('tel:', ''))
                except:
                    # tel = loop.find('div', class_='_1azoctd').find('a', href=True)
                    phone = ''

                print('\n')

                storage = {'name': head, 'type': teeping, 'reiting': rait, 'street': place_1, 'adres': place_2,
                           'phone': phone}

                with open(f'{file_name}.csv', 'a+', encoding='utf-16') as file:
                    pisar = csv.writer(file, delimiter=';', lineterminator="\r")
                    pisar.writerow(
                        [storage['name'], storage['type'], storage['street'], storage['adres'],
                         storage['phone']])
        count += 1
