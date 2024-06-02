import time

import bs4
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.headless = True

with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                      options=chrome_options) as driver:  # Открываем хром
    driver.get("https://2gis.ru/samara/search/Аптеки/page/2")  # Открываем страницу
    time.sleep(5)  # Время на прогрузку страницы
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    heads = soup.find_all('div', class_='_zjunba')
    # print(len(heads))
    for i in heads:
        w = i.find_next('a').get('href')
        print('https://2gis.ru' + w)
        get_url = ('https://2gis.ru' + w)
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:  # Открываем хром
            driver.get(get_url)  # Открываем страницу
            time.sleep(5)  # Время на прогрузку страницы
            block = bs4.BeautifulSoup(driver.page_source, 'html.parser')
