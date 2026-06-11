from rag import RagService
import streamlit as st
import config_data as config

st.title("智能助手")
st.divider()

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

if "history" not in st.session_state:
    st.session_state["history"] = [{"role":"assistant","content":"你好，有什么可以帮你？"}]

for message in st.session_state["history"]:
    st.chat_message(message["role"]).write(message["content"])

input = st.chat_input()

if input:
    st.chat_message("user").write(input)
    st.session_state["history"].append({"role":"user","content":input})

    ai_res_list = []
    with st.spinner("思考中。。。"):
        res_stream = st.session_state["rag"].chain.stream({"input":input},config.SESSION_CONFIG)

        def capture(genetor,cache_list):
            for chuck in genetor:
                cache_list.append(chuck)
                yield chuck

        st.chat_message("assistant").write_stream(capture(res_stream,ai_res_list))
        st.session_state["history"].append({"role":"assistant","content":"".join(ai_res_list)})


