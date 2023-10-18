# log
import os
import logging
LOG_FORMAT = "%(levelname)s:     %(message)s"
LOG_LEVEL = logging.INFO
LOG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/logs'

# 启用的fastapi app
FASTAPI_HOST = '127.0.0.1'
FASTAPI_APPS = {
    'hello_world': 8080
}