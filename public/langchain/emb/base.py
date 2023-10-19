from typing import List

import numpy
from langchain.embeddings.base import Embeddings
from sklearn.preprocessing import normalize


class EmbeddingsAdapter(Embeddings):
    """适配langchain.gpvector，对embedding额外做了一次正则化再存入db"""
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return normalize(self.embeddings.embed_documents(texts))

    def embed_query(self, text: str) -> List[float]:
        query_embed = self.embeddings.embed_query(text)
        query_embed_2d = numpy.reshape(query_embed, (1, -1))  # 将一维数组转换为二维数组
        normalized_query_embed = normalize(query_embed_2d)
        return normalized_query_embed[0].tolist()  # 将结果转换为一维数组并返回