from agno.tools import tool
from rag import knowledge_base


@tool
def search_knowledge_base(query: str) -> str:
    

    results = knowledge_base.search(query, k=4)

    if not results:
        return "No relevant internal notes found. Fall back to web search."

    return "\n\n---\n\n".join(
        f"[{chunk.source} › {chunk.heading}] (score {score:.2f})\n{chunk.text}"
        for score, chunk in results
    )
