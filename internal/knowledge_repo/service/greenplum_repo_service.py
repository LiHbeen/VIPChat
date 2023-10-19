from langchain.vectorstores import PGVector
from sqlalchemy import text

from public.knowledge_repo.cache.base import embedding_pool
from public.knowledge_repo.common import knowledge_repo_path
from public.knowledge_repo.service import KnowledgeRepoService, VectorStoreType
from langchain.embeddings.base import Embeddings
from typing import List, Dict, Optional
from langchain.docstore.document import Document

from public.langchain.emb.base import EmbeddingsAdapter
from settings import SCORE_THRESHOLD, DEVICE, REPO_CONFIG
from langchain.vectorstores.pgvector import DistanceStrategy


class GreenplumRepoService(KnowledgeRepoService):
    pg_vector: PGVector

    def vs_type(self) -> str:
        return VectorStoreType.GREENPLUM.value

    def do_init(self):
        embeddings = embedding_pool.load(self.embed_model, DEVICE)
        self.pg_vector = PGVector(
            embedding_function=EmbeddingsAdapter(embeddings),
            collection_name=self.repo_name,
            distance_strategy=DistanceStrategy.EUCLIDEAN,
            connection_string=REPO_CONFIG.get("pg").get("connection_uri")
        )

    def do_create(self):
        """pgvector自动创建"""
        pass

    def do_delete(self):
        """删除langchain.gpvector内部实现的相关表的数据"""
        with self.pg_vector.connect() as connect:
            connect.execute(text(f'''
                    -- 删除 langchain_pg_embedding 表中关联到 langchain_pg_collection 表中 的记录
                    DELETE FROM langchain_pg_embedding
                    WHERE collection_id IN (
                      SELECT uuid FROM langchain_pg_collection WHERE name = '{self.repo_name}'
                    );
                    -- 删除 langchain_pg_collection 表中 记录
                    DELETE FROM langchain_pg_collection WHERE name = '{self.repo_name}';
            '''))
            connect.commit()

    def do_search(
        self,
        query: str,
        top_k: int,
        score_threshold: float,
        embeddings: Embeddings,
    ) -> List[Document]:
        pass

    def do_add_doc(self, docs: List[Document], **kwargs) -> List[Dict]:
        ids = self.pg_vector.add_documents(docs)
        doc_infos = [{"id": id, "metadata": doc.metadata} for id, doc in zip(ids, docs)]
        return doc_infos

    def do_delete_doc(self, kb_file, **kwargs):
        pass


if __name__ == '__main__':
    repo_service = GreenplumRepoService(
        repo_name='vip'
    )
    repo_service.do_create()
