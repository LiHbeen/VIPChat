from concurrent.futures.thread import ThreadPoolExecutor
from typing import Callable, Dict, List, Tuple

from internal.env import get_num_cpu_cores

local_executor = ThreadPoolExecutor(max_workers=get_num_cpu_cores())


def add_task_to_thread_pool(
    func: Callable,
    params: List[Tuple[List, Dict]],
    use_local_executor: bool = False
):
    """
    使用高级封装的线程池并发执行任务，通过future生成器返回结果
    参见https://docs.python.org/zh-cn/3/library/concurrent.futures.html
    :param func:
    :param params:
    :param use_local_executor:
    :return:
    """
    executor = local_executor if use_local_executor else ThreadPoolExecutor(max_workers=get_num_cpu_cores())
    list_future = []
    for param in params:
        args, kwargs = param
        future = executor.submit(func, *args, **kwargs)
        list_future.append(future)
    # as_completed()方法是一个生成器，在没有任务完成的时候，会阻塞，
    # 在有某个任务完成的时候，会yield这个任务，就能执行for循环下面的
    # 语句，然后继续阻塞住，循环到所有的任务结束
    for future in list_future:
        yield future.result()
