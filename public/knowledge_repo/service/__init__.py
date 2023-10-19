import abc
import os
from enum import Enum
from typing import Union, List
from abc import abstractmethod

from langchain.embeddings.base import Embeddings
from langchain.schema import Document

from public.knowledge_repo.common import knowledge_repo_path, docs_path


class VectorStoreType(Enum):
    GREENPLUM = 'greenplum'


class KnowledgeRepoService(abc.ABC):
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
    def do_create(self):
        """
        创建知识库
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
        embeddings: Embeddings,
    ) -> List[Document]:
        """
        搜索知识库相关的文档片段
        """
        pass


class KnowledgeRepoServiceFactory:
    @classmethod
    def build(cls, repo_name: str, vs_type: Union[str, VectorStoreType]) -> KnowledgeRepoService:
        """
        :param repo_name: 知识库名字
        :param vs_type: 向量存储类型
        :return:
        """
        if isinstance(vs_type, str):
            vs_type = VectorStoreType(vs_type)
        if vs_type == VectorStoreType.GREENPLUM:
            from public.knowledge_repo.service.greenplum_repo_service import GreenplumRepoService
            return GreenplumRepoService(
                repo_name
            )
        else:
            raise ValueError(f'unsupported vector store `{vs_type}`.')


