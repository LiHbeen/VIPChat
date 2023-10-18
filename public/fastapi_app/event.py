import multiprocessing

from fastapi import FastAPI


def set_app_event(app: FastAPI, started_event: multiprocessing.Event = None):
    """fastapi app设置启动事件，用于追踪launcher是否全部正常启动"""
    @app.on_event("startup")
    async def on_startup():
        if started_event is not None:
            started_event.set()