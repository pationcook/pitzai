from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from utils.cache import get_cache, set_cache

# 🔥 lazy LLM
def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=200
    )

def estimate_tokens(text: str) -> int:
    return int(len(str(text)) / 4)


# =========================
# 병렬 Researcher 생성
# =========================
def create_researcher(role):

    def node(state):
        llm = get_llm()

        user_input = state["messages"][-1].content

        cache_key = f"research:{role}:{user_input}"
        cached = get_cache(cache_key)

        if cached:
            return {
                "research_results": [cached],
                "tokens": state.get("tokens", 0)
            }

        system = f"""
You are a Researcher ({role})

Focus only on:
{role}

Return concise summary (max 5 lines)
"""

        messages = [SystemMessage(content=system)] + state["messages"][-2:]

        response = llm.invoke(messages)
        content = response.content.strip()

        set_cache(cache_key, content)

        return {
            "research_results": [content],
            "tokens": state.get("tokens", 0) + estimate_tokens(content)
        }

    return node


# =========================
# Aggregator
# =========================
def aggregator(state):
    combined = "\n\n".join(state.get("research_results", []))

    return {
        "messages": [combined],
        "tokens": state.get("tokens", 0)
    }


# =========================
# Final Agent
# =========================
def final_agent(state):
    llm = get_llm()

    combined = "\n".join(state.get("research_results", []))
    cache_key = f"final:{combined}"

    cached = get_cache(cache_key)
    if cached:
        return {
            "messages": [cached],
            "tokens": state.get("tokens", 0)
        }

    system = """You are a Senior AI Analyst.

Write final report in Korean.

Format:
[제목]
[요약]
[핵심 포인트]
[결론]
"""

    messages = [SystemMessage(content=system), combined]

    response = llm.invoke(messages)
    content = response.content

    set_cache(cache_key, content)

    return {
        "messages": [content],
        "tokens": state.get("tokens", 0) + estimate_tokens(content)
    }


# =========================
# export
# =========================
research_news = create_researcher("Latest News")
research_tech = create_researcher("Technology")
research_market = create_researcher("Market Analysis")