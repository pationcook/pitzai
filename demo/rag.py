from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=3)

def retrieve_context(query: str) -> str:
    try:
        results = search.invoke(query)

        texts = []
        for r in results:
            texts.append(r.get("content", ""))

        # 🔥 길이 제한 (토큰 절약 핵심)
        context = "\n".join(texts)[:1000]

        return context

    except Exception as e:
        return f"검색 실패: {str(e)}"