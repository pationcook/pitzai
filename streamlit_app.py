import streamlit as st
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()  # 🔥 이거 반드시 root에서 실행되게

from demo.graph import graph

st.set_page_config(page_title="PITZ AI Demo", layout="wide")

st.title("PITZ AI demo")

# 🔥 설명서 UI
with st.expander("📘 시스템 설명"):
    st.markdown("""
    ### 구조
    🧠 Overview

    이 프로젝트는 LangGraph 기반 Multi-Agent AI 시스템으로,
    Researcher / Analyst / Writer가 협업하여 정보를 처리하는 구조입니다.
    - Researcher: RAG로 외부 지식 검색 및 요약
    - Analyst: Researcher의 결과를 분석하여 인사이트 도출
    - Writer: Analyst의 인사이트를 바탕으로 최종 보고서 작성
    ### 특징
    - **LangGraph**: 에이전트 간의 명확한 인터페이스
    - **RAG**: 외부 지식 활용으로 정보의 정확성 및 최신성 확보
    - **Streamlit**: 실시간 결과 시각화 및 사용자 인터랙션
    ### 사용법
    1. 질문 입력: 사이드바에 질문을 입력하세요. 예: "AI 최신 동향"
    2. 실행: "🚀 실행" 버튼을 클릭하면 멀티 에이전트가 작동합니다.
    3. 결과 확인: 각 에이전트의 출력과 최종 보고서를 실시간으로 확인할 수 있습니다.
    4. 토큰 사용량: 사이드바에서 각 단계별 및 누적 토큰 사용량을 모니터링하세요.
    5. 최종 결과: 최종 보고서는 페이지 하단에서 확인할 수 있습니다.
    ### 주의사항
    - API 키: `.env` 파일에 유효한 API 키가 설정되어 있어야 합니다.
    - 토큰 한도: API 사용량에 따른 토큰 한도를 초과하지 않도록 주의하세요.
    """)

query = st.text_input("질문", "AI 최신 동향")

MAX_TOKEN = 100000
final = ""
total_tokens = 0
step_tokens = 0

if st.button("🚀 실행"):

    inputs = {
        "messages": [HumanMessage(content=query)],
        "step": 0,
        "tokens": 0
    }

    config = {"configurable": {"thread_id": "demo_001"}}



    with st.spinner("멀티 에이전트 실행 중..."):

        for event in graph.stream(inputs, config=config, stream_mode="values"):

            if "messages" in event:
                last = event["messages"][-1]
                if hasattr(last, "content"):
                    st.write(last.content)
                    final = last.content   # 🔥 마지막 결과 저장

            if "tokens" in event:
                step_tokens = event["tokens"]
                total_tokens += event["tokens"]

st.sidebar.metric("이번 실행", step_tokens)
st.sidebar.metric("누적 사용량", total_tokens)
st.sidebar.metric("남은 토큰", MAX_TOKEN - total_tokens)

st.sidebar.progress(min(total_tokens / MAX_TOKEN, 1.0))

st.subheader("📄 최종 결과")
st.write(final)



# import streamlit as st
# from dotenv import load_dotenv
# from langchain_core.messages import HumanMessage
# from app.graph import graph

# load_dotenv()

# st.set_page_config(page_title="Galaxy AI Agent", layout="wide")
# st.title("🌌 Galaxy AI Multi-Agent (Parallel + Cache)")
# st.sidebar.title("📊 Token Usage")

# query = st.text_input(
#     "질문 입력",
#     "삼성전자 Galaxy AI 최신 동향"
# )

# if st.button("🚀 실행"):
#     config = {"configurable": {"thread_id": "demo"}}

#     inputs = {
#         "messages": [HumanMessage(content=query)],
#         "tokens": 0,
#         "research_results": []
#     }

#     final_result = ""
#     total_tokens = 0

#     for event in graph.stream(inputs, config=config, stream_mode="values"):

#         if "messages" in event:
#             last = event["messages"][-1]
#             if hasattr(last, "content"):
#                 st.write(last.content)
#                 final_result = last.content
#             else:
#                 st.write(last)
#                 final_result = last

#         if "tokens" in event:
#             total_tokens = event["tokens"]

#     MAX = 100000

#     st.sidebar.metric("사용 토큰", total_tokens)
#     st.sidebar.progress(min(total_tokens / MAX, 1.0))

#     st.subheader("📄 최종 결과")
#     st.write(final_result)