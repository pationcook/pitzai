from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

from agents.agents import (
    research_news,
    research_tech,
    research_market,
    aggregator,
    final_agent
)

# =========================
# State
# =========================
class AgentState(TypedDict):
    messages: list
    tokens: Annotated[int, operator.add]   # 🔥 이거 추가
    research_results: Annotated[list, operator.add]


# =========================
# Graph
# =========================
workflow = StateGraph(AgentState)

# 노드 등록
workflow.add_node("research_news", research_news)
workflow.add_node("research_tech", research_tech)
workflow.add_node("research_market", research_market)

workflow.add_node("aggregator", aggregator)
workflow.add_node("final", final_agent)

# 🔥 병렬 시작
workflow.add_edge(START, "research_news")
workflow.add_edge(START, "research_tech")
workflow.add_edge(START, "research_market")

# 병렬 → aggregator
workflow.add_edge("research_news", "aggregator")
workflow.add_edge("research_tech", "aggregator")
workflow.add_edge("research_market", "aggregator")

# aggregator → final
workflow.add_edge("aggregator", "final")
workflow.add_edge("final", END)

graph = workflow.compile()