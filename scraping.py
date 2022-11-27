from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
import re
import random
import time 



def get_source_html(url):
    # Парсер html разметки страницы с ссылками!
    useragent = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.random}")

    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

    driver.maximize_window()

    try:
            driver.get(url=url)
            time.sleep(3)

            driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div').click()
            time.sleep(3)
               
            with open("ranobe_url.html", 'w', encoding='UTF-8') as f:
                f.write(driver.page_source) 




    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()





def get_url(file_path):
    # Парсер ссылкок!
    with open(file_path) as f:
        src = f.read()

        body = []
        
        soup = BS(src, 'lxml')
        div = soup.find_all('a', {'class': ['menu__item text-truncate', 'menu__item text-truncate menu__item_active']})      
        for i in div:
            chapter = 'https://ranobelib.me' + i.get('href')
            body.append(chapter)

            
        with open('urls.txt', 'w') as f:
            for i in body:
                f.write(f"{i} \n")





def get_content(file_path):
    # Парсер контента!
    with open(file_path) as fi:
        urls_list = [url.strip() for url in fi.readlines()]
    


        for urls in urls_list:
            useragent = UserAgent()

            options = webdriver.ChromeOptions()
            options.add_argument(f"user-agent={useragent.random}")

            driver = webdriver.Chrome(executable_path='./chromedriver', options=options)


            try:
                driver.get(url=urls)
                with open('ranobe.html', 'w', encoding='UTF-8') as f:
                    f.write(driver.page_source)

                    html_file = file_path='./ranobe.html'
                    
                    with open(html_file) as file:
                        src = file.read()
                        content = []
                        soup = BS(src, 'lxml')
                        div = soup.find('div', class_ = 'reader reader_text').find_next('div', class_ = 'reader-container container container_center').find_all('p')
                        content.append(div)

                        file_name = re.sub('https://ranobelib.me/', '', urls) + '.html'
                        with open(re.sub('/', '_', file_name), 'w') as fl:
                            for u in content:
                                fl.write(f'{u}\n')

                time.sleep(1)
            except Exception as ex:
                print(ex)
            finally:
                driver.close()
                driver.quit()





# get_source_html и get_url используются для получения ссылок глав!
def main():
    get_source_html(input('Введите ссылку: '))
    # get_url(file_path='./ranobe_url.html')
    # get_content(file_path='./urls.txt')


if __name__ == '__main__':
    main()




