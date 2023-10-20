import os

from settings import KNOWLEDGE_PATH


def knowledge_repo_path(repo_name):
    return os.path.join(KNOWLEDGE_PATH, repo_name)


def docs_path(repo_name):
    return os.path.join(knowledge_repo_path(repo_name), "docs")


def validate_repo_name(repo_name):
    """True则验证通过"""
    if repo_name is None or repo_name.strip() == "":
        return False
    if '..' in repo_name:
        return False
    return True