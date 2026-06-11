from langchain_core.documents import Document

from vector_store import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
import config_data as config
from file_history_store import get_history


def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt


class RagService(object):
    def __init__(self):
        self.vector_store = VectorStoreService(DashScopeEmbeddings())

        self.model = ChatTongyi(model=config.CHAT_MODEL_NAME)

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "请以提供的资料为主，回答用户提问，资料为：{context}"),
            ("system", "并且我提供用户对话历史如下："),
            MessagesPlaceholder("chat_history"),
            ("human", "用户提问：{input}"),
        ])

        self.chain = self._get_chain()

    def _get_chain(self):
        retriever = self.vector_store.get_retriever()

        def format_docs(docs: list[Document]):

            if docs is None:
                return "无参考资料"

            doc_content = ""
            for doc in docs:
                doc_content += f"文档片段:{doc.page_content}\n 文档元数据：{doc.metadata} \n\n"
            return doc_content

        def format_for_retriever(value: dict) -> str:
            return value["input"]

        def format_for_prompt_template(value: dict) -> dict:
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["chat_history"] = value["input"]["chat_history"]
            return new_value

        chain = {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(format_for_retriever) | retriever | format_docs
                } | RunnableLambda(format_for_prompt_template) | self.prompt_template | print_prompt | self.model | StrOutputParser()

        new_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="chat_history"
        )

        return new_chain


if __name__ == '__main__':
    # {'input': 'foo'}, {'configurable': {'session_id': '[your-value-here]'}}
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    res = RagService().chain.invoke({"input": "禅道账号密码是什么?"},session_config)
    print(res)
