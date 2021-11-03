
from fastapi import FastAPI, Request
from driver_checker import DriverChecker

app = FastAPI()

@app.post('/check_elibrary')
async def restart_tor(req: Request):
    data = await req.json()
    link = data.get('link')
    if link:
        checker = DriverChecker()
        checker.check_elibrary(link)
        return True
    else:
        return False