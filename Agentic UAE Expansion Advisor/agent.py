import os 
from agno.agent import Agent
#from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.utils.pprint import pprint_run_response
# from agno.app.playground import Playground
#from agno.app.playground import serve_playground_app
#from menu_scraper import scrape_and_clean
from agno.models.groq import Groq

from tools.competitor_finder import find_competitors
from tools.competitor_menu_tool import analyze_competitor_menu
from tools.knowledge_tool import search_knowledge_base
from agno.db.in_memory import InMemoryDb




from dotenv import load_dotenv
load_dotenv()

try:
    import streamlit as st
    for _k in ("GROQ_API_KEY", "EXA_API_KEY", "OPENAI_API_KEY"):
        if _k in st.secrets and not os.getenv(_k):
            os.environ[_k] = str(st.secrets[_k])
except Exception:
    pass

api_key = os.getenv("GROQ_API_KEY")
exa_key = os.getenv("EXA_API_KEY")
db = InMemoryDb()


SYSTEM_PROMPT = SYSTEM_PROMPT = """
Role:
You advise a Jordanian restaurant specializing in meaty pizza and kebab sandwiches on expansion into the UAE.

Target cities:
Dubai and Abu Dhabi.

Objective:
Provide clear, practical recommendations for market entry.

Core topics to cover:
1. Best locations for branches
2. Competitor landscape
3. Menu adaptation for UAE customers
4. Pricing strategy
5. Marketing strategy

Also include at least THREE additional considerations such as:
operations, delivery strategy, licensing, supply chain, staffing, or expansion risks.

Business reasoning rules:
- Always explain WHY a recommendation is good.
- Include tradeoffs when recommending locations or strategies.
- Example: higher foot traffic vs higher rent.

Customer insights:
Include estimated spending behavior when discussing customers.
Examples:
- Individual meals: 35–55 AED
- Pizza meals: 45–70 AED
- Family orders: 120–200 AED

Location references:

Dubai:
Dubai Marina, JBR, Downtown Dubai, Business Bay, DIFC, Jumeirah, Al Barsha

Abu Dhabi:
Yas Island, Al Reem Island, Khalidiyah, Al Maryah Island, Saadiyat Island

Guidelines:
- Prioritize Talabat for delivery. Secondary: Deliveroo, Careem.
- Highlight Jordanian authenticity as a brand advantage.
- Mention marketing opportunities during Ramadan, Eid, and UAE National Day.

Memory usage rules:
- Remember previous user decisions (e.g., selected city, budget, concept).
- Build on past responses instead of repeating full analysis.
- If the user refers to "it" or "that location", infer from conversation history.

Formatting rules:

# Section
## Subsection
- Short bullet points

For customer segments use:

Segment Name
Characteristics:
- bullet
- bullet

Spending Behavior:
- Estimated spend in AED

End each response with:

Top Recommendation:
(the single most important action)
"""


model = Groq(
    api_key=os.environ["GROQ_API_KEY"],
    id="openai/gpt-oss-120b",
    temperature=0.3,
    max_tokens=16384,
    request_params={"reasoning_effort": "low"},
)



agent = Agent(
    name="UAE Market Expansion Advisor",
    description=SYSTEM_PROMPT,
    model=model,
    tools=[search_knowledge_base,
           ExaTools(num_results=2, text_length_limit=500, livecrawl="fallback", api_key=os.getenv("EXA_API_KEY")),
           find_competitors,
            analyze_competitor_menu
           ],


    db=db,
    tool_call_limit=5,
    add_history_to_context=True,
    num_history_runs=5,



    instructions=[
        "Keep responses under 500 words unless deeper analysis is requested.",
        "Use clear headings and bullet points.",
        "Provide practical recommendations rather than generic explanations.",
        "Avoid repeating information across sections.",
        "Always call search_knowledge_base first for UAE market facts; use web search only for gaps or very recent data.",
        "When you use knowledge base content, cite it inline as [source file]."
    ],

    markdown=True,
    
)

def run_chat():
    print("\n--------------------------------------")
    print("UAE Restaurant Expansion AI Advisor")
    print("--------------------------------------")
    print("Ask strategic questions about expanding")
    print("a Jordanian restaurant into Dubai and Abu Dhabi.")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("Ask the advisor: ")

        if user_input.lower() in ["exit", "quit"]:
            print("\nSession ended.")
            break

        response = agent.run(user_input)

        pprint_run_response(response)



if __name__ == "__main__":
    run_chat()


'''app = Playground(agent=[agent]).get_app()

if __name__ == "__main__":
    serve_playground_app(app, reload=True)'''



'''market_agent = Agent(
    name="Market Research Agent",
    model=model,
    tools=[ExaTools(num_results=3), find_competitors],
    instructions=[
        "Focus only on competitors and market trends",
        "Return concise insights"
    ],
)'''





'''menu_agent = Agent(
    name="Menu Optimization Agent",
    model=model,
    tools=[analyze_competitor_menu],
    instructions=[
        "Analyze menus and suggest improvements",
        "Focus on pricing and items"
    ],
)'''



'''strategy_agent = Agent(
    name="Strategy Agent",
    model=model,
    instructions=[
        "You are the final decision maker",
        "Combine insights from other agents",
    ],
)'''