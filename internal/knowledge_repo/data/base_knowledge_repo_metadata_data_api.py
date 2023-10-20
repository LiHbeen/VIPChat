from internal.knowledge_repo.db.base import sqlalchemy_data_api
from internal.knowledge_repo.db.model.repo_model import BaseKnowledgeRepoMetadataModel


class BaseKnowledgeRepoMetadataDataApi:
    @classmethod
    def build(cls) -> "BaseKnowledgeRepoMetadataDataApi":
        return cls()

    @sqlalchemy_data_api
    def get_base_knowledge_repo_metadata(self, session, repo_name):
        repo_metadata = session.query(BaseKnowledgeRepoMetadataModel).filter_by(repo_name=repo_name).first()
        return repo_metadata

    @sqlalchemy_data_api
    def create_base_knowledge_repo_metadata(self, session, repo_name, vs_type, embed_model):
        repo_metadata = session.query(BaseKnowledgeRepoMetadataModel).filter_by(repo_name=repo_name).first()
        if not repo_metadata:
            repo_metadata = BaseKnowledgeRepoMetadataModel(repo_name=repo_name, vs_type=vs_type, embed_model=embed_model)
            session.add(repo_metadata)
        return repo_metadata