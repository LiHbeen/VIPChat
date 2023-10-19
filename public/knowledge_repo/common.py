import os

from settings import KNOWLEDGE_PATH


def knowledge_repo_path(repo_name):
    return os.path.join(KNOWLEDGE_PATH, repo_name)


def docs_path(repo_name):
    return os.path.join(knowledge_repo_path(repo_name), "docs")