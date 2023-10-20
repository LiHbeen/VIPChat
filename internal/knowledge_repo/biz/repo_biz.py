from typing import Union

from internal.knowledge_repo.common import validate_repo_name
from internal.knowledge_repo.data import KnowledgeRepoDataApiFactory, VectorStoreType
from internal.knowledge_repo.data.base_knowledge_repo_metadata_data_api import BaseKnowledgeRepoMetadataDataApi


class KnowledgeRepoBizApi:
    """业务层"""
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

    def create_repo(
        self
    ) -> None:
        knowledge_info = self.base_knowledge_data_api.get_base_knowledge_repo_metadata(self.repo_name)
        if knowledge_info is not None:
            raise RuntimeError(f"已存在同名知识库 {self.repo_name}")
        self.repo_data_api.create_repo()
        self.base_knowledge_data_api.create_base_knowledge_repo_metadata(
            repo_name=self.repo_name,
            vs_type=self.vs_type,
            embed_model=self.embed_model
        )


if __name__ == '__main__':
    from settings import EMBEDDING_MODEL

    biz_api = KnowledgeRepoBizApi(
        repo_name='vip_test',
        vs_type='greenplum',
        embed_model=EMBEDDING_MODEL,
    )
    biz_api.create_repo()
