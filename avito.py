import json
from numpy import append
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import time
import csv

options = webdriver.ChromeOptions()

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.85")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(
    executable_path="C:\\MyProjects\\in progress\\GetCoreTeam\\chromedriver.exe",
    options=options
)
print("\n\n")
try:
    start_time = time.time()
    advertisement = []
    advertisement_limitation = []

    driver.get("https://www.avito.ru/krasnodar/tovary_dlya_kompyutera/klaviatury_i_myshi-ASgBAgICAUTGB7xO?cd=1&q=%D0%BC%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F+%D0%BA%D0%BB%D0%B0%D0%B2%D0%B8%D0%B0%D1%82%D1%83%D1%80%D0%B0")
    time.sleep(2)

    n = 0

    with open("report.csv","w", encoding='utf=8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Название',
                'Цена',
                'Дата',
                'Имя продавца',
                'Ссылка'
            )
        )

    while True:

        all_keyboard = driver.find_elements(By.XPATH,"//div[@data-marker='item']")

        all_keyboard[n].click()

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        
        price = driver.find_elements(By.CLASS_NAME,"js-item-price")[1].text.strip()
        price = price.replace(' ','')
        title = driver.find_element(By.CLASS_NAME,"title-info-title-text").text
        username = driver.find_element(By.XPATH,"//div[@data-marker='seller-info/name']").text
        post_time = driver.find_element(By.CLASS_NAME,'style-item-metadata-date-1y5w6').text
        print('#'*20)
        print(f"\nНазвание объявления: {title}\nURL объявления: {driver.current_url}")
        print('-'*20)
        print(f"Имя продавца: {username}\nЦена: {price}₽\nДата: {post_time}\n")  

        advertisement.append(
            {
                'Название':title,
                'Цена':price,
                'Дата':post_time,
                'Имя продавца':username,
                'Ссылка':driver.current_url 
            }
        )

        with open("report.json", "w", encoding='utf=8') as file:
            json.dump(advertisement, file, indent=4, ensure_ascii=False)

        with open("report.csv","a", encoding='utf=8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    price,
                    post_time,
                    username,
                    driver.current_url
                )
            )
        
        cifra = price
        if (int(cifra)) <=2500:
            # print('Подходит')
            advertisement_limitation.append(
                {
                    'Название':title,
                    'Цена':price,
                    'Дата':post_time,
                    'Имя продавца':username,
                    'Ссылка':driver.current_url 
                }
            )
        
            with open("report_ogran.json", "w", encoding='utf=8') as file:
                json.dump(advertisement_limitation, file, indent=4, ensure_ascii=False)

        driver.close()

        driver.switch_to.window(driver.window_handles[0])
        # time.sleep(1)

        if n<49:
            n+=1
        else:
            next = driver.find_element(By.XPATH,"//span[@data-marker='pagination-button/next']").click()
            n = 0
            time.sleep(1)
        
        pagination = driver.find_element(By.CLASS_NAME,'pagination-item_active-NcJX6').text

        print(f'Обрабатывается объявление {n} на странице {pagination}')

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
    finish_time = time.time() - start_time
    print(f"\n\nВремя выполнения: {finish_time:.1f} секунд")