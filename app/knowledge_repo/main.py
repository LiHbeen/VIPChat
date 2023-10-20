import uvicorn
import os
from fastapi import FastAPI
from internal.env import get_sys_plat
from internal.fastapi_setting.cors import allow_cross_domain
from internal.fastapi_setting.event import set_app_event
from settings import FASTAPI_APPS, FASTAPI_HOST, DEBUG
from .routers import docs

VERSION = "0.1.0"
app = FastAPI(
    debug=DEBUG,
    title="知识库api",
    description="知识库api",
    version=VERSION,
)
app.include_router(docs.router)


class FastApiService:
    def start(self, sym):
        set_app_event(app, sym)
        allow_cross_domain(app)
        plat = get_sys_plat()
        if plat == 'windows':
            service_name = os.path.dirname(os.path.realpath(__file__)).split('\\')[-1]
        elif plat == 'linux':
            service_name = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
        else:
            raise Exception(f'不支持的系统:{plat}')
        uvicorn.run(app=f"app.{service_name}.main:app", host=FASTAPI_HOST, port=FASTAPI_APPS[service_name])
