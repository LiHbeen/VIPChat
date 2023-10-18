import uvicorn
import os
from fastapi import FastAPI

from public.env import get_sys_plat
from public.fastapi_app.event import set_app_event
from settings import FASTAPI_APPS, FASTAPI_HOST

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/error")
async def error():
    raise Exception()


class FastApiService:
    def start(self, sym):
        set_app_event(app, sym)
        plat = get_sys_plat()
        if plat == 'windows':
            service_name = os.path.dirname(os.path.realpath(__file__)).split('\\')[-1]
        elif plat == 'linux':
            service_name = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
        else:
            raise Exception(f'不支持的系统:{plat}')
        uvicorn.run(app=f"app.{service_name}:app", host=FASTAPI_HOST, port=FASTAPI_APPS[service_name])


if __name__ == '__main__':
    service = FastApiService()
    service.start()
