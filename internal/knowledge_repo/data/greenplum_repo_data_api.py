from langchain.vectorstores import PGVector
from internal.knowledge_repo.cache.base import embedding_pool
from internal.knowledge_repo.data import KnowledgeRepoDataApi, VectorStoreType
from langchain.embeddings.base import Embeddings
from typing import List, Dict, Optional
from langchain.docstore.document import Document

from internal.langchain.emb.base import EmbeddingsAdapter
from settings import SCORE_THRESHOLD, DEVICE, VS_CONFIG
from langchain.vectorstores.pgvector import DistanceStrategy


class GreenplumRepoDataApi(KnowledgeRepoDataApi):
    pg_vector: PGVector

    def vs_type(self) -> str:
        return VectorStoreType.GREENPLUM.value

    def do_init(self):
        embeddings = embedding_pool.load(self.embed_model, DEVICE)
        self.pg_vector = PGVector(
            embedding_function=EmbeddingsAdapter(embeddings),
            collection_name=self.repo_name,
            distance_strategy=DistanceStrategy.EUCLIDEAN,
            connection_string=VS_CONFIG.get("pg").get("connection_uri")
        )

    def do_create_repo(self):
        """pgvector使用greenplum，不需要创建，需要先安装vector扩展"""
        pass

    def do_delete(self):
        """删除langchain.gpvector内部实现的相关表的数据"""
        with self.pg_vector.connect() as connect:
            connect.execute(f'''
                    -- 删除 langchain_pg_embedding 表中关联到 langchain_pg_collection 表中 的记录
                    DELETE FROM langchain_pg_embedding
                    WHERE collection_id IN (
                      SELECT uuid FROM langchain_pg_collection WHERE name = '{self.repo_name}'
                    );
                    -- 删除 langchain_pg_collection 表中 记录
                    DELETE FROM langchain_pg_collection WHERE name = '{self.repo_name}';
            ''')
            connect.commit()

    def do_search(
        self,
        query: str,
        top_k: int,
        score_threshold: float,
    ) -> List[Document]:
        pass

    def do_add_doc(self, docs: List[Document], **kwargs) -> List[Dict]:
        ids = self.pg_vector.add_documents(docs)
        doc_infos = [{"id": id, "metadata": doc.metadata} for id, doc in zip(ids, docs)]
        return doc_infos

    def do_delete_doc(self, kb_file, **kwargs):
        with self.pg_vector.connect() as connect:
            filepath = kb_file.filepath.replace('\\', '\\\\')
            connect.execute(
                    f''' DELETE FROM langchain_pg_embedding WHERE cmetadata::jsonb @> '{"source": "{filepath}"}'::jsonb;''')
            connect.commit()

    def do_clear(self):
        self.pg_vector.delete_collection()
        self.pg_vector.create_collection()
