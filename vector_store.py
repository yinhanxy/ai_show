from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    def __init__(self, embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.COLLECTION_NAME,
            embedding_function=self.embedding,
            persist_directory=config.PERSIST_DIRECTORY,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.SIMILAR_DOCUMENT_NUM})


if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorStoreService(DashScopeEmbeddings()).get_retriever()
    res = retriever.invoke("onelink地址是什么")
    print(res)
