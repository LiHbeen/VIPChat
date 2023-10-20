from typing import Union, List

from fastapi import UploadFile

from internal.knowledge_repo.common import validate_repo_name
from internal.knowledge_repo.data import KnowledgeRepoDataApiFactory, VectorStoreType
from internal.knowledge_repo.data.base_knowledge_repo_metadata_data_api import BaseKnowledgeRepoMetadataDataApi


class DocsBizApi:
    """文档相关的业务层"""
    def __init__(self, repo_name: str, vs_type: Union[str, VectorStoreType], embed_model: str):
        """
        :param repo_name: 知识库名字
        :param vs_type: 向量存储类型
        """
        self.repo_name = repo_name
        self.embed_model = embed_model
        if isinstance(vs_type, str):
            vs_type = VectorStoreType(vs_type)
        self.vs_type = vs_type
        if not validate_repo_name(self.repo_name):
            raise ValueError("知识库名包含非法字符")
        if self.repo_name is None or self.repo_name.strip() == "":
            raise ValueError("知识库名不能为空")
        self.repo_data_api = KnowledgeRepoDataApiFactory.build(
            repo_name=repo_name,
            vs_type=vs_type,
            embed_model=embed_model
        )
        self.base_knowledge_data_api = BaseKnowledgeRepoMetadataDataApi.build()

    def add_docs(
        self,
        repo_name: str,
        file_names: List[UploadFile],
        override: bool,
        chunk_size: int,
        chunk_overlap
    ):
        """
        添加文档到repo路径，并分片向量化
        :param files: 上传文件，支持多文件
        :param repo_name: 知识库名称
        :param override: 覆盖文件
        :param chunk_size: 知识库中单段文本最大长度
        :param chunk_overlap: 知识库中相邻文本重合长度
        """
        if not validate_repo_name(self.repo_name):
            raise ValueError("知识库名未通过验证")

        knowledge_info = self.base_knowledge_data_api.get_base_knowledge_repo_metadata(self.repo_name)
        if knowledge_info is not None:
            raise RuntimeError(f"知识库 {self.repo_name} 不存在.")
        return ''

