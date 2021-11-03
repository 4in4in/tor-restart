
import requests
import time
import subprocess

class UrlChecker:

    __proxies = dict(
        http='socks5://10.32.1.21:9050',
        https='socks5://10.32.1.21:9050'
    )

    def __init__(self) -> None:
        self.__session = self.__create_session()

    def __del__(self):
        self.__session.close()

    def __create_session(self):
        session = requests.session()
        session.proxies = self.__proxies
        return session

    def get_current_ip(self):
        ip_check_url = 'http://httpbin.org/ip'
        get_ip = lambda req_obj: req_obj.get(ip_check_url).json().get('origin', 'not found')
        req_objects = dict(tor=self.__session, normal=requests)
        ips = dict(((req_obj, get_ip(req_objects[req_obj])) for req_obj in req_objects))
        return ips

    def check_elibrary(self):
        status = 0
        while status != 200:
            print('getting elibrary')
            elib_req = self.__session.get('https://www.elibrary.ru', timeout=2)
            status = elib_req.status_code
            if status != 200:
                self.restart_tor()
        print(status)

    def restart_tor(self):
        print('restarting tor...')
        rc = subprocess.Popen('./restart-tor.sh', stdout=subprocess.PIPE)
        rc.wait()
        if rc.returncode != 0:
            raise Exception('Error while restarting docker container')
        time.sleep(2)
    
    

if __name__ == '__main__':
    url_checker = UrlChecker()
    url_checker.check_elibrary()
