import sys

import fastapi
import langchain


def get_num_cpu_cores():
    import numexpr
    n_cores = numexpr.utils.detect_number_of_cores()
    return n_cores


def get_sys_plat():
    import sys
    plat = sys.platform
    if plat.startswith('win'):
        plat = 'windows'
    elif plat.startswith('linux'):
        plat = 'linux'
    return plat


def get_langchain_version():
    return langchain.__version__


def get_python_version():
    return sys.version


def get_fastapi_version():
    return fastapi.__version__
