from selenium import webdriver
import json
import subprocess
import time

class DriverChecker:

    __remote_addr = 'http://10.32.1.21:4444/wd/hub'
    __preferences = (
        ("network.proxy.type", 1),
        ("network.proxy.socks", "tor-proxy"),
        ("network.proxy.socks_port", 9050)
    )

    def __init__(self):
        self.__driver = webdriver.Remote(
            command_executor=self.__remote_addr,
            options=self.__get_tor_options()
        )

    def __del__(self):
        self.__driver.quit()
        print('shutdown the driver...')

    def __get_tor_options(self):
        options = webdriver.FirefoxOptions()
        for preference in self.__preferences:
            options.set_preference(*preference)
        return options

    def check_elibrary(self, link):
        print(f'checking link {link}...')
        availability = False
        while not availability:
            self.__driver.get(link)
            if 'eLIBRARY.RU' in self.__driver.title:
                availability = True
                print('link is available!')
            else:
                self.restart_tor()

        return availability
    
    def restart_tor(self):
        print('restarting tor...')
        rc = subprocess.Popen('./restart-tor.sh', stdout=subprocess.PIPE)
        rc.wait()
        if rc.returncode != 0:
            raise Exception('Error while restarting docker container')
        time.sleep(2)

if __name__ == '__main__':
    checker = DriverChecker()
    
    print(checker.check_elibrary('https://www.elibrary.ru/querybox.asp'))
