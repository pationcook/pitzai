
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage

from demo.agents import researcher_agent, analyst_agent, writer_agent

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    step: int
    tokens: Annotated[int, operator.add]   # 누적

workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_agent)
workflow.add_node("analyst", analyst_agent)
workflow.add_node("writer", writer_agent)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

graph = workflow.compile()