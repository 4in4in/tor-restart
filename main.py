
from fastapi import FastAPI
from url_checker import UrlChecker

app = FastAPI()

@app.get('/check_elibrary')
def restart_tor():
    checker = UrlChecker()
    checker.check_elibrary()
    return True
