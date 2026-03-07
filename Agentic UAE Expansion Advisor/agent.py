import os 
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.utils.pprint import pprint_run_response
# from agno.app.playground import Playground
#from agno.app.playground import serve_playground_app
#from menu_scraper import scrape_and_clean

from tools.competitor_finder import find_competitors
from tools.competitor_menu_tool import analyze_competitor_menu



from dotenv import load_dotenv
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
exa_key = os.getenv("EXA_API_KEY")



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

Location references:

Dubai:
Dubai Marina, JBR, Downtown Dubai, Business Bay, DIFC, Jumeirah, Al Barsha

Abu Dhabi:
Yas Island, Al Reem Island, Khalidiyah, Al Maryah Island, Saadiyat Island

Guidelines:

- Prioritize Talabat for delivery. Secondary: Deliveroo, Careem.
- Highlight Jordanian authenticity as a brand advantage.
- Mention marketing opportunities during Ramadan, Eid, and UAE National Day.
- Include estimated rent ranges (AED/year) and example meal prices (AED).
- Identify likely customer segments where relevant.

Formatting:

# Section
## Subsection
- Bullet points

End each response with:

Top Recommendation:
(the single most important action)
"""
#memory = ConversationBufferMemory()


model = OpenAIChat(
    api_key=os.environ["OPENAI_API_KEY"],
    id="gpt-4.1-mini",
    temperature=0.3,
    max_tokens=800
)



agent = Agent(
    name="UAE Market Expansion Advisor",
    description=SYSTEM_PROMPT,
    model=model,
    tools=[ExaTools( num_results=3,api_key=os.getenv("EXA_API_KEY")),
           find_competitors,
            analyze_competitor_menu
           ],


    #memory=memory,



    instructions=[
        "Keep responses under 500 words unless deeper analysis is requested.",
        "Use clear headings and bullet points.",
        "Provide practical recommendations rather than generic explanations."
        "Avoid repeating information across sections."
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
