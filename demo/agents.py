from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from demo.rag import retrieve_context
import os
from langchain_groq import ChatGroq

def get_llm():
    # 환경변수에서 키를 가져오되, 없으면 None 반환
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        # 에러 발생 시 사용자가 알 수 있도록 처리
        st.error("GROQ_API_KEY가 설정되지 않았습니다. Secrets를 확인하세요.")
        return None

    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=200,
        groq_api_key=api_key  # 키를 명시적으로 전달
    )
def estimate_tokens(text: str):
    return int(len(str(text)) / 4)


# =========================
# Researcher (RAG)
# =========================
def researcher_agent(state):
    llm = get_llm()

    query = state["messages"][-1].content
    context = retrieve_context(query)

    system = f"""
You are a Researcher.

Use the context below.

[Context]
{context}

Return concise summary (max 5 lines)
"""

    res = llm.invoke([SystemMessage(content=system)])

    used = estimate_tokens(res.content)

    return {
        "messages": [res],
        "next": "supervisor",
        "step": state.get("step", 0) + 1,
        "tokens": used
    }


# =========================
# Analyst
# =========================
def analyst_agent(state):
    llm = get_llm()

    system = """You are an Analyst.
Extract insights in bullet points.
"""

    messages = [SystemMessage(content=system)] + state["messages"][-2:]

    res = llm.invoke(messages)

    used = estimate_tokens(res.content)

    return {
        "messages": [res],
        "next": "supervisor",
        "step": state.get("step", 0) + 1,
        "tokens": used
    }


# =========================
# Writer
# =========================
def writer_agent(state):
    llm = get_llm()

    system = """You are a Writer.

Write final report in Korean.

Format:
[제목]
[요약]
[핵심]
[결론]
"""

    messages = [SystemMessage(content=system)] + state["messages"][-3:]

    res = llm.invoke(messages)

    used = estimate_tokens(res.content)

    return {
        "messages": [res],
        "next": "supervisor",
        "step": state.get("step", 0) + 1,
        "tokens": used
    }