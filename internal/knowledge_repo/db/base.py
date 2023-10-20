"""通过orm在mysql保存知识库的基本信息"""
from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

from settings import DATABASE_URI

engine = create_engine(
    DATABASE_URI,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
)
Base = declarative_base()  # 模型基类
Base.metadata.create_all(bind=engine)  # 自动创建表
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#creating-a-session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 封装sqlalchemy的session模块，自动打开关闭session，自动提交、回滚事务
@contextmanager
def session_scope():
    """
    自动打开关闭session
    >>> from internal.knowledge_repo.db.model.repo_model import KnowledgeBaseModel
    >>> with session_scope() as session:
    >>>     session.add(KnowledgeBaseModel(...))
    """
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def sqlalchemy_data_api(f):
    """专注处理data层"""
    @wraps(f)
    def _wrap_func(self, *args, **kwargs):
        with session_scope() as session:
            result = f(self, session, *args, **kwargs)
        return result

    return _wrap_func