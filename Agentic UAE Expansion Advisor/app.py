import os 
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.utils.pprint import pprint_run_response



os.environ["OPENAI_API_KEY"] = ""
os.environ["EXA_API_KEY"] = ""

KNOWLEDGE_BASE = {}

agent = Agent(
    model=OpenAIChat(model="gpt-4o-mini",
    max_tokens=900),
    tools=ExaTools(),
    knowledge_base=KNOWLEDGE_BASE,
    description=(),
    instructions=(),
    markdown=True,
    show_tools_calls=True,
)