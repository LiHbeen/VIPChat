# log
import os
import logging
LOG_FORMAT = "%(levelname)s:     %(message)s"
LOG_LEVEL = logging.INFO
LOG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/logs'

# 启用的fastapi app
FASTAPI_HOST = '127.0.0.1'
FASTAPI_APPS = {
    # 'hello_world': 8080
    'knowledge_repo': 8005,
}
ORIGINS = [
    "*",
]
DEBUG = False

# knowledge repo
KNOWLEDGE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/LOCAL_REPO'
if not os.path.isdir(KNOWLEDGE_PATH):
    os.mkdir(KNOWLEDGE_PATH)
# 向量存储库
VS_CONFIG = {
    "pg": {
        "connection_uri": "postgresql://fastgpt4399:205d649dff2ee998ae64f797bceb5e52@10.0.3.86:5432/vip_gpt_reply",
    }
}
DATABASE_URI = 'mysql+pymysql://ocss_admin:WkdKQWIyTnpjMTh5TURFMg@10.0.3.63:3306/vip_gpt_reply'
# 深度学习
MODEL_PATH = os.path.dirname(os.path.realpath(__file__)) + '/model_repo'
if not os.path.isdir(MODEL_PATH):
    os.mkdir(MODEL_PATH)
import torch
if torch.cuda.is_available():
    DEVICE = "cuda"
elif torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"
# 知识库匹配相关度阈值，取值范围在0-1之间，SCORE越小，相关度越高，取到1相当于不筛选，建议设置在0.5左右
SCORE_THRESHOLD = 1
EMBEDDING_MODEL = 'hfl/chinese-bert-wwm-ext'