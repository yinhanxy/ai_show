import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库文件上传服务")

upload_file = st.file_uploader(
    label="请上传文件",
    type=['txt'],
    accept_multiple_files=False,
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024 #KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小{file_size:.2f} KB")

    txt = upload_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中。。。"):
        time.sleep(2)
        res = st.session_state["service"].upload_by_str(txt, file_name)
        st.write(res)