
MD5_PATH ="./data/md5.txt"

# chroma
COLLECTION_NAME = "rag"
PERSIST_DIRECTORY = "./chroma_db"

# spliter
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50
SEPARATORS = ["\n\n","\n",".","!","?","。","！","？"," ",""]

#
SIMILAR_DOCUMENT_NUM = 2

#
CHAT_MODEL_NAME = "qwen3-max"

SESSION_CONFIG = {
        "configurable": {
            "session_id": "user_001"
        }
    }