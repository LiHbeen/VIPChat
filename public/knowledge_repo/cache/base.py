from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
import threading
from contextlib import contextmanager
from collections import OrderedDict
from typing import List, Any, Union, Tuple, Dict

from settings import DEVICE, EMBEDDING_MODEL


class ThreadSafeCacheKV:
    """线程安全的kv键值对对象"""
    def __init__(
        self,
        key: Union[str, Tuple],
        value: Any = None,
        pool: "CachePool" = None,
    ):
        self._key = key
        self._value = value
        self._pool = pool
        self._lock = threading.RLock()
        self._load_event = threading.Event()
        self.on_start()

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: key: {self._key}, obj: {self._value}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: key: {self._key}, obj: {self._value}>"

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: Any):
        self._value = v

    def on_start(self):
        self._load_event.clear()

    def on_load(self):
        self._load_event.wait()

    def on_finish(self):
        self._load_event.set()

    @contextmanager
    def acquire(self):
        try:
            self._lock.acquire()
            if self._pool is not None:
                self._pool._cache.move_to_end(self._key)  # 最新访问的数据放到队尾
            yield self.value  # 上下文管理器应用yield
        finally:
            self._lock.release()


class CachePool:
    """实现线程安全的缓存，按最久时间替换缓存值"""
    def __init__(self, capity: int = -1):
        self._capity = capity
        self._cache = OrderedDict()
        self.atomic = threading.RLock()  # 同时间只允许一个加载操作

    def keys(self) -> List[str]:
        return list(self._cache.keys())

    def _fifo(self):
        """FIFO淘汰策略"""
        if isinstance(self._capity, int) and self._capity > 0:
            while len(self._cache) > self._capity:
                self._cache.popitem(last=False)

    def get(self, key: Union[str, Tuple]) -> ThreadSafeCacheKV:
        cache: ThreadSafeCacheKV = self._cache.get(key)
        if cache is not None:
            cache.on_load()  # KV对正在修改时不可读
        return cache

    def set(self, key: str, obj: ThreadSafeCacheKV) -> ThreadSafeCacheKV:
        self._cache[key] = obj
        self._fifo()
        return obj

    def pop(self, key: str = None) -> ThreadSafeCacheKV:
        if key is None:
            k, v = self._cache.popitem(last=False)
            return v
        else:
            return self._cache.pop(key, None)

    def acquire(self, key: Union[str, Tuple]):
        cache = self.get(key)
        if cache is None:
            raise RuntimeError(f"CachePool {key} not found.")
        elif isinstance(cache, ThreadSafeCacheKV):
            return cache.acquire()
        else:
            return cache


class EmbeddingPool(CachePool):
    def load(self, model: str = None, device: str = None):
        self.atomic.acquire()
        model = model or EMBEDDING_MODEL
        device = device or DEVICE
        key = (model, device)
        if not self.get(key):
            # 待当前线程加载完后，其他线程才可以读取pool里面的kv
            item = ThreadSafeCacheKV(key, pool=self)
            self.set(key, item)
            with item.acquire():
                self.atomic.release()  # 同时间只有一个加载线程
                embeddings = HuggingFaceBgeEmbeddings(
                    model_name=model,
                    model_kwargs={'device': device}
                )
                item.value = embeddings
                item.on_finish()
        else:
            self.atomic.release()
            return self.get(key).value
