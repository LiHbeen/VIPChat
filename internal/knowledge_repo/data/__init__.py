import abc
import os
from enum import Enum
from typing import Union, List, Dict
from abc import abstractmethod

from langchain.embeddings.base import Embeddings
from langchain.schema import Document

from internal.knowledge_repo.common import knowledge_repo_path, docs_path
from settings import EMBEDDING_MODEL


class VectorStoreType(Enum):
    GREENPLUM = 'greenplum'


class KnowledgeRepoDataApi(abc.ABC):
    """数据层接口"""
    def __init__(
        self, repo_name: str, embed_model: str = None, vector_name: str = "vector_store"
    ):
        self.repo_name = repo_name
        self.embed_model = embed_model
        self.vector_name = vector_name
        self.repo_path = knowledge_repo_path(self.repo_name)
        self.doc_path = docs_path(self.repo_name)
        self.vs_path = self.get_vs_path()
        self.do_init()

    def get_vs_path(self):
        return os.path.join(knowledge_repo_path(self.repo_name), self.vector_name)

    @abstractmethod
    def do_init(self):
        pass

    @abstractmethod
    def do_create_repo(self):
        """
        创建知识库向量存储库
        """
        pass

    @abstractmethod
    def do_delete(self):
        """
        删除知识库
        """
        pass

    @abstractmethod
    def vs_type(self) -> str:
        """向量存储类型"""
        pass

    @abstractmethod
    def do_search(
        self,
        query: str,
        top_k: int,
        score_threshold: float,
    ) -> List[Document]:
        """
        搜索知识库相关的文档片段
        """
        pass

    @abstractmethod
    def do_add_doc(self, docs: List[Document], **kwargs) -> List[Dict]:
        pass

    @abstractmethod
    def do_delete_doc(self, kb_file, **kwargs):
        pass

    @abstractmethod
    def do_clear(self):
        pass

    def create_repo(self):
        """创建知识库"""
        if not os.path.isdir(knowledge_repo_path(self.repo_name)):
            os.mkdir(knowledge_repo_path(self.repo_name))
        if not os.path.isdir(docs_path(self.repo_name)):
            os.mkdir(docs_path(self.repo_name))
        self.do_create_repo()

    def search_docs(self):
        """文档搜索"""
        docs = self.do_search()
        return docs

    def clear_vs(self):
        """清除相关表的所有数据"""
        self.do_clear()

    def delete_repo(self):
        """删除知识库"""
        pass

    def add_doc(self):
        pass

    def delete_doc(self):
        pass

    def update_doc(self):
        pass

    def exist_doc(self):
        pass

    def count_file(self):
        pass

    def get_doc_by_id(self):
        pass

    def list_doc(self):
        pass


class KnowledgeRepoDataApiFactory:
    @classmethod
    def build(cls, repo_name: str, vs_type: Union[str, VectorStoreType], embed_model: str = EMBEDDING_MODEL) -> KnowledgeRepoDataApi:
        """
        :param repo_name: 知识库名字
        :param vs_type: 向量存储类型
        :return:
        """
        if isinstance(vs_type, str):
            vs_type = VectorStoreType(vs_type)
        if vs_type == VectorStoreType.GREENPLUM:
            from internal.knowledge_repo.data.greenplum_repo_data_api import GreenplumRepoDataApi
            return GreenplumRepoDataApi(
                repo_name=repo_name, embed_model=embed_model
            )
        else:
            raise ValueError(f'unsupported vector store `{vs_type}`.')


