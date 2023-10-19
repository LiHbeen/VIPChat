from public.env import get_python_version, get_sys_plat, get_fastapi_version, get_langchain_version


class SystemInfo(object):
    """系统配置信息"""
    def __init__(self):
        self.python_version = get_python_version()
        self.langchain_version = get_langchain_version()
        self.platform = get_sys_plat()
        self.fastapi_version = get_fastapi_version()

    def __str__(self):
        message = "检测到系统信息:\n" + \
            "\n".join([f"{k}: {v}" for k, v in self.__dict__.items()])
        return message