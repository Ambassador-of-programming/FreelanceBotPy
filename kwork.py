from undetected_chromedriver import By
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep

import undetected_chromedriver as uc
import json
import datetime


class Kwork():
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.user_agent = UserAgent().chrome
        self.options_chrome = uc.ChromeOptions().add_argument(f'user-agent={self.user_agent}')
        self.driver = uc.Chrome(headless=True, use_subprocess=False, 
            options=self.options_chrome, version_main=124)
    
    def check_login(self) -> bool:
        """ Check that the user is authorized on the site """

        self.driver.get('https://kwork.ru/inbox')
        dialog = self.driver.page_source
        soup = BeautifulSoup(dialog, 'html.parser')
        if soup.find('a', class_='login-js'):
            return False
        else:
            return True

    def log_in(self):
        """ If the user is not authorized we perform the authorization and save the cookie """

        try:
            self.driver.get('https://kwork.ru/')
            sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, 'a[class="login-js"]').click()
            sleep(2)
            username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
            username_input.clear()
            username_input.send_keys(self.login)
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
            password_input.clear()
            password_input.send_keys(self.password)
            self.driver.find_element(By.CSS_SELECTOR,
                'button[class="signin-signup__content-button kw-button kw-button--size-40 kw-button--green"]').click()
            sleep(5)
            # Добавляем куки в браузер
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except:
            pass

    def online(self):
        """
        Using cookies, log in to your profile and in a perpetual loop stay constantly 
        online and refresh the page every 30 seconds
        """

        while True:
            self.driver.get('https://kwork.ru/inbox')
            page_sourse = self.driver.page_source
            soup = BeautifulSoup(page_sourse, 'html.parser')
            if soup.find('a', class_='login-js'):
                self.log_in()
            else:
                sleep(15)
                self.driver.refresh()
                sleep(15)

if __name__ == '__main__':
    try:
        with open('config/all_data.json', "r") as read:
            data = json.loads(read.read()) 
        kwork = Kwork(login=data['kwork.ru']['login'], password=data['kwork.ru']['password'])
        kwork.online()

    except Exception as e:
        with open(file='error.txt', mode='a+') as write:
            write.write(f'Date: {datetime.datetime.today()} | {str(e)}\n')

# docker run -it --rm --name kwork-app -v /dev/shm:/dev/shm kwork   