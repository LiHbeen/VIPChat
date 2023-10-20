from sqlalchemy import Column, Integer, String, func, TIMESTAMP

from internal.knowledge_repo.db.base import Base


class BaseKnowledgeRepoMetadataModel(Base):
    """
    知识库模型
    """
    __tablename__ = 'base_knowledge_repo_metadata'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='知识库ID')
    repo_name = Column(String(50), comment='知识库名称')
    vs_type = Column(String(50), comment='向量库类型')
    embed_model = Column(String(50), comment='嵌入模型名称')
    file_count = Column(Integer, default=0, comment='文件数量')
    creator = Column(String(50), default='', comment='创建人')
    ct = Column(TIMESTAMP, default=func.now(), comment='创建时间')
    ut = Column(TIMESTAMP, default=func.now(), comment='更新时间')

    def __repr__(self):
        return f"<KnowledgeBase(id='{self.id}', kb_name='{self.kb_name}', vs_type='{self.vs_type}', embed_model='{self.embed_model}', file_count='{self.file_count}', create_time='{self.create_time}')>"