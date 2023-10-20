import os
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

from fastapi import APIRouter, UploadFile

from app.base import ResponseModel, Code
from internal.knowledge_repo.biz.docs_biz import DocsBizApi
from internal.knowledge_repo.common import validate_repo_name, docs_path
from internal.threading_utils import add_task_to_thread_pool
from settings import VS_TYPE, EMBEDDING_MODEL

router = APIRouter(
    prefix="/knowledge_repo/docs",
    tags=["知识库文档上传"],
)


@router.get("/add", response_model=ResponseModel)
async def add(
    files: List[UploadFile],
    repo_name: str,
    override: bool,
    chunk_size: int,
    chunk_overlap: int,
) -> ResponseModel:
    """
    提交文档->分片->计算向量->存储
    :param files: 上传文件，支持多文件
    :param repo_name: 知识库名称
    :param override: 覆盖文件
    :param chunk_size: 知识库中单段文本最大长度
    :param chunk_overlap: 知识库中相邻文本重合长度
    :return:
    """
    docs_biz_api = DocsBizApi(repo_name, VS_TYPE, EMBEDDING_MODEL)
    validate_repo_name(repo_name)
    uploaded_files, fail_upload_files = batch_upload(files, repo_name, override)
    fail_vector_files = []
    # result = docs_biz_api.add_docs(
    #     repo_name=repo_name,
    #     file_names=uploaded_files,
    #     override=True,
    #     chunk_size=chunk_size,
    #     chunk_overlap=chunk_overlap,
    # )
    # # fail_vector_files.update(result.data["failed_files"])
    return ResponseModel(
        code=Code.SUCCESS,
        message='上传成功',
        data={
            'fail_upload_files': fail_upload_files,
            'fail_vector_files': fail_vector_files,
        }
    )


def batch_upload(
    files: List[UploadFile],
    repo_name: str,
    override: bool,
):
    """
    使用线程池接收批量文件
    :param files:
    :param repo_name: 知识库名字
    :param override: 覆盖原有文件
    :return:
    """
    params = [
        ([], {"file": file, "repo_name": repo_name, "override": override})
        for file in files
    ]
    uploaded_files = []
    fail_upload_files = []
    for uploaded_filename in add_task_to_thread_pool(
        func=save_file,
        params=params,
        use_local_executor=False,
    ):
        status, filename = uploaded_filename
        if status:
            uploaded_files.append(uploaded_filename)  # 上传成功
        else:
            fail_upload_files.append(filename)
    return uploaded_files, fail_upload_files


def save_file(
    file: UploadFile,
    repo_name: str,
    override: bool,
):
    """
    接收文件
    :param files:
    :param repo_name: 知识库名字
    :param override: 覆盖原有文件
    :return: status, filename
    """
    status = True
    filename = file.filename
    try:
        file_path = f"{docs_path(repo_name)}/{filename}"
        file_content = file.file.read()
        if os.path.isfile(file_path) and override:
            with open(file_path, "wb") as f:
                f.write(file_content)
        elif os.path.isfile(file_path) and not override:
            pass
        else:
            with open(file_path, "wb") as f:
                f.write(file_content)
    except:
        status = False
    return status, filename