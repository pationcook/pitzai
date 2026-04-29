from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def search_web(query: str) -> str:
    """웹 검색 도구"""
    search = TavilySearchResults(max_results=3)
    return search.invoke(query)

@tool
def python_repl(code: str) -> str:
    """파이썬 코드 실행 도구"""
    from langchain_experimental.utilities import PythonREPL
    repl = PythonREPL()
    return repl.run(code)

tools = [search_web, python_repl]