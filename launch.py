import multiprocessing
import os
import sys
import logging
from logging import handlers
from multiprocessing import Process

from cmd.cmd_parser import parse_arguments
from internal import SystemInfo
from internal.env import get_num_cpu_cores
import settings
from settings import LOG_FORMAT, LOG_LEVEL, FASTAPI_APPS, LOG_PATH, DEBUG


class VIPGptLaucher:
    def __init__(self):
        self.init_environment()

    def init_environment(self):
        handler = handlers.RotatingFileHandler(f"{LOG_PATH}/Laucher.log", maxBytes=1024 * 50, backupCount=5, encoding='utf8')
        self.logger = logging.getLogger('launcher')
        self.logger.setLevel(LOG_LEVEL)
        self.logger.addHandler(handler)
        logging.basicConfig(format=LOG_FORMAT)

        os.environ["NUMEXPR_MAX_THREADS"] = str(get_num_cpu_cores())
        sys.path.append(os.path.dirname(os.path.realpath(__file__)))

    def start(self):
        """开多个协程启动各个模块"""
        import signal
        args = parse_arguments()
        settings.DEBUG = args.debug

        processes = dict()

        def handler(signalname):
            def f(signal_received, frame):
                raise KeyboardInterrupt(f"{signalname} received")
            return f

        # 关闭后关掉所有进程
        # fork出来的子进程会继承信号量
        signal.signal(signal.SIGINT, handler("SIGINT"))  # ctrl+c
        signal.signal(signal.SIGTERM, handler("SIGTERM"))  # 终止信号

        self.logger.info(SystemInfo())

        self.logger.info('开始启动服务组件.')
        # 启用fastapi based app
        import importlib
        # threading.Event信号量追踪进程是否开启成功
        START_SYM = multiprocessing.Event()
        for f_app in FASTAPI_APPS:
            self.logger.info(f'Try to load fastapi based app: {f_app}.')
            service = importlib.import_module(f"app.{f_app}.main").FastApiService
            self.logger.info(f'{f_app} loading success.')
            process = Process(
                target=service().start,
                name=f"{f_app} app Server",
                kwargs=dict(sym=START_SYM),
                daemon=True,  # 主进程关闭时自动关闭子进程
            )
            processes[f_app] = process

        for pname, p in processes.items():
            # 子进程内抛出异常，父进程不受影响，需要一个事件来判断是否启动完毕
            p.start()
            p.name = f"VIPGpt:{pname}:{p.pid}"
            START_SYM.wait()
        self.logger.info('启动成功.')
        while True: pass


if __name__ == '__main__':
    laucher = VIPGptLaucher()
    laucher.start()
