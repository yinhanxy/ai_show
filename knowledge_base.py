"""
知识库服务
"""
import datetime
import os

import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def check_md5(md5_str: str):
    if not os.path.exists(config.MD5_PATH):
        open(config.MD5_PATH, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(config.MD5_PATH, 'r', encoding="utf-8").readlines():
            line = line.strip()
            if md5_str == line:
                return True

        return False


def save_md5(md5_str: str):
    with open(config.MD5_PATH, 'a', encoding="utf-8") as f:
        f.write(md5_str + "\n")


def get_str_md5(input_str: str, encoding="utf-8"):
    md5_str = hashlib.md5(input_str.encode(encoding)).hexdigest()

    return md5_str


class KnowledgeBaseService(object):

    def __init__(self):
        os.makedirs(config.PERSIST_DIRECTORY, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.COLLECTION_NAME,
            embedding_function=DashScopeEmbeddings(),
            persist_directory=config.PERSIST_DIRECTORY,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=config.SEPARATORS,
            length_function=len,
        )

    def upload_by_str(self, data, filename):

        md5 = get_str_md5(data)

        if check_md5(md5):
            return "[跳过]数据已存在知识库中"

        if len(data) > config.CHUNK_SIZE:
            chuck_texts = self.spliter.split_text(data)
        else:
            chuck_texts = [data]

        metadata = {
            "source": filename,
            "md5": md5,
            "create_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "create_user": "user100",
        }

        self.chroma.add_texts(
            chuck_texts,
            metadatas = [metadata for _ in chuck_texts],
        )

        save_md5(md5)

        return "[成功]数据成功加载到知识库中"


if __name__ == '__main__':
    service = KnowledgeBase()
    print(service.upload_by_str("张三","file_001"))
    # r1 = get_str_md5("周杰伦")
    # print(r1)
    # r2 = get_str_md5("周杰伦")
    # print(r2)
    # r3 = get_str_md5("周杰伦2")
    # print(r3)
    # save_md5("7a8941058aaf4df5147042ce104568da")
    # print(check_md5("7a8941058aaf4df5147042ce104568da"))
